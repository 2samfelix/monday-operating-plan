# monday.com Q3 2026 actuals

Actual results for the quarter ended **September 30, 2026** (fiscal Q3 2026), for scoring the locked call (`q3-2026-call-locked`) and the locked plan (`plan-2026-locked`). This file and everything else in `scoring/` is new; no locked file was edited.

## Source

The only source is the Q3 2026 Form 6-K and its Exhibit 99.1, saved from SEC EDGAR by the repository owner on November 10, 2026 (about 18:38 UTC). Copies are in `scoring/sources/`.

| Document | EDGAR URL |
|---|---|
| Form 6-K cover, "For the month of November 2026" | https://www.sec.gov/Archives/edgar/data/1845338/000117891326005085/zk2636355.htm |
| Exhibit 99.1, press release "monday.com Announces Third Quarter 2026 Results", dated November 9, 2026 | https://www.sec.gov/Archives/edgar/data/1845338/000117891326005085/exhibit_99-1.htm |

- **Filing:** accession 0001178913-26-005085, filed November 9, 2026.
- **No other sources:** no memory, news or third-party data.
- **Script:** every value below is read from the exhibit by `scoring/score_q3_2026.py`, not typed, and cross-checked as shown.

## Actuals

Statement figures are USD thousands, converted to USD millions. Each figure is checked against a second place in the filing.

| Metric (locked definition) | Actual | Where in Exhibit 99.1 | Second place in the filing (cross-check) |
|---|---|---|---|
| Revenue, Q3 2026 | **$377.535M** | Condensed consolidated statements of operations, "Revenue", three months ended Sep 30, 2026: 377,535 | Highlights: "Revenue was $377.5 million, an increase of 19% year-over-year" ✓ |
| Non-GAAP operating income | **$89.352M** | Reconciliation of GAAP to non-GAAP, "Non-GAAP operating income": 89,352 | GAAP 31,187 + SBC 30,203 + foundation contribution 18,000 + restructuring 9,962 = 89,352 ✓. Non-GAAP gross profit 333,822 − R&D 69,984 − S&M 145,370 − G&A 29,116 = 89,352 ✓. Highlights: "$89.4 million" ✓ |
| Non-GAAP operating margin (derived) | **23.67%** | 89,352 / 377,535 | Reconciliation table: "Non-GAAP operating margin 24%"; highlights: "24%" ✓ |
| All-customer net dollar retention | **108%** | Recent business highlights: "Net dollar retention rate was 108%." | No second figure in the filing (the release gives the rate once). |
| Paid customers with more than $50k ARR | **5,038** | Recent business highlights: "...more than $50,000 in ARR was 5,038, up 26% from 3,993 as of September 30, 2025." | 5,038 / 3,993 − 1 = 26.2%, the stated "up 26%" ✓ |
| Adjusted FCF, company definition (adds back restructuring payments) | **$62.996M** | Reconciliation of net cash provided by operating activities to adjusted free cash flow: 62,996 | FCF 15,805 + HQ build-out 0 + restructuring payments 47,191 = 62,996 ✓. Highlights: "$63.0 million of adjusted free cash flow" ✓ |
| Adjusted FCF, plan "reported basis" (no restructuring add-back) | **$15.805M** | Same table: OCF 20,396 − PP&E 4,159 − capitalized software 432 + HQ build-out 0 | Equals the "Free cash flow" line (HQ build-out was 0 in Q3) ✓ |
| Adjusted FCF, plan "guide basis" (excludes restructuring cash) | **$62.996M** | As the company's adjusted FCF above | — |
| Restructuring payments (cash) | **$47.191M** | Adjusted FCF reconciliation, "Restructuring payments (2)" | Note (2): $32.0M employee-related + $15.2M settlement and exit of leased offices ✓ |
| Restructuring charges (P&L) | **$9.962M** (Q3); $31.398M (nine months) | Statements of operations, "Restructuring charges" | Note (2) to the reconciliation: $10.0M in Q3 = $21.2M employee-related + $2.5M facility and other − $13.8M SBC reversal credit ✓ |
| Cash + marketable securities, Sep 30, 2026 | **$1,099.394M** | Balance sheet: cash and cash equivalents 869,554 + marketable securities 229,840 | Cash flow statement, "Cash and cash equivalents – end of period": 869,554 ✓ |
| Current RPO | **$759M** | Recent business highlights | — (recorded only; no call) |
| Updated FY2026 outlook | Revenue $1,473–1,475M; non-GAAP operating income $268–270M; adjusted FCF $282–288M | Financial outlook | — |
| Q4 2026 outlook | Revenue $380–382M; non-GAAP operating income $68–70M | Financial outlook | — |
| Q2 2026 count of customers > $50k (needed for trigger T3) | **Not found in the supplied documents** | The release gives Q3 2026 and Q3 2025 only. | — |
| New share repurchase authorization | **Not found in the supplied documents** | No authorization is announced. The cash flow statement shows no Q3 repurchases (nine months: 734,971). | — |

## Tie-out to the locked plan

The filing's Q3 2025 comparatives match the locked plan's sourced history (`Historical_Drivers`):

| Q3 2025 figure | Filing | Locked plan |
|---|---|---|
| Revenue | 316,855 | 316,855 ✓ |
| Non-GAAP operating income | 47,484 | 47,484 ✓ |
| Customers > $50k | 3,993 | 3,993 ✓ |

The units and the fiscal period line up with the plan.

## Definitions: matches and two ambiguities

**What matches:**
- **Revenue:** GAAP revenue as reported.
- **Margin:** derived, as in the call.
- **NDR:** the reported whole percentage, as the call's scoring rule says.
- **Customers > $50k:** the reported count.

**Ambiguity 1: non-GAAP operating income.**
- **The two definitions:** the locked plan defines it as "GAAP operating income excluding SBC, restructuring (from Q2 2026) and the 2024 foundation contribution (company definition)". The Q3 2026 figure also excludes a new **$18.0M** contribution to the monday.com Foundation, made in Q3 2026.
- **How it's scored:** the call's scoring rule says "actual as reported by the company", so the scorecard uses the reported $89.352M.
- **The other reading:** a literal reading of the plan's wording, which excludes only the 2024 contribution, gives $71.352M. That would fall inside the call range. It is recorded here and **not used**.

**Ambiguity 2: adjusted FCF.**
- **The locked definition:** the plan's `Definitions` sheet gives the company's definition at the lock date as "OCF − PP&E − capitalized software + HQ build-out add-back; no add-back for restructuring or severance".
- **The new definition:** the Q3 2026 release adds back "restructuring-related cash payments".
- **How it's handled:** both bases from the locked plan are reported.
  - **Reported basis** (no add-back): $15.805M.
  - **Guide basis** (excludes restructuring cash): $62.996M.
