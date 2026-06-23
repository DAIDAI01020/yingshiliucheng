---
name: scene-board-image-prompter
description: Write built-in imagegen prompts for professional scene storyboard board / production design board images. Use when characters, props, setting, scene function, character positions, camera positions, eyelines, shot beats, and lighting/material direction are already selected, and the user wants one board/grid image showing the scene reference, character refs, prop refs, overhead camera map, shot preview cells, and material/light references. This skill outputs prompts only; it does not choose story, style, or generate video.
---

# Scene Board Image Prompter

## Core Role

`$scene-board-image-prompter` writes one professional built-in `image` prompt for a scene storyboard / production design board.

Use it only after the scene decisions already exist:

```text
characters selected
props selected
set / location selected
scene function selected
character positions selected
camera positions / shot numbers selected
lighting and material direction selected
```

It outputs a single copyable prompt for built-in imagegen to create a board/grid image.

It does not choose characters, choose props, choose scene style, audit shot logic, write Banana prompts, write Jimeng/Seedance motion prompts, or generate video.

## Default Tool Boundary

Storyboard board images default to built-in `image` / imagegen.

Reason:

```text
built-in imagegen is better for natural-language layout instructions, one complete board image, blank label bands, visual reference grids, and preserving a production-design-board feel.
Banana/Banana Pro may be used later only to refine or regenerate individual cells/keyframes, not as the default first board image tool.
Jimeng is not used for storyboard board still images.
```

## Required Inputs

Use all available inputs, but do not invent missing production decisions.

Required for a formal board:

```text
scene_name
scene_function
aspect_ratio
main setting / environment
characters and stable appearance
props and material/size
character position relationship
camera positions or shot numbers
shot beats / key moments
lighting direction
material references
continuity note
AI risk controls
```

If important inputs are missing, output:

```text
missing_fields:
route_back_to:
```

For quick/test, write a lighter board prompt but label it `quick/test`.

## TVC Segment Storyboard Board

Use this route when `$storyboard-planner` provides `tvc_segment_storyboard_lock` or when the user asks for TVC广告故事板测试, 剧情包装广告故事板, 每一大段故事板, or 直接给 image 出故事板.

Default tool remains built-in `image` / imagegen.

Rules:

```text
One large segment/chapter = one horizontal storyboard board.
Use `tvc_segment_storyboard_lock` as the image authority.
Inherit characters, costumes, props, products, scene, style, and shot beats from upstream director/prompt outputs.
Do not redesign characters, props, products, scene, or style.
If `jimeng_direct_reference_board: true`, the whole board will be uploaded to Jimeng/Seedance as one visual reference image. Make every visual cell large, clean, and easy for a video model to parse.
Do not turn the board into a poster, brand key visual, marketing PPT, or dense readable text layout.
```

Board types:

```text
ad_sequence_board: 6-12 large TVC storyboard frames arranged in a clean grid, like an agency ad board. Each frame shows one clear commercial beat, product/brand moment, character action, and camera feeling. Simple frame numbers are allowed. Captions should be sparse or blank unless the user supplies exact copy.
design_reference_board: production design guide style, with character design/model sheet, costume, hero props/product, set design, color/material swatches, and 3-6 key visual frames.
spatial_continuity_board: video-model control board, with main scene reference, overhead camera map, fixed character positions, eyelines, shooting execution flow, 4-6 storyboard preview cells, and lighting/material strip.
```

TVC board layout:

```text
top header band: blank project/segment/title area, no readable small text
left hero panel: main segment scene reference or key art frame with locked characters, product/brand object, environment, and emotional relationship
character design/model sheet row: character front/side/back or 3-4 stable pose/costume cells when upstream provides character appearance
props/product column: hero props, product structure, material, scale, wear/use state, close-up cells
set design row: location/set geography, entrance/window/table/vehicle/product placement, atmosphere reference
center strip: rhythm line or simple arrow flow showing the segment's 4-8 key beats
right column: product/brand exposure, benefit cue, ending landing visual, using blank label boxes
bottom row: shot storyboard preview cells, one image per key beat
bottom strip: lighting, color palette, material swatches, skin/fabric/product-surface references
footer note strip: blank note area for later readable labels
```

Direct-to-Jimeng / Seedance board rules:

```text
The board is a reference control image for video generation, not the final video frame.
Keep white margins, grid lines, numbering, arrows, labels, and note areas visually secondary.
Make character faces, costumes, props/products, main set, and key action frames much larger than labels.
Do not fill the board with tiny text. Use blank caption bars, simple numbers, broad arrows, and clean section spacing.
If copy/slogan is needed, use it as a design cue only; exact readable text should be added later in editing.
```

TVC segment prompt shape:

