# Banana Pro Prompt Patterns

Use these patterns as compact starting points. Keep prompts specific to the user's subject and avoid copying placeholder text.

## Text-to-Image

```text
生成一张[输出类型]：[主体]位于[场景]，画面比例[比例]。
构图：[景别/视角/主体位置/前中后景关系]。
视觉：[材质、光线、色彩、镜头语言、风格]。
细节：[必须保留或强调的结构、纹理、品牌、动作、情绪]。
约束：画面干净，不出现随机文字、水印、二维码、额外标志或无关元素。
```

## Image-to-Image

```text
以输入图作为主要参考，保持[主体/产品/角色/UI]的身份、比例、结构、颜色和关键细节一致。
目标：将画面改为[新场景/新动作/新风格/新构图]。
构图：[景别、镜头、主体位置、背景关系]。
光影与质感：[真实摄影/商业广告/插画/设定图等具体要求]。
约束：不要改变核心身份特征，不添加随机文字、水印、二维码或无关道具。
```

## Multi-Reference

Assign roles before the prompt:

- Image 1: character reference
- Image 2: scene reference
- Image 3: product or prop reference
- Image 4: composition or style reference

```text
综合所有参考图生成一张[输出类型]。
角色：严格参考 Image 1 的身份、脸型、发型、服装、比例和气质。
场景：使用 Image 2 的空间结构、光线方向、材质和氛围。
产品/道具：保持 Image 3 的品牌、结构、颜色、比例和关键细节一致。
构图/风格：参考 Image 4 的镜头语言和画面节奏，但不要复制不相关元素。
最终画面：[具体动作、景别、镜头、环境、光影、风格]。
约束：参考图之间的元素必须融合自然，不要生成拼贴感、随机文字、水印或二维码。
```

## Character Sheet

```text
生成角色设定图：同一角色三视图，正面、侧面、背面，白色背景，清晰角色设计稿。
角色特征：[年龄/体型/发型/服装/配饰/气质]。
一致性：三视图必须保持同一角色一致，五官、发型、服装结构、颜色、比例和配饰完全一致。
风格：[项目美术风格或摄影/插画要求]。
约束：不要出现场景、动作姿态、复杂背景、随机文字、水印或二维码。
```

## Clean Scene Plate

```text
生成纯场景空镜：[场景名称/空间类型]。
只表现环境空间、道具陈设、材质、光影和氛围；无人、无角色、无人物剪影、无动物、无主体人物。
构图：[广角/中景/俯拍/平视等]，[前景/中景/背景层次]。
风格：[真实摄影/电影感/商业广告/概念设定等]。
约束：画面干净，不出现随机文字、水印、二维码或不相关主体。
```

## Product Or Prop Design

```text
生成道具/产品设定图：[产品或道具名称]，主体清晰，白色或干净中性背景。
保持品牌、结构、颜色、比例、材质和关键细节一致。
展示方式：[单角度/多角度参考/局部细节/包装与主体关系]。
质感：[材质、反光、工艺、边缘、标识处理]。
约束：无人物干扰，不改变核心设计，不出现随机文字、水印、二维码或额外品牌。
```

For vehicles, add: `多角度参考，保持同一车辆一致性，车身比例、轮毂、灯组、品牌识别和颜色完全一致。`

## Storyboard First Frame

```text
生成 16:9 分镜首帧：[镜头编号/标题]。
主体：[角色/产品/道具]，严格保持与参考资产一致。
场景：[场景资产]，保持空间结构、光线和氛围一致。
动作：[当前镜头瞬间动作]。
镜头：[景别、焦段感、机位、运动趋势]。
光影与风格：[整体影像风格，真实摄影/商业广告/电影感等]。
构图：[主体位置、前中后景、视觉焦点]。
约束：不要随机字幕、水印、二维码；不要改变角色、场景或道具的核心识别特征。
```

## QA Checklist

Before handing off, check:

- The model is `google/gemini-3.1-flash-image-preview`.
- `image_config.aspect_ratio` and `image_config.image_size` match the task.
- Reference image roles are explicit when images are used.
- Identity, product, UI, or scene continuity anchors are stated.
- The prompt avoids random text, watermarks, QR codes, and unrelated objects.
