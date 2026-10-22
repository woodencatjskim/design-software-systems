# Compatibility and installation verification

The portable interface is the complete `skills/design-software-systems/` folder: standard `SKILL.md` frontmatter, relative references, a template, and a license. Optional `agents/openai.yaml` supplies Codex display metadata. Other hosts can use the Markdown without interpreting that file.

The skill requires no executable runtime, cloud account, API key, MCP server, or diagram renderer. Python is used only for this repository's development checks. The optional Skills installer requires Node.js.

## Installation targets

```bash
npx skills add woodencatjskim/design-software-systems --skill design-software-systems -a codex
npx skills add woodencatjskim/design-software-systems --skill design-software-systems -a claude-code
npx skills add woodencatjskim/design-software-systems --skill design-software-systems -a cursor
```

The installer chooses the appropriate agent directories and may share files through symlinks. For manual installation, copy the complete skill folder into the host's documented location. Do not copy only the entrypoint. Installed references are self-contained; repository examples and evaluation records are optional reading and not required at runtime.

## Verification scope

The development record below distinguishes successful packaging/install checks from native application execution. A file being installed does not prove that every host automatically activates it or follows it equally well.

| Check | Scope |
|---|---|
| Package validator and unit tests | Discovery fields, local references, boundaries, evaluation input shape |
| Skill Creator quick validator | Frontmatter and starter-placeholder validation |
| Skills CLI installation | See recorded outcome below |
| Behavioral comparison | Eight prompts per condition in application subagents; see [evaluation](../evals/README.md) |
| Native Codex, Claude Code, Cursor execution | Not tested in this release; installer targets are not runtime certification |

Agent behavior, skill discovery, and installation conventions can change. Consult the [Agent Skills specification](https://agentskills.io/specification) and [Skills CLI documentation](https://github.com/vercel-labs/skills) for current requirements.

## Recorded installation outcome

On 2026-10-22, Skills CLI **1.5.18** installed the local repository into an isolated project for **Codex, Claude Code, and Cursor**. The run used Node.js 22.19.0. The cached package declares Node.js >=18; consult current installer requirements for future versions.

The installer discovered exactly one skill. It placed the shared package at `.agents/skills/design-software-systems` for the universal Codex/Cursor targets and created a Claude Code symlink at `.claude/skills/design-software-systems`. All **10 installed files** were byte-compared with the source, and the Claude Code symlink resolved to that shared package. No user-global skill installation was changed.

Installation from **`woodencatjskim/design-software-systems` on GitHub also passed** for the same three targets in a second isolated project. All 10 downloaded skill files matched the local source, and the Claude Code symlink resolved correctly. The source commit and individual file hashes are in [the installation record](../evals/results/2026-10-22/installation.json). Native host invocation remains outside this check.

The initial [GitHub Actions run](https://github.com/woodencatjskim/design-software-systems/actions/runs/39713983980) passed the package validator and all seven test methods on **Python 3.11 and 3.13**. Subsequent commits are checked by the same workflow.

The repository-review development extension was also installed locally with Skills CLI 1.5.18 into a separate temporary project for Codex, Claude Code, and Cursor targets. All **13** proposed package files matched source bytes, installed relative references resolved inside the package, and the Claude Code symlink resolved correctly. This is a local candidate-package check, not a new released GitHub-install record or native host invocation test. See the [development evaluation record](../evals/results/2026-10-22-repository-review/README.md).

## Discovery status

The public GitHub repository has system-design, software-architecture, agent-skills, and agent-specific topics. Direct GitHub installation works. On 2026-10-22, immediately after publication, `skills find design-software-systems --owner woodencatjskim` returned no result. Directory indexing is not under this repository's control; publication and a successful install do not establish immediate skills.sh search visibility.
