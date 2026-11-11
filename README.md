# monday.com Operating Plan, Q3 2026 to Q4 2027

An outside-in operating plan for monday.com, built only from public SEC filings. It was fixed before the company reported Q3 2026 results on November 9, 2026.

**Information cutoff:** October 28, 2026. No data published after that date is used in the workbooks. The Q3 2026 scoring in `scoring/` uses the Q3 2026 Form 6-K filed November 9, 2026.

## Management question

If growth decelerates faster than guided after the July 2026 restructuring, how should management adjust hiring and operating spend to protect margin and cash generation without damaging long-term growth?

## Summary of results

From the `Executive_Summary` sheet of `monday_plan.xlsx`, in USD millions. FCF means adjusted free cash flow.

1. Revenue: Base $1,489.2M (FY26) and $1,706.2M (FY27); Downside $1,484.3M and $1,626.5M.
2. Non-GAAP operating income: Base $252.1M and $328.5M; Downside $247.1M and $249.4M.
3. Non-GAAP operating margin: Base 16.9% and 19.3%; Downside 16.6% and 15.3%.
4. FCF on the guidance basis (before severance): Base $285.0M (FY26) and $371.4M (FY27; range $328.5M to $403.5M at 1.0x to 1.23x conversion); Downside $281.1M and $249.4M. Including severance, FY26 FCF is $252.5M Base and $246.1M Downside.
5. The FY27 revenue gap between Base and Downside (4.7% of Base) is about 1.13 times the average 4-quarter-ahead backtest miss. The two cases cannot be told apart in advance, so the plan acts on triggers rather than on the forecast.

The Downside assumes growth decelerates faster (2.6 points a year instead of 1.3) and that operating expense dollars stay at the Base level before any management response.

## The five workbooks

| File | Purpose |
|---|---|
| `monday_sourcebook.xlsx` | Source book. Quarterly and annual figures and guidance copied from SEC filings, each with a Row ID and a Source ID linking to the filing. |
| `monday_analysis.xlsx` | Historical analysis: guidance accuracy, growth decomposition, margin structure, cash conversion and deceleration. |
| `monday_q3_call.xlsx` | Pre-registered call for Q3 2026 (low / mid / high) on revenue, operating income, margin, net dollar retention and customers above $50K ARR. |
| `monday_driver_audit.xlsx` | Evidence audit for the plan's drivers, including the backtest used to choose the revenue method. |
| `monday_plan.xlsx` | The operating plan: Base and Downside cases for Q3 2026 to Q4 2027, cash bridge, management-response breakevens, trigger metrics, checks and a `Scorecard` left blank at the lock (the Q3 2026 scoring is in `scoring/`). |

`PHASE3_DESIGN.md` is the design brief for the plan.

## How to read the model

Start with the `Executive_Summary` sheet in `monday_plan.xlsx`, a one-page summary in which every number is a formula link into the model. Then:

- `Recommendation`: the triggers, their thresholds and the actions mapped to each tier.
- `Assumptions`: every assumption, with its current level, forecast path, rationale, evidence and sensitivity.
- `Revenue_Build`, `Opex`, `PnL` and `Cash_FCF`: the quarterly build.
- `Scenarios`: Base compared with Downside.
- `Method_Changes`: every change of method and owner ruling, with its date.
- `Checks`: the input tie-outs to the source files and the internal checks.

The `Executive_Summary` title still reads "DRAFT, not locked". The file was locked with that wording and will not be edited.

## Pre-registration and locks

Two GitHub Releases locked the forecasts on October 28 and 29, 2026, before the Q3 2026 results were known. Each lists the SHA-256 hash of its files, so anyone can confirm the file has not changed since.

| Release (tag) | Published (GitHub, UTC) | Commit | Locks |
|---|---|---|---|
| `q3-2026-call-locked` | 2026-10-28 21:43:23 | `60e2932` | The Q3 2026 call (`monday_q3_call.xlsx`) |
| `plan-2026-locked` | 2026-10-29 17:31:14 | `07a7363` | The operating plan (`monday_plan.xlsx`) |

SHA-256 of each workbook (identical on `main` and in both tags where the file is present):

| File | SHA-256 |
|---|---|
| `monday_plan.xlsx` | `125af68742c9d3501cd2f23944899cc4625cf5285e79ba9ea2bee34f24315419` |
| `monday_q3_call.xlsx` | `49463d1fbb678fd26b59c3c81e70cb52613a4a73906b846bcaaf034be76bb722` |
| `monday_sourcebook.xlsx` | `50c1c3fc6a631dbcfa9d122b7af2cfbf02b5d35659bb1343cb23739c04594e8f` |
| `monday_analysis.xlsx` | `07cb0b2497c8d0c9e6844076b163bf532d14d9ee332f67c8447d4254dcf444fd` |
| `monday_driver_audit.xlsx` | `154bfde55ed6a6d08428da1fb2f96fb8acc51dbf428c7547e4bb9c720c48e12c` |

