"""
Pre-select 25 rows for careful audit from the existing 200-row sample.
Stratified across edge types (~6 per type), with a fixed random seed so the
selection is reproducible and citable in the paper.

Strategy per edge type:
  - 1 well-known / "easy" row (e.g. famous SNP, common metabolite)
  - 1 obscure / "hard" row
  - 4-5 random rows in between

The point: a sample that's diverse but balanced.
"""
import csv
import random
from pathlib import Path

random.seed(42)

INPUT = Path("audit/edge_sample.tsv")
OUTPUT = Path("audit/edge_sample_25.tsv")

# Per-edge-type targets
TARGETS = {
    "SnpToPhenotype": 7,
    "FoodToNutrient": 6,
    "MicrobeToNutrient": 6,
    "MicrobeToGene": 6,
}

# "Easy" hints — names/IDs that should bias toward well-known examples
EASY_HINTS = {
    "SnpToPhenotype": ["rs7903146", "rs9939609", "rs1801282", "rs429358",
                       "rs10757274", "rs599839", "rs11591147"],
    "FoodToNutrient": ["strawber", "salmon", "almond", "avocado", "spinach",
                       "broccoli", "blueber", "oat", "lentil", "kale"],
    "MicrobeToNutrient": ["Akkermansia", "Faecalibacterium", "Bifidobacterium",
                          "Lactobacillus", "Bacteroides", "Clostridium",
                          "Christensenella"],
    "MicrobeToGene": ["TLR4", "NFKB1", "IL6", "IL10", "MUC2", "TJP",
                      "TNF", "IL1B", "FOXP3"],
}


def has_hint(row, hints):
    """True if any hint substring appears in source_name or target_name/symbol."""
    blob = " ".join([
        row.get("source_name", "") or "",
        row.get("target_name", "") or "",
        row.get("target_symbol", "") or "",
        row.get("source_id", "") or "",
    ]).lower()
    return any(h.lower() in blob for h in hints)


def select():
    rows = list(csv.DictReader(open(INPUT), delimiter="\t"))
    print(f"Loaded {len(rows)} rows from {INPUT}\n")

    # Reset all verdicts so user re-audits cleanly
    for r in rows:
        r["verdict"] = ""
        r["audit_notes"] = ""

    # Group rows by edge type
    by_type = {}
    for r in rows:
        by_type.setdefault(r["edge_type"], []).append(r)

    selected = []
    for edge_type, target_count in TARGETS.items():
        candidates = by_type.get(edge_type, [])
        random.shuffle(candidates)

        easy = [r for r in candidates if has_hint(r, EASY_HINTS.get(edge_type, []))]
        rest = [r for r in candidates if not has_hint(r, EASY_HINTS.get(edge_type, []))]

        # 1-2 "easy" rows + the rest random
        n_easy = min(2, len(easy))
        picked = easy[:n_easy] + rest[: target_count - n_easy]
        # If still short (very small candidate pool), take whatever's left
        if len(picked) < target_count:
            picked.extend(easy[n_easy : n_easy + (target_count - len(picked))])
        picked = picked[:target_count]

        print(f"  {edge_type}: {len(picked)} selected")
        for p in picked:
            tgt = (p.get("target_name") or p.get("target_symbol") or "?").strip().strip("'")
            src = (p.get("source_name") or p.get("source_id") or "?").strip().strip("'")
            pmid = (p.get("pmid") or "—").strip().strip("'")
            print(f"      {src[:40]:<40s} -> {tgt[:35]:<35s} (PMID {pmid})")
        selected.extend(picked)
        print()

    # Write the subset
    fieldnames = list(rows[0].keys()) if rows else []
    with open(OUTPUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        w.writeheader()
        w.writerows(selected)

    print(f"\n✓ Wrote {len(selected)} rows to {OUTPUT}")
    print(f"  Open in Excel and fill the 'verdict' column for each row.")


if __name__ == "__main__":
    select()
