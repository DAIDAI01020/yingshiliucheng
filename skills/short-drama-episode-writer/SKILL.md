---
name: short-drama-episode-writer
description: Write short drama episode outlines, scene structures, opening hooks, conflict escalation, reversal points, cliffhangers, and next-episode leads for vertical micro-series and character-driven short-form drama.
---

# Short Drama Episode Writer

## Core Role

Turn concept and characters into episode structure.

Use when the user needs分集大纲, 单集结构, 场次安排, or wants an existing script tightened for short drama rhythm.

## Episode Rhythm

| 段落 | 功能 |
| --- | --- |
| 0-3秒 | 钩子：冲突、悬念、反常识、强情绪 |
| 3-15秒 | 建立人物关系和当前困境 |
| 15-35秒 | 冲突升级或信息反转 |
| 35-55秒 | 情绪爆点、动作点或关键选择 |
| 结尾 | 留悬念、反转、下一集引子 |

## Output

| 集数 | 开场钩子 | 本集冲突 | 关键场次 | 反转点 | 结尾悬念 | 下一集引子 |
| --- | --- | --- | --- | --- | --- | --- |

## Existing Script Diagnosis

When the user gives a finished script:

| 诊断项 | 结论 | 修改建议 |
| --- | --- | --- |
| 钩子是否够快 |  |  |
| 人物关系是否清楚 |  |  |
| 冲突是否升级 |  |  |
| 反转是否有效 |  |  |
| 结尾是否有追看 |  |  |
| AI执行难点 |  |  |

## Formal Hook Gate

For managed formal short-drama projects, output or update `references/hook-audit.md` before visual execution:

```text
status: draft / approved / passed
hook_audit_packet
opening_hook
audience_question
information_gap
conflict_entry
character_relation_clarity
payoff_or_cliffhanger
ai_execution_risk
```

The hook check is not a rewrite request by default. If the script already exists, diagnose whether the first 3-8 seconds are strong enough and suggest targeted fixes only where the hook, information gap, or conflict entry is weak.

## Approval Evidence

Keep proposed material `draft`. Use `passed` only for a completed applicable review and `approved` only for an actual accepted decision; record its source. File creation alone does not pass a production gate. Preserve existing valid approvals and stable character/episode IDs.

## Rules

- Do not rewrite a finished script unless the user asks.
- First diagnose structure, then suggest targeted edits.
- Keep each episode shootable and AI-generatable.
