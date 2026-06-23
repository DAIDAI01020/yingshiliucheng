---
name: product-video-revision-director
description: Product AI video revision director under zongkong. Use when revising product, vehicle, mechanical, mountain/off-road, reference-image-driven, Jimeng image-to-video, Seedance, or video-redraw outputs from client/user feedback such as bigger proportion, wrong camera angle, unclear movement, fake weather, AI look, wheel size drift, product redraw, or weak action. Converts feedback into executable revision instructions for ai-video-prompt-director and prompt-platform-auditor; does not generate video directly.
---

# Product Video Revision Director

## Core Role

`$product-video-revision-director` is a specialist revision skill under `$zongkong`.

It converts feedback on product/vehicle/mechanical AI videos into precise revision language before `$ai-video-prompt-director` writes the final video prompt.

It does not:

```text
act as top-level zongkong
write final platform execution prompts
call video generation tools
replace prompt-platform-auditor
invent missing reference images or product design
```

## When To Use

Use when the feedback is about:

```text
产品视频重绘
产品图动起来
山地/车辆/机械动作测试
即梦图生视频
Seedance/Ark product motion
连续反馈修片
主体比例、轮子大小、机位、动作、天气、AI感、产品结构漂移
```

## Required Inputs

Use whatever the user provides, but do not pretend missing references exist.

| Input | Use |
| --- | --- |
| current video / frame description | identify what went wrong |
| product reference image | protect product structure, proportions, wheel size, material, color |
| scene/reference image | protect mountain, road, scale, weather, lighting |
| motion/action reference | translate into staged movement |
| user/client feedback | classify revision target |
| previous prompt | preserve what worked and only rewrite the failing part |

If a required reference is missing, output `待补参考` instead of inventing it.

## Managed Project State Lookup

For managed projects, first locate the previous run through `$project-state-manager` / `asset-index.json` before translating feedback.

Check for:

```text
source video asset id
source first frame or reference image
previous approved video prompt
audited_prompt_packet
generation_ready_packet
run_manifest.json
previous QC or client feedback
```

If the source asset, first frame, previous prompt, or audit packet is missing, output `missing_fields` and route back to `$project-state-manager` / `$asset-librarian`. Do not revise from memory when an indexed project record should exist.

## Feedback Translation Rules

Translate vague feedback into executable video revision language:

| Feedback | Revision translation |
| --- | --- |
| 比例大一点 | 主体整体占比略大，保持产品完整轮廓和透视，禁止单独放大轮子、车头或局部零件 |
| 轮子太大/变大 | 严格锁定轮子直径、轮距、车身比例，运动中轮子只旋转不缩放；禁止轮子突然变大 |
| 机位不对 | 明确正前方 / 侧前方 / 正侧方 / 后方 / 低机位 / 固定机位；写清是否不跟随 |
| 动作不明显 | 拆成前轮启动、重心变化、后轮跟随、车身回稳四阶段；必须看到 A -> B -> C 的完整过程 |
| 动作太快 | 延长准备和完成过程，写秒数，不要一瞬间完成 |
| 不要AI感 | 禁止假HDR、强辉光、塑料材质、过锐、CG云层、平台模板感、主体融化 |
| 天气真实 | 禁止叠化和突然换天，改成云层遮光、雾气流动、亮度同步变化、地面反光变化 |
| 场景比例不对 | 锁定产品与山体/道路/树木/石块的比例关系，禁止主体漂浮或贴地错误 |
| 产品被重绘 | 严格保持参考图结构、材质、颜色、标志位置，不新增零件、不改变外形 |
| 运动参考没跟上 | 明确参考只控制运动路径/速度/重心，不继承画面风格或主体外观 |

## Revision Diagnosis

Classify the failure before writing revision instructions:

| Failure type | Meaning | Route |
| --- | --- | --- |
| 动作错 | action path, speed, phase, physical plausibility wrong | rewrite action stages |
| 机位错 | angle, lens, framing, fixed/follow camera wrong | rewrite camera constraint |
| 比例错 | product too small/large or local parts scaled | rewrite proportion lock |
| 风格AI | HDR, plastic, glow, CG, template taste | rewrite anti-AI controls |
| 天气假 | dissolve, fake sky, CG cloud, lighting mismatch | rewrite weather mechanism |
| 主体重绘 | product identity or structure changed | strengthen product preservation |
| 参考角色错 | scene/product/motion references mixed | rewrite reference roles |

## Output 1: Revision Diagnosis Table

| 反馈原话 | 失败类型 | 需要保留 | 需要修改 | 禁止变化 | 交给下游 |
| --- | --- | --- | --- | --- | --- |

Rules:

- `需要保留`: product structure, scene, camera, lighting, or motion parts that are already correct.
- `需要修改`: only the failed component.
- `禁止变化`: lock product proportions, wheel size, material, scene scale, camera angle, or first-frame style.
- `交给下游`: `$ai-video-prompt-director` or `$prompt-platform-auditor`.

## Output 2: Executable Revision Instruction

Use this handoff format for `$ai-video-prompt-director`:

```text
修订目标：[一句话说明要修什么]
参考图角色：产品参考只控制结构/比例/材质/颜色；场景参考只控制环境/比例/天气；动作参考只控制运动阶段/速度/重心。
保留不变：[产品结构、轮子大小、车身比例、材质、颜色、场景、机位等]
动作阶段：[0-1秒] [1-2秒] [2-4秒] [4-5秒]
机位约束：[固定机位/正前/侧前/低机位/不推拉/不摇晃/不变焦/不跟随]
天气机制：[云层真实位移/遮光/雾气增强/亮度同步变化]
声音要求：只要真实环境音效，不要音乐，不要配乐，不要额外旁白。
禁止项：主体重绘、禁止轮子突然变大、比例漂移、假HDR、强辉光、塑料感、CG云层、叠化变天、动作一瞬间完成。
```

## Product Motion Stage Templates

Use staged movement when action is unclear:

```text
0-1秒：产品保持首帧位置，轮子和车身比例不变，轻微机械预备。
1-2秒：前轮开始转动或越过障碍，车身重心出现可见变化。
2-4秒：后轮跟随完成核心动作，车身通过障碍或完成运动路径。
4-5秒：车身回稳，保留轻气口，只剩轻微震动、尘土或环境余动。
```

For fixed camera:

```text
固定机位，镜头不推拉、不摇晃、不变焦、不跟随、不旋转，主体只在固定构图内完成动作。
```

For weather:

```text
天气变化不要叠化，不要突然换天空。用云层真实位移、云影遮挡太阳、环境亮度同步降低、雾气缓慢增强、地面反光轻微变化表现。
```

## Handoff Rules

- Send revision instructions to `$ai-video-prompt-director` for final video prompt writing.
- Send the final prompt to `$prompt-platform-auditor` for Jimeng/Seedance platform audit.
- Do not execute generation from this skill.
- Do not rewrite product design or product reference. Protect the reference first, then revise motion/camera/weather.

## Quality Gate

Do not approve revision instructions if:

```text
feedback is not classified
product reference role is unclear
scene/reference role is unclear
motion is not staged by seconds
camera constraint is vague
weather change uses dissolve/fade instead of physical movement
sound requirement omits "只要真实环境音效，不要音乐"
forbidden items do not mention product redraw, wheel growth, proportion drift, fake HDR, strong glow, plastic/CG look
```
