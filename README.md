# hybrid-video-pipeline

A reproducible **narration-driven video pipeline** that combines two rendering engines:

| Engine | Used for |
|---|---|
| **MoneyPrinterTurbo + Pexels** | Real footage (stock / local clips) chosen to match each narration beat |
| **OpenMontage + Remotion** | Animated infographics: news cards, title cards, stat cards, bar/line charts, badges |
| **Edge TTS** | Narration in any installed voice (example: `id-ID-GadisNeural`, Indonesian) |

The idea: **the script drives the visuals**. Each section is split into two alternating halves — one real-video half and one infographic half — so both engines appear in every scene. Generated clips, narration, subtitles and manifests are produced by scripts and validated against OpenMontage JSON schemas.

## Example run included

`artifacts/` contains a complete worked example: **"Tujuh Triwulan: Tumbuhnya Vietnam Sudah Menyalip Indonesia, Ekonominya Belum?"** — a ~242 s, 1920×1080 explainer about Vietnam vs Indonesia GDP per capita (2025–2026 data). The example demonstrates:

- a news-headline cold open + title card,
- BPS/NSO quarterly growth charts,
- World Bank current-vs-constant USD stat cards,
- an IMF projection card with a mandatory **PROYEKSI** badge,
- mixed Vietnam/Indonesia footage matched to the narration,
- append-only decision history across human-approval gates.

See [`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md) for the example's sources.

## Repository layout

| Path | Purpose |
|---|---|
| `artifacts/` | Canonical JSON: brief, script, scene_plan, asset_manifest, decision_log, data_manifest, tts_timings |
| `scripts/` | Generation scripts: TTS, audio/subtitles, MPT batches, Remotion build/render, trimming, manifest |
| `remotion/` | Standalone Remotion project with all infographic compositions |
| `docs/` | Pipeline notes and example data sources |

## Requirements

- Python 3.11+ with `edge-tts`, `jsonschema`
- `ffmpeg` / `ffprobe` on PATH
- MoneyPrinterTurbo checkout with a configured `pexels_api_keys` entry (free key from pexels.com/api)
- Node.js 22+ and Remotion dependencies (`cd remotion && npm install`)
- An OpenMontage-style pipeline workspace for the `edit` and `compose` stages

**No API keys or credentials are committed.** Configure them locally.

## Pipeline stages

```
idea → script → scene_plan → assets → edit → compose
```

Each stage produces one schema-validated artifact, gets a self-review, and is checkpointed at a human approval gate. Meaningful choices are appended to `artifacts/decision_log.json` (identified by `category` + `subject`), so a changed decision never overwrites history.

Example decisions from the worked run:

| ID | Decision |
|---|---|
| d-016 | Extend video duration to match real TTS speech |
| d-017 / d-018 / d-019 / d-021 | Footage sourcing iterations (local → Pexels → diverse → mixed VN/ID) |
| d-020 | Add news-headline intro + title intro |

## Reproduce the example (order)

1. `scripts/tts_sample.py` — sample voice check
2. `scripts/tts_all.py` — section narration + measured timings
3. `scripts/retime_to_tts.py` — retime script + scene plan to real audio
4. `scripts/intro_tts.py` — intro narration
5. `scripts/build_audio_subs.py` — full mix, subtitles, music
6. `scripts/mpt_mixed_parallel.sh`, `scripts/mpt_intro.sh` — real footage via MPT/Pexels
7. `scripts/build_remotion.py`, `scripts/render_gfx.sh` — infographic MP4s
8. `scripts/trim_footage.py` — trim footage to alternating half-scenes
9. `scripts/finalize_all_assets.py` — validated asset manifest

Then continue at `edit` and `compose` in OpenMontage.

## Adapting to a new topic

Replace `artifacts/brief.json`, `script.json` and `scene_plan.json` with your own content (keeping the same schema), adjust `remotion/src/gfx_data.ts` compositions, update the MPT search terms in the batch scripts, and rerun. The narration→visual routing, 50/50 alternating structure, QA checkpoints and decision logging stay the same.
