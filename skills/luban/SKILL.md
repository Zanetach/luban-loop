---
name: luban
description: Luban Loop end-to-end engineering workflow from requirement to implemented, verified, review-ready delivery. Use when the user asks to use Luban, analyze, review, build, fix, implement, scaffold, create or continue a project, ship, land, or take a requirement to completion. This entrypoint orchestrates bundled specialist modules and Quality Guardrails as a closed delivery loop.
license: MIT
---

# Luban Loop

One entrypoint for engineering work. This skill bundles specialist modules and Square guardrails inside the Luban directory and coordinates them into one closed loop.

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
rules/             # shared rules used by bundled modules
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

Additional bundled modules are available when the task calls for them: `design/`, `write/`, `learn/`, `read/`, and `health/`.

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

## Autonomy Contract

Luban is an execution loop, not a planning checkpoint. For implement, fix, build, ship, install, configure, or "make it work" requests, continue automatically through Build -> Verify -> fix failures -> Verify again -> Check -> Seal. Do not stop after a plan unless the user explicitly asked only for analysis, strategy, or a decision plan.

Default stance: decide and act. The user should normally only see progress updates and the final evidence-backed result, not approval prompts between phases. Do not ask "should I continue?", "want me to implement?", or "should I handle the remaining item?" when the answer can be inferred from the active goal and the action stays inside the stop conditions below.

Use a compact plan as an internal steering artifact, then execute it in the same turn. Ask for feedback only when continuing would cross a real decision boundary:

- destructive or irreversible action: delete data, reset history, publish, charge money, send messages, close issues, merge, tag, release, deploy, or modify external services
- new runtime, framework, database, paid service, protocol, broad abstraction, or dependency not already implied by the project
- missing credential, secret, account access, legal/business choice, or product requirement that cannot be inferred from current context
- two plausible interpretations would produce materially different user-visible behavior or migration cost
- verification is blocked after the same blocker has been worked around or retried with the cheapest safe recovery

Everything else should be handled by stating the assumption and proceeding. If a check fails, enter Rootfinder when needed, diagnose, patch, and rerun the relevant checks. The loop ends only when the requirement is satisfied with evidence or a concrete blocker remains.

## Project Mode Contract

When the requirement implies a project-level result, Luban enters Project Mode. This does not require the user to say "from scratch", "from 0 to 1", or "project mode". Project Mode applies both to new projects and to existing projects that need a requirement carried through to a working product slice.

Project Mode goal: turn a requirement into a runnable, inspectable project result, not a concept, plan, scaffold-only shell, partial module, or list of next steps.

Builder must detect whether the delivery surface is project-level by reading the request and repository context. If the work requires multiple modules, screens, commands, routes, services, data surfaces, generated artifacts, or integration steps to produce a usable result, treat it as Project Mode and automatically decompose the work into phases without waiting for approval:

```text
intent
  -> product slice      # smallest complete result that proves the requirement
  -> module map         # screens, commands, data, services, styles, tests, docs, or deploy surface
  -> scaffold/build     # create or extend the project structure and core modules
  -> module loops       # for each module: build -> verify -> fix -> verify
  -> integration loop   # connect modules and verify the user-facing flow
  -> polish loop        # fill obvious missing states, docs, and rough edges required for the result
  -> final verification # run the strongest practical checks
  -> Seal
```

Rules:

- Pick the smallest complete product slice that can be run or inspected end to end.
- For a new project, create the minimum structure needed for that slice. For an existing project, preserve current architecture and extend the smallest surfaces needed for that slice.
- Generate modules automatically from the goal and current stack. A module can be a source file, component, command, route, API, data model, style surface, test, fixture, README section, installer, or generated artifact.
- Each module gets its own loop: implement the module, verify its local behavior, fix failures, then continue to the next module.
- After module loops, run an integration loop that exercises the complete user path or artifact.
- Do not stop at "project skeleton created" unless the user explicitly asked only for a skeleton.
- Do not ask the user to choose routine implementation details. Choose defaults that fit the existing workspace, explain them briefly in Seal, and continue.
- If there is no existing stack, choose the simplest common stack that satisfies the request and can be verified locally. A new runtime, paid service, external account, deployment target, database, or broad infrastructure choice still follows the Autonomy Contract boundary.
- If the requested result is visual or interactive, verify a rendered/runtime surface, not only typecheck or build.
- Remaining modules can be listed in Seal only when they are intentionally outside the first complete product slice, blocked by a real boundary, or lower priority than the delivered runnable result.

## Plan Contract

Plan is a contract, not a separate specialist capability. Use the agent's native planning when available; otherwise fall back to this minimal Luban shape before Build:

