# Recommended steps — hybrid video pipeline

This is the working procedure used to produce the example video. Follow it in order for any new topic.

## 0. Decide the brief before generating anything

Write `artifacts/brief.json` with:

- a title that states the actual claim (e.g. *"Tumbuhnya Vietnam Sudah Menyalip Indonesia, Ekonominya Belum?"*),
- an evidence hierarchy — which source is **proof**, which is **context**, which is a **labeled projection**,
- an explicit visual router: which narration words trigger real footage and which trigger infographics,
- price-basis and labeling rules (e.g. "IMF must say *proyeksi* + *current USD*").

Log every meaningful choice in `artifacts/decision_log.json` with a unique `(category, subject)` pair. If a choice changes later, **append** a new entry with the same pair — never edit the old one.

## 1. Research and verify data first

- Prefer national statistical agencies (BPS, NSO) for actuals; use IMF/World Bank only with vintage and price basis stated.
- Confirm the IMF vintage from the source page itself (the example used FlareSolverr after a direct 403).
- Save everything in `artifacts/data_manifest.json`, including quarters, revisions, FX, population and source URLs.
- If two sources disagree, do not average them — state the basis difference.

## 2. Script in the narration language

- Keep the register consistent (the example uses polite Indonesian: *marilah, senantiasa, silakan*).
- Every factual claim needs a `source_ref` pointing at the manifest.
- Let the story **resolve**: give the explanation and a real conclusion, not just a statistic.
- Split into scenes of 5–20 s; for each, specify the real-footage subject and the infographic spec.

## 3. Render narration before locking timing

1. Generate a **sample** of the most numbers-heavy section and approve the voice.
2. Render all sections with the chosen Edge TTS voice.
3. Measure real durations with `ffprobe`.
4. **Retime the script and scene plan to the real audio** — do not force speech into a planned duration (the example had to expand from 117 s to 220 s).
5. Build the full narration mix with small gaps and a final hold.

## 4. Build visuals with both engines

- Real footage: MoneyPrinterTurbo with Pexels (configure `pexels_api_keys` locally). Use search terms matched to each scene's meaning — skyline, factory, port, bank, crowd — not one repeated style.
- Infographics: Remotion compositions rendered at 1920×1080, 30 fps, with frame-based animation only.
- QA one frame per visual style before batching. Check for typos in rendered text.

## 5. Assemble

- Normalize all clips to identical codec/fps/resolution **before** concat; otherwise the concat demuxer can silently drop seconds.
- Pad the video with a held final frame so it covers the narration tail.
- Mix music under narration at low volume (~0.12).
- Loop music from a **clean cut** — check the source for silent tails first (−91 dB zones will otherwise appear as muting).

## 6. Review and publish

- ffprobe the final file: duration, resolution, codecs, audio presence.
- Sample frames from the opening, middle and ending.
- Check audio levels in the problem windows that were reported.
- Write `render_report.json` and `final_review.json` before presenting the video.
- Push artifacts, scripts, Remotion source and Backlot state to GitHub.

## Hard rules learned the hard way

| Rule | Why |
|---|---|
| Never claim a quarterly per-capita level if the agency does not publish one | BPS/NSO publish quarterly growth only |
| Always state price basis | current USD and constant 2015 USD give opposite winners |
| Never put IMF and TradingEconomics numbers in the same chart | different basis = misleading comparison |
| Append decisions, don't edit them | the board and reviewers rely on audit history |
| Measure TTS before setting scene durations | text length ≠ speech length |
| Normalize clips before concat | avoids silent frame loss |
| Check music source for silent tails | prevents mid-video muting |
