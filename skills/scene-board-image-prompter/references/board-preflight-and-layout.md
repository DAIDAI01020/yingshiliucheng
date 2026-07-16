# Board Preflight And Layout

## Contents

- Common preflight
- Variant requirements
- Common layout
- Text and risk rules

## Common Preflight

Pass only when:

```text
an approved source packet or selected board unit exists
the board variant and board id are clear
characters/props/products/set decisions required by the variant exist
positions, camera map, eyelines, or axis exist when continuity/coverage needs them
key beats or preview cells are selected
light/material direction exists where visual references need it
video_reference_inherit and do_not_inherit exist when video use is implied
```

Fail when a board tries to cover several unrelated story turns, compresses multiple board units, invents missing characters/props/camera decisions, or lacks the control information that gives the board a production function.

## Variant Requirements

```text
production_design_storyboard_board -> hero scene, character design, props/products, set geography, blocking path, camera map, execution flow, preview cells, light/material strip
commercial_segment_board -> segment function, locked commercial/program/event/brand objects, hero frame, key beats, landing, reference boundary
ad_sequence_board -> ordered large beat cells, stable identity/product/style, sparse numbering, clear video-reference boundary
design_reference_board -> character/model sheet, hero props/products/program objects, set/stage/location, 3-6 key frames, light/material/color strip
spatial_continuity_board -> main scene, overhead map, fixed positions, eyelines, execution flow, preview cells, light/material strip
short_drama_scene_continuity_board -> master wide, axis/eyeline map, A/B background sides, coverage cells, prop/light anchors
```

## Common Layout

Use large visual zones:

```text
header/title band with blank label space
hero scene or master-wide panel
character/subject reference cells when applicable
prop/product/object cells
set/stage/location geography
overhead camera/axis map when applicable
execution/beat flow
storyboard or coverage preview cells
light/material/color strip
blank note/footer area
```

Keep white/light-gray margins, grid lines, arrows, and labels visually secondary. Make content cells large enough for human review and downstream reference use.

## Text Rules

Allow blank title bars, empty label boxes, simple numbers, arrows, color lines, and camera icons. Avoid dense paragraphs, exact captions, legal copy, logos, tiny UI, or fake typography.

## Risk Selection

Select risks by board content:

```text
layout risks -> crowded cells, tiny text, unclear hierarchy, poster/PPT drift
continuity risks -> identity drift, prop movement, room repaint, axis/eyeline error, light-position drift
product risks -> structure/proportion/material drift
photographic cell risks -> face/hand/material/light artifacts only where people or real photography appear
video-reference risks -> layout contamination, missing characters, wrong positions, board artifacts treated as scene content
```

Do not paste a universal live-action anti-AI list into graphic maps or non-photographic cells.
