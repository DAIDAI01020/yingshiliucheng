# Shot format, references, selection and revisions

Use `scripts/manage-shot-production.py` from this skill. Existing registries remain readable; unset legacy ratios produce a warning. New short-drama intakes contain `format_spec` with an initially empty `master_ratio`; resolve it from the user's project before composition or generation. No screen orientation is assumed.

`upsert --project-root PATH --input PACKET.json` merges supplied top-level fields into existing shots. Omitted fields persist; replace a nested object explicitly only with its complete intended contents. New shots inherit `project-intake.json -> project_intake_packet.format_spec.master_ratio` when their `ratio` is absent. Declared master/delivery ratios constrain shot ratios. The generation gate separately requires an explicit matching ratio for new intakes; it never edits a provider job behind the user's back.

Additional optional packet fields:

| Field | Meaning |
| --- | --- |
| `ratio` | Actual rendition ratio, e.g. 16:9, 9:16, 4:3 |
| `camera_id` | Stable setup ID, scoped to its scene |
| `camera_reference_shot_id` | Shot supplying a reused approved first frame |
| `reference_roles` | Asset/revision, inherited features and exclusions |
| `source_evidence` | Original chapter/event evidence entry pointers |
| `frame_selection` | Candidate observations, selected ID, context revision, reason, stale flag |

`previous_shot_id` only describes the edit. `dependencies` require `qc_passed`/`accepted`; camera reference edges require a predecessor at least `image_approved` with an approved-frame path before image/video work. Prompt drafting may proceed before that frame exists. Textual `continuity_in.inherits_from` participates in revision propagation but does not itself require a generated frame. Blocked/stale reference or continuity parents prevent their dependent batch. The union is checked for missing IDs and cycles. `next-batch` orders ready shots by anchor class, risk, then shot order. It does not execute tools or infer creative approval; verify actual files and relevant continuity state before submission.

Use `transition` for status changes on existing shots. Upsert may register existing externally produced shots with accurate status/evidence, but cannot change an existing shot's status. If a frame-selection record exists, image approval and later statuses require a passed observed candidate, selection reason, nonempty winner file and matching `approved_first_frame`. No selection record is fabricated for legacy shots. Visual QC stays with the image QC owner.

Production-input changes supplied to `upsert` mark the edited shot and its actual dependency descendants stale. This includes ratio, camera references, continuity, source evidence, platform plan, image-prompt and approved-frame paths. Old files are retained. For file-content edits at the same path, shared-lock edits or evidence changes made outside the packet, run explicitly:

```powershell
python scripts/manage-shot-production.py invalidate --project-root PATH --shot-id E01_S01_001 --reason "scene lock v3 changes phone ownership"
python scripts/manage-shot-production.py summary --project-root PATH
python scripts/manage-shot-production.py transition --project-root PATH --shot-id E01_S01_001 --status prompt_ready --resume
```

Resume stale work at `planned`, `continuity_locked` or `prompt_ready`, after checking the affected inputs. Old selections remain stale until reviewed/replaced. Unaffected siblings remain usable. State flags do not cancel already-running provider jobs or delete their results; reconcile those jobs before another submission.

Checks: `python -X utf8 -m unittest discover -s skills/project-state-manager/tests -v` from the repository root, plus the existing state/E2E tests. Fixtures do not call paid models or prove semantic visual quality.
