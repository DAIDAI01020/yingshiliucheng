---
name: midjourney
description: Generate real Midjourney images through a standalone Legnext API workflow, and prepare polished Midjourney prompts, parameter suffixes, reference-image roles, style/omni reference setups, version choices, and QA checklists. Use when Codex is asked to generate with Midjourney, submit Midjourney jobs, package reusable Midjourney prompt workflows for teammates, create prompt packs, use V7/V8.1/Niji, style references, omni references, image prompts, tiles, product shots, character sheets, cinematic frames, storyboard frames, or Midjourney video prompts.
---

# Midjourney

## Operating Principle

Default to real generation through the standalone Legnext API when the user asks to generate a Midjourney image. This skill is intentionally independent of LunaLab's local canvas and backend so it can be shared with teammates.

Only fall back to a prompt-only handoff when the user asks for prompts or Legnext is not configured. Do not silently use generic image tools and do not claim a result came from Midjourney unless it was submitted through Legnext, Midjourney web, Discord, or another explicit Midjourney workflow.

Use the user's language for prompt content. For Chinese briefs, write Chinese prompts unless the user asks for English.

## Version Defaults

Use conservative defaults unless the user specifies otherwise:

- Image prompts: `--v 7` as the stable default, because current Midjourney docs still identify V7 as the default.
- Experimental/faster jobs: offer `--v 8.1` when the user explicitly wants the newest/fastest model or HD/SD behavior.
- Anime/eastern illustration: use `--niji 7` when the user asks for Niji, anime, manga, or illustration aesthetics.
- Literal prompting: add `--raw` when prompt adherence, product fidelity, UI fidelity, or reduced house style matters.

If the user asks for "latest" Midjourney behavior, check official Midjourney docs before answering because model and parameter support changes frequently.

## Setup

Require one environment variable:

```bash
export LEGNEXT_API_KEY="..."
```

Optional:

```bash
export LEGNEXT_BASE_URL="https://api.legnext.ai"
export LEGNEXT_CALLBACK_URL="https://example.com/webhook"
```

Never print API keys or include them in final answers.

On this Windows/Codex workflow, prefer the Node runner because it does not require a separate Python install:

```powershell
& 'C:\Program Files\Adobe\Adobe Creative Cloud Experience\libs\node.exe' scripts\submit_midjourney.mjs doctor
```

The original Python runner is kept as a fallback for machines with Python installed.

## Real Generation Workflow

1. Prepare the final Midjourney prompt.
   - Follow the prompt workflow below.
   - Include Midjourney parameters directly in the prompt suffix.

2. Submit through the bundled helper:

```bash
node scripts/submit_midjourney.mjs run \
  "final prompt --ar 16:9 --v 7 --raw --s 100 --c 5"
```

Add `--callback "https://..."` or `LEGNEXT_CALLBACK_URL` when the user wants Legnext webhook delivery.

3. Poll until completion.
   - The helper prints `submitted`, progress `status`, and final `completed.imageUrls`.
   - If the helper reports `LEGNEXT_API_KEY is required`, say Legnext is not configured and do not retry with another image provider.
   - If the helper reports authentication, balance, rate limit, or upstream errors, report that exact category concisely.

4. Return the generated image URL and the final prompt.
   - Prefer the four single-image results from `completed.localPaths` for Codex display, using absolute-path Markdown image syntax.
   - If Legnext also returns a grid/preview image, do not show it first; show the four individual images first.
   - Include remote `completed.imageUrls` as fallback links when useful.
   - Mention that it was generated through Midjourney via Legnext.
   - Include concise failure details if generation did not complete.

## Prompt Workflow

1. Clarify only blocking intent.
   - If subject, output type, platform use, or aspect ratio is missing, make a reasonable assumption and state it briefly.
   - Ask one concise question only when the missing detail would change the prompt materially.
   - Capture: subject, output type, aspect ratio, style, reference images, consistency constraints, version/model, and must-avoid artifacts.

2. Choose the task pattern.
   - Text-to-image: no reference image.
   - Image prompt: use uploaded/hosted image URLs to influence content, composition, and color.
   - Style reference: use `--sref` for visual language, palette, medium, lighting, or texture.
   - Omni reference: use `--oref` for a person, character, object, vehicle, or prop identity in V7.
   - Tile: use `--tile` for seamless patterns.
   - Video: use video-specific parameters only.
   - Read `references/prompt-patterns.md` for reusable prompt structures.

3. Build the prompt body before parameters.
   - Lead with the subject and output type.
   - Specify composition, camera/framing, lighting, material, environment, mood, and style.
   - State continuity anchors for characters, products, logos, colors, proportions, outfits, and UI layout.
   - Prefer positive visual instructions over long negative lists.
   - Keep parameter flags at the very end, with no punctuation after them.

4. Select parameters.
   - Read `references/parameter-guide.md` when the task needs exact ranges, compatibility notes, or video parameters.
   - Default to `--ar 16:9` for cinematic frames, storyboard frames, UI references, and video first frames.
   - Default to `--ar 1:1` only for square assets, icons, profile images, or when unspecified and square is useful.
   - Use `--s 50-150` for controlled commercial/product/UI work; raise stylize for more artistic exploration.
   - Use `--c 0-20` for controlled outputs; raise chaos for exploration.
   - Add `--no text, watermark, logo, qr code` only when random text or marks would be harmful.

5. Produce or submit.
   - For generation requests, run the real generation workflow.
   - For prompt-only requests, include the final Midjourney prompt in one clean block.
   - List reference roles when images are involved.
   - Include a short QA checklist for subject fidelity, aspect ratio, reference handling, text/logo risk, and unwanted artifacts.

## Output Contract

Use this shape after successful real generation:

```markdown
Generated through Midjourney via Legnext:

![result 1](/absolute/local/path-0.png)
![result 2](/absolute/local/path-1.png)
![result 3](/absolute/local/path-2.png)
![result 4](/absolute/local/path-3.png)

Prompt:
[final prompt]
```

Use this shape for prompt-only Midjourney handoffs:

```markdown
## Midjourney Prompt
[prompt body] --ar 16:9 --v 7 --raw

## Reference Roles
[only when images are provided]

## Notes
[1-3 concise parameter/version notes when useful]

## QA Checklist
[3-5 concise checks]
```

For prompt packs, make each prompt self-contained and include its intended use, aspect ratio, and any reference role assumptions.

## Resource Guide

- Read `references/parameter-guide.md` for current parameter ranges, compatibility notes, version guidance, and official source links.
- Read `references/prompt-patterns.md` for task-specific prompt templates and examples.
- Use `scripts/submit_midjourney.mjs` to submit and poll real standalone Legnext Midjourney image-generation tasks on Windows/Codex.
- Use `scripts/submit_midjourney.py` as a Python fallback.
- By default, completed images are downloaded to `~/.codex/generated_images/midjourney`; show those local paths in Codex responses so users can see images inline.
