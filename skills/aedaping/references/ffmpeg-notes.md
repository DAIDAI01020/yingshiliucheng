# FFmpeg Notes for AE and Video Wall Delivery

## AE export starting point

Prefer exporting one full-wall master from After Effects, then split that master into screen tiles. This avoids AE composition drift between screens and keeps timing consistent.

Recommended master choices:

- Use a mezzanine codec if the file will be re-encoded, such as ProRes 422 HQ, DNxHR HQX, or image sequence.
- Use the exact full-wall canvas when known: `columns * screen_width` by `rows * screen_height`.
- Keep square pixels unless the site playback system requires otherwise.
- Use constant frame rate.

## Tile encoding

For most playback systems:

- H.264: `libx264 -crf 18 -preset medium -pix_fmt yuv420p`
- H.265: `libx265 -crf 20 -preset medium -pix_fmt yuv420p`
- Higher-end servers may prefer ProRes, Hap, NotchLC, or vendor-specific codecs.

Ask before assuming a codec when the venue uses media servers such as Disguise, Watchout, Resolume, Pixera, Millumin, or BrightSign.

## Mapping convention

Use row-major naming from top-left to bottom-right:

- `r01_c01`: top-left
- `r01_c02`: first row, second column
- `r02_c01`: second row, first column

Keep a CSV/JSON manifest with file name, row, column, crop origin, output width, and output height.

## Common checks

- All tiles must have the same duration and frame rate.
- All tiles should start at timecode zero unless the system asks otherwise.
- Disable audio on every tile unless there is a dedicated screen audio requirement.
- If the source resolution is not divisible by the layout, prefer scaling the full-wall master to an exact divisible canvas over making uneven tile sizes.
- Confirm whether the physical wall is normal row-major order or has a custom processor mapping.
