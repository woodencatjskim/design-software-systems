# Contributing

Keep changes tied to an observed design failure or a concrete user need. Prefer a small correction over another universal checklist. Preserve the skill's ability to answer a bounded question briefly.

## Local checks

Use Python 3.11 or newer:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
```

The validator checks package metadata, relative file destinations, self-contained skill links, and evaluation data shape. It does not check external URL availability, Markdown heading anchors, or semantic correctness.

## Changing guidance

1. Describe a realistic request and the undesirable behavior.
2. Update only the relevant entrypoint or reference. Do not require every reference on every invocation.
3. Verify technical guarantees against primary documentation; record assumptions and version dependence.
4. Run the applicable cases in `evals/prompts.json`. Keep answer keys hidden from the answering agent and disclose model/environment limits.
5. Record before/after outputs and review meaningful criteria from `evals/rubric.md`.

No vendor-specific runtime, renderer, account, or network access should become a requirement for ordinary use. Repository development tools may have explicit dependencies. Use type hints, descriptive names, argument validation, and docstrings for Python tools; test both accepted and rejected inputs for core validation logic.

## Sources and releases

Credit external ideas and preserve notices for any reused text or code. Do not add full third-party transcripts or proprietary examples. Update version metadata and compatibility/evaluation records when releasing. Describe untested agents honestly. A passing static check must never be presented as a production-system test.
