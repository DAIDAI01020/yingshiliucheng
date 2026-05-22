# Midjourney Prompt Patterns

Use these as compact structures. Replace bracketed fields and keep the final prompt natural.

## Text-To-Image

```text
[subject], [output type], [action or pose], [environment], [composition/framing], [camera/lens or visual perspective], [lighting], [materials/details], [style/medium], [mood], clean image, no random text --ar [ratio] --v 7 [parameters]
```

## Cinematic Storyboard Frame

```text
[shot scale] cinematic storyboard frame of [subject] [action], set in [location/time], [camera angle and movement implication], [foreground/midground/background composition], [lighting and color palette], [continuity anchors], film still quality, clear readable silhouettes --ar 16:9 --v 7 --s 150 --c 10
```

## Product / Prop Fidelity

```text
[product/prop name] hero image, preserve [shape/material/color/proportions/logo placement], placed in [environment], [composition], [lighting], premium commercial photography, crisp surface detail, accurate scale, no extra labels or invented text --ar [ratio] --v 7 --raw --s 75 --c 5
```

## Character Sheet

```text
[character name/description], character design sheet, [front/side/back or expression set], consistent face, hair, outfit, proportions, and accessories, neutral background, clean readable design, [style] --ar [ratio] --v 7 --raw --s 100 --c 5
```

For an identity reference, append:

```text
--oref [URL] --ow [value]
```

## Style Reference

```text
[content prompt in simple terms], [composition], [lighting], [important subject details] --sref [URL or code] --sw [weight] --ar [ratio] --v 7
```

Keep the text prompt about content. Do not say "copy this style"; `--sref` already carries that job.

## Omni Reference

```text
[desired scene/action for the referenced person/object], preserve the referenced [identity/object form] while changing [setting/style/action], [composition], [lighting], [style] --oref [URL] --ow [weight] --ar [ratio] --v 7 --raw
```

Use lower `--ow` when the user wants looser adaptation or a different style.

## UI / Interface Reference Frame

```text
high-fidelity product UI reference frame for [app/workflow], [specific layout], readable Chinese interface text only where specified, realistic screen capture style without browser chrome, [state/progress/focus], crisp spacing and hierarchy, no random labels, no watermark --ar 16:9 --v 7 --raw --s 50 --c 5
```

## Seamless Pattern

```text
seamless repeating pattern tile of [motifs], [style/medium], balanced spacing, clean edges, repeatable wallpaper or textile design --tile --ar 1:1 --v 7 --s 200
```

## Video Prompt

```text
[starting frame role or image URL] [subject/action], [camera movement], [motion details], [atmosphere], maintain [identity/layout/style anchors], avoid warping and random text --motion low --bs 1 --raw
```

Use `--motion high` only when the user asks for large motion and accepts more artifact risk. Add `--loop` for a loop or `--end [URL]` for a custom ending frame.

## Prompt Pack Item Format

```markdown
### [Use Case / Shot Name]
`[final Midjourney prompt]`

Reference roles: [style ref / omni ref / image prompt, only if relevant]
QA: [one sentence about what to inspect]
```
