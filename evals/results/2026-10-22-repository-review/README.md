# Repository review evaluation — completed development comparison

All 14 planned answers and the condition-blinded review are complete. **Released v0.1.0 and the proposed guidance each passed 28/28 frozen property judgments; all seven paired comparisons tied.** No unsupported material defect or blocking issue was identified. This record does not demonstrate comparative quality improvement.

The [protocol and criteria](../../repository-review/README.md), [fixture answer key](../../repository-review/answer-key.json), task, and source hashes were frozen before answering. [Provenance](provenance.json) records the conditions, sources, unedited answers, attempt history and review artifacts. No fixture or skill was tuned after seeing these answers.

## Paired results

Each answer was assessed on disposition, evidence, reasoning/counterevidence, and repair decision. Both answers in every row passed all four properties. The table links the original answers, not rewritten summaries.

| Case | Released v0.1.0 | Proposed guidance | Supported decision | Blinded preference |
|---|---|---|---|---|
| case-17 | [01](responses/run-01.md) | [08](responses/run-08.md) | Enabled import bypasses capacity guard; repair and test both writers | Tie |
| case-42 | [09](responses/run-09.md) | [02](responses/run-02.md) | Shared database CHECK protects capacity; no mandatory repair | Tie |
| case-28 | [03](responses/run-03.md) | [10](responses/run-10.md) | Documents and facets are tenant-scoped; no isolation repair | Tie |
| case-63 | [11](responses/run-11.md) | [04](responses/run-04.md) | Global facets disclose categories/counts; scope rows before aggregation | Tie |
| case-35 | [05](responses/run-05.md) | [12](responses/run-12.md) | Acceptance precedes commit; commit before yielding acceptance | Tie |
| case-91 | [13](responses/run-13.md) | [06](responses/run-06.md) | Commit precedes acceptance under the stated recovery contract; preserve ordering | Tie |
| case-56 | [07](responses/run-07.md) | [14](responses/run-14.md) | Adapter durability remains unresolved; obtain implementation/configuration/recovery evidence | Tie |

The reviewer also checked plausible additional concerns beyond the answer key. Run 05's abandoned transaction and run 13's conditional cleanup concern are defensible, scoped observations rather than false accepted-message-loss findings. They did not change the pairwise repair decision. See the unedited [blinded assessment](blind-review.md) and [per-property judgments](blind-review.json).

## Execution and blinding

Each answer used a fresh application subagent session and a separate temporary workspace containing one fixture, one skill snapshot and the task. Answerers were instructed not to read other cases, tests, rubrics, repository documentation or answers. Filesystem separation was procedural, not OS-enforced. Local probes were allowed; network, installs and service/skill edits were not. All answers satisfy the 450-word limit, and frozen source hashes were checked after execution.

Initially eight answers completed; runs 08 and 09 failed at the runtime usage limit, and runs 11–14 were not started. At the user's request, the six outstanding case/condition combinations completed in fresh sessions using the same exposed application mechanism and inherited settings, without a model override. Invalid prior attempts remain recorded; they are not counted as successful trials. Exact model revision and sampling settings are not exposed, so provider-level stability across the initial and resumed cohorts cannot be independently guaranteed. These results are descriptive, not an estimate of a causal skill effect.

A fresh reviewer received the original task, frozen criteria, answer key, fixtures and unedited answers labeled X/Y. Per-case order was shuffled with Python random.Random(73129). The reviewer did not receive skill snapshots, condition identities, traces or earlier conclusions. The [reviewer task](blind-review-task.txt) records its instructions. The [mapping](blind-mapping.json) was opened for result aggregation only after review files were saved; original review files are preserved unchanged. The creator checked the report and mapping afterward, so this is not an independent external audit.

Most original answers cite a service/ prefix matching their answering workspace. The reviewer normalized it to the corresponding case file and checked the line contents. The original citations are retained.

## Evidence boundaries and deterministic checks

The retained traces are self-reported file/command summaries, not full tool transcripts. The blinded reviewer did not receive them and did not authenticate the twelve answers' reported experiments. Source-supported causal reasoning passed; claimed exact runtime versions and observed probe outputs remain unverified. The reviewer separately checked only the transaction state at first yield and generator close for cases 35 and 91, as disclosed in its report.

- All 14 repository unit test methods passed locally: seven validator tests and seven fixture tests.
- The repository package/link validator and Skill Creator quick validator passed.
- Skills CLI 1.5.18 installed the proposed package for Codex, Claude Code and Cursor in an isolated project. All 13 installed files matched source bytes, relative references stayed within the package, and the Claude Code symlink resolved. Native host invocation was not tested.
- Fixture controls execute real SQLite queries and generator boundaries. The interruption control closes the writer connection and reopens the database; it does not simulate SIGKILL, host loss or disk loss. Sequential controls do not establish concurrency behavior.

## Interpretation

The guidance makes repository tracing, counterevidence and repair decisions explicit, and the fixtures make specific regressions observable. This evaluation found no material regression, but also no demonstrated advantage over v0.1.0. It did not compare this extension with another public skill.

These are small, synthetic, development-selected cases, not held-out systems or production repositories. There is one trial per case/condition, one blinded reviewer, no variance estimate, no pinned model identity, and no independently captured token/time measurement. Stronger quality claims require separate unseen cases and repeated comparisons under a verifiable runtime.
