# AE Screen Split Reference

## Default Method

Use one full-canvas source layer in every output comp. Keep the layer at `Scale = 100%, 100%`. Crop by setting the comp size to the target screen rectangle and shifting the source layer with `Position`.

Default center-anchor formulas:

```text
anchor_x = source_width / 2
anchor_y = source_height / 2
position_x = anchor_x - screen_x
position_y = anchor_y - screen_y
```

In AE:

- Press `A` and set `Anchor Point`.
- Press `P` and set `Position`.
- Press `S` and confirm `Scale = 100%, 100%`.

## Horizontal Continuous Screens

If the user gives only widths and all heights match the source height, infer `x` from cumulative widths:

```text
screen_1_x = 0
screen_2_x = screen_1_width
screen_3_x = screen_1_width + screen_2_width
```

Example:

```text
Source: 5120 x 1152
Widths: 1536, 2048, 1536
Rects:
Left: x=0, y=0, w=1536, h=1152
Center: x=1536, y=0, w=2048, h=1152
Right: x=3584, y=0, w=1536, h=1152
```

## Vertical Split

Example:

```text
Source: 3840 x 1080
Top: x=0, y=0, w=3840, h=540
Bottom: x=0, y=540, w=3840, h=540
```

Source center is `1920, 540`.

```text
Top Position: 1920, 540
Bottom Position: 1920, 0
```

## Screens With Gaps

Gaps are allowed when the stage has physical empty space. Do not auto-close gaps unless the user asks.

Example:

```text
Source: 5000 x 1200
Left: x=0, y=0, w=1600, h=1200
Center: x=1800, y=0, w=1400, h=1200
Right: x=3400, y=0, w=1600, h=1200
```

There is a `200 px` gap between left and center, and a `200 px` gap between center and right.

## Unequal Heights

Use each screen's own `height` as its comp height. Position is still based on the screen rectangle's top-left `x,y`.

Example:

```text
Source: 4096 x 1536
Left: x=0, y=256, w=1024, h=1024
Center: x=1024, y=0, w=2048, h=1536
Right: x=3072, y=256, w=1024, h=1024
```

Source center is `2048, 768`.

```text
Left Position: 2048, 512
Center Position: 1024, 768
Right Position: -1024, 512
```

## Common Mistakes

- Do not use "Fit to Comp" unless resizing is intentional.
- Do not make each comp contain a pre-cropped export if the goal is to calculate crop positions from one master.
- Do not change Anchor Point independently per screen in the default method.
- Do not ignore negative Position values; they are normal for right-side or lower-side crops.
