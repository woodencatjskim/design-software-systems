# Evaluation

This repository separates package validation from behavioral evaluation. Neither proves that a suggested architecture works in production.

## Static checks

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
```

The validator checks this package's discovery metadata, required files, copied license, basic local Markdown links, resource boundaries, UI metadata, and evaluation input structure. Seven test methods exercise valid and malformed inputs, missing files, duplicate case IDs, and link/path escapes. It does not validate external URLs, anchors, all Markdown syntax, or architecture semantics.

## Repository review development suite

[Repository review cases](repository-review/README.md) add three matched defect/protected pairs and one missing-evidence case. Seven additional test methods establish the actual SQLite and generator behavior of the executable fixtures, including legitimate access and failed operations. The complete unit suite now has fourteen methods. These controls do not grade an agent or prove production concurrency/durability.

The review protocol uses one fresh session per case and condition, with the answer key and paired counterpart withheld from answerers. It separately checks disposition, source evidence, failure reasoning/counterevidence, and the repair decision, and records unsupported material findings. This addresses limitations of the earlier prose-only comparison below. The fixtures are development cases rather than a held-out benchmark.

The [recorded development run](results/2026-10-22-repository-review/README.md) is incomplete: eight responses completed, two trials failed at the runtime usage limit, and four were not started. Completed responses met the frozen criteria in creator review, but only one case has both conditions. No improvement or comparative win is established; the planned blinded review remains outstanding.

## Recorded behavioral smoke comparison

Date: 2026-10-22. See [prompts](prompts.json), [criteria](rubric.md), [per-case evidence](results/2026-10-22/review.md), and [provenance and hashes](results/2026-10-22/provenance.json).

Three isolated subagent sessions answered the same eight prompts in English with a 500-word maximum per answer:

1. Ordinary agent without an additional architecture skill.
2. Agent supplied with `design-software-systems` and its references.
3. Agent supplied with Anthropic's basic `system-design` skill.

The answering agents did not receive the rubric or other answers. Each condition used one session for all eight cases, with inherited runtime/model settings and no model override. No network, installs, or live implementation tests were permitted. This was an application subagent evaluation, **not** a Codex/Claude Code/Cursor runtime comparison. The runner did not expose a pinned model identifier, sampling parameters, or per-condition token usage; those were not independently measured.

| Condition | Criteria passed | Failed | Unverified | Critical failures observed |
|---|---:|---:|---:|---:|
| No additional architecture skill | 32 / 32 | 0 | 0 | 0 |
| This skill | 31 / 32 | 1 | 0 | 0 |
| Anthropic basic system-design | 32 / 32 | 0 | 0 | 0 |

The failure is a formatting issue: this skill's saved bounded answer includes an `Exercise: bounded-question` label before the requested two paragraphs. The two explanatory paragraphs are correct, but the complete artifact exceeds that requested structure. The original response is retained.

**This run does not demonstrate an improvement over the baseline or the reference skill.** All conditions handled the sampled architecture checks. The value currently established is a reusable, inspectable workflow and domain guidance; incremental model quality remains unproven. Do not advertise these results as a competitive win.

The creator also graded the outputs, using explicit excerpts in the review. Grading was model-assisted, not blinded or independently audited. The prompts deliberately expose the hazards and may be easy for a capable model. Conditions were isolated, but cases within each condition shared context. Automatic skill selection, realistic repository tracing, Korean output, repeated sampling, actual failure injection, and native agent invocation were not evaluated in this run. Follow-up evaluation should include those harder cases rather than simply enlarge a favorable score.

Raw responses are under `results/2026-10-22/responses/` and are unedited. The exact external reference instructions are not redistributed; their source URL and content hash are recorded. Setup summaries are recorded as summaries, not claimed to be an exact transcript of the runner.
