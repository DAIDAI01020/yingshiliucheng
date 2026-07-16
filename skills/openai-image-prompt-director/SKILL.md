---
name: openai-image-prompt-director
description: Compatibility entry for adapting film, storyboard, KV, product, graphic, typography, LED/stage, or local-edit image briefs to the built-in OpenAI/ChatGPT image route. Use when the user explicitly asks for an OpenAI image prompt rather than direct built-in generation; delegate image semantics to frame-vision-director and platform compilation to prompt-platform-auditor.
---

# OpenAI Image Prompt Director

## Compatibility Role

Keep this skill as a narrow compatibility entry. Do not maintain a second image-prompt system here.

Use this route:

```text
$frame-vision-director
-> image_prompt_source_packet
-> $prompt-platform-auditor with platform_target: built_in_image
-> final copyable prompt
```

If the user asks to generate rather than receive a prompt, route after compilation to `$builtin-imagegen-director` and built-in imagegen.

## Rules

- Inherit `deliverable_profile`, `response_mode`, reference roles, style lock, and controlled-change boundaries.
- Preserve the visible target, must-preserve lock, must-change delta, composition/layout, light/material, text/logo policy, and ratio.
- Let `$prompt-platform-auditor` decide built-in image language and risk compaction.
- Do not require camera brands, focal lengths, apertures, anti-AI realism, mother-library fields, or negative blocks unless the deliverable profile needs them.
- Do not output a default comparison table.
- Do not call external OpenAI APIs or ask for API keys.

## Output

For `response_mode: direct`, return only the final copyable prompt. For `compact`, add one short adaptation note. Show source and audit packets only for `diagnostic`.
