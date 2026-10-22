# Sources and design influences

Research date: 2026-10-22. This file distinguishes inspiration from implementation evidence. External links and their licenses are not an endorsement of this project.

## Original course

- **Hayk Simonyan**, [Design Software Systems Like a Senior Engineer – Complete Course](https://www.youtube.com/watch?v=soTfFFIQQ8U), published by **freeCodeCamp.org**, 3:16:48.
- [Official course introduction](https://www.freecodecamp.org/news/learn-how-to-design-software-systems-like-a-senior-engineer-in-our-new-course/).
- [Our Korean analysis](system-design-course-analysis.ko.md): analysis of the full English automatic captions, with timestamped references and technical qualifications. It is a research snapshot written before this skill, not the current package specification. Screen-only diagrams/code were not independently reviewed.

The course informed the five-stage workflow and the content-delivery, reservation, and messaging examples. The installed skill contains independently written operational guidance. We do not redistribute the full transcript, slides, or video assets. Examples do not describe the actual internal architecture or current traffic of Spotify, Booking.com, or WhatsApp.

## Public skills studied

| Source | Studied strength | How it informed this project |
|---|---|---|
| [pinchen147/system-design-skill](https://github.com/pinchen147/system-design-skill) | Evidence, invariants, alternatives, durable acceptance, domain references | Require an explicit reason and verification condition for important decisions |
| [Anthropic system-design](https://github.com/anthropics/knowledge-work-plugins/blob/main/engineering/skills/system-design/SKILL.md) and [architecture](https://github.com/anthropics/knowledge-work-plugins/blob/main/engineering/skills/architecture/SKILL.md) | Concise procedure and ADR structure | Keep the entrypoint focused and distinguish proposed from accepted decisions |
| [wondelai/system-design](https://github.com/wondelai/skills/tree/main/system-design) | Capacity estimation and common designs | Provide arithmetic examples with assumptions and separate physical amplification |
| [alirezarezvani/senior-architect](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/skills/senior-architect) | Technology decisions and existing-project analysis | Account for the current stack, operating constraints, and migration cost |
| [wshobson/architecture-patterns](https://github.com/wshobson/agents/tree/main/plugins/backend-development/skills/architecture-patterns) | Domain boundaries and testable modules | Use boundary and testability reasoning when the problem calls for it |

These were qualitative design references, not copied packages. We did not incorporate their scripts, templates, or full skill texts into the installed skill. The development evaluation uses a separately fetched Anthropic reference; the public evidence includes its source identity and hash, not a bundled copy of that instruction file. The evaluation compares behavior under a small task set, not author reputation or installation counts.

## Primary technical references

- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/18/transaction-iso.html): isolation and serialization retries.
- [PostgreSQL pg_trgm](https://www.postgresql.org/docs/17/pgtrgm.html): indexed similarity and pattern search.
- [AWS transactional outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html): DB/event dual-write failures.
- [AWS S3 presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html): expiration, reuse, and object operations.
- [AWS ALB listeners](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html): WebSocket support.
- [Redis Pub/Sub](https://redis.io/docs/latest/develop/pubsub/): at-most-once delivery.
- [Cassandra BATCH](https://cassandra.apache.org/doc/latest/cassandra/developing/cql/dml.html#batch) and [architecture](https://cassandra.apache.org/_/cassandra-basics.html): batch and replication qualifications.
- [Signal X3DH](https://signal.org/docs/specifications/x3dh/) and [Double Ratchet](https://signal.org/docs/specifications/doubleratchet/): key agreement and message-key evolution.

Consult documentation for the deployed version before implementation; this project does not freeze vendor behavior.

## Packaging references

- [Agent Skills specification](https://agentskills.io/specification).
- [Skills CLI](https://github.com/vercel-labs/skills) and [directory FAQ](https://skills.sh/docs/faq).
- [OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills) for optional Codex metadata and invocation.

The standard package and supporting instructions are the portable interface. Agent-specific discovery, invocation, and automatic selection remain host behavior and are recorded separately in the compatibility report.