```text
Goal: <what must be true when done>
Surface: <source, docs, config, schema, package, install path, service, or release surface>
Steps: <2-5 concrete steps, each with verify; in Project Mode, include module loops and integration verification>
Stop Conditions: <only the decision boundaries that require user input>
Done Evidence: <commands, artifacts, screenshots, runtime checks, or remote state that prove completion>
```

Rules:

- Keep it compact. A plan that slows down a small fix violates Luban.
- Every step must bind to a surface and a verification signal.
- For implementation requests, execute after planning without asking for approval.
- For Project Mode, the plan must name the first complete product slice, generated module map, module-loop verification, and final integration check.
- For analysis or architecture requests, the plan can be the final deliverable.
- If the native plan lacks surface, verification, stop conditions, or done evidence, patch those gaps using this contract before building.

## Continuation Contract

Do not turn in-scope work into a "next step" note. If audit, review, verification, or implementation discovers a highest-value remaining item and it still fits the user's stated goal, continue the loop and handle it before Seal.

Size alone is not a stop condition. A large refactor, file split, or multi-file cleanup should be planned with the Plan Contract and executed when it is the next necessary in-scope move. Stop only when the item crosses an Autonomy Contract decision boundary, contradicts the user's scope, or needs missing product/account/legal input.

In Seal, list remaining debt only when it is intentionally out of scope, blocked, lower priority than the completed goal, or unsafe to continue without user input. If the handoff says "next most valuable" or "remaining main debt", it must also say why Luban did not execute it now.

## User Feedback Contract

Feedback requests are exceptional. Before asking, check whether the answer is already implied by the active user goal, repository context, or Autonomy Contract. If it is, proceed.

Allowed feedback requests:

- choose between materially different product behavior, migration shape, public API, data retention, release/deploy action, or paid/external service
- provide a missing secret, account, license, private data source, or legal/business decision
- approve an irreversible operation named in the Autonomy Contract

Disallowed feedback requests:

- asking to continue after a successful plan
- asking whether to fix the next in-scope audit hotspot
- asking whether to rerun or broaden verification after a relevant failure
- asking whether to refresh generated or install surfaces required by the changed behavior
- asking whether to do a larger in-scope refactor solely because it is larger

If feedback is required, ask one precise question and pause. Otherwise continue and report the result in Seal.

## 1. Understand

Read the real project context before acting:

- current directory or repository root
- current git status, including untracked files
- project instructions such as `AGENTS.md`, `CLAUDE.md`, README, manifests, Makefiles, CI, and test docs as needed
- relevant source files before proposing edits

Lock the delivery surface before planning. Name what the requested work actually ships through:

- source behavior, docs, config, schema, public API, generated artifact, package/archive, release asset, deployment, or external service state
- the files or commands that define that surface
- what must stay explicitly out of scope

If a repo has tracked generated artifacts, package manifests, release archives, docs indexes, public pages, AI/crawler files, or installer outputs, treat them as part of the delivery surface only when the change reaches them. Decide this up front instead of discovering it during handoff.

Ask only when ambiguity would materially change the implementation. Otherwise state the assumption and proceed.

If the request is only about product direction, architecture, or whether something should exist, read `think/SKILL.md` and stop after a decision-complete plan unless the user explicitly asks to implement. This stop rule applies only to analysis/strategy requests, not to implement/fix/build requests.

If the user asks to implement, still use `think/SKILL.md` only as much as needed to produce a compact execution plan, then continue to Build without waiting for approval.

## 2. Plan

Apply Square / Quality Guardrails during planning:

- state load-bearing assumptions
- choose the simplest sufficient approach
- reject speculative abstractions and broad rewrites
- make each success criterion verifiable
- satisfy the Plan Contract: Goal, Surface, Steps, Stop Conditions, and Done Evidence

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

For each step, attach the shipped artifact or surface it affects. Examples:

```text
1. Change: update skill routing text -> surface: SKILL.md -> verify: install/grep smoke test
2. Change: refresh release package -> surface: dist/archive -> verify: package audit + inspect entries
3. Final: user-facing behavior installed -> surface: local skill dirs -> verify: fresh install smoke test
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

Keep source and shipped artifacts aligned. If the change affects a generated file, package input, installer output, release archive, public index, or machine-readable discovery file, either refresh and verify that surface or state why it is intentionally not changed.

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

Separate source failures from environment misses. When a declared check fails because a local dependency, font, browser, service, or tool is absent, do the cheapest safe recovery first (temporary venv, documented install, fallback env var, or read-only service probe) and rerun the check before calling the project broken. Report both the original miss and the recovered result.

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
- every intended shipped artifact or install surface is refreshed or explicitly left out
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

The installer should install one top-level `luban` skill with specialist modules and Square nested inside it. If an environment only has `luban/SKILL.md` without the nested modules, use the rules above directly, but say in the final handoff that bundled specialist modules were not available in that environment.
