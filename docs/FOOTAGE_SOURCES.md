# Free, agent-friendly footage sources

Curated list of stock-footage providers that are both **free** and **usable by an AI agent**
(API, MCP server, or a stable download URL — no browser clicking required).

This pipeline already sources real-video halves from **Pexels** (via MoneyPrinterTurbo) and from
**Wikimedia Commons / Archive.org** (via `scripts/get_clips.py` → OpenMontage `direct_clip_search`).
The providers below are drop-in candidates for widening that pool without adding paid generations.

## Quick reference

| Provider | Free tier | Attribution | Agent access | Best for |
|---|---|---|---|---|
| **Pexels** | Yes | Not required | Free REST API | General B-roll, people, cities (already used here) |
| **Coverr** | Yes, no signup to download | Not required | REST API + **MCP server**, 1,000 free calls/mo | Curated HD/4K, background clips |
| **Pixabay** | Yes | Not required | Free REST API | Large HD/4K library, music & SFX too |
| **Unsplash** | Yes | Not required | REST API | Stills for image-based scenes (video coverage varies) |
| **Mixkit** | Yes | Not required, *but check license* | Direct download | 4K, vertical, backgrounds, music, SFX |
| **Wikimedia Commons** | Yes | Per-file (often CC BY / SA) | MediaWiki API | Historical, educational, documentary |
| **Archive.org / Prelinger** | Yes | Per-item (many public domain) | Advanced Search + download API | Archival, public-domain film |
| **NASA Image & Video Library** | Yes | Public domain (guidelines apply) | `images-api.nasa.gov`, no key needed | Space, Earth, science |
| **Dareful** | Yes | **Required** (CC BY 4.0) | Direct download | 4K nature/drone/aerial |
| **Vecteezy (free)** | Yes | **Required** | Direct download | Large searchable catalog |
| **Vidsplay** | Yes | See terms | Direct download | Nature/backgrounds, weekly updates |
| **Videvo / Videezy** | Mixed free + paid | Often required for free clips | Direct download | General filler footage |
| **Pond5 Free / Canva / Life of Vids** | Rotating or tier-limited | Varies | Mostly manual | Occasional one-off clips |

## Tier 1 — free, no attribution, API or MCP (recommended default)

### Pexels (already in this repo)
- License: free for personal and commercial use, **no attribution required**, modify freely.
- Do **not** resell unaltered clips or redistribute them as a stock library.
- API key (free): <https://www.pexels.com/api/>
- Search endpoint: `GET https://api.pexels.com/videos/search?query=<terms>&per_page=15`
  with header `Authorization: $PEXELS_API_KEY`.
- Current pipeline path: MoneyPrinterTurbo with `pexels_api_keys` configured locally.

### Coverr — most agent-friendly
- Free HD/4K stock video and royalty-free music, **no signup needed to download**, no attribution,
  personal and commercial use.
- REST: `GET https://api.coverr.co/videos?query=<terms>&api_key=$COVERR_API_KEY`
- MCP (give an agent the whole library):
  ```bash
  claude mcp add --transport http coverr https://mcp.coverr.co/mcp
  ```
- Free tier includes **1,000 API calls/month**. API key: <https://coverr.co/> → Developers / API.

### Pixabay
- License: free for commercial use, **no attribution required**; same resale/redistribution limits.
- API key (free): <https://pixabay.com/api/docs/>
- Search endpoint: `GET https://pixabay.com/api/videos/?key=$PIXABAY_API_KEY&q=<terms>`
- Also serves images, music and sound effects from the same account.

### Unsplash
- Best for stills / image-based scenes rather than motion.
- API: `GET https://api.unsplash.com/search/photos?query=<terms>` with
  `Authorization: Client-ID $UNSPLASH_ACCESS_KEY`.

### Mixkit (Envato) — free, with a license trap to watch
- No watermark, no attribution required, direct downloads.
- Two licenses: **Mixkit Video Free License** (commercial OK — YouTube, ads, social) and
  **Mixkit Video Restricted License** (personal / non-commercial only).
- An agent must record which license each downloaded clip carries.

## Tier 2 — free, but attribution or conditions apply

- **Dareful** <https://dareful.com/> — 240+ free 4K/HD nature and aerial clips under
  **CC BY 4.0**. Credit is required, e.g. `Video courtesy of Dareful`.
- **Vecteezy** <https://www.vecteezy.com/free-videos> — large free catalog; free downloads require
  attribution (Pro removes it).
- **Vidsplay** <https://www.vidsplay.com/> — 500+ royalty-free clips updated weekly; check their
  terms of use and keep credit metadata.
- **Videvo / Videezy** — mixed free and paid catalogs; many free clips require attribution.
- **Pond5 Free**, **Canva Stock Video**, **Life of Vids** — rotating or account-limited free picks.

## Tier 3 — public domain / open archives (zero licensing ambiguity)

Ideal for documentary and archival scenes; already partly wired into `scripts/get_clips.py`.

- **Wikimedia Commons** <https://commons.wikimedia.org/wiki/Commons:Video> — 360,000+ freely
  licensed videos. License is **per file**; check the file page. Current `get_clips.py` uses the
  `wikimedia` source.
- **Internet Archive** <https://archive.org/details/movies> — public-domain and CC film, including
  the Prelinger Archives. License is **per item**. Current `get_clips.py` uses the `archive_org` source.
  - Search: `GET https://archive.org/advancedsearch.php?q=<terms>&fl[]=identifier&rows=50&output=json`
  - Download: `https://archive.org/download/<identifier>/<filename>`
- **NASA Image & Video Library** <https://images-api.nasa.gov/search?q=<terms>&media_type=video> —
  no API key required for basic use; NASA content is generally public domain (no implied
  endorsement, avoid using astronaut likenesses for commercial endorsement).
- Other US government open-media sources: NOAA, USGS, Smithsonian Open Access, Library of Congress.

## Wiring a new source into this pipeline

`scripts/get_clips.py` currently calls OpenMontage's `direct_clip_search` with:

```python
"sources": ["wikimedia", "archive_org"],
```

1. **If your OpenMontage tool registry supports the provider**, add it to that list (for example a
   `pexels` source) and keep the narration-matched `queries` and `slots` unchanged.
2. **Otherwise**, fetch clips with the provider's REST/MCP endpoint in a small script, write the
   results into the scene's `assets/video/raw_stock` directory, and continue with
   `scripts/trim_footage.py` → `scripts/finalize_all_assets.py`. The downstream pipeline only needs
   local files; it does not care which API supplied them.
3. **Always record provenance**: source name, clip ID/URL, license, and attribution string in the
   asset manifest and `artifacts/decision_log.json`. That keeps the worked example reproducible.

## Caveats

- "Free" usually means free for personal/commercial use, **not** unlimited redistribution. Do not
  sell unaltered stock clips or republish them as a competing stock library.
- License terms can change. Save a timestamped copy of the license/attribution notice for every
  clip you ship.
- Avoid clips with identifiable people in a negative context, brand logos, or embedded copyrighted
  music — those are the most common reasons a "free" clip is still unsafe for commercial use.
