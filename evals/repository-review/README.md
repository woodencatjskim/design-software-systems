# Repository review evaluation

This suite targets hidden defects, counterevidence, and repair decisions. The original eight prose prompts remain a separate regression suite. These fixtures do not prove behavior in a production service or database other than the SQLite model supplied here.

## Answering protocol

Give each answerer a fresh isolated directory containing exactly one case and a skill snapshot. Use this task verbatim:

> Review the supplied service snapshot against CONTRACT.md. Identify material architecture defects, if any, and the evidence needed to decide on a repair. Cite relative file names and line numbers, explain reachable consequences, and suggest proportionate corrections and verification. Distinguish what this snapshot establishes from what it cannot establish. Do not modify the service. Answer in English, at most 450 words. Use plain file:line references, not Markdown file links.

Allow read-only inspection and isolated temporary checks if desired. Do not provide tests, this README, the answer key, other cases, other answers, or the wider repository to the answerer. Copy only the individual case into its workspace: the identifiers intentionally do not reveal the expected result. Do not place the counterpart in an accessible parent folder. In a shared agent filesystem, path restrictions are procedural rather than an OS isolation guarantee; disclose that limitation.

Use fresh sessions per case and condition. Freeze task, fixture hashes, skill snapshots, and rubric before running. Compare the released skill with the proposed skill using the same inherited model/tool settings and budget. Record what the runtime does not expose; do not invent model IDs or token measurements. Mark failed or missing runs invalid, never successful. Publish unedited responses and source identities.

## Frozen review criteria

The [answer key](answer-key.json) defines the expected finding for each case. Grade four properties per response:

1. **Disposition:** finds the seeded violation, rules out the targeted concern in its supplied scope, or retains the missing-evidence check as unresolved, as appropriate.
2. **Evidence:** cites the relevant reachable call/write/read path and decisive protection or missing source. Verify cited locations; do not reward a filename alone.
3. **Reasoning and counterevidence:** provides a concrete failure sequence or explains why existing enforcement blocks it, including legitimate successful behavior. A proposed hypothetical is not an executed result.
4. **Repair decision:** gives a correction and discriminating verification for a defect; avoids an unnecessary repair for a protected path; requests the specific evidence needed for an unresolved check.

Also count unsupported material defects separately. Conditional suggestions clearly labeled as such are not automatically false positives. A defensible additional defect should be investigated against the fixture contract rather than rejected just because it is not in the key. Do not require exact phrasing or grade architectural correctness by regex.

Hide condition labels from the reviewer and randomize display order where practical. Reveal condition mapping only after grading. The reviewer may see fixtures and the key. The creator still adjudicates disagreements, so this is not an independent external audit. Distinguish reviewer judgments from deterministic fixture checks.

## Fixture controls

There are three matched pairs and one evidence-gap case. A pair changes only the mechanism under review. Normal operations still work in both versions. The decisive differences concern a shared database invariant, a derived response field, and an acceptance/commit boundary.

```bash
python -m unittest discover -s tests -p test_review_fixtures.py -v
```

Seven test methods verify actual schema/query/generator behavior and rejected inputs. The interruption test closes the connection at the acceptance event and reopens the database; it is not a SIGKILL, power-loss, or deployment durability test. No concurrency claim is inferred from a sequential test. The missing-adapter case intentionally cannot establish durability from the supplied source.

These are development cases selected while designing the change, not a held-out benchmark. Passing them cannot establish general superiority. Keep future unseen system families separate from development fixtures; do not tune repeatedly against a supposed holdout.
