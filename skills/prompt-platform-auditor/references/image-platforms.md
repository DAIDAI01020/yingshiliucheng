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

For `model_target:gpt_image_2_5`, `gpt_image_2_5_flare`, or `gpt_image_2_5_sunburst`, or a new built-in request explicitly routed to the migrated Images 2.5 default, also apply [gpt-image-2-5.md](gpt-image-2-5.md). Keep a project pinned to GPT Image 2 or an older model on its existing rules.

For direct generation, do not print the full prompt first unless requested. After a successful built-in image result, do not append QC or status text in the same response.

## Banana And Banana Pro

Use Chinese visible-frame instruction with concise English camera/lens/light/material terms only where useful, followed by Chinese targeted negatives.

Put the strongest image target first. Keep one dominant visual goal per image. Assign narrow roles to every reference.

For KV, product advertising, environments, and concept posters, use the relevant semantic owner's approved design. The original paired examples in `$banana-pro`'s `references/design-prompt-examples.md` illustrate adaptation; they do not replace the brief or become global style defaults.

When producing paired built-in / Banana prompts, lock the same subject, concept, composition, palette, text, and reference roles across both. Adapt instruction structure only. Use explicit object relationships and visible light/material behavior where relevant; do not assert that Banana needs a fixed magic syntax or that wording alone guarantees better images.

For manual website/app use, return copyable natural language plus aspect ratio and reference mapping as needed. Keep JSON, model IDs, and unsupported parameter suffixes outside the image prompt. Unless the selected execution interface explicitly supports a separate negative field, express a few relevant exclusions as natural-language constraints in the prompt.

Keep typography/graphic tasks governed by shape, spacing, hierarchy, and medium. Use camera/perspective/light instructions for photographic or spatial tasks when they affect the intended image. Do not add cinema, megastructures, rim light, film grain, or lens brands by default.

Use a compact prompt when the user requests speed/token saving. A compact prompt must still preserve exact structure, identity, composition, light, material, reference roles, ratio, and the few risks most likely to damage the output.

Do not treat Banana as a fallback for built-in imagegen or vice versa.

## Jimeng Image

Use only when the user explicitly chooses Jimeng for still-image generation. Keep Chinese wording direct and image-oriented. Control visible subject, scene, composition, light/material, text/logo, reference roles, and ratio. Avoid English-heavy camera stacks.

## Midjourney

Use concise phrase-based visual language. Put visual nouns, composition, light, palette, and material first; place supported parameters at the end. Require an aspect-ratio parameter when ratio matters. Remove director rationale and long prose.

Do not invent or update platform/version parameters without confirming the selected workflow's supported syntax.

## Local Edits

First distinguish in-frame edits, crop-only changes, and actual camera relocation using `$frame-vision-director`'s camera-change rule. Reject any overlap between preservation locks and requested changes. A new camera preserves the physical scene, not its old projection or composition.

For an unchanged camera, begin with the applicable base lock (remove fields the user wants changed):

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
