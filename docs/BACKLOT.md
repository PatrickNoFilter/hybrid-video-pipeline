# Backlot board

[Backlot](https://github.com/...) is OpenMontage's local review board. It reads the project state directly from disk — nothing needs to be pushed to a server.

## Live board for the example run

```
http://127.0.0.1:4750/p/vietnam-indonesia-gdp
```

If the server is not running, start it from the OpenMontage checkout:

```bash
cd /path/to/OpenMontage
.venv/bin/python -m backlot open vietnam-indonesia-gdp
```

## What is in `backlot/`

| File | Meaning |
|---|---|
| `project.json` | Project identity: id, title, pipeline type, style playbook |
| `checkpoint_<stage>.json` | Latest state of each stage (`idea`, `script`, `scene_plan`, `assets`, `edit`, `compose`) |
| `history/checkpoint_<stage>_<timestamp>.json` | Archived superseded checkpoints — every revision is preserved |
| `events.jsonl` | Board event log |
| `decision_log.json` | Cumulative decisions, identified by `(category, subject)` |

The board shows the latest entry for each decision pair as **current** (tagged *revised* when superseded). That is why a changed choice must be appended with the **same** `category` and `subject`.

## Stage status recap for the worked example

| Stage | Status | Gate |
|---|---|---|
| idea | completed | approved after 8 revisions (title, data scope, framing) |
| script | completed | approved after intro, politeness and source-credit revisions |
| scene_plan | completed | approved (25 half-scenes after intro footage removal) |
| assets | completed | approved after 4 footage-sourcing revisions |
| edit | completed | auto — subtitles later disabled (`d-023`) |
| compose | completed | auto — music loop fixes (`d-024`, `d-025`) |

## Reproducing the board locally

1. Copy this repo's `backlot/` folder into `OpenMontage/projects/vietnam-indonesia-gdp/`.
2. Copy `artifacts/*.json` into the same project's `artifacts/` folder.
3. Run `python -m backlot open vietnam-indonesia-gdp` from OpenMontage.
4. Open the URL printed by the command.

The rendered video itself is not committed (media is gitignored); regenerate it with the scripts, or copy `renders/final.mp4` from the original workspace.


## Storyboard navigation (custom UI edit)

The local Backlot UI in this environment (`OpenMontage/backlot/ui/board.js` and
`board.css`) was extended for easier navigation of long storyboards:

| Control | What it does |
|---|---|
| Scene number chips | One clickable chip per scene — scrolls the filmstrip to that card |
| Search box | Filters cards by scene id, section label, description or narration; `Esc` clears it |
| Strip / Grid toggle | Switch between the horizontal filmstrip and a wrapped grid of cards; choice persists in `localStorage` |
| Click a card | Opens its full narration, timecode and shot notes, plus **"Open in final render"** to jump the video to that scene |
| ← / → keys | Step through visible scene cards without leaving the keyboard (ignored while typing in the search box) |
| Selected card | Amber outline marks the current scene across re-renders and SSE refreshes |

The edited UI files are included in this repo at `backlot-ui/board.js` and
`backlot-ui/board.css`. Copy them into `OpenMontage/backlot/ui/` to apply the
same navigation to another installation.

Hard-refresh the board after updating `board.js` / `board.css` (the watcher only
monitors `projects/`, not UI files).

## Second worked project — `kok-bisa-vietnam-id`
A second, longer run is included for the Indonesian-language video
**"Kok Bisa Orang Vietnam 'Lebih Kaya' dari Indonesia?"**. Its state lives in
`backlot/projects/kok-bisa-vietnam-id/` (checkpoints, archived `history/`,
`decision_log.json`, `events.jsonl`, `project.json`) and the canonical artifacts
in `artifacts/projects/kok-bisa-vietnam-id/`.

Live board:
```
http://127.0.0.1:4750/p/kok-bisa-vietnam-id
```
Start it with `.venv/bin/python -m backlot open kok-bisa-vietnam-id` from the
OpenMontage checkout.

Stage status recap:
| Stage | Status | Note |
|---|---|---|
| idea | completed (approved) | Title and source list accepted after several revisions |
| script | completed (approved) | 10 sections; narration text preserved across 5 user revisions |
| scene_plan | awaiting_human (reopened) | Rombakan total: 19 beats 100% infografis OpenMontage, tanpa footage real; durasi 633.43 s |
| assets | pending rebuild | Aset lama (3 footage + 16 still) tidak dipakai; akan dibuat ulang setelah scene_plan approved |
| edit | stalled — superseded | Status lama tersimpan di `history/`; alur kembali ke scene_plan |

This run follows the revised approval flow documented in
`RECOMMENDED_STEPS.md` §3: the Edge TTS narration (`id-ID-GadisNeural`) was
rendered and measured **before** the scene-plan approval gate. Section audio is
generated locally into `assets/audio/sections/<id>.mp3` and is intentionally not
committed; regenerate it with `scripts/tts_all.py`-style code after restoring
the artifacts.
