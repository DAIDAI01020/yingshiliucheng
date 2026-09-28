---
name: client-feedback-interpreter
description: Interpret vague client feedback into actionable film visual revisions. Use when clients say things like more premium, too AI, not cinematic enough, too messy, not on brand, not impactful, product inaccurate, people look fake, or the image does not match the proposal, and convert that feedback into specific changes for style, storyboard, prompts, references, regeneration, QC, or PPT wording.
---

# Client Feedback Interpreter

## Core role

Translate client language into production actions. Do not immediately rewrite everything. First identify what the client is really reacting to and which part of the workflow should change.

## Common translations

| 客户反馈 | 可能含义 | 执行动作 |
| --- | --- | --- |
| 不够高级 | 元素太多、材质廉价、光线不克制 | 减少元素密度，增强材质、留白、控制光比 |
| 太AI | 过度锐化、假光影、主体不真实 | 加强真实摄影逻辑，降低特效词，补充负面词 |
| 不够大气 | 尺度不够、镜头太平、节奏弱 | 加大空间尺度，改低机位/广角/推进感 |
| 不像品牌 | 色彩、产品、语气或符号偏离 | 回到品牌色、产品结构、核心价值和调性 |
| 画面太乱 | 主体层级不清、背景抢戏 | 简化主体，明确前中后景，压低背景细节 |
| 人物太假 | 脸、手、姿态、皮肤、表情问题 | 简化动作，补充人物参考，强化负面词 |
| 产品不准 | 结构、比例、材质、标识错误 | 加产品参考图，明确不可改变结构 |
| 没有记忆点 | 缺少核心视觉符号或落版 | 强化主视觉、产品轮廓、主题符号 |

## Output

### 反馈翻译表

| 反馈原话 | 真实问题判断 | 影响范围 | 执行动作 | 对应Skill | 是否触发重出图 | 备注 |
| --- | --- | --- | --- | --- | --- | --- |

### 修改优先级

| 优先级 | 修改项 | 原因 | 下一步 |
| --- | --- | --- | --- |

## Rules

- If feedback is vague, translate it into 2-3 likely execution meanings and recommend the most practical one.
- If feedback affects only one image, do not change the full style package.
- Treat repeated feedback as evidence to investigate. Check reference roles, prompt inheritance, execution artifacts, and intended style before proposing a bible change; repetition alone does not authorize a global redesign.
- After interpreting feedback, route execution to `$revision-director`.
- Inspect available media before diagnosing; use `$image-qc-director` or `$video-qc-director` as applicable. Label interpretations as hypotheses when evidence is absent.
- Translate each revision into a visible acceptance condition and preservation boundary, not just an extra adjective or longer negative prompt.
