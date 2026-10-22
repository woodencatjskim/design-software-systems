"""Establish the observable behavior of matched architecture review fixtures."""

import importlib
import importlib.util
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType

CASE_ROOT = Path(__file__).resolve().parents[1] / "evals/repository-review/cases"
INVENTORY_CASES = ("case-17", "case-42")
SEARCH_CASES = ("case-28", "case-63")
MESSAGE_CASES = ("case-35", "case-91")


def load_module(case_id: str, module_name: str) -> ModuleType:
    """Load a fixture as its own package so relative imports retain real wiring.

    Args:
        case_id: Identifier of an existing fixture directory.
        module_name: Name of a Python module in that fixture.

    Returns:
        The isolated imported module.
    """
    if case_id not in INVENTORY_CASES + SEARCH_CASES + MESSAGE_CASES:
        raise ValueError("Unknown executable review fixture")
    if module_name not in {"api", "jobs", "repository", "storage"}:
        raise ValueError("Unknown fixture module")
    package_name = "review_fixture_" + case_id.replace("-", "_")
    if package_name not in sys.modules:
        package_path = CASE_ROOT / case_id / "__init__.py"
        specification = importlib.util.spec_from_file_location(package_name, package_path)
        if specification is None or specification.loader is None:
            raise ImportError(f"Cannot load fixture package {case_id}")
        package = importlib.util.module_from_spec(specification)
        sys.modules[package_name] = package
        specification.loader.exec_module(package)
    return importlib.import_module(f"{package_name}.{module_name}")


def create_database(case_id: str, filename: str = ":memory:") -> sqlite3.Connection:
    """Initialize an isolated database using the fixture's actual schema.

    Args:
        case_id: Identifier of an executable fixture.
        filename: Temporary SQLite path, or an in-memory database.

    Returns:
        An open connection owned by the caller.
    """
    if case_id not in INVENTORY_CASES + SEARCH_CASES + MESSAGE_CASES:
        raise ValueError("Unknown executable review fixture")
    if not isinstance(filename, str) or not filename:
        raise ValueError("A database filename is required")
    schema = (CASE_ROOT / case_id / "schema.sql").read_text(encoding="utf-8")
    connection = sqlite3.connect(filename)
    try:
        connection.executescript(schema)
        connection.execute("PRAGMA synchronous=FULL")
    except sqlite3.Error:
        connection.close()
        raise
    return connection


class ReviewFixtureTests(unittest.TestCase):
    """Test actual SQLite results; these tests do not grade model responses."""

    def test_inventory_accepts_valid_orders(self) -> None:
        """Both API and import can allocate valid stock in either variant."""
        for case_id in INVENTORY_CASES:
            for module_name, function_name in (("api", "reserve"), ("jobs", "import_order")):
                with self.subTest(case=case_id, writer=module_name):
                    connection = create_database(case_id)
                    self.addCleanup(connection.close)
                    writer = getattr(load_module(case_id, module_name), function_name)
                    self.assertTrue(writer(connection, "desk", 1))

    def test_second_writer_and_database_enforcement(self) -> None:
        """The same import exceeds capacity only without the global DB constraint."""
        for case_id, expected in (("case-17", 2), ("case-42", 1)):
            with self.subTest(case=case_id):
                connection = create_database(case_id)
                self.addCleanup(connection.close)
                api = load_module(case_id, "api")
                jobs = load_module(case_id, "jobs")
                self.assertTrue(api.reserve(connection, "desk", 1))
                self.assertFalse(api.reserve(connection, "desk", 1))
                self.assertEqual(jobs.import_order(connection, "desk", 1), expected == 2)
                allocated = connection.execute("SELECT allocated FROM inventory").fetchone()[0]
                self.assertEqual(allocated, expected)

    def test_search_preserves_legitimate_access(self) -> None:
        """Both variants return the correct authorized document list."""
        for case_id in SEARCH_CASES:
            with self.subTest(case=case_id):
                connection = create_database(case_id)
                self.addCleanup(connection.close)
                result = load_module(case_id, "api").search(connection, "alpha")
                self.assertEqual(result["documents"], [(1, "Team handbook")])

    def test_search_summary_is_part_of_authorization(self) -> None:
        """Only the unscoped aggregation discloses another tenant's categories."""
        for case_id, expected in (
            ("case-28", [("handbook", 1)]),
            ("case-63", [("acquisition", 1), ("finance", 1), ("handbook", 1)]),
        ):
            with self.subTest(case=case_id):
                connection = create_database(case_id)
                self.addCleanup(connection.close)
                result = load_module(case_id, "api").search(connection, "alpha")
                self.assertEqual(result["facets"], expected)

    def test_message_normal_completion(self) -> None:
        """Both variants commit when the event generator is fully consumed."""
        for case_id in MESSAGE_CASES:
            with self.subTest(case=case_id):
                connection = create_database(case_id)
                self.addCleanup(connection.close)
                connection.isolation_level = None
                events = load_module(case_id, "api").submit(connection, "m1", "hello")
                self.assertEqual(list(events), ["accepted"])
                self.assertEqual(connection.execute("SELECT body FROM messages").fetchall(),
                                 [("hello",)])

    def test_interruption_at_acceptance_boundary(self) -> None:
        """Closing the writer at ACK rolls back only the uncommitted variant."""
        for case_id, expected in (("case-35", []), ("case-91", [("hello",)])):
            with self.subTest(case=case_id), tempfile.TemporaryDirectory() as directory:
                filename = str(Path(directory) / "messages.sqlite")
                connection = create_database(case_id, filename)
                connection.isolation_level = None
                events = load_module(case_id, "api").submit(connection, "m1", "hello")
                try:
                    self.assertEqual(next(events), "accepted")
                finally:
                    # Model interruption before the generator resumes; this is not a host-crash test.
                    connection.close()
                    events.close()
                observer = sqlite3.connect(filename)
                try:
                    self.assertEqual(observer.execute("SELECT body FROM messages").fetchall(),
                                     expected)
                finally:
                    observer.close()

    def test_invalid_inputs_do_not_change_state(self) -> None:
        """Reject invalid writer inputs and absent tenant/message identities."""
        for case_id in INVENTORY_CASES:
            connection = create_database(case_id)
            self.addCleanup(connection.close)
            for module_name, function_name in (("api", "reserve"), ("jobs", "import_order")):
                writer = getattr(load_module(case_id, module_name), function_name)
                for quantity in (0, -1, True, "1"):
                    with self.subTest(case=case_id, writer=module_name, quantity=quantity):
                        with self.assertRaises(ValueError):
                            writer(connection, "desk", quantity)
            allocated = connection.execute("SELECT allocated FROM inventory").fetchone()[0]
            self.assertEqual(allocated, 0)
        for case_id in SEARCH_CASES:
            connection = create_database(case_id)
            self.addCleanup(connection.close)
            with self.assertRaises(ValueError):
                load_module(case_id, "api").search(connection, "")
        for case_id in MESSAGE_CASES:
            connection = create_database(case_id)
            self.addCleanup(connection.close)
            with self.assertRaises(ValueError):
                next(load_module(case_id, "api").submit(connection, "", "hello"))
        with self.assertRaises(ValueError):
            load_module("../outside", "api")
        with self.assertRaises(ValueError):
            create_database("case-17", "")


if __name__ == "__main__":
    unittest.main()
