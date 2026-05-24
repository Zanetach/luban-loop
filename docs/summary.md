# Luban Loop Project Summary

## Positioning

Luban Loop is an engineering delivery workflow for AI coding agents. It gives users a simple entrypoint while keeping the agent accountable for context reading, decision-making, implementation, debugging, verification, review, and final handoff.

鲁班闭环是一个面向 AI 编程 Agent 的工程交付流程。用户只需要描述需求，流程会接管从需求澄清、实现、问题定位、验证到交付说明的完整闭环。

## Tagline

```text
From requirement to verified delivery.
从需求到可验证交付。
```

## User Entry

```text
Use Luban to implement: <requirement>
用 Luban 实现：<需求>
```

## Core Promise

Luban Loop does not promise that every task is easy. It promises that the agent will not skip the engineering basics:

- understand the real project context
- clarify decisions before coding when needed
- keep changes scoped and simple
- diagnose root causes before patching symptoms
- run project-relevant verification
- review readiness before handoff
- report evidence and remaining risks

## Bundled Skills

The installer includes the complete workflow dependency set:

- `luban`: the public Luban Loop entrypoint
- `luban/think`: Chalkline / 墨斗 for requirement clarification and tradeoff decisions
- `luban/square`: Square / 规矩 for quality guardrails
- `luban/hunt`: Rootfinder / 寻因 for root-cause debugging
- `luban/check`: Gauge / 验尺 for readiness review

## Workflow

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

## Why It Matters

AI agents are strongest when they can move quickly, but speed without verification creates fragile output. Luban Loop keeps the interface simple for users while making the agent responsible for the discipline normally expected from a senior engineer.

The workflow is intentionally lightweight. Small tasks stay small. Risky changes get stronger planning, debugging, verification, and review.

## External Copy

```text
Luban Loop is a bilingual engineering delivery workflow for AI coding agents.
It turns a plain user requirement into implementation, verification, review, and a final handoff with evidence.
```

```text
鲁班闭环是一个面向 AI 编程 Agent 的工程交付 workflow。
它把一句简单需求推进成实现、验证、评审和带证据的交付说明。
```
