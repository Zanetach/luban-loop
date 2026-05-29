# Luban Loop Capability Review / 鲁班闭环能力审查

## Verdict

Luban Loop is now a real integrated workflow package, not a thin wrapper. It installs one top-level `luban` skill and bundles the complete specialist module set plus Square quality guardrails inside that skill directory.

```text
skills/luban/
  SKILL.md
  scripts/discover_verify.py
  think/
  design/
  check/
  hunt/
  write/
  learn/
  read/
  health/
  rules/
  square/
```

## Capability Map

| Capability | Module | What It Enables |
| --- | --- | --- |
| Delivery orchestration | `luban/SKILL.md` | One user-facing entrypoint from requirement to implementation, verification, review, and handoff. |
| Requirement and plan judgment | `luban/think` | Clarifies vague requirements, evaluates tradeoffs, and produces decision-complete plans before coding. |
| Interface and visual design | `luban/design` | Guides frontend/UI work, screenshot-driven polish, typography, layout, and distinctive visual direction. |
| Root-cause debugging | `luban/hunt` | Diagnoses failures, regressions, crashes, broken behavior, and screenshot defects before patching. |
| Review and release readiness | `luban/check` | Reviews diffs, audits projects, checks release readiness, and validates evidence before handoff. |
| Writing and polishing | `luban/write` | Rewrites Chinese and English prose, removes AI-like wording, and polishes release/social/docs copy. |
| Research synthesis | `luban/learn` | Turns unfamiliar domains or source bundles into structured, publishable output. |
| Source reading | `luban/read` | Fetches URLs and PDFs as clean Markdown for citation, reading, and downstream synthesis. |
| Agent/project health | `luban/health` | Audits Codex/Claude setup, instruction surfaces, verification quality, and maintainability signals. |
| Quality guardrails | `luban/square` | Enforces simplicity, surgical changes, explicit assumptions, and verifiable success criteria. |
| Shared rules | `luban/rules` | Provides durable-context, language, and anti-pattern rules used by bundled modules. |

## User-Facing Workflow

```text
Use Luban to implement: <requirement>
用 Luban 实现：<需求>
```

Default delivery path:

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

Specialized modules are available when needed, but they do not clutter the top-level skill namespace. They live under `luban/`.

## Installation Behavior

One-line install:

```bash
curl -fsSL https://raw.githubusercontent.com/Zanetach/luban-loop/main/scripts/install.sh | bash
```

Install result:

```text
~/.agents/skills/luban
~/.codex/skills/luban
~/.claude/skills/luban
```

The installer copies the complete bundled directory. It does not separately fetch specialist modules or Square during install. Those capabilities are already included in the repository archive.

`scripts/install.sh` is the single public installer: it installs from a local checkout when the repository is present, and bootstraps from GitHub when run through `curl | bash`.

## Review Findings

### Strengths

- One clean top-level skill: `luban`.
- Full specialist module set is bundled under `luban`.
- Square provides the quality guardrails while using Luban naming.
- Install works for `~/.agents/skills`, `~/.codex/skills`, and Claude Code's `~/.claude/skills`.
- Verification script checks skill presence, Python helper compilation, shell script syntax, and important bundled references.
- Verification script smoke-tests local install output for Agents, Codex, and Claude Code targets.
- GitHub Actions now runs `./scripts/verify.sh` on pushes and pull requests.
- Upstream attribution is documented in `NOTICE.md`.

### Remaining Risks

- The documented one-line installer tracks `main`, which is convenient for updates but not reproducible. For stable releases, publish a tag and document a pinned install URL.
- Nested specialist modules are bundled as internal resources, so agents must enter through `luban` to get the intended orchestration. Direct top-level calls like `think` are intentionally not installed.
- Upstream specialist module and Square content was vendored at the time of integration. Future upstream changes require a deliberate sync.

## Verification Evidence

Commands run locally:

```bash
./scripts/verify.sh
python3 skills/luban/check/scripts/audit_signals.py --root /Users/zane/Documents/Github/luban-loop
curl -fsSL https://raw.githubusercontent.com/Zanetach/luban-loop/main/scripts/install.sh | bash -n
```

Install smoke test used temporary `AGENTS_HOME`, `CODEX_HOME`, and `CLAUDE_HOME` directories and confirmed these installed files:

```text
luban/SKILL.md
luban/think/SKILL.md
luban/design/SKILL.md
luban/check/SKILL.md
luban/hunt/SKILL.md
luban/write/SKILL.md
luban/learn/SKILL.md
luban/read/SKILL.md
luban/health/SKILL.md
luban/square/SKILL.md
```

## Capability Score

```text
Workflow completeness: 9/10
Installation simplicity: 9/10
Bundled capability coverage: 9/10
Verification posture: 8/10
Release reproducibility: 7/10
```

Overall: **8.4/10**.

The main next improvement is tagged releases with pinned install commands.
