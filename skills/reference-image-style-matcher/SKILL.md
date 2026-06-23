---
name: reference-image-style-matcher
description: Reverse-match user-provided reference images to the curated film/TVC/short-drama visual reference library before prompt writing. Use when a user sends reference images and wants similar or same-level cinematic style, professional prompt translation, scene style mapping, Banana/Banana Pro/Jimeng/MJ prompts, or video first-frame style control. Extracts visible image features, assigns reference-image roles, matches the closest mother-library reference families, and outputs camera/light/color/material/composition rules for downstream directors.
---

# Reference Image Style Matcher

## Core Role

`$reference-image-style-matcher` is the reference-image reverse lookup layer.

It answers:

```text
这张参考图实际是什么视觉机制？
它更接近母库里的哪类电影/TVC/摄影风格？
哪些地方可以借鉴，哪些不能照搬？
后续提示词应该怎样写，才能保住效果而不是空喊电影感？
```

It does not write final image or video prompts. It produces prompt-ready visual rules for:

```text
style-reference-director
scene-style-map-director
style-bible-director
frame-vision-director
ai-video-prompt-director
prompt-platform-auditor
```

## Required Workflow

When a formal project includes reference images, use this skill before style selection or prompt writing:

```text
reference image(s)
-> reference-image-style-matcher
-> style-reference-director
-> scene-style-map-director
-> style-bible-director
-> frame/video prompt
-> prompt-platform-auditor
```

For quick tests, use a lightweight version: visual features + one best match + prompt translation notes.

## Library Matching

Use `$reference-visual-library` as the source of truth.

| Project line | Match against |
| --- | --- |
| Commercial / promo / TVC / brand film / event / LED | `commercial-promo-library.md` + `shared-elite-cinematography.md` |
| Short drama / narrative / suspense / romance / family / crime | `short-drama-story-library.md` + `shared-elite-cinematography.md` |
| Unknown type | choose the closest line, state the assumption, and include one cinematography anchor |

Do not claim an exact film match unless the user explicitly provides that reference. Prefer:

```text
接近某类视觉机制
相似于某个参考体系的光线/构图/材质方法
```

## Mother-Library Match To Prompt Rule

Reference image analysis alone is not enough. After reading the image, always connect it to the mother library and provide a final-prompt translation sentence.

Required chain:

```text
参考图视觉特征
-> 母库相似项
-> 匹配原因
-> 可继承机制
-> 不继承内容
-> 给最终提示词的转译句
```

`给最终提示词的转译句` must be self-contained and must include:

```text
光线方向
空间压迫/开放关系
构图调度
焦段心理效果
色彩边界
材质触感
人物表演/情绪状态
AI风险负面控制
```

Do not output only “参考这张图风格” or “类似某电影风格”. The matcher result must give downstream prompt directors executable visual language.

## Output 1: 参考图视觉解析表

| 参考图 | 参考角色 | 可见主体/场景 | 景别/机位 | 构图机制 | 镜头/景深感觉 | 光线 | 色彩 | 材质 | 情绪 | 不继承项 | AI风险 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Rules:

- `参考角色` must be narrow: 人物脸、服装、动作、场景、构图、光线、色调、材质、道具、气氛.
- `构图机制` must describe foreground/midground/background, negative space, occlusion, symmetry, compression, reflections, or viewpoint.
- `不继承项` must block unwanted background, text, logo, identity, color, composition, or styling.
- Never average several references into one vague style.

## Output 2: 母库匹配表

| 参考图 | 最接近母库方向 | 匹配度 | 匹配原因 | 顶级摄影锚点 | 可借鉴机制 | 不能照搬 | 给最终提示词的转译句 | 下游使用方式 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Rules:

- Give 1 primary match and up to 2 secondary matches.
- `匹配原因` must refer to visible evidence: lens distance, lighting source, color boundary, blocking, texture, emotional pressure.
- `顶级摄影锚点` must be translated into executable visual language, not left as a name.
- `给最终提示词的转译句` must be concise enough to embed inside every final image/video prompt and must contain light, space, lens, composition, color, material, performance, and AI risk.
- If confidence is low, say `低/中` and give two alternatives instead of pretending certainty.

## Output 3: 提示词转译指令

| 用途 | 必须继承 | 可变化 | 禁止 | 给下游提示词的写法 |
| --- | --- | --- | --- | --- |

The handoff must include:

```text
景别
机位
构图
摄影机/影像系统
焦段
光圈或景深
光线来源和方向
色彩边界
材质质感
情绪强度
参考图角色
AI风险负面词
```

## Prompt Translation Standard

A matched reference is useful only after translation.

Bad:

```text
参考 Fincher，电影感，高级，真实。
```

Good:

```text
程序化悬疑片的克制调度：长焦轻微压缩室内空间，门框和桌面形成前景遮挡，冷白荧光灯从头顶压下，低饱和灰绿色墙面和旧木桌材质，人物表情清楚但被空间压迫。
```

## Safety And Copyright Rules

- Do not copy protected frames, exact production design, celebrity likeness, logos, brands, or distinctive copyrighted compositions.
- Interpret “一样的风格” as “similar visual mechanism”, not exact recreation.
- Do not ask AI tools to generate readable long text from a reference image.
- If the reference image contains text or logos, mark them as `不继承文字/logo`.

## Downstream Contract

`$style-reference-director` receives:

```text
project line assumption
primary/secondary library matches
cinematography anchor
borrowable mechanisms
do-not-copy list
AI risks
```

`$scene-style-map-director` receives:

```text
which scene each reference controls
what changes by scene
what remains project DNA
camera/lens/light/color/material rules
```

`$frame-vision-director` and `$ai-video-prompt-director` receive:

```text
self-contained style language to embed inside every final prompt
reference image role constraints
platform risks for the auditor
```
