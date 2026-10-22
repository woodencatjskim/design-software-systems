# Reviewing implemented design

Use for a repository architecture review or a change spanning state owners, callers, or trust boundaries. The aim is a useful repair decision, not a quota of findings. Match the depth and output format to the request.

## Establish the contract and coverage

Identify the required result, unacceptable result, and relevant failure scope. Separate documented intent from observed behavior; a discrepancy is a question about intended behavior when the contract itself is ambiguous.

Start with the requested flow and its callers. For each authoritative value or protected object, find the other paths that can change or expose it: background jobs, imports, administrative endpoints, webhook handlers, legacy versions, exports, search projections, and caches **when present**. Follow imports, route registration, configuration, database definitions, and callers to establish reachability. A suggestive filename or an unused helper does not establish a production path. Do not claim exhaustive coverage when some writers or deployment settings are unavailable.

Record the enforcement location: a database constraint, atomic statement, transaction, shared owner, or authorization boundary. Check the caller's assumptions as well as the implementation. A check in one API may not cover a batch writer; a missing local check may already be enforced by a shared gateway or the database.

Stop expanding the search when the important claim's paths and enforcement are accounted for, or when missing evidence is explicitly recorded. Avoid reviewing unrelated subsystems merely because they exist.

## Construct a failure sequence

For an important suspected defect, identify:

1. Preconditions and the entry path that makes the scenario reachable.
2. State read, identity used, decision made, and state written by each actor.
3. Transaction/commit boundaries and externally visible responses or effects.
4. The smallest interleaving, retry, interruption, or version mismatch that breaks the contract.
5. The resulting invalid state or observation and the mechanism that should prevent it.

Name an actual ordering: “A reads available; B reads available; A commits; B commits” is more useful than “race condition.” Check that the chosen isolation, conditional update, constraint, or lock permits that sequence before asserting it. For lifecycle races, identify the transition guard and whether competing transitions use the same authority. For an external effect, distinguish the local record, dispatch, remote result, and reconciliation identity.

Do not assume a function name such as `save`, `send`, or `transaction` establishes durability. Trace when its effect becomes recoverable, and when the caller exposes success. Conversely, asynchronous projection is not loss if an authoritative durable record already covers the promised recovery window.

## Try to disprove the finding

Before presenting a suspected defect, inspect relevant counterevidence: caller authorization, shared policy enforcement, schema constraints/triggers, transaction boundaries, stable effect identities, durable upstream records, and routing or feature settings. Explain why the protection covers this path or why it does not. A path disabled in supplied deployment configuration is not a confirmed live defect; a hypothetical enablement can be a conditional risk if relevant.

Classify the outcome:

| Outcome | Evidence needed | Report |
|---|---|---|
| Demonstrated defect | Contract, reachable path, concrete violation, applicable safeguards checked | Fix recommendation with source locations and sequence; distinguish static reasoning from an executed reproduction |
| Conditional risk | A credible violation depends on an explicit unresolved precondition | The condition and the smallest check that resolves it |
| Unresolved check | Required source, deployment fact, or experiment is unavailable | What is missing, why it matters, and how to obtain evidence |
| Concern ruled out in inspected scope | A concrete safeguard blocks the candidate sequence | Brief explanation when useful; do not count as a defect or global safety certification |

Retain the identity of an unresolved concern when evidence becomes inaccessible; absence of new evidence does not erase a prior finding. Do not invent missing files, logs, settings, or test results. Do not convert the number of missing documents into a severity score.

## Make the repair decision reviewable

Rank findings by the violated contract and reachable consequence, separately from evidence strength. Give the smallest correction that closes the demonstrated path, its compatibility/operational cost, and a check that would fail before and succeed after. Avoid proposing a new service where a shared invariant or guarded update suffices. Related symptoms of one root cause belong together.

If implementation or tests are available, prefer an isolated reproduction using the project's real semantics. Check concurrent requests, retries, interruption points, or caller compatibility as appropriate. A fake store or a sequential example does not prove the behavior of the production database under concurrency. Run only local, authorized checks; otherwise provide the exact proposed experiment and observable result. Never label a proposed test as passed.

Include findings, useful ruled-out concerns, and remaining checks in proportion to the task. An empty finding list is valid. Use [the finding template](../assets/review-finding-template.md) only if a saved review benefits from it.

## Resume without stale conclusions

When saving a substantial review, record source locations and the observed commit plus relevant working-tree changes when available. Outside Git, identify the files or supplied snapshot and its limits. Recheck affected sources and dependent findings after changes; unchanged HEAD does not imply an unchanged working tree. Preserve user notes and accepted decisions. Do not silently promote a historical result to a fresh verification.
