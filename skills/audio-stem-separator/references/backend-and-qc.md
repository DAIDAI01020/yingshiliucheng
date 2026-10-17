# Backend, Execution And QC

## Supported Route

Use a trusted checkout of [MSST](https://github.com/ZFTurbo/Music-Source-Separation-Training) with its compatible Python environment and the matching cinematic checkpoint/config from the [upstream pretrained model list](https://github.com/ZFTurbo/Music-Source-Separation-Training/blob/main/docs/pretrained_models.md). That list distinguishes BandIt speech/music/effects from musical instrument separation. The [DnR BandIt v2 configuration](https://github.com/ZFTurbo/Music-Source-Separation-Training/blob/main/configs/config_dnr_bandit_v2_mus64.yaml) explicitly declares speech, music and sfx.

Inspect the installed upstream CLI/version before execution. The adapter uses `inference.py`, model type `bandit` or `bandit_v2`, config, checkpoint, input/output directories, FLOAT output and an explicit stem filename template. No upstream code/weights are bundled. A model checkpoint must come from a trusted source: the upstream loader may deserialize Python objects.

Keep code/environment/model weights in a local tools/cache location, not the workflow source or media output. Do not install into the shared Codex Python environment by default. Setup scope can cover normal dependencies; ask only for a material unresolved storage/download/cost decision. Never upload private media to an online splitter without user scope covering that upload.

## Commands

### Persistent local reuse

After the initial setup, save a version-1 JSON profile to `$CODEX_HOME/tools/audio-separation/backend.json` (fallback `~/.codex/tools/audio-separation/backend.json`). It contains absolute `backend_root`, `backend_python`, `config`, `checkpoint` paths, `model_type`, and preferably `config_sha256` / `checkpoint_sha256` from the verified files. This machine-specific file stays outside Git. For another location use `--backend-profile` or `AUDIO_STEM_BACKEND_PROFILE`.

Explicit CLI fields override `MSST_*` environment values, which override the profile. A missing default profile reports missing configuration; a missing explicit profile or mismatching registered hash fails clearly. Neither case downloads anything. Inspect local files and repair registration before treating the model as absent. Retain matching configuration and model architecture; a partial download is not a valid checkpoint.

With registration complete, ordinary calls are:

```powershell
python scripts/separate_audio.py doctor
python scripts/separate_audio.py separate --input "PATH/video.mp4" --output-dir "PATH/project/audio-runs/v002"
```

Do not repeat clone, pip installation, model conversion or downloads per run. Keep output directories separate from the persistent runtime. Any setup downloader must reuse a complete checksum-verified file; only missing/corrupt weights or an explicitly chosen model/version change warrants another download. Loading a model into GPU/RAM is normal on a new process and is not downloading it again.

### Explicit backend selection

```powershell
python scripts/separate_audio.py doctor --backend-root "PATH/MSST" --backend-python "PATH/python.exe" --config "PATH/cinematic.yaml" --checkpoint "PATH/model.ckpt"
python scripts/separate_audio.py separate --input "PATH/video.mp4" --output-dir "PATH/project/audio-runs/v001" --backend-root "PATH/MSST" --backend-python "PATH/python.exe" --config "PATH/cinematic.yaml" --checkpoint "PATH/model.ckpt" --model-type bandit_v2
python scripts/separate_audio.py verify --input "PATH/mix.wav" --speech "PATH/speech.wav" --music "PATH/music.wav" --sfx "PATH/sfx.wav"
```

Environment defaults: `MSST_ROOT`, `MSST_PYTHON`, `MSST_CONFIG`, `MSST_CHECKPOINT`. Use `--audio-stream N` for the zero-based audio stream. `--force-cpu` is an explicit device choice; do not silently change requested hardware. FFmpeg/ffprobe are required. The host uses PyYAML for config checks; the upstream environment owns inference dependencies.

Readiness checks paths/config labels and available tools; real inference still needs a successful backend smoke test. A missing backend remains an actionable dependency, not a reason to report three generated stems. `verify` can also validate authorized outputs from another true cinematic separator.

The adapter records the audio stream start relative to the source container start. It rebases the extracted working WAV to zero while preserving internal timing; apply the recorded offset when placing stems under the original video. For timecode-based NLE sequences, preserve the separately supplied edit-sequence offset too. Arbitrary trimming/retiming requires an explicit edit map.

## Validation

- Decode all three files; compare channels, rate and durations against the selected source stream.
- Keep each complete stem on the same start position. Do not trim leading silence independently.
- Compare source and stem playback at representative moments; technical alignment alone cannot detect model lag or stem leakage.
- Inspect speech consonants, reverb tails, music pumping, impacts and background ambience. Silence in one stem can be correct and is not automatically a failure.
- Recombine for an audible sanity check where useful; a perfect mathematical residual is not proof of correct semantic separation.
- Save version/hash/model information. Partial outputs stay incomplete; do not fill a missing stem with silence to pass validation.

The unit/integration fixtures test routing guards, config labels, stream handling and real FFmpeg decoding. They do not establish model quality or a working ML environment. Run a real mixed-audio separation after installing the backend before claiming it is ready for production.
