---
name: luban
description: Luban Loop end-to-end engineering workflow from requirement to implemented, verified, review-ready delivery. Use when the user asks to use Luban, build, fix, implement, ship, land, or take a simple requirement to completion. This entrypoint orchestrates Waza think/hunt/check and Quality Guardrails as a closed delivery loop.
license: MIT
---

# Luban Loop

One entrypoint for engineering work. This skill bundles the full Waza skill set and Square guardrails inside the Luban directory and coordinates them into one closed loop.

## Bundled Modules

The public installed skill is `luban`. Its supporting modules are internal files under this skill directory:

```text
think/SKILL.md     # Chalkline / 墨斗: planning and tradeoffs
design/SKILL.md    # Design / 造型: frontend and interface design
check/SKILL.md     # Gauge / 验尺: review and release readiness
hunt/SKILL.md      # Rootfinder / 寻因: root-cause debugging
write/SKILL.md     # Write / 润文: prose rewrite and polish
learn/SKILL.md     # Learn / 学艺: domain research synthesis
read/SKILL.md      # Read / 取材: URL/PDF/source reading
health/SKILL.md    # Health / 巡检: agent and project health audit
square/SKILL.md    # Square / 规矩: quality guardrails
rules/             # Waza shared rules used by bundled modules
```

When a phase says to use a bundled module, read the corresponding bundled `SKILL.md` file from this directory. Do not require these modules to be installed as separate top-level skills.

## Naming

Use the Luban names when explaining the workflow to users. Keep the underlying skill/tool names for actual invocation and implementation.

| Luban name | Chinese | Underlying capability | Responsibility |
| --- | --- | --- | --- |
| Builder | 营造 | Luban | Own the delivery flow, implementation, and verification. |
| Chalkline | 墨斗 | `think/` | Clarify requirements, decisions, boundaries, and tradeoffs. |
| Square | 规矩 | square | Keep implementation simple, disciplined, scoped, and verifiable. |
| Rootfinder | 寻因 | `hunt/` | Diagnose failures and root causes before fixing symptoms. |
| Gauge | 验尺 | `check/` | Review readiness, risks, diffs, and evidence before handoff. |
| Seal | 落印 | Luban handoff | Output delivery notes, verification evidence, non-scope, and remaining risks. |

Additional bundled Waza modules are available when the task calls for them: `design/`, `write/`, `learn/`, `read/`, and `health/`.

## Workflow Contract

```text
requirement
  -> Builder      # own the goal, repo context, plan, execution, and verification
  -> Chalkline    # clarify boundaries, tradeoffs, and approach when needed
  -> Square       # apply simplicity, surgical changes, assumptions, and verification throughout
  -> Build        # make the smallest project-consistent change
  -> Rootfinder   # only if tests, runtime behavior, or diagnosis fail
  -> Verify       # run project-declared focused and broader checks
  -> Gauge        # review diff and release/merge risk before final handoff
  -> Seal         # summarize changes, evidence, non-scope, and remaining risk
```

Builder owns orchestration, execution, and verification selection. Seal owns the final handoff. The bundled modules own specialist workflow phases. Square is not a single checklist item; it is the quality guardrail across plan, build, verify, and check.

The user should only need to say:

```text
用 Luban 实现：<需求>
Use Luban to implement: <requirement>
```

Common user-facing prompts:

```text
用 Luban 修复：<问题>
Use Luban to fix: <bug or broken behavior>

用 Luban 分析：<方向或方案>
Use Luban to analyze: <decision or proposal>

用 Luban 检查：<当前改动>
Use Luban to review: <current changes>
```

Keep the workflow light for small tasks and stricter for risky changes. Do not invoke Superpowers from this workflow.

## 1. Understand

Read the real project context before acting:

- current directory or repository root
- current git status, including untracked files
- project instructions such as `AGENTS.md`, `CLAUDE.md`, README, manifests, Makefiles, CI, and test docs as needed
- relevant source files before proposing edits

Ask only when ambiguity would materially change the implementation. Otherwise state the assumption and proceed.

If the request is only about product direction, architecture, or whether something should exist, read `think/SKILL.md` and stop after a decision-complete plan unless the user explicitly asks to implement.

If the user asks to implement, still use `think/SKILL.md` only as much as needed to produce a compact execution plan, then continue to Build.

## 2. Plan

Apply Square / Quality Guardrails during planning:

- state load-bearing assumptions
- choose the simplest sufficient approach
- reject speculative abstractions and broad rewrites
- make each success criterion verifiable

