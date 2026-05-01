"""
Score the manual audit. Reads audit/edge_sample_25.tsv, normalizes verdicts,
computes verification rates and 95% Wilson confidence intervals per edge type,
and writes a paper-ready Markdown summary.
"""
import csv
import math
from collections import Counter, defaultdict
from pathlib import Path

INPUT = Path("audit/edge_sample_25.tsv")
OUTPUT = Path("audit/audit_summary.md")


def wilson_ci(successes, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half) * 100, min(1.0, centre + half) * 100)


def normalize(v):
    v = (v or "").strip().upper()
    # Map common aliases
    if v in ("N/A", "NA", "NULL"):
        return "NA"
    if v in ("VERIFIED", "PARTIAL", "UNVERIFIED"):
        return v
    return ""


def main():
    rows = list(csv.DictReader(open(INPUT), delimiter="\t"))
    print(f"Loaded {len(rows)} sampled edges from {INPUT}")

    audited = []
    for r in rows:
        v = normalize(r.get("verdict", ""))
        if v:
            r["verdict_norm"] = v
            audited.append(r)
    print(f"Audited (with normalized verdict): {len(audited)}")
    if not audited:
        print("No audited rows. Exiting.")
        return

    by_type = defaultdict(list)
    for r in audited:
        by_type[r["edge_type"]].append(r["verdict_norm"])

    print()
    print(f"{'Edge type':<22} {'n':>3} {'V':>4} {'P':>4} {'U':>4} {'NA':>4} {'V%':>6} {'95% CI':>14}")
    print("-" * 76)

    out = ["# Audit summary\n"]
    out.append(f"_Audited: {len(audited)} of 25 sampled edges_\n")
    out.append("## Per-edge-type results\n")
    out.append("| Edge type | n | Verified | Partial | Unverified | NA | Verified % | 95% CI |")
    out.append("|---|---:|---:|---:|---:|---:|---:|---:|")

    overall = Counter()
    for t in sorted(by_type):
        c = Counter(by_type[t])
        # NA excluded from denominator
        n_excl_na = sum(c[k] for k in ("VERIFIED", "PARTIAL", "UNVERIFIED"))
        v = c["VERIFIED"]
        p = c["PARTIAL"]
        u = c["UNVERIFIED"]
        na = c["NA"]
        rate = (v / n_excl_na * 100) if n_excl_na else 0.0
        lo, hi = wilson_ci(v, n_excl_na)
        print(f"{t:<22} {n_excl_na:>3} {v:>4} {p:>4} {u:>4} {na:>4} {rate:>5.0f}% [{lo:>3.0f}-{hi:>3.0f}]%")
        out.append(f"| {t} | {n_excl_na} | {v} | {p} | {u} | {na} | {rate:.0f}% | {lo:.0f}–{hi:.0f}% |")
        overall.update(by_type[t])

    n_all = sum(overall[k] for k in ("VERIFIED", "PARTIAL", "UNVERIFIED"))
    v_all = overall["VERIFIED"]
    rate_all = v_all / n_all * 100 if n_all else 0
    lo_all, hi_all = wilson_ci(v_all, n_all)
    print("-" * 76)
    print(f"{'OVERALL':<22} {n_all:>3} {v_all:>4} {overall['PARTIAL']:>4} {overall['UNVERIFIED']:>4} {overall['NA']:>4} {rate_all:>5.0f}% [{lo_all:>3.0f}-{hi_all:>3.0f}]%")
    out.append(f"| **OVERALL** | **{n_all}** | **{v_all}** | **{overall['PARTIAL']}** | **{overall['UNVERIFIED']}** | **{overall['NA']}** | **{rate_all:.0f}%** | **{lo_all:.0f}–{hi_all:.0f}%** |")

    out.append("\n## Draft paragraph for §3.3\n")
    out.append(
        f"To assess data quality beyond automated provenance, we manually audited a stratified random sample of "
        f"{len(audited) + overall['NA'] - overall['NA']} edges (≈6 per edge type) drawn from the four primary "
        f"edge types of the cardiometabolic KG. Each edge was verified against its source reference: PubMed "
        f"abstracts for SnpToPhenotype, MicrobeToNutrient, and MicrobeToGene edges; USDA FoodData Central "
        f"entries for FoodToNutrient edges. An edge was classified as VERIFIED if the source explicitly stated "
        f"the encoded relationship between source and target entities; PARTIAL if both entities were referenced "
        f"in the source but the relationship was not stated in the abstract (typically described in supplementary "
        f"figures or full-text tables); UNVERIFIED if the source did not support the relationship; "
        f"and NA if the source was inaccessible. Of {n_all} evaluable edges, "
        f"{v_all} ({rate_all:.0f}%, 95% CI [{lo_all:.0f}, {hi_all:.0f}]%) were classified VERIFIED, "
        f"{overall['PARTIAL']} ({100*overall['PARTIAL']/n_all:.0f}%) PARTIAL, and "
        f"{overall['UNVERIFIED']} ({100*overall['UNVERIFIED']/n_all:.0f}%) UNVERIFIED. "
        f"Per-edge-type rates are reported in Table 2."
    )

    OUTPUT.write_text("\n".join(out))
    print(f"\nReport written to {OUTPUT}")


if __name__ == "__main__":
    main()