```text
为一段[TVC segment_name]制作一张横版 TVC storyboard board，画面是广告故事板测试图和制作控制板，不是海报，不是营销PPT。

本板只继承上游已定设定：人物为[character_lock]，服装为[costume_lock]，道具为[prop_lock]，产品/品牌露出为[product_or_brand_lock]，场景为[scene_lock]，整体风格为[style_lock_compact]。不要重新设计人物、道具、产品、场景或风格。

这张板后续会整张上传给即梦/Seedance作为视频参考图，所以画面必须让视频模型清楚识别：人物是谁、穿什么、道具/产品是什么、主要场景是什么、关键动作节拍是什么。白底排版、分格线、编号、箭头和备注区只能作为辅助结构，不能成为画面主体。

左侧主视觉大区域：展示本大段主场景和人物/产品关系，像广告故事板的 hero frame / key visual frame，[scene_lock]中[characters/products]按照段落功能[segment_function]处在同一空间里。

角色设计区域：用 character design / model sheet cells 展示[character_lock]，包含稳定外貌、服装、身形、表演状态，可用正面/侧面/背面或3-4个姿态格表现；只继承上游形象，不重新设计。

道具/产品区域：用 props / product reference cells 展示[prop_lock]和[product_or_brand_lock]的形状、比例、材质、磨损、使用状态和关键细节，可包含局部特写、尺寸对比和空白备注框。

场景设计区域：用 set design cells 展示[scene_lock]的空间地理、门窗桌椅/道路/车辆/产品位置、气氛和主光源，让场景关系可被拍摄团队理解。

中间节奏线：用4-8个连续 storyboard preview cells 表现关键 beat：[key_beats]，每格保持同一人物、同一道具/产品、同一场景逻辑和连续视觉风格。

右侧区域：展示产品/品牌记忆点和结尾落点[ending_or_brand_landing]，只用空白标签框和简单编号，不生成可读广告语、logo或小字。

底部横条：lighting/material/color reference，展示本段光线方向、色彩板、真实材质、皮肤、衣料、产品表面、环境灰尘或旧物磨损，像专业美术设定板里的 swatches。

整体像专业广告分镜 storyboard board / production design guide，包含主视觉、角色设计、道具/产品、场景设计、关键镜头、色彩材质和备注空白区；真实摄影缩略图质感，分区清楚，节奏明确，产品/人物/道具关系清楚。

禁止：重新设计人物、换服装、改变产品结构、改变道具比例、变成海报、营销PPT感、可读小字、乱码文字、随机logo、水印、假HDR、过度锐化、塑料皮肤、空间关系混乱、把备注区写满假文字。

[aspect_ratio]。
```

### 广告连续画面板 Prompt Shape

Use this when `board_type: ad_sequence_board`.

```text
为一支[TVC/ad name]制作一张横版广告 storyboard sequence board，像专业TVC广告分镜板，不是海报，不是PPT。

整张板由[6-12]个大画面格组成，每格是一个清楚的广告镜头/关键beat，按阅读顺序排列。所有格子保持同一主角[character_lock]、同一服装/发型、同一产品/品牌物件[product_or_brand_lock]和统一广告色调[style_lock_compact]。

每格都要有真实摄影感：明确景别、人物动作、产品位置、环境光线和情绪状态。关键beat包括：[key_beats]。产品/品牌露出要清楚但不要伪造不可读logo或广告语。

允许：简单大号镜头编号、少量空白字幕条、手写感色块或图形标记。禁止：密集小字、乱码文字、把版面做成海报、人物五官漂移、产品变形、每格风格不一致。

这张板后续会整张上传给即梦/Seedance作为视频参考图。请让每个画面格足够大、主体清楚、动作连续，避免视频模型把白边、编号、字幕条、分格线当成真实场景内容。

[aspect_ratio]。
```

### 空间连续性控制板 Prompt Shape

Use this when `board_type: spatial_continuity_board`.

```text
为一段[TVC/scene name]制作一张横版 video reference control board，用于后续整张上传给即梦/Seedance控制人物位置、视线、镜头节拍和空间连续性。

左上是 Main Scene Reference：展示主要场景、人物位置、桌椅/门窗/产品/道具关系和主光源。
中上是 Overhead Camera Map：用简单俯视图固定每个角色、产品/道具、机位编号、移动方向和视线方向。
右侧是 Shooting Execution Flow：用[4-6]个竖向节拍卡表现镜头、移动和情绪变化。
中下是 Character Reference：展示每个主要人物稳定外貌、服装、表演状态。
底部是 Shot Storyboard Preview：展示[key_beats]的关键画面，人物不能消失，位置和视线必须连续。
最底部是 Lighting & Material Reference：展示主光源、皮肤、衣料、产品/道具材质、空间表面和色彩板。

这张板的目标是防止视频模型出现多人漂移、位置不对、视线不对、人物消失、道具消失。画面要清楚、格子大、空间关系明确。不要生成密集可读文字、乱码文字、复杂花哨UI或营销PPT感。

[aspect_ratio]。
```

