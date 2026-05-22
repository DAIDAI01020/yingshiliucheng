# Midjourney Parameter Guide

Use this guide for parameter suffixes. Place parameters at the end of the prompt, separated by spaces, with no trailing punctuation.

Sources checked May 16, 2026:

- Version: https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version
- Parameter list: https://docs.midjourney.com/docs/parameter-list
- Aspect ratio: https://docs.midjourney.com/hc/en-us/articles/31894244298125-Aspect-Ratio
- Image prompts: https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts
- Style reference: https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference
- Omni reference: https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference
- Video: https://docs.midjourney.com/docs/en/video

## Core Image Parameters

| Parameter | Use | Practical default |
| --- | --- | --- |
| `--ar W:H` / `--aspect W:H` | Output shape. No decimals. | `--ar 16:9` for cinematic/storyboard/UI, `--ar 9:16` for mobile, `--ar 1:1` for square assets. |
| `--v 7` | Stable current default image model. | Use unless a different version is requested. |
| `--v 8.1` | Newer/faster model with HD/SD behavior. | Offer when the user asks for newest/fastest or V8.1 explicitly. |
| `--niji 7` | Anime/eastern illustration model. | Use for anime, manga, character illustration, Japanese game art. |
| `--raw` | Reduces default Midjourney styling. | Use for product, UI, literal art direction, and prompt adherence. |
| `--s #` / `--stylize #` | Artistic interpretation, 0-1000 in current models. | 50-150 controlled; 250-500 expressive; 750+ exploratory. |
| `--c #` / `--chaos #` | Variety across the image grid, 0-100. | 0-10 controlled; 20-40 exploration; 60+ wild ideation. |
| `--q #` / `--quality #` | Initial grid compute/detail. | V7 default `1`; use `2` or `4` only when worth extra cost. |
| `--seed #` | Repeatability/experimentation. | Use when comparing prompt changes or making controlled variants. |
| `--no ...` | Exclude unwanted elements. | Keep concise, e.g. `--no text, watermark, qr code`. |
| `--tile` | Seamless pattern tile. | Use for wallpaper, textile, surface pattern, game textures. |
| `--repeat #` / `--r #` | Multiple runs. | Use only when the user wants breadth and understands GPU cost. |

## Reference Parameters

| Parameter | Use | Notes |
| --- | --- | --- |
| Image URL before text | General image prompt for content, composition, colors. | Text should describe the desired result, not "edit this image." |
| `--iw #` | Image prompt weight. | Use to tune influence of image prompts when available. |
| `--sref URL_OR_CODE` | Style reference for look, palette, medium, texture, lighting. | Requires a text prompt. Can combine multiple refs. |
| `--sw #` | Style reference weight, 0-1000. | Default is 100; lower for subtle, higher for strong style matching. |
| `--sv #` | Style reference version. | V7 defaults to `--sv 6`; `--sv 4` accesses older V7 behavior/style codes. |
| `--oref URL` | Omni Reference for person/object/vehicle/prop identity in V7. | Only one image. More costly. Not for inpainting/outpainting. |
| `--ow #` | Omni Reference weight. | Use lower values when the reference identity should be looser. |
| `--p ...` / `--profile ...` | Personalization or moodboard profile. | Use only when the user provides a profile/moodboard ID or asks for it. |

## Video Parameters

Use video-specific parameters only for video prompts.

| Parameter | Use |
| --- | --- |
| `--motion low` | Subtle motion, slow camera, calmer scenes. Default choice. |
| `--motion high` | Bigger movement/camera action; higher glitch risk. |
| `--loop` | Reuse starting frame as ending frame. |
| `--end URL` | Set a custom ending frame URL. |
| `--bs 1`, `--bs 2`, `--bs 4` | Video batch size; lower saves GPU time. |
| `--raw` | More literal motion control. |

## Compatibility Notes

- Parameters belong at the end of the prompt; do not put normal prompt text after parameter flags.
- Aspect ratios use integer ratios. Convert decimals such as 1.39:1 to `139:100`.
- `--q 4` is not compatible with Omni Reference.
- Image-only prompts are not compatible with `--stylize` or `--weird`; include text when using those controls.
- Style Reference is for style, not identity. Use Omni Reference for identity/object continuity in V7.
- Omni Reference accepts one image and is not compatible with V6.1 editing features such as inpainting/outpainting.
- Video prompts support only video-specific parameters such as motion, raw, loop, end frame, and batch size.

## Suggested Suffixes

- Controlled product/UI: `--ar 16:9 --v 7 --raw --s 75 --c 5`
- Cinematic storyboard: `--ar 16:9 --v 7 --s 150 --c 10`
- Character continuity: `--oref URL --ar 16:9 --v 7 --raw --s 100`
- Style exploration: `--sref URL --sw 200 --ar 3:4 --v 7 --s 300 --c 25`
- Anime character: `--ar 2:3 --niji 7 --s 250 --c 10`
- Seamless pattern: `--tile --ar 1:1 --v 7 --s 200`
- Video first-frame animation: `--motion low --bs 1 --raw`
