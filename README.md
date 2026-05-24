# Luban Loop

**Luban Loop** is a bilingual engineering delivery workflow for AI coding agents. It turns a plain requirement into implementation, verification, review, and a final handoff with evidence.

**鲁班闭环** 是一个面向 AI 编程 Agent 的工程交付 workflow：从需求描述出发，推进到实现、验证、评审和带证据的交付说明。

![Luban Loop card](assets/luban-loop-card.png)

## Use It

```text
Use Luban to implement: <requirement>
用 Luban 实现：<需求>
```

Other common prompts:

```text
Use Luban to fix: <bug or broken behavior>
用 Luban 修复：<问题>

Use Luban to analyze: <decision or proposal>
用 Luban 分析：<方向或方案>

Use Luban to review: <current changes>
用 Luban 检查：<当前改动>
```

## Workflow

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

## Roles

| Role | Chinese | Responsibility |
| --- | --- | --- |
| Builder | 营造 | Owns the goal, project context, implementation flow, and verification selection. |
| Chalkline | 墨斗 | Clarifies requirements, decisions, boundaries, and tradeoffs. |
| Square | 规矩 | Keeps implementation simple, disciplined, scoped, and verifiable. |
| Build | 实作 | Makes the smallest complete change that fits the existing project. |
| Rootfinder | 寻因 | Diagnoses root causes before fixing failures or unexpected behavior. |
| Verify | 验证 | Runs tests, QA, browser/runtime checks, and collects evidence. |
| Gauge | 验尺 | Reviews the diff, risks, gaps, quality guardrails, and readiness. |
| Seal | 落印 | Outputs delivery notes, verification evidence, non-scope, and remaining risks. |

## What It Solves

Most agent workflows fail in one of four places:

- They start coding before the requirement is decision-complete.
- They over-design small tasks and add unnecessary abstractions.
- They fix symptoms without finding the root cause.
- They claim completion without reproducible verification evidence.

Luban Loop adds a lightweight structure around those failure points without turning every task into a heavy process.

## Install

One-line install:

```bash
curl -fsSL https://raw.githubusercontent.com/Zanetach/luban-loop/main/scripts/install-remote.sh | bash
```

This installs the bundled Luban workflow skills into both agent skill locations:

```text
~/.agents/skills/luban
~/.agents/skills/think
~/.agents/skills/hunt
~/.agents/skills/check
~/.agents/skills/square

~/.codex/skills/luban
~/.codex/skills/think
~/.codex/skills/hunt
~/.codex/skills/check
~/.codex/skills/square
```

If you already cloned the repository, run the local installer:

```bash
./scripts/install.sh
```

The public workflow name is **Luban Loop**. The installed skill name is `luban`.

## Verify

```bash
./scripts/verify.sh
```

This validates the bundled skill file and compiles the verification discovery script.

## Repository Layout

```text
skills/luban/SKILL.md                      # Luban Loop skill instructions
skills/luban/scripts/discover_verify.py    # repo-aware verification command discovery
skills/think/                              # Waza Chalkline planning skill
skills/hunt/                               # Waza Rootfinder debugging skill
skills/check/                              # Waza Gauge review skill
skills/square/                             # Square quality guardrails skill
docs/summary.md                            # external-facing project summary
docs/luban-loop-flow.mmd                   # Mermaid workflow diagram
assets/luban-loop-flow.svg                 # workflow diagram source image
assets/luban-loop-flow.png                 # workflow diagram PNG
assets/luban-loop-card.svg                 # promotional card source image
assets/luban-loop-card.png                 # promotional card PNG
scripts/install.sh                         # local skill installer
scripts/install-remote.sh                  # curl-based one-line installer
scripts/verify.sh                          # local validation script
```

## License

MIT
