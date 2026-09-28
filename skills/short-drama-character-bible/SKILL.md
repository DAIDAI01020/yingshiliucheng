---
name: short-drama-character-bible
description: Create and maintain character bibles for short drama AI workflows, including character biographies, relationship maps, visual anchors, costume anchors, performance keywords, reference image roles, and continuity constraints for multi-scene generation.
---

# Short Drama Character Bible

## Core Role

Protect character continuity across scripts, keyframes, and videos.

Use before generating multiple scenes with recurring characters, or when the user provides character reference images.

## Character Bible

| 项目 | 内容 |
| --- | --- |
| 角色名 |  |
| 年龄/身份 |  |
| 外貌锚点 | 脸型、发型、身高体态、标志性特征 |
| 服装锚点 | 主服装、颜色、材质、配饰 |
| 性格/欲望 |  |
| 关系网 |  |
| 表演关键词 | 克制、爆发、犹豫、冷漠、温柔、压迫感等 |
| 参考图角色 | 人物身份/服装/妆发/表情/动作/构图 |
| AI一致性提示 | 每次生成必须保持的脸、发型、服装、比例、气质 |
| 禁止偏移 | 不能改变年龄、发型、服装结构、身份气质等 |

## Formal Gate Output

For managed formal short-drama projects, output or update `references/character-continuity.md` with:

```text
status: draft / approved / passed
character_continuity_packet
character_id
name
story_role
face_anchor
hair_anchor
age_body_anchor
costume_anchor
performance_anchor
relationship_state
reference_image_roles
generation_anchor
allowed_scene_changes
forbidden_drift
character_continuity_source
director_contribution_packet
visual_helpfulness_targets
```

The `generation_anchor` must be compact enough for image/video prompts and specific enough to prevent face, hair, costume silhouette, age, body type, and performance drift.

For formal projects, `director_contribution_packet` must state:

```text
owner_skill: short-drama-character-bible
decision_owned: character identity, costume silhouette, relationship state, performance anchor, reference image roles
visual_controls_contributed: face anchor, hair anchor, age/body anchor, costume anchor, body proportion, expression range, performance restraint
downstream_must_preserve: generation_anchor, forbidden_drift, reference_image_roles, character_continuity_source
must_not_be_overwritten_by: style reference, camera movement, platform beautification, unrelated actor likeness
```

`visual_helpfulness_targets` should list the concrete face/hair/costume/body/performance details that a prompt must protect.

## Relationship Map

| 角色A | 角色B | 关系 | 冲突 | 情绪状态 |
| --- | --- | --- | --- | --- |

## Approval Evidence

Keep proposed material `draft`. Use `passed` only for a completed applicable review and `approved` only for an actual accepted decision; record its source. File creation alone does not pass a production gate. Preserve existing valid approvals and stable character/episode IDs.

## Rules

- Do not let a style reference override character identity.
- Separate character reference from scene/style/composition references.
- If character consistency is weak, recommend character sheet generation before story scenes.
- Avoid changing hairstyle, age, costume silhouette, or identity markers between scenes unless scripted.
