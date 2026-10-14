# Adaptation and connected shot production

Read the relevant section for novels, multiple delivery formats, recurring camera setups, candidate frames or revisions. These are extensions to existing owner skills, not additional approval rounds.

## Format and runtime

The intake `format_spec` is the project authority. Copy the resolved ratio into each shot packet, scene handoff, image job and `generation_ready_packet.ratio`; the latter must be explicit. Example: `master_ratio: "16:9"`, `delivery_ratios: ["9:16"]`. An empty template means unresolved, never an implicit portrait default. Existing projects retain their recorded format; do not bulk migrate production files during workflow maintenance.

- 16:9: use lateral blocking, two-shots, foreground/background depth and environmental evidence when they advance the scene. Do not replace them automatically with isolated close-ups.
- 9:16: check readable faces, vertical depth, shoulder occlusion and subtitle safety. A wide shot is still valid when its information remains readable.
- Other ratios: design for the actual frame, subject relationships and viewing context. Do not reject an image solely because width is less than height.
- Multiple deliveries: preserve story/character/scene IDs; give separate rendition shot IDs such as `E01_S01_003_L` and `E01_S01_003_P`, with distinct prompts, frames, runs and QC. Decide shot by shot between crop, reframing and a new composition. Check both actors, eyelines, plot props, entrances and subtitle areas; cropping is not automatically equivalent coverage.
- Before execution, the platform auditor verifies that the selected model/task accepts the ratio, dimensions and per-shot duration. Source-locked edit/extend tasks inherit source dimensions. A mismatch requires a supported route or a disclosed adaptation, never silent stretching, cropping or fallback to the provider default.

Runtime, hook speed and landscape/portrait are independent decisions. Reuse an accepted script's pacing; opening hooks, pauses and ending closure follow its intended viewing experience.

## Novel and long-source evidence

Owner: `$short-drama-episode-writer`; `$short-drama-character-bible` maintains shared character identities and relationships. Existing short scripts need no novel indexing stage.

For long source material, retain the original and make a chapter/event map before episode adaptation. Assign stable `source_id` and `event_id`. Each adapted beat records:

```text
source_id / file / source_revision_or_sha256
chapter / line_or_paragraph_range / event_id
fact_or_short_excerpt / characters / chronological_order
adaptation_delta / unresolved_conflict
```

Search original chapters using character aliases, objects, locations and event terms (local text search is sufficient for smaller sources); read the surrounding passage before using a hit. Summaries locate evidence but do not establish facts. Cross-check names, causality, chronology, prop ownership, secrets and when each character learns them. Preserve deliberate ambiguity. Mark newly invented bridges as adaptation, never as a source quotation. Feed relevant passages and shared facts to the current scene instead of repeatedly loading the whole novel.

Store project evidence in `references/source-evidence.md` and point to its stable entries in each shot's `source_evidence`. If the source changes, recheck affected entries, then invalidate only their dependent shots. A vector index/reranker is an optional future backend for very long sources; this workflow does not claim that service is installed.

## Camera and reference graph

Owner: `$short-drama-scene-director`. Start from its existing scene geography and background-side lock. Record a stable `camera_id` per setup (master, A-side, B-side, insert), position/height, view direction, lens intent, axis side, visible background, character blocking and light direction. Reuse the setup only while these constraints still hold.

Use `camera_reference_shot_id` for the approved frame actually guiding a later shot. Choose a matching setup and current character/prop state before choosing the most recent frame. `previous_shot_id` means edit order; it need not be the reference parent. Parent references must exist and the combined production/reference graph must be acyclic. If a proposed graph loops, select a separate master anchor or remove the unnecessary reference edge.

Keep `reference_roles` narrow: file/asset and revision, identity/wardrobe/scene/camera role, inherited features and excluded features. A previous face must not freeze the current expression; an old frame must not restore an already-moved prop. Use only the number/type of references accepted by the current platform.

Approve the master/setup anchor before dependent image batches. An approved frame can unlock related frames without waiting for its whole video to finish; full-clip dependencies stay in `dependencies`. The scheduler only suggests work and does not submit generation. Physically inspect reference files and applicable continuity decisions before execution.

ViMax's camera-transition video trick is optional research, not the default: it spends another video generation and can introduce drift. Prefer existing approved frames, spatial boards or deliberate image editing. Use an extra transition generation only when useful and within the user's generation scope/budget.

## Candidate frames and selection

Owners: image execution creates candidates; `$image-qc-director` compares them. Use multiple candidates for difficult identity, reverse shots, prop handoffs or hero compositions when the authorized budget supports it. Reuse existing candidates first. Do not silently turn a one-image request into multiple paid calls.

Compare actual pixels against the approved reference and the target ratio: identity/costume, room geometry, camera axis/eyeline, prop state, action readability, framing and visual defects. Record every candidate's path, QC decision and concrete observation. A VLM can assist where available; its score does not replace visual evidence. One candidate still needs QC. If every candidate fails, select none and report the specific repair.

Persist `frame_selection` in the shot packet, then put the winner's exact path in `artifacts.approved_first_frame`:

```json
{
  "context_revision": "prompt-v3 + scene-lock-v2 + refs-v4 + 16:9",
  "candidates": [
    {"candidate_id": "A", "path": "generation-runs/run-003/frame-A.png", "qc_decision": "passed", "evidence": "A remains camera-left; phone in right hand; window behind B matches the lock"},
    {"candidate_id": "B", "path": "generation-runs/run-003/frame-B.png", "qc_decision": "rejected", "evidence": "Hands and phone ownership swapped"}
  ],
  "selected_candidate_id": "A",
  "reason": "Preserves geography and prop ownership in the requested frame",
  "stale": false
}
```

The state tool validates this record, paths and selection consistency; it does not itself see images or judge quality. In-place changes to a prompt/reference file require explicit `invalidate` because unchanged paths cannot reveal changed content. Reuse a selection only while prompt, reference revisions, scene lock, model and ratio still match. A new selection must record the new context and clear `stale` only after a new review.

## Revisions, delivery and evidence

Owner: `$project-state-manager`; use [its state commands](../../project-state-manager/references/shot-production-extensions.md). Keep old runs for comparison and resume at the earliest affected stage. Updating a file in place, changing source facts or revising a shared scene lock requires invalidating each directly affected shot; reference/continuity descendants are then marked stale automatically. A failed provider run alone is `blocked`, not a reason to rebuild unrelated approved frames.

Video QC still checks actual motion, continuity, duration, audio and edit points; a winning still image is not a passed video. Assembly needs an ordered shot list, consistent delivery dimensions/FPS, sound continuity and an actual playback check. Route speech/music/effects separation to `$audio-stem-separator` only when needed, and editable subtitles to `$video-srt-director`. Preserve its confirmed punctuation/three-space style. Do not label a collection of scene clips as a finished episode.

## Design source and boundaries

Adapted ideas from [HKUDS/ViMax](https://github.com/HKUDS/ViMax/tree/fd4b72e7731be6e5f88486206d25ea59849b0285): source retrieval in novel adaptation, camera/reference relationships, and candidate keyframe comparison. This is an independent integration into the existing skill/state system, not a ViMax installation, copied implementation, MCP connection or benchmark claim. Its horizontal-only guards, fixed generation defaults and additional transition-video costs are not inherited.