The revenue trigger's Watch tier was written into `Method_Changes` and committed (`6324743`) before it was tested. The Action tier was chosen after that test, and the workbook says so. `monday_plan.xlsx` passes all 349 of its checks.

To check a file on Windows PowerShell:

```powershell
cd $HOME\Downloads
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/2samfelix/monday-operating-plan/plan-2026-locked/monday_plan.xlsx" -OutFile "monday_plan.xlsx"
Get-FileHash .\monday_plan.xlsx -Algorithm SHA256
```

## Q3 2026 results

monday.com reported Q3 2026 results on November 9, 2026. They were scored against the locked call (`q3-2026-call-locked`) and the locked plan (`plan-2026-locked`).

- **Score:** 3 of 4 scored calls landed inside their locked ranges. Revenue was $377.535M, against a range of $374.471M to $382.350M. All-customer NDR was 108%, against 107% to 110%. Paid customers above $50K ARR were 5,038, against 5,028 to 5,128.
- **The miss:** non-GAAP operating income was $89.352M, above the $62.931M to $72.754M range by $16.598M. It is published as a miss.
- **Triggers:** no trigger fired. None could have fired on Q3 alone, because each needs two consecutive quarters.
  - T2: the beat against the guidance midpoint was +2.313%, against a threshold of below 1.4827%.
  - T3: net adds of customers above $50K ARR were 204, against a threshold of at or below 194.

Details:

- [`scoring/q3-2026-scorecard.md`](scoring/q3-2026-scorecard.md): the scorecard, with the misses explained and the ambiguities flagged.
- [`scoring/q3-2026-actuals.md`](scoring/q3-2026-actuals.md): the actuals and where each one is in the filing.
- [`scoring/q3-2026-verification.txt`](scoring/q3-2026-verification.txt): the script's checks and recomputed variances.

## How Q3 2026 was scored

- The trigger thresholds were fixed on the lock date. The Q3 2026 results were not used to change them.
- After the results, the actuals were recorded in [`scoring/`](scoring/), not in the workbooks' `Scorecard` sheets:
  - [`scoring/monday_q3_actuals.json`](scoring/monday_q3_actuals.json) holds the actuals.
  - The `scoring/*.md` files hold the actuals and the scorecard.
  - [`scoring/score_q3_2026.py`](scoring/score_q3_2026.py) reads every value and recomputes every variance.
- The locked files and Releases were not edited.
- The `Scorecard` in `monday_plan.xlsx` also listed the items to check on November 9. The answers are in section 2 of the scorecard. For example, the FY2026 adjusted FCF guide does exclude restructuring by the release's own definition, though the outlook bullet itself does not restate the exclusion.

## Labels

Every number in the workbooks carries one of three labels:

- **Sourced**: copied from a filing or an earlier workbook, with a Row ID or cell reference. Shown in blue.
- **Derived**: calculated by a formula from other cells. Shown in black.
- **Assumed**: a judgement, with a rationale and a sensitivity. Shown in orange on a light orange fill.

## Limits

- This is not monday.com's internal budget, and it does not reconstruct one. It is an outside-in forecast built from public filings.
- It is not guidance. The Base case is a beat-adjusted central estimate and sits above the top of the FY2026 guided ranges for revenue and operating income.
- The cost in lost growth of cutting spend cannot be measured from public data. The plan shows breakeven revenue losses instead of predicting that cost.
- Forecast accuracy drops beyond two quarters ahead. Q3 and Q4 2027 lie beyond the tested horizon.
- Open items listed in the workbook at the lock:
  - **Answered by the Q3 2026 results** (scorecard, section 2):
    - The FY2026 adjusted FCF guide does exclude restructuring, by the company's definition.
    - Restructuring payments in Q3 2026 were $47.2M: $32.0M employee-related and $15.2M for exiting leased offices. The plan assumed $16.25M of severance cash.
  - **Still open:**
    - The guidance-beat trigger (T2) has never fired, and Q3 2026 was not on the trigger side.
    - The revenue trigger's (T1) first thresholds are in Q4 2026, so it has no reading yet.

## Data sources

- SEC EDGAR filings by monday.com Ltd. (CIK 0001845338): Form 20-F annual reports for FY2021 to FY2025; 6-K earnings releases from Q2 2021 to Q2 2026; interim financial statements and MD&A; the July 22, 2026 restructuring 6-K; and other 6-Ks. All 49 sources are listed with URLs and accession numbers in the `Sources` sheet of `monday_sourcebook.xlsx`.
- The investor relations website (ir.monday.com) could not be reached and was not used. No secondary sources were used.