Run repo-aware verification discovery before finalizing the plan when a repository is available. If `scripts/discover_verify.py` exists next to this `SKILL.md`, run:

```bash
python3 <luban-skill-dir>/scripts/discover_verify.py --root <repo-root>
```

Use the output to attach realistic verification to each step. Prefer high-confidence project-declared commands over inferred commands.

Write a compact plan with verification attached:

```text
1. Change: <specific behavior> -> verify: <test/check>
2. Change: <specific behavior> -> verify: <test/check>
3. Final: <acceptance criterion> -> verify: <command/manual check>
```

For trivial work, 2-3 sentences are enough. For larger work, include touched modules, success criteria, verification commands, API/schema/config changes, and rollback notes.

Do not add a new runtime, service, framework, dependency, database, protocol, or broad abstraction without explicit approval.

## 3. Build

Before editing code, read `square/SKILL.md`. Keep its rules active through Build, Verify, and Check:

- Make the smallest change that satisfies the requirement.
- Do not add speculative flexibility or abstractions.
- Do not clean, rewrite, reformat, or refactor unrelated code.
- Match the existing style.
- Remove only unused code introduced by this change.
- Every changed line must trace back to the request.

Do not enter Rootfinder by default. Read `hunt/SKILL.md` only when the task becomes a bug, regression, failing test, crash, unexpected runtime behavior, or unexplained mismatch between expected and actual output.

When `hunt` is triggered, diagnose the root cause before patching symptoms. The root cause should name a specific file, function, condition, or data path.

After the root cause is known, return to Build and make the smallest fix.

## 4. Verify

Prefer project-declared verification over generic commands. If it was not already run during Plan, run the bundled discovery script:

```bash
python3 <luban-skill-dir>/scripts/discover_verify.py --root <repo-root>
```

Check the current repository for likely sources before choosing commands:

- `AGENTS.md`, `CLAUDE.md`, README, contribution docs, or test docs
- `package.json`, `pyproject.toml`, `Makefile`, `justfile`, `Taskfile`, CI configs, or language-specific manifests
- existing test files near the changed code

Run verification in order:

1. focused test or check for the changed behavior
2. regression test if one was added or touched
3. broader project check when shared behavior changed
4. browser, UI, or media QA when the delivered behavior is visual, interactive, audio/video, or depends on local serving

If no project command exists, infer the narrowest reliable command from the stack and state that it was inferred. If verification cannot run, say exactly why and give the strongest manual check actually performed.

When the discovery script returns multiple candidates, use this priority:

1. commands explicitly documented in project instructions or test docs
2. manifest scripts such as `test`, `qa`, `qa:evidence`, `e2e`, `lint`, `typecheck`, `check`, or `build`
3. CI commands matching the touched stack
4. inferred language defaults, only when no better command exists

For frontend, game, visual, 3D, or audio work, do not treat syntax checks as sufficient. If the project provides a `qa`, `qa:evidence`, or `e2e` command, run it before handoff. If it does not, perform the smallest practical browser/runtime check and report exactly what was verified, such as HTTP reachability, nonblank canvas/media, image load, audio start, core user flow, and responsive screenshot review.

## 5. Check

Before final handoff, read `check/SKILL.md` when code, tests, schema, config, public API, release files, or shared behavior changed.

Review the diff against the original requirement:

- no unrelated files changed
- no user work overwritten
- no public API/schema/config change left undocumented
- no generated artifact or package surface accidentally changed
- no Square violation: unnecessary abstraction, broad rewrite, hidden assumption, or unverified claim
- tests or manual checks support the completion claim

Fix safe issues. Do not discard, stash, reset, or overwrite user changes.

## 6. Handoff

Final response must be short and evidence-based:

- what changed
- verification run and result
- files touched when useful
- what was intentionally not changed
- real remaining risk, if any

Do not end with vague offers. Provide the next concrete command only when it is genuinely useful.

## Quality Bar

Do not call work complete unless:

- the requirement is satisfied or the blocker is explicit
- relevant verification ran, or the reason it could not run is clear
- user work in the git tree was preserved
- final claims are backed by command output, file inspection, or a concrete manual check

## Fallback

The installer should install one top-level `luban` skill with the Waza and Square modules nested inside it. If an environment only has `luban/SKILL.md` without the nested modules, use the rules above directly, but say in the final handoff that bundled specialist modules were not available in that environment.
