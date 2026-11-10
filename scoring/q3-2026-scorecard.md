# monday.com Q3 2026 scorecard

The locked Q3 2026 call (`q3-2026-call-locked`, `monday_q3_call.xlsx`) and the locked operating plan (`plan-2026-locked`, `monday_plan.xlsx`), scored against the actual Q3 2026 results. Actuals and their sources are in `q3-2026-actuals.md`. Trigger T3 also uses the Q2 2026 Exhibit 99.1 (https://www.sec.gov/Archives/edgar/data/1845338/000117891326003971/exhibit_99-1.htm) for the June 30, 2026 count of customers over $50k.

- **Locked values:** every forecast value is read from its locked cell by `score_q3_2026.py`, and every variance below is recomputed there (output in `q3-2026-verification.txt`).
- **Nothing in the locked files changed:** no threshold, range or definition was changed after seeing the results.

## 1. Q3 call: scored

**Rule** (from `monday_q3_call.xlsx`, `Scorecard`): "Within range if LOW <= actual <= HIGH (actual as reported by the company)". It's inclusive and compared with the stored, unrounded values. NDR is scored on the reported whole percentage.

| Metric | Low | Mid | High | Actual | Actual − Mid | Result |
|---|---|---|---|---|---|---|
| Revenue (USD m) | 374.471 | 378.382 | 382.350 | **377.535** | −0.847 (−0.22%) | **Hit** (inside) |
| Non-GAAP operating income (USD m) | 62.931 | 69.637 | 72.754 | **89.352** | +19.715 (+28.31%) | **Miss**: above the range by 16.598 |
| All-customer NDR | 107% | 108.5% | 110% | **108%** | −0.5 pp | **Hit** (inside) |
| Paid customers > $50k ARR | 5,028 | 5,111 (5,110.5 unrounded) | 5,128 | **5,038** | −73 (−1.43%) | **Hit**, but only 10 above the low end |

**Score: 3 of 4 scored calls inside their ranges; 1 miss (non-GAAP operating income, above the range).**

Not scored, recorded as the rules say:

| Item | Locked value | Actual | Note |
|---|---|---|---|
| Non-GAAP operating margin (derived from the calls) | 16.8% / 18.4% / 19.0% | **23.67%** (reported 24%) | Derived, not scored. 526 bps above the derived mid and 464 bps above the derived high, because operating income missed high. |
| Adjusted FCF | NO CALL | $63.0M as reported (company now adds back restructuring payments); $15.8M without that add-back | See the FCF watch item below. |
| Current RPO | NO CALL | $759M | Recorded only. |
| FCF watch item | Prior Q3s: 29–34% of revenue, 1.9–2.7× non-GAAP operating income | Company adjusted FCF: **16.7%** of revenue, **0.71×**. Without the restructuring add-back: **4.2%**, **0.18×**. | Far below every prior Q3 on both measures. The reasons, from the filing, are in section 4. |

## 2. Operating plan: Base, actual vs plan

The plan's `Scorecard` asks for plan, actual and difference. It sets no hit/miss bands, so none are applied here.

| Line (plan `Scorecard` / `Cash_FCF`) | Plan (Base) | Actual | Difference |
|---|---|---|---|
| Revenue Q3 2026, USD m | 378.383 | 377.535 | −0.848 (−0.22%) |
| Non-GAAP operating income Q3 2026, USD m | 69.637 | 89.352 | +19.715 (+28.31%) |
| Non-GAAP operating margin Q3 2026 | 18.40% | 23.67% | +5.26 pp |
| Adjusted FCF, reported basis (plan definition: no restructuring add-back), USD m | 56.910 (low confidence) | 15.805 | **−41.105 (−72.23%)** |
| Adjusted FCF, guide basis (excludes restructuring cash), USD m (`Cash_FCF!E7`) | 73.160 (low confidence) | 62.996 | −10.164 (−13.89%) |
| NDR (indicator only) | 108.5% | 108% | −0.5 pp |
| Customers > $50k ARR | 5,110.5 | 5,038 | −72.5 (−1.42%) |
| Cash + marketable securities, Sep 30, 2026, USD m | 1,123.238 | 1,099.394 | −23.844 (−2.12%) |

**The plan's checklist for November 9** (`monday_plan.xlsx`, `Scorecard` rows 13–17). Findings are recorded; nothing in the plan is changed.

1. **Does the FY2026 adjusted FCF guide exclude restructuring and severance?** Yes, by the release's own definition. Adjusted FCF is now "free cash flow plus costs associated with the build-out of our corporate headquarters and restructuring-related cash payments". The FY2026 outlook ($282–288M) is given in adjusted FCF. The outlook bullet itself does not restate the exclusion.
2. **Severance and restructuring cash paid in Q3:** restructuring payments were **$47.2M**, against the plan's assumed severance cash of **$16.25M**. Of that, $32.0M was employee-related and $15.2M was for the settlement and exit of leased offices.
3. **Restructuring charges recognized in Q3:** **$10.0M** net, made up of $21.2M employee-related plus $2.5M facility and other, less a $13.8M SBC reversal credit. Nine months: $31.4M, including $21.4M in Q2. The plan's Q3 line was $25.0M.
4. **T1, T2 and T3:** see section 3.
5. **Updated FY2026 guide:**
   - Revenue $1,473–1,475M.
   - Non-GAAP operating income $268–270M.
   - Adjusted FCF $282–288M.
   - New share repurchase authorization: **not found in the supplied documents**. No repurchases in Q3.

## 3. Scenarios and triggers

Every trigger fires only after **two consecutive quarters** (`Recommendation`). Q3 2026 is therefore at most a first reading. **No trigger fired, and none could have on Q3 alone.**

| Trigger | Threshold (locked) | Q3 2026 reading | Status |
|---|---|---|---|
| T1 Watch (revenue vs Base path) | First threshold is Q4 2026: $390.816M | No Q3 threshold. Q3 revenue was −0.22% against the Base path. | Not applicable to Q3 |
| T1 Action (revenue vs Downside path) | First threshold is Q4 2026: $389.987M | No Q3 threshold. The Downside path equals Base in Q3 ($378.382M). | Not applicable to Q3 |
| T2 (revenue beat vs guidance midpoint) | below 1.4827% | Beat vs the $369.0M midpoint (guide $368–370M): **+2.313%** | **Not** on the trigger side: no first reading |
| T3 (net adds of customers > $50k) | at or below 194 | 5,038 − 4,834 (June 30, 2026, from the Q2 2026 Exhibit 99.1) = **204** | **Not** on the trigger side, by 10: no first reading |

**Which scenario:** neither. The Downside differs from Base only from Q4 2026, so Q3 cannot separate the two cases. Q3 revenue (−0.22% against both paths) fits either.

## 4. Material misses: what the filing says drove them

**Non-GAAP operating income ($89.4M; the call range was $62.9–72.8M).**
- **Spending:** the beat came from spending, not revenue. Revenue was $0.8M below the call mid. Compared with the plan's Base Q3 lines, the filing's non-GAAP lines give:

  | Line | Actual | Plan | Effect on operating income |
  |---|---|---|---|
  | R&D | $70.0M | $84.1M | +$14.1M |
  | Sales and marketing | $145.4M | $151.3M | +$6.0M |
  | G&A | $29.1M | $31.1M | +$1.9M |
  | Gross profit | $333.8M | $336.1M | −$2.3M |

  These sum to the +$19.7M difference.
- **What the filing says:** in its own words, Q3 "reflect[s] disciplined execution on profitability" with "record non-GAAP operating income". Sales and marketing ($145.4M) was lower than in Q3 2025 ($151.8M).
- **The foundation contribution:** non-GAAP operating income also excludes an **$18.0M** contribution to the monday.com Foundation, made in Q3 2026. The call's rule ("as reported by the company") counts the reported $89.4M, so this is a miss.
  - Under a literal reading of the plan's definition, which names only the 2024 contribution, the figure would be $71.4M, inside the range.
  - That reading is flagged, not used: it would resolve an ambiguity in the forecast's favor.
- **What it doesn't say:** the filing gives no further reason why R&D was $14.1M below the plan's assumption.

**Adjusted FCF, reported basis ($15.8M; plan $56.9M, low confidence; the Q3 call was NO CALL).**
- **Operating cash flow:** $20.4M, against $95.1M in Q3 2025.
- **Restructuring payments:** $47.2M, almost three times the plan's $16.25M severance assumption.
  - The plan assumed severance only; the filing includes $15.2M for exiting leased offices.
  - Employee-related payments alone were $32.0M.
- **Other operating lines:** "Accrued expenses and other liabilities, net" used $87.1M of cash (Q3 2025: a $30.2M inflow), and deferred revenue fell $2.7M.
- **Guide basis:** on the guide basis (restructuring cash excluded), adjusted FCF of $63.0M was still $10.2M below the plan's $73.2M.
- **Interest income:** financial income, net, was $12.5M, against $15.8M in Q3 2025.

**Not material: cash plus marketable securities ($1,099.4M; plan $1,123.2M; −2.1%).** The FCF shortfall above explains more than this gap. The filing doesn't break the difference down further.

## 5. Ambiguities, flagged and not resolved in the forecast's favor

1. **Non-GAAP operating income and the 2026 foundation contribution** (section 4): scored as reported.
2. **The adjusted FCF definition changed:** the company now adds back restructuring payments, while the plan's locked definition has no such add-back. Both bases are reported; the plan's reported-basis line uses the locked definition.
3. **NDR basis:** the release defines NDR as "a weighted average ... for the four quarters ending with the most recent quarter". The plan says the "measurement basis [is] not disclosed". The reported 108% is scored as given.
4. **Both locked workbooks still read "DRAFT":** the Q3 call's README reads "DRAFT, NOT LOCKED", and the plan's title says the same. Both are locked by their Releases and hashes, which match. The plan's README notes this.
5. **T3's Q2 count comes from a second filing:** the Q3 documents don't give the June 30, 2026 count, so it was taken from the Q2 2026 Exhibit 99.1, supplied separately. It matches the locked source book (4,834), so the plan's input and the scored input are the same number. T3 cleared by only 10 customers (204 against at or below 194).

## 6. Post-hoc notes (for the next reforecast; they do not change the locked plan)

Lessons only. No threshold, path or assumption in `monday_plan.xlsx` or `monday_q3_call.xlsx` is changed by them.

- **Operating expenses fell faster than assumed after the July 2026 restructuring.** The plan carried Q3 non-GAAP R&D, sales and marketing, and G&A at ratios that came in $22.0M above actual spending. The operating income method (guidance midpoint plus a historical dollar beat) didn't anticipate a quarter with a beat of $31.4M against the $58M midpoint.
- **Restructuring cash came early and was larger.** It included lease exits, which the severance assumption didn't cover. A reforecast should model restructuring cash by category and in the quarters it's paid.
- **The company's adjusted FCF definition now adds back restructuring payments.** Future scorecards should state which definition they use.
- **Fourth-quarter guidance points toward the T1 thresholds.** The Q4 2026 revenue guide ($380–382M, midpoint $381.0M) sits below both Q4 thresholds:

  | Q4 threshold | Level | Beat needed vs the $381.0M midpoint |
  |---|---|---|
  | T1 Watch | $390.8M | +2.58% |
  | T1 Action | $390.0M | +2.36% |

  At the last-eight-quarter median beat (2.54%), Q4 revenue would be about $390.7M. That's just below the Watch threshold and just above the Action threshold. Whether Watch has a first reading is decided by the Q4 results, not by this note.
- **The FY2026 guide midpoints point in opposite directions from the plan:**
  - **Revenue:** the $1,474M midpoint is below both the Base ($1,489.2M) and the Downside ($1,484.3M).
  - **Non-GAAP operating income:** the $269M midpoint is above the Base ($252.1M).
