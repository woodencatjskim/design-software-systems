# Repository review evaluation — incomplete comparison

This development run tests the proposed repository-review extension against released v0.1.0. **The planned comparison is incomplete because the subagent runtime reached its usage limit.** Failed or unstarted trials are not passes. There is no demonstrated improvement or comparative win in this record.

The [protocol and criteria](../../repository-review/README.md), [fixture answer key](../../repository-review/answer-key.json), and source hashes were frozen before answering. See [provenance](provenance.json) for condition mapping, fixture/skill hashes, task text, and execution status. Source files and the task were not changed in response to answers.

## Completed evidence

Each completed answer used a fresh application subagent session and a separate temporary workspace containing only its task, one fixture, and one skill snapshot. The answerer was instructed not to read other cases, tests, rubrics, repository documentation, or answers. Filesystem separation was procedural rather than OS-enforced. Local probes were allowed; network, installs, and service/skill edits were not. English answers were limited to 450 words.

The creator reviewed the completed answers against the supplied source and frozen rubric. This review was **not blinded**. The separately planned blinded review was not run. The table records explicit evidence, not a model-quality leaderboard.

| Run / condition / case | Disposition and evidence | Reasoning and repair decision |
|---|---|---|
| [01](responses/run-01.md) / released / case-17 | Finds the enabled import writer and absence of an upper DB constraint | Reproduces allocated=2 at capacity=1; guarded update/constraint and migration reconciliation proposed |
| [02](responses/run-02.md) / proposed / case-42 | Rules out overselling using the DB CHECK and import rollback | Explains shared enforcement; reports valid, rejected, and concurrent local operations; no redesign demanded |
| [03](responses/run-03.md) / released / case-28 | Traces both document and facet queries to tenant predicates | Checks foreign/shared categories and empty tenants; no leak or redundant infrastructure asserted |
| [04](responses/run-04.md) / proposed / case-63 | Identifies returned facets as an unscoped aggregation | Reports cross-tenant categories and shared-category count contamination; scopes rows before GROUP BY |
| [05](responses/run-05.md) / released / case-35 | Traces immediate transport forwarding to yield-before-commit | Reports process-exit probe losing the accepted row; proposes commit-before-yield and failure cleanup |
| [06](responses/run-06.md) / proposed / case-91 | Uses commit-before-yield as counterevidence | Reports a local SIGKILL/recovery probe preserving the row; does not demand replication outside the contract |
| [07](responses/run-07.md) / released / case-56 | Keeps adapter durability unresolved rather than confirmed safe or broken | Gives both possible adapter semantics and requests implementation/configuration plus a recovery check |
| [10](responses/run-10.md) / proposed / case-28 | Traces both tenant predicates and rules out the aggregation leak | Checks shared categories and legitimate access; no repair warranted for the inspected path |

The eight completed answers meet the four frozen properties in this creator review: disposition, evidence, reasoning/counterevidence, and repair decision. No unsupported material finding was identified in those answers. Run 05 also identifies transaction cleanup behavior; its operational consequences are explicitly conditional on an open connection, and the source supports the reported suspended-transaction concern. The key is not an exhaustive list of every possible defect.

The retained traces are self-reported file/command summaries, not full tool transcripts or independent proof of every execution claim. The creator separately ran the deterministic fixture controls below. Only case-28 has both condition responses (runs 03 and 10); both correctly rule out the seeded concern. The other completed responses cover different case subsets, so **do not compare their aggregate condition pass rates**. Runs 08 and 09 failed with a runtime usage-limit error; already-started run 10 completed, and runs 11–14 were not launched after the limit was reported.

## Deterministic checks completed

- All 14 repository unit test methods passed locally: seven existing validator tests and seven new fixture tests.
- The repository package/link validator and Skill Creator quick validator passed.
- The local Skills CLI 1.5.18 installed the proposed package for Codex, Claude Code, and Cursor targets in an isolated project. All 13 installed files matched source bytes, relative references remained within the package, and the Claude Code symlink resolved. This does not establish native invocation behavior.
- The fixture controls execute real SQLite queries and generator boundaries. Their interruption check closes the writer connection and reopens the database, rather than simulating host/disk loss. Some answering agents separately report stronger subprocess probes; these are recorded as their reported checks.

## Limits and remaining work

Complete the missing counterpart trials and a condition-blinded review before claiming a completed comparison. Preserve these outputs and invalid run records when resuming. If the model or runtime changes, rerun both arms under the new environment rather than pool incomparable runs. Cases are deliberately small, synthetic, development-selected fixtures; no held-out system family or production repository was evaluated. There is one trial per planned case/condition, no variance estimate, no exact pinned model identity exposed, and no independently captured token/time measurement.

The changed instructions make the review method more explicit and the new fixtures make regressions observable. This partial run does not establish that the proposed skill detects more hidden defects than v0.1.0 or another public skill.