## Board Layout Standard

The board should look like a professional film production-design guide, not a poster, not a marketing page, and not a decorative moodboard.

Use this layout:

```text
top header band: project / scene / shot range / duration / scene function, with mostly blank label space
left large panel: main scene reference, showing the actual set geography and character relationship
center top panel: overhead camera map, with simple shapes, character positions, prop positions, camera numbers, arrows, eyeline lines
right column: shooting execution flow, 4-6 beat cards with shot size, camera position, emotion, action idea shown visually
middle row: character reference cells, stable face/costume/body state, front/side/back when useful
side or lower cells: prop references, product/object structure, material and scale
bottom row: shot/keyframe preview cells, one image per key beat
bottom strip: lighting and material reference cells, practical lamp/window light/skin/fabric/wood/metal/glass/dust
footer note strip: one blank continuity-note bar
```

## Text Rule

Do not ask imagegen to create readable small text.

Allowed:

```text
blank title bands
empty label boxes
simple large numbers like 1, 2, 3, 4
arrows
color-coded lines
simple icon-like camera markers
empty note panels
```

Forbidden:

```text
readable paragraphs
exact Chinese/English captions
brand logos
legal text
small UI labels
fake typography as a design feature
```

Final readable labels can be added later in layout software.

## Prompt Formula

Use Chinese natural-language instructions with a few English production terms.

```text
为一场[scene_name]制作一张横版 production design storyboard board，画面是电影美术设定板和场戏控制板，不是海报，不是宣传页。

整体是干净的白色/浅灰纸面排版，专业 film production design guide 质感，分区清楚，留出空白标题栏、编号框、箭头、色块和备注区；不要生成可读小字，不要乱码文字，不要logo。

左侧大区域：主场景参考，[setting/environment/time/light]，[characters]按照[character_position_relationship]处在同一空间中，能看清[door/window/table/prop/space cues]。

中上区域：overhead camera map，用简洁平面图表现[characters]的位置、[props]的位置、门窗桌椅关系、机位编号、镜头方向箭头和视线关系；空间关系清楚，不追求真实小字。

右侧竖栏：shooting execution flow，用[4-6]个小画面表现本场戏关键beat：[beat_1]、[beat_2]、[beat_3]、[beat_4]。

中下区域：character reference cells，展示[character_A]、[character_B]、[character_C]的稳定外貌、服装、年龄状态和表演状态，像剧组角色参考图。

侧边/下方区域：prop reference cells，展示[props]的形状、比例、材质、磨损和使用状态。

底部横条：lighting and material reference，展示[lighting_direction]、[practical_sources]、[materials]，包括皮肤、衣料、桌面、墙面、玻璃/金属/木头/灰尘等真实材质。

底部关键帧预览：shot storyboard preview cells，展示[shot/keyframe list]，每格保持同一场景、同一人物、同一道具和连续空间关系。

整体真实摄影缩略图质感，统一色调，人物位置清楚，道具比例准确，机位地图清楚，关键镜头预览有连续性，像专业电影项目给导演/摄影/美术/AI出图团队看的场戏控制板。

保留真实摄影的不完美：自然皮肤纹理、轻微瑕疵、衣料褶皱、环境灰尘、旧物磨损、自然暗部颗粒、真实光源、真实景深和原有光比。

禁止：海报感、营销PPT感、花哨UI、过度设计、可读小字、乱码文字、随机logo、水印、塑料皮肤、假HDR、过度锐化、CG感、模板感、人物五官漂移、道具变形、空间关系混乱、机位箭头混乱。

[aspect_ratio]。
```

## Output Shape

Return:

```text
## 内置 image 故事板宫格提示词

[copyable prompt]

## 生成备注
- 工具：内置 image / imagegen
- 用途：一张场戏故事板控制板，不是最终视频提示词
- 后续：可把单格裁出后交给 Banana/Banana Pro 精修，关键帧再交给 ai-video-prompt-director 写即梦/Seedance运动提示词
```

## Anti-AI Requirements

Every prompt must include:

```text
真实摄影缩略图质感
自然皮肤纹理
衣料褶皱
环境灰尘或旧物磨损
自然暗部颗粒
明确现实光源
真实景深
不过度锐化
不磨皮
不做假HDR
```

## Quality Gate

Do not output the final prompt if a formal board lacks:

```text
scene function
main set geography
character positions
prop roles
camera map or shot numbers
key beats
lighting/material direction
continuity note
AI risk controls
```

## Hard Rules

- This skill outputs image prompt only.
- Default tool is built-in imagegen.
- Do not write Banana split prompts here.
- Do not write Jimeng/Seedance motion prompts here.
- Do not ask imagegen to create exact readable small text.
- Do not redesign upstream characters, props, scene, or style.
