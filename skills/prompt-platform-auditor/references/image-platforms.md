# Image Platform Compilation

Use only the section matching `platform_target`.

## Contents

- Built-in imagegen
- Banana and Banana Pro
- Jimeng Image
- Midjourney
- Local edits and reference roles

## Built-In Imagegen

Use Chinese natural visual instruction first. Use English camera, lens, light, or material terms only when they improve precision.

Prefer:

```text
visible target -> unchanged constraints -> requested change -> spatial layout -> light/material -> relevant avoid items -> ratio
```

Avoid parameter dumps, repeated camera brands, oversized negative lists, or an abstract style shell before the visible frame.

For direct generation, do not print the full prompt first unless requested. After a successful built-in image result, do not append QC or status text in the same response.

## Banana And Banana Pro

Use Chinese visible-frame instruction with concise English camera/lens/light/material terms only where useful, followed by Chinese targeted negatives.

Put the strongest image target first. Keep one dominant visual goal per image. Assign narrow roles to every reference.

Use a compact prompt when the user requests speed/token saving. A compact prompt must still preserve exact structure, identity, composition, light, material, reference roles, ratio, and the few risks most likely to damage the output.

Do not treat Banana as a fallback for built-in imagegen or vice versa.

## Jimeng Image

Use only when the user explicitly chooses Jimeng for still-image generation. Keep Chinese wording direct and image-oriented. Control visible subject, scene, composition, light/material, text/logo, reference roles, and ratio. Avoid English-heavy camera stacks.

## Midjourney

Use concise phrase-based visual language. Put visual nouns, composition, light, palette, and material first; place supported parameters at the end. Require an aspect-ratio parameter when ratio matters. Remove director rationale and long prose.

Do not invent or update platform/version parameters without confirming the selected workflow's supported syntax.

## Local Edits

Begin with the base lock:

```text
只修改[目标区域]，严格保持[背景、构图、透视、光线、色调、景深、比例、非目标主体]不变。
```

Then state the exact delta and integration rule. Reject prompts that ask for a new full-frame style during a narrow edit unless the user explicitly requests a repaint.

## Reference Roles

For each reference, state:

```text
controls: identity / costume / pose / product structure / scene / composition / light / color / material / start-end frame
do_not_inherit: unwanted identity / background / style / text / logo / color / camera behavior
```

Do not approve `参考这张图` without a role boundary.
