---
name: aedaping
description: Calculate accurate After Effects parameters for splitting one full-canvas video into rectangular LED wall, stage screen, irregular screen, unequal-width screen, and multi-screen deliverables. Use when the user needs AE comp sizes, layer Anchor Point, Position, Scale, coordinate mapping, export names, or handoff checks for large-screen video splitting.
---

# AE Daping

Use this skill to guide AE users through precise single-row video-wall splitting. The primary output is an AE operation sheet or AE automation script, not a command-line render.

## Primary Input

Ask for or infer:

- Source canvas size: `source_width x source_height`
- Each screen piece size: `name, width, height` or just widths when height equals the source height

Coordinate convention:

- Users should not have to repeat `x/y` for normal work.
- The script calculates `x` by adding the widths of previous pieces from left to right.
- Automatic layout always uses `y=0`.
- `width, height` is the screen's crop size and the AE comp size to create.
- The full-canvas origin `0,0` is the top-left corner.

If the user only gives widths, infer full source height. If the project needs gaps, vertical offsets, or non-zero `y`, ask for explicit rectangles as a special case.

## AE Calculation

Use AE's center-anchor workflow by default because it matches the usual imported footage behavior.

For every screen comp:

```text
Comp Width = screen width
Comp Height = screen height

Layer Anchor Point X = source width / 2
Layer Anchor Point Y = source height / 2

Layer Position X = source width / 2 - screen x
Layer Position Y = source height / 2 - screen y

Layer Scale = 100%, 100%
```

Do not scale, stretch, or fit the source layer unless the user explicitly asks for resizing. The split should happen by comp size plus layer Position.

## AE Automation Script

When the user wants AE to create the split comps automatically, provide `scripts/ae_daping_splitter.jsx`.

Use it this way:

1. Import the full-canvas video in AE.
2. Select that source video or source comp in the Project panel.
3. Run `File > Scripts > Run Script File...`.
4. Choose `ae_daping_splitter.jsx`.
5. Enter each piece as widths or `name,width,height`.

The script creates one numbered comp per screen, adds the same full source to each comp, and sets `Anchor Point`, `Position`, and `Scale` using the default formulas above. It also creates a full-size `MASTER` comp and places all split comps back into their original positions for management and checking.

The script accepts these main input formats:

Pure widths:

```text
1920,1920
```

For `3840x2160`, this creates two `1920x2160` comps that stitch back to `3840x2160`.

Named widths:

```text
Left,1920
Right,1920
```

This uses the source height automatically.

Named width and height:

```text
Left,1920,2160
Right,1920,2160
```

Use the full rectangle format only as a special case when a screen needs a non-zero `y`, a gap, or exact placement:

```text
Left,0,256,1024,1024
Center,1024,0,2048,1536
Right,3072,256,1024,1024
```

It also accepts Excel-style tab-separated columns copied into the input box.

Strict automatic-layout validation:

- Piece widths must add up exactly to the source width.
- Piece heights must equal the source height.
- Widths and heights must be positive whole pixels.
- The script stops and shows an error if the pieces cannot stitch back to the source canvas.

Naming and master comp:

- Split comps are named `01_Name_WIDTHxHEIGHT`, `02_Name_WIDTHxHEIGHT`, etc.
- Unnamed width-list pieces are named `01_S01_WIDTHxHEIGHT`, `02_S02_WIDTHxHEIGHT`, etc.
- The master comp is named `prefix_MASTER_SOURCEWIDTHxSOURCEHEIGHT`.
- The master comp is for management/checking; each numbered split comp remains the independent screen output.

## Required Response Shape

Every AE-splitting answer should include:

1. A short confirmation of source canvas and coordinate convention.
2. A "new comp sizes" table.
3. A reminder: drag the same full original video into every comp.
4. A per-screen AE parameter table with `Anchor Point`, `Position`, and `Scale`.
5. Export naming suggestions, such as `left_1536x1152.mov`, `center_2048x1152.mov`.
6. Validation notes: check out-of-bounds rectangles, accidental overlaps, unintended gaps, and mismatched heights.

Keep the language beginner-friendly and practical for AE users. Respond in the user's language. Tell them which AE shortcut opens each property:

- `A`: Anchor Point
- `P`: Position
- `S`: Scale

## Example

Input:

```text
Source: 5120 x 1152
Left: x=0, y=0, w=1536, h=1152
Center: x=1536, y=0, w=2048, h=1152
Right: x=3584, y=0, w=1536, h=1152
```

Output values:

```text
Source center / Anchor Point for all comps: 2560, 576

Left comp: 1536 x 1152
Anchor Point: 2560, 576
Position: 2560, 576
Scale: 100%, 100%

Center comp: 2048 x 1152
Anchor Point: 2560, 576
Position: 1024, 576
Scale: 100%, 100%

Right comp: 1536 x 1152
Anchor Point: 2560, 576
Position: -1024, 576
Scale: 100%, 100%
```

## Validation Rules

Before finalizing numbers, check:

- `x >= 0`, `y >= 0`, `width > 0`, `height > 0`
- `x + width <= source_width`
- `y + height <= source_height`
- Adjacent screens are continuous only when the user expects no gaps.
- Gaps are valid for stage layouts if they match the physical design.
- Overlaps are suspicious and should be called out unless the user intentionally wants duplicated regions.

## Optional FFmpeg Use

Only use `scripts/split_video_wall.ps1` or `scripts/split_video_wall.py` when the user explicitly asks to batch-cut rendered files outside AE. For AE operation guidance, do not lead with FFmpeg.

Read `references/ae-screen-split.md` for more examples, including vertical splits, gaps, and unequal-height screens. Read `references/ffmpeg-notes.md` only for codec or command-line post-processing questions.
