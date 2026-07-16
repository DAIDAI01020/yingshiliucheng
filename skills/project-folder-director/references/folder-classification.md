# Folder Classification Reference

Use broad categories. Do not over-sort.

## Folder Roles

| Folder | Use |
| --- | --- |
| `docs` | Word, PDF, Markdown, TXT, Excel, PPT, source docs, scripts, storyboards, reports. |
| `images` | PNG, JPG, WebP, TIFF, generated images, reference grids, contact sheets, poster/KV drafts. |
| `videos` | MP4, MOV, AVI, MKV, WebM. |
| `prompts` | Prompt text, input JSON, run manifests, generation jobs, generation-ready files. |
| `references` | ZIP/RAR/7Z packages or obvious downloaded reference packages. |
| `review` | Review notes or comparison material only when the user wants it separated. |
| `delivery` | Final handoff files. |
| `archive` | Retained old material, only when the user asks to archive. |
| `00_inbox` | Unknown or ambiguous files. |

## Simple Rules

| File or name pattern | Target |
| --- | --- |
| `.doc`, `.docx`, `.pdf`, `.md`, `.txt`, `.ppt`, `.pptx`, `.xls`, `.xlsx`, `.csv` | `docs` |
| `.png`, `.jpg`, `.jpeg`, `.webp`, `.tif`, `.tiff`, `.bmp` | `images` |
| `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm` | `videos` |
| `prompt`, `提示词`, `_input.json`, `run_manifest`, `generation_job`, `generation_ready` | `prompts` |
| `.zip`, `.rar`, `.7z` | `references` |
| `delivery`, `deliver`, `交付` | `delivery` |
| unknown | `00_inbox` |

## Safety

- Preserve original filenames unless there is a collision.
- On collision, append `_dup01`, `_dup02`, and so on before the extension.
- Do not infer that an older version can be deleted.
- Keep a visible plan before any move operation.
