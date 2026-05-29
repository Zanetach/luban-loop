<div align="center">
  <img src="assets/luban-loop-card.png" width="760" alt="Luban Loop" />
  <h1>Luban Loop</h1>
  <p><b>From requirement to verified delivery.</b></p>
  <p><b>从一句需求，到实现、验证、评审和带证据的交付。</b></p>
  <a href="https://github.com/Zanetach/luban-loop/stargazers"><img src="https://img.shields.io/github/stars/Zanetach/luban-loop?style=flat-square" alt="Stars"></a>
  <a href="https://github.com/Zanetach/luban-loop/releases"><img src="https://img.shields.io/github/v/tag/Zanetach/luban-loop?label=version&style=flat-square" alt="Version"></a>
  <a href="https://github.com/Zanetach/luban-loop/actions/workflows/verify.yml"><img src="https://img.shields.io/github/actions/workflow/status/Zanetach/luban-loop/verify.yml?branch=main&label=verify&style=flat-square" alt="Verify"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" alt="License"></a>
</div>

## Why

Luban Loop is a bilingual engineering delivery workflow for AI coding agents. It gives the user one simple instruction, then makes the agent accountable for the work normally expected from a careful engineer: read the real project, clarify decisions when needed, keep the change scoped, debug root causes, run verification, review the diff, and hand off with evidence.

鲁班闭环不是提示词合集，也不是把任务拆成很多空步骤。它是一个闭环交付协议：小任务保持轻量，风险任务自动加强规划、寻因、验证和评审；用户不需要反复追问“继续吗”，Agent 应该把可完成的工作做完。

## See It

![Luban Loop flow](assets/luban-loop-flow.png)

```text
Requirement / 需求输入
  -> Builder / 营造
  -> Chalkline / 墨斗
  -> Square / 规矩
  -> Build / 实作
  -> Rootfinder / 寻因
  -> Verify / 验证
  -> Gauge / 验尺
  -> Seal / 落印
```

## Use It

Ask for the public entrypoint, then describe the job:

```text
Use Luban to implement: <requirement>
用 Luban 实现：<需求>
```

Common patterns:

```text
Use Luban to fix: <bug or broken behavior>
用 Luban 修复：<问题>

Use Luban to analyze: <decision or proposal>
用 Luban 分析：<方向或方案>

Use Luban to review: <current changes>
用 Luban 检查：<当前改动>
```

The installed public surface is one top-level `luban` skill. Specialist modules are bundled inside that skill directory and are orchestrated by the Luban entrypoint.

## What It Solves

Most AI coding failures happen at the boundaries, not inside a single edit:

| Failure point | Luban response |
|---|---|
| Coding starts before the requirement is decision-complete | Chalkline clarifies boundaries, tradeoffs, and success criteria |
| The patch grows beyond the actual need | Square keeps the change scoped, simple, and verifiable |
| The agent patches symptoms | Rootfinder diagnoses the failure before changing code |
| Completion is claimed without proof | Verify runs project-relevant checks and captures evidence |
| Risk is hidden in the handoff | Gauge reviews the diff, gaps, and release readiness |
| Users only get a vague summary | Seal reports changes, verification, non-scope, and remaining risk |

## Bundled Modules

Luban installs one top-level `luban` skill and keeps the supporting modules under `luban/`:

| Module | Luban name | Purpose |
|---|---|---|
| `luban/SKILL.md` | Builder / 营造 | Owns context reading, execution flow, verification choice, and final delivery |
| `think/` | Chalkline / 墨斗 | Clarifies requirements, decisions, tradeoffs, and implementation plans |
| `design/` | Design / 造型 | Guides UI, frontend, layout, interaction, and visual polish work |
| `hunt/` | Rootfinder / 寻因 | Finds root causes for failures, regressions, crashes, and broken behavior |
| `check/` | Gauge / 验尺 | Reviews diffs, release readiness, risks, and evidence quality |
| `write/` | Write / 润文 | Polishes Chinese and English prose, docs, releases, and public copy |
| `learn/` | Learn / 学艺 | Turns unfamiliar domains or source bundles into structured synthesis |
| `read/` | Read / 取材 | Reads URLs, PDFs, and source material for downstream work |
| `health/` | Health / 巡检 | Audits agent setup, instructions, verification surfaces, and maintainability |
| `square/` | Square / 规矩 | Provides quality guardrails for simplicity, scope, assumptions, and verification |

See [Capability Review](docs/capability-review.md) for the full capability map, review findings, verification evidence, and remaining risks.

## Install

Install the latest stable release:

```bash
curl -fsSL https://raw.githubusercontent.com/Zanetach/luban-loop/main/scripts/install.sh | bash
```

The installer resolves GitHub's latest release tag automatically, downloads that release archive, then installs the bundled `luban` skill into supported agent locations:

```text
~/.agents/skills/luban
~/.codex/skills/luban
~/.claude/skills/luban
```

If the repository is already cloned, install from the local checkout:

```bash
./scripts/install.sh
```

Pinned release, development, and local install details are documented in [Release Runbook](docs/release.md).

## Verify

Run the project-declared verification command:

```bash
./scripts/verify.sh
```

It validates the skill bundle, compiles helper scripts, checks shell syntax, runs behavior tests, checks semantic contracts, and smoke-tests installation into temporary Agents, Codex, and Claude Code skill directories.

GitHub Actions runs the same verifier on pushes, pull requests, and version tags.

## Repository Layout

```text
skills/luban/SKILL.md                      # public Luban Loop entrypoint
skills/luban/scripts/discover_verify.py    # repo-aware verification discovery
skills/luban/think/                        # Chalkline planning and tradeoff module
skills/luban/design/                       # interface and visual design module
skills/luban/hunt/                         # root-cause debugging module
skills/luban/check/                        # review and release readiness module
skills/luban/write/                        # prose polishing module
skills/luban/learn/                        # research synthesis module
skills/luban/read/                         # source reading module
skills/luban/health/                       # agent and project health audit module
skills/luban/square/                       # quality guardrails module
skills/luban/rules/                        # shared workflow and language rules
docs/summary.md                            # external-facing project summary
docs/capability-review.md                  # capability map and review evidence
docs/release.md                            # release and install runbook
assets/luban-loop-flow.*                   # workflow diagram
assets/luban-loop-card.*                   # project card
scripts/install.sh                         # public installer and local installer
scripts/install-remote.sh                  # compatibility wrapper
scripts/verify.sh                          # local verification script
scripts/check_semantic_contract.py         # semantic guard for Luban behavior
tests/test_discover_verify.py              # verification discovery tests
VERSION                                    # release version source
NOTICE.md                                  # upstream attribution
```

## Design Contract

Luban Loop stays deliberately small at the user surface:

| Principle | Rule |
|---|---|
| One entrypoint | Users invoke `luban`; bundled modules stay internal |
| Closed loop | Implementation requests continue through build, verify, review, and handoff |
| Evidence first | Final delivery names commands, outputs, changed files, and remaining risk |
| Scope discipline | Repository boundaries are explicit; unrelated projects do not leak into docs or delivery |
| Lightweight by default | Small changes stay small; risky changes receive stronger process |

## Release

Current version is recorded in [VERSION](VERSION). Release steps are kept in [docs/release.md](docs/release.md), including tagged install verification with `LUBAN_LOOP_REF`.

## License

MIT License. See [LICENSE](LICENSE).
