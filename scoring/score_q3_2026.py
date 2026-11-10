#!/usr/bin/env python3
"""Score the locked Q3 2026 call and the locked operating plan against monday.com's Q3 2026 results.

    python3 scoring/score_q3_2026.py            # prints the full verification output

Read-only. The locked workbooks (monday_q3_call.xlsx, monday_plan.xlsx) are opened with
openpyxl in read-only mode and never written. Every forecast value is read from its locked
cell, not typed here. Every actual is read from the supplied filing in scoring/sources/
(Form 6-K and Exhibit 99.1, accession 0001178913-26-005085), not typed here; the script
fails if a value cannot be found or a cross-check does not tie.

Sources (saved from SEC EDGAR on 2026-11-10 by the repository owner):
  https://www.sec.gov/Archives/edgar/data/1845338/000117891326005085/zk2636355.htm
  https://www.sec.gov/Archives/edgar/data/1845338/000117891326005085/exhibit_99-1.htm
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import sys
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
EXHIBIT = ROOT / "scoring" / "sources" / "exhibit_99-1.htm"
COVER = ROOT / "scoring" / "sources" / "zk2636355.htm"
LOCKED = {
    "monday_q3_call.xlsx": "49463d1fbb678fd26b59c3c81e70cb52613a4a73906b846bcaaf034be76bb722",
    "monday_plan.xlsx": "125af68742c9d3501cd2f23944899cc4625cf5285e79ba9ea2bee34f24315419",
}
UNCHANGED = {  # the other workbooks, as listed in the README and the plan-2026-locked Release
    "monday_sourcebook.xlsx": "50c1c3fc6a631dbcfa9d122b7af2cfbf02b5d35659bb1343cb23739c04594e8f",
    "monday_analysis.xlsx": "07cb0b2497c8d0c9e6844076b163bf532d14d9ee332f67c8447d4254dcf444fd",
    "monday_driver_audit.xlsx": "154bfde55ed6a6d08428da1fb2f96fb8acc51dbf428c7547e4bb9c720c48e12c",
}

failures: list[str] = []


def check(ok: bool, what: str) -> None:
    print(f"  [{'PASS' if ok else 'FAIL'}] {what}")
    if not ok:
        failures.append(what)


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# --- 1. The locked files are unchanged ------------------------------------------------------
print("1. Locked and supporting workbooks (SHA-256 against the Releases / README)")
for name, want in {**LOCKED, **UNCHANGED}.items():
    got = sha256(ROOT / name)
    check(got == want, f"{name} {got[:12]}… == {want[:12]}…")

# --- 2. The supplied filing as text ---------------------------------------------------------
def to_lines(path: Path) -> list[str]:
    raw = path.read_bytes().decode("cp1252", errors="replace")
    raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", "", raw)
    raw = re.sub(r"(?i)</(p|div|tr|h\d|li)>", "\n", raw)
    raw = re.sub(r"(?i)</t[dh]>", " | ", raw)
    text = html.unescape(re.sub(r"<[^>]+>", "", raw)).replace("\xa0", " ")
    out = []
    for line in text.split("\n"):
        line = re.sub(r"\s+", " ", line).strip(" |")
        if line:
            out.append(line)
    return out


ex = to_lines(EXHIBIT)
cover = " ".join(to_lines(COVER))
prose = re.sub(r"\s+", " ", re.sub(r"[●|]", " ", " ".join(ex)))


def table_row(label: str, n: int = 4, start: str | None = None) -> list[float]:
    """The first n numbers after the line that equals `label` (after `start`, if given), in USD thousands."""
    i0 = ex.index(start) if start else 0
    i = next(k for k in range(i0, len(ex)) if ex[k] == label)
    vals: list[float] = []
    for line in ex[i + 1:]:
        m = re.fullmatch(r"\$?\s*\|?\s*\(?\s*([\d,]+(?:\.\d+)?)\s*\|?\s*\)?\s*%?\)?", line)
        if not m:
            if line in ("—", "-"):
                vals.append(0.0)
            else:
                break
        else:
            v = float(m.group(1).replace(",", ""))
            vals.append(-v if "(" in line else v)
        if len(vals) == n:
            return vals
    raise ValueError(f"row {label!r}: found {vals}")


print("\n2. Source documents")
check("monday.com Ltd." in cover and "For the month of November 2026" in cover, "cover: Form 6-K of monday.com Ltd., month of November 2026")
check("Exhibit 99.1" in cover and "exhibit_99-1.htm" in COVER.read_text("cp1252", errors="replace"), "cover lists Exhibit 99.1 (press release dated November 9, 2026)")
check("third quarter ended September 30, 2026" in prose, "exhibit: results for the third quarter ended September 30, 2026")
check("Three months ended September 30," in ex, "statements: three months ended September 30, 2026 (first column) and 2025")

# --- 3. Actuals (USD thousands from the statements; Q3 2026 is column 1, Q3 2025 column 2) ----
OPS = "CONDENSED"  # first statement header
rev = table_row("Revenue")                                   # statements of operations
ngoi = table_row("Non-GAAP operating income")                # reconciliation of operating income
gaap_oi = table_row("GAAP operating income (loss)")
sbc = table_row("Share-based compensation", start="Reconciliation of operating income (loss)")
found = table_row("Charitable contribution to foundation (1)")
restr = table_row("Restructuring charges (2)")
ng_gp = table_row("Non-GAAP gross profit")
ng_rd = table_row("Non-GAAP research and development")
ng_sm = table_row("Non-GAAP sales and marketing")
ng_ga = table_row("Non-GAAP general and administrative")
ocf = table_row("Net cash provided by operating activities", start="Reconciliation")
ppe = table_row("Purchase of property and equipment", start="Reconciliation")
capsw = table_row("Capitalized software development costs", start="Reconciliation")
fcf = table_row("Free cash flow")
hq = table_row("Purchase of property and equipment related to build-out of our corporate headquarters (1)")
rpay = table_row("Restructuring payments (2)")
afcf = table_row("Adjusted free cash flow", start="Restructuring payments (2)")
cash = table_row("Cash and cash equivalents", n=2)
mkt = table_row("Marketable securities", n=2)


def sentence(pattern: str) -> re.Match:
    m = re.search(pattern, prose)
    if not m:
        raise ValueError(f"not found in the supplied documents: {pattern}")
    return m


ndr = sentence(r"Net dollar retention rate was (\d+)%")
c50 = sentence(r"number of paid customers with more than \$50,000 in ARR was ([\d,]+), up (\d+)% from ([\d,]+) as of September 30, 2025")
crpo = sentence(r"Current remaining performance obligations \(cRPOs\) were \$(\d+) million")
fy_rev = sentence(r"full year 2026, monday.com currently expects: Total revenue of \$([\d,]+) million to \$([\d,]+) million")
fy_oi = sentence(r"Non-GAAP operating income of \$(\d+) million to \$(\d+) million and operating margin of approximately 18%, assuming a negative FX impact of 100 to 200 basis points. Adjusted")
fy_fcf = sentence(r"Adjusted free cash flow of \$(\d+) million to \$(\d+) million")
q4_rev = sentence(r"fourth quarter of fiscal year 2026, monday.com currently expects: Total revenue of \$(\d+) million to \$(\d+) million")
q2_count = re.search(r"\$50,000 in ARR was [\d,]+, up \d+% from [\d,]+ as of June 30, 2026", prose)

A = {
    "revenue": rev[0] / 1000,
    "ngoi": ngoi[0] / 1000,
    "ndr": int(ndr.group(1)) / 100,
    "c50": int(c50.group(1).replace(",", "")),
    "afcf_company": afcf[0] / 1000,
    "cash_sec": (cash[0] + mkt[0]) / 1000,
}
A["margin"] = A["ngoi"] / A["revenue"]
# The plan's adjusted FCF bases (Definitions!B4 and Cash_FCF rows 7 and 11), from the filing's lines:
A["afcf_reported_basis"] = (ocf[0] + ppe[0] + capsw[0] + hq[0]) / 1000      # no add-back for restructuring cash
A["afcf_guide_basis"] = (ocf[0] + ppe[0] + capsw[0] + hq[0] + rpay[0]) / 1000  # excludes restructuring cash

print("\n3. Cross-checks inside the filing (each actual tied to a second place)")
check(abs(A["revenue"] - 377.5) < 0.05 and "Revenue was $377.5 million" in prose, f"revenue {rev[0]:,.0f}k (statement) = $377.5 million (highlights)")
check(gaap_oi[0] + sbc[0] + found[0] + restr[0] == ngoi[0], f"non-GAAP op. income: GAAP {gaap_oi[0]:,.0f} + SBC {sbc[0]:,.0f} + foundation {found[0]:,.0f} + restructuring {restr[0]:,.0f} = {ngoi[0]:,.0f}k")
check(abs(ng_gp[0] - ng_rd[0] - ng_sm[0] - ng_ga[0] - ngoi[0]) <= 1, f"non-GAAP op. income = non-GAAP GP {ng_gp[0]:,.0f} - R&D {ng_rd[0]:,.0f} - S&M {ng_sm[0]:,.0f} - G&A {ng_ga[0]:,.0f} (within $1k rounding)")
check("Non-GAAP operating income was $89.4 million" in prose and "Non-GAAP operating margin was 24%" in prose, "highlights: non-GAAP operating income $89.4 million, margin 24%")
check(round(A["margin"] * 100) == 24, f"margin {A['margin']:.4%} rounds to the reported 24%")
check(ocf[0] + ppe[0] + capsw[0] == fcf[0], f"FCF: OCF {ocf[0]:,.0f} - PP&E {-ppe[0]:,.0f} - cap. software {-capsw[0]:,.0f} = {fcf[0]:,.0f}k")
check(fcf[0] + hq[0] + rpay[0] == afcf[0], f"adjusted FCF: FCF {fcf[0]:,.0f} + HQ {hq[0]:,.0f} + restructuring payments {rpay[0]:,.0f} = {afcf[0]:,.0f}k")
check("$63.0 million of adjusted free cash flow" in prose and "Net cash provided by operating activities was $20.4 million" in prose, "highlights: OCF $20.4 million, adjusted FCF $63.0 million")
check(table_row("CASH AND CASH EQUIVALENTS - End of period", n=1)[0] == cash[0], f"cash at Sep 30: balance sheet {cash[0]:,.0f} = cash flow statement end of period")
check(abs(int(c50.group(1).replace(",", "")) / int(c50.group(3).replace(",", "")) - 1 - int(c50.group(2)) / 100) < 0.005, f"customers >$50k: {c50.group(1)} vs {c50.group(3)} a year earlier = +{c50.group(2)}% as stated")

print("\n4. Tie-out of the filing's prior-year column to the locked plan (Historical_Drivers, Sourced)")
call = openpyxl.load_workbook(ROOT / "monday_q3_call.xlsx", data_only=True, read_only=True)
plan = openpyxl.load_workbook(ROOT / "monday_plan.xlsx", data_only=True, read_only=True)
hd = plan["Historical_Drivers"]
hd_rows = {r[0]: r for r in hd.iter_rows(values_only=True) if r and r[0]}
hdr = next(r for r in hd.iter_rows(values_only=True) if r and r[0] == "Metric")
q325 = list(hdr).index("Q3 2025")
check(hd_rows["Revenue"][q325] == rev[1], f"Q3 2025 revenue: filing {rev[1]:,.0f} = plan {hd_rows['Revenue'][q325]:,.0f}")
check(hd_rows["Customers >$50k ARR"][q325] == int(c50.group(3).replace(",", "")), f"Q3 2025 customers >$50k: filing {c50.group(3)} = plan {hd_rows['Customers >$50k ARR'][q325]:,}")
ngoi_row = next((r for k, r in hd_rows.items() if str(k).startswith("Operating income (non-GAAP)")), None)
if ngoi_row is not None:
    check(ngoi_row[q325] == ngoi[1], f"Q3 2025 non-GAAP op. income: filing {ngoi[1]:,.0f} = plan {ngoi_row[q325]:,.0f}")

# --- 5. Locked values (read from their cells) ------------------------------------------------
sc = call["Scorecard"]
L = {k: (sc[f"C{r}"].value, sc[f"D{r}"].value, sc[f"E{r}"].value) for k, r in
     [("revenue", 5), ("ngoi", 6), ("margin", 7), ("ndr", 8), ("c50", 9)]}
ps, rec, cf, pnl = plan["Scorecard"], plan["Recommendation"], plan["Cash_FCF"], plan["PnL"]
P = {"revenue": ps["C4"].value, "ngoi": ps["C5"].value, "margin": ps["C6"].value, "afcf_reported_basis": ps["C7"].value,
     "ndr": ps["C8"].value, "c50": ps["C9"].value, "cash_sec": ps["C10"].value, "afcf_guide_basis": cf["E7"].value,
     "severance": -cf["E10"].value, "gp": pnl["E7"].value, "rd": pnl["E8"].value, "sm": pnl["E9"].value, "ga": pnl["E10"].value,
     "sbc": pnl["E13"].value, "restr": pnl["E14"].value, "downside_rev_q3": pnl["E21"].value}
T = {"t1_watch_q4": rec["C5"].value, "t1_action_q4": rec["C6"].value, "t2": rec["C8"].value, "t3": rec["C9"].value}
guid = {}
for ws in plan.worksheets:
    for row in ws.iter_rows(values_only=True):
        if row and isinstance(row[0], str) and row[0].startswith("Q3 2026 Revenue guidance") and isinstance(row[2], (int, float)):
            guid[row[0].split()[-1]] = row[2]
guide_mid = (guid["low"] + guid["high"]) / 2

print("\n5. Q3 call scorecard (rule: within range if LOW <= actual <= HIGH, inclusive, actual as reported)")
rows = []
for key, label, actual, fmt in [("revenue", "Revenue (USD m)", A["revenue"], "{:.3f}"), ("ngoi", "Non-GAAP operating income (USD m)", A["ngoi"], "{:.3f}"),
                                 ("ndr", "All-customer NDR (reported whole %)", A["ndr"], "{:.2f}"), ("c50", "Paid customers >$50k ARR", A["c50"], "{:.0f}")]:
    lo, mid, hi = L[key]
    pos = "INSIDE (hit)" if lo <= actual <= hi else ("ABOVE (miss)" if actual > hi else "BELOW (miss)")
    rows.append((key, actual, lo, mid, hi, pos))
    print(f"  {label:38s} actual {fmt.format(actual):>9}  low {fmt.format(lo)}  mid {fmt.format(mid)}  high {fmt.format(hi)}  "
          f"vs mid {actual - mid:+.3f} ({(actual / mid - 1):+.2%})  vs edge {(actual - hi) if actual > hi else (actual - lo) if actual < lo else 0:+.3f}  -> {pos}")
lo, mid, hi = L["margin"]
print(f"  {'Non-GAAP op. margin (derived; NOT scored)':38s} actual {A['margin']:.4f}  low {lo:.4f}  mid {mid:.4f}  high {hi:.4f}  vs mid {A['margin'] - mid:+.4f} ({(A['margin'] - mid) * 1e4:+.0f} bps)")
print(f"  {'Adjusted FCF / cRPO':38s} NO CALL (recorded only): adjusted FCF as reported ${A['afcf_company']:.3f}M; cRPO ${crpo.group(1)}M")

print("\n6. Plan scorecard (Base; actual vs plan and difference; the plan sets no hit/miss bands)")
for key, label in [("revenue", "Revenue Q3 2026, USD m"), ("ngoi", "Non-GAAP op. income Q3 2026, USD m"), ("margin", "Non-GAAP op. margin Q3 2026"),
                   ("afcf_reported_basis", "Adjusted FCF, reported basis (plan definition), USD m"), ("afcf_guide_basis", "Adjusted FCF, guide basis, USD m"),
                   ("ndr", "NDR (indicator)"), ("c50", "Customers >$50k ARR"), ("cash_sec", "Cash + marketable securities Sep 30, USD m")]:
    a, p = A[key], P[key]
    print(f"  {label:54s} plan {p:12.4f}  actual {a:12.4f}  difference {a - p:+12.4f}  ({(a / p - 1):+.2%})")

print("\n7. Explaining the operating income difference (filing non-GAAP lines vs plan Base Q3, USD m)")
diff_lines = {"gross profit": (ng_gp[0] / 1000, P["gp"], +1), "R&D": (ng_rd[0] / 1000, P["rd"], -1), "S&M": (ng_sm[0] / 1000, P["sm"], -1), "G&A": (ng_ga[0] / 1000, P["ga"], -1)}
tot = 0.0
for name, (a, p, sign) in diff_lines.items():
    eff = sign * (a - p)
    tot += eff
    print(f"  {name:13s} actual {a:9.3f}  plan {p:9.3f}  effect on operating income {eff:+8.3f}")
check(abs(tot - (A["ngoi"] - P["ngoi"])) < 0.002, f"line effects sum {tot:+.3f} = operating income difference {A['ngoi'] - P['ngoi']:+.3f} (within $2k rounding)")
print(f"  memo: SBC actual {sbc[0] / 1000:.3f} vs plan {P['sbc']:.3f}; restructuring charges actual {restr[0] / 1000:.3f} vs plan {P['restr']:.3f}; foundation contribution excluded {found[0] / 1000:.3f}")
print(f"  memo: operating income under a literal reading of the plan definition (2026 foundation contribution NOT excluded): {(ngoi[0] - found[0]) / 1000:.3f} -> "
      f"{'inside' if L['ngoi'][0] <= (ngoi[0] - found[0]) / 1000 <= L['ngoi'][2] else 'outside'} the call range (flagged, not used)")

print("\n8. Cash items")
print(f"  restructuring payments ${rpay[0] / 1000:.3f}M (of which employee-related $32.0M, leases $15.2M per note 2) vs plan Q3 severance cash ${P['severance']:.2f}M")
check("$32.0 million in employee-related payments and $15.2 million related to the settlement" in prose, "note (2): $32.0M employee-related + $15.2M leases = restructuring payments")
print(f"  restructuring charges ${restr[0] / 1000:.3f}M (Q3) and ${restr[2] / 1000:.3f}M (nine months) vs plan Q3 ${P['restr']:.1f}M")
print(f"  Q3 FCF watch item: adjusted FCF (company) / revenue {A['afcf_company'] / A['revenue']:.1%}, / non-GAAP op. income {A['afcf_company'] / A['ngoi']:.2f}x; "
      f"reported basis (plan definition) {A['afcf_reported_basis'] / A['revenue']:.1%} and {A['afcf_reported_basis'] / A['ngoi']:.2f}x  (prior Q3s: 29-34%, 1.9-2.7x)")

print("\n9. Triggers (all need two consecutive quarters; Q3 2026 is at most the first reading)")
beat = A["revenue"] / guide_mid - 1
print(f"  T1 Watch / Action: no Q3 2026 threshold (first thresholds Q4 2026: Watch {T['t1_watch_q4']:.3f}, Action {T['t1_action_q4']:.3f}). Not applicable to Q3.")
print(f"     memo: Q3 revenue {A['revenue']:.3f} vs Base path {P['revenue']:.3f} ({A['revenue'] / P['revenue'] - 1:+.2%}); Downside path Q3 {P['downside_rev_q3']:.3f} (same as Base in Q3)")
print(f"  T2: beat vs guidance midpoint {guide_mid:.1f} = {beat:+.4%} vs threshold {T['t2']:.4%} -> {'BELOW threshold (first reading on the trigger side)' if beat < T['t2'] else 'NOT below threshold (no first reading)'}")
print(f"  T3: net adds = Q3 count {A['c50']:,} - Q2 2026 count: "
      + ("found" if q2_count else "Q2 2026 count NOT FOUND in the supplied documents -> T3 not evaluated"))
q4m = (int(q4_rev.group(1)) + int(q4_rev.group(2))) / 2
print(f"  post-hoc memo (not a trigger): Q4 2026 revenue guide ${q4_rev.group(1)}-{q4_rev.group(2)}M, midpoint {q4m:.1f}; Q4 Watch threshold {T['t1_watch_q4']:.3f} needs a "
      f"{T['t1_watch_q4'] / q4m - 1:+.2%} beat, Action {T['t1_action_q4']:.3f} needs {T['t1_action_q4'] / q4m - 1:+.2%}")
print(f"  updated FY2026 guide: revenue ${fy_rev.group(1)}-{fy_rev.group(2)}M, non-GAAP op. income ${fy_oi.group(1)}-{fy_oi.group(2)}M, adjusted FCF ${fy_fcf.group(1)}-{fy_fcf.group(2)}M")

# --- 10. The portfolio results file --------------------------------------------------------
print("\n10. Portfolio results file (scoring/monday_q3_actuals.json), validated with the site's rules")
doc = json.loads((ROOT / "scoring" / "monday_q3_actuals.json").read_text())
a, t = doc["actuals"], doc["triggers"]
check(doc["version"] == 1 and doc["status"] == "scored", "version 1, status scored")
check(doc["source"]["retrieved_at"] >= "2026-11-09T13:30:00Z", f"retrieved_at {doc['source']['retrieved_at']} is after 2026-11-09T13:30:00Z")
check(a["revenue_usd_m"] == round(A["revenue"], 1), f"revenue_usd_m {a['revenue_usd_m']} = {A['revenue']:.3f} to 1 decimal")
check(a["non_gaap_operating_income_usd_m"] == round(A["ngoi"], 1), f"non_gaap_operating_income_usd_m {a['non_gaap_operating_income_usd_m']} = {A['ngoi']:.3f} to 1 decimal")
check(abs(a["non_gaap_operating_margin"] - a["non_gaap_operating_income_usd_m"] / a["revenue_usd_m"]) <= 0.0005, f"margin {a['non_gaap_operating_margin']} = op. income / revenue within 0.05 pp")
check(a["net_dollar_retention"] == A["ndr"] and a["customers_over_50k_arr"] == A["c50"], "NDR and customers match the filing")
check(abs(t["t2_revenue_beat_vs_guidance_mid"] - (a["revenue_usd_m"] / guide_mid - 1)) <= 0.00005, f"t2 {t['t2_revenue_beat_vs_guidance_mid']} = revenue / {guide_mid} - 1 within 0.005 pp (site rule)")
print(f"  t3_net_adds_customers_over_50k = {t['t3_net_adds_customers_over_50k']!r}: the site requires a number; NOT FOUND in the supplied documents, so the file does not yet validate.")

print(f"\nRESULT: {len(failures)} failed check(s)" + (": " + "; ".join(failures) if failures else ""))
sys.exit(1 if failures else 0)
