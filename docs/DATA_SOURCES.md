# Data sources and verification

All numeric claims in the video trace to `artifacts/data_manifest.json`.

## Quarterly growth (primary proof)

| Quarter | Vietnam (NSO) | Indonesia (BPS) |
|---|---:|---:|
| 2025 Q1 | 7.05% | 4.87% |
| 2025 Q2 | 8.16% | 5.12% |
| 2025 Q3 | 8.25% | 5.04% |
| 2025 Q4 | 8.46% | 5.20% |
| 2026 Q1 | 8.15%* | 5.61% |
| 2026 Q2 | 8.81%* | 5.29% |
| 2026 Q3 | 9.95% | 5.47% |

\* Vietnam Q1/Q2 2026 were revised upward in the Q3 2026 NSO release (from 7.83%/8.39%).

Sources:
- NSO Vietnam Q3 2026 press release: https://www.nso.gov.vn/en/data-and-statistics/2026/11/press-release-socio-economic-performance-in-the-q3-and-the-nine-months-of-2026/
- NSO Vietnam Q4 2025 press release: https://www.nso.gov.vn/en/data-and-statistics/2026/01/press-release-social-economic-situation-in-the-fourth-quarter-and-2025/
- BPS quarterly YoY via TradingEconomics (source: Statistics Indonesia): https://tradingeconomics.com/indonesia/gdp-growth-annual

## Levels

- World Bank API, `NY.GDP.PCAP.CD` (current US$) and `NY.GDP.PCAP.KD` (constant 2015 US$):
  https://api.worldbank.org/v2/country/VNM;IDN/indicator/NY.GDP.PCAP.CD
- IMF WEO **October 2026**, "GDP per capita, current prices": Vietnam 5.26 thousand, Indonesia 5.15 thousand.
  The page was retrieved through **FlareSolverr** after direct requests returned 403; this confirmed the vintage and current-price basis.

## Growth drivers (scene s8)

NSO Q3 2026 release: industry & construction +12.50%, contributing 51.57% of total growth; exports +23.27%; FDI disbursement 9M 2026 = US$21.07bn (+12.1%).

## Population & FX (scene s9)

World Bank `SP.POP.TOTL` (VN 101.6M, ID 285.7M in 2025) and `PA.NUS.FCRF` (IDR 15,855 → 16,478 in 2025 = +3.9%; VND ~24,165 → ~25,000).

## Footage licensing

All real-video halves come from **Pexels** (Pexels License) via MoneyPrinterTurbo, with queries matched to each scene's narration (Vietnam skyline/factory/port; Indonesia BPS office/bank/rupiah/Jakarta crowd; newsroom for the intro). No API key is stored in this repo.
