# Design Software Systems

[한국어](README.ko.md) · [Skill instructions](skills/design-software-systems/SKILL.md) · [Evaluation](evals/README.md) · [Sources](docs/sources.md)

An open Agent Skill for **system design, architecture review, and evolving existing software**. Turn requirements into a proportionate design with capacity estimates, data/API contracts, explicit trade-offs, and concrete correctness checks.

Use it to answer questions such as:

- What is the smallest architecture that meets our workload and operating constraints?
- Can two users reserve the last available room?
- What happens if a server crashes immediately after acknowledging a message?
- How can we change a schema while older clients are still running?

## Install

```bash
npx skills add woodencatjskim/design-software-systems --skill design-software-systems
```

Choose your agent in the installer. For a specific target:

```bash
npx skills add woodencatjskim/design-software-systems --skill design-software-systems -a codex
npx skills add woodencatjskim/design-software-systems --skill design-software-systems -a claude-code
npx skills add woodencatjskim/design-software-systems --skill design-software-systems -a cursor
```

The Skills CLI requires Node.js; use the version required by its [current installation documentation](https://github.com/vercel-labs/skills). The installed skill itself is Markdown and YAML: no Python, Node.js, API key, MCP server, or renderer is required to read and follow it.

For manual installation, copy the **entire** `skills/design-software-systems/` directory into your agent's documented skill location. Copying only `SKILL.md` loses the references. See [compatibility and what was actually tested](docs/compatibility.md).

The [releases page](https://github.com/woodencatjskim/design-software-systems/releases) also provides a standalone skill ZIP with a SHA-256 checksum for manual installation.

## Use

Select `design-software-systems` using your agent's skill mechanism, then describe the problem. In Codex, explicitly invoke it with `$design-software-systems`. Other agents have their own invocation conventions.

```text
Use design-software-systems to design a private file-sharing service for
5,000 employees. We already use PostgreSQL and object storage. Explain
tenant authorization, upload failure recovery, and when a CDN would help.
```

```text
Review this booking design with design-software-systems. Check simultaneous
reservations, duplicate requests, expired holds, and delayed payment results.
```

```text
Use design-software-systems to plan this API change from the current repository.
Preserve older clients and explain the rollout, backfill, and rollback limits.
```

Instructions are in English; answers follow the user's language. Important missing requirements are surfaced, and assumptions remain explicit.

## What you get

| Task | Result |
|---|---|
| New system | Scope, estimates, data/API contracts, minimal architecture, critical flows, verification plan |
| Existing system | Evidence from relevant code and docs, targeted change, compatibility and migration plan |
| Architecture review | Prioritized findings with evidence, failure scenarios, remedies, and unknowns |
| Small decision | A concise recommendation and a condition for revisiting it |

The workflow connects requirements → invariants and workload → data/contracts and components → failure behavior → decisions and verification. It adds components only when a requirement or evidence justifies them. It does not require a microservices stack or a lengthy document for every question.

Domain references cover [content delivery](skills/design-software-systems/references/content-delivery.md), [transactional inventory](skills/design-software-systems/references/transactional-inventory.md), and [realtime messaging](skills/design-software-systems/references/realtime-messaging.md). They are loaded only when relevant.

## Examples

- [Small document catalog](examples/small-document-catalog.md): a deliberately simple architecture.
- [Hotel booking](examples/hotel-booking.md): atomic allocation and uncertain payments.
- [Messaging review](examples/messaging-review.md): durability and latency contradictions.

These are illustrative design notes, not deployed systems or measured performance claims. Outputs normally use Markdown and optional Mermaid/text diagrams. No HTML renderer or additional skill is needed.

## Quality and limits

The repository includes a package validator, regression tests, eight behavioral prompts, and a recorded comparison with an ordinary agent and Anthropic's basic system-design guidance. See [the evaluation record](evals/README.md) for actual results and limitations. Static checks do not prove architectural correctness, and a small model-assisted evaluation does not establish general superiority.

The skill does not deploy infrastructure or guarantee throughput, availability, security, or recovery. Those promises require implementation, measurement, and review. Product-specific guarantees should be checked against the deployed version's official documentation.

## Development

Python 3.11+ is needed only for repository validation:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for making a focused change and recording behavioral evidence.

## Inspiration and attribution

Developed with reference to **[Design Software Systems Like a Senior Engineer – Complete Course](https://www.youtube.com/watch?v=soTfFFIQQ8U)** by **Hayk Simonyan**, published on **freeCodeCamp.org**. The course informed the design workflow and the music, booking, and messaging problem families. Technical qualifications and additional failure-handling guidance are our own analysis, linked to primary documentation.

We also studied existing public architecture skills to improve evidence handling, scope control, and decision records. [Sources and design influences](docs/sources.md) describe what informed this work. This is an independent project, not an official course companion or an endorsement by the instructor, freeCodeCamp, or the benchmark authors. No full transcript or video assets are redistributed.

## License

[MIT](LICENSE) for this repository's original materials. Linked external materials retain their own licenses.
