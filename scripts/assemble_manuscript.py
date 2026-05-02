"""
Assemble the cardiometabolic KG manuscript from per-section Markdown files
into a single document.

Outputs:
  - docs/paper/manuscript.md      (canonical merged Markdown)
  - docs/paper/manuscript.docx    (if pandoc is installed)

The script is deliberately strict about file presence: a missing section
fails loudly rather than producing a silently incomplete manuscript.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

PAPER_DIR = Path("docs/paper")
SECTIONS_DIR = PAPER_DIR / "sections"
OUT_MD = PAPER_DIR / "manuscript.md"
OUT_DOCX = PAPER_DIR / "manuscript.docx"

# ---------------------------------------------------------------
# Manuscript assembly order
# ---------------------------------------------------------------

# Front matter — written here directly so we don't depend on
# a separate file for boilerplate.
FRONT_MATTER = """\
# NuGeMi-KG: A FAIR tri-layer knowledge graph integrating nutrigenetics, gut microbiome, and food chemistry for cardiometabolic precision nutrition

**Sharath Thoniyot**¹, **Vijayakumar Balakrishnan**¹

¹ Department of Computer Science, Birla Institute of Technology and Science Pilani, Dubai Campus, United Arab Emirates

**Corresponding author:** Sharath Thoniyot (p20230010@dubai.bits-pilani.ac.in)

---

## Abstract

**Background.** Cardiometabolic diseases arise from the interplay of genetic susceptibility, gut microbiome activity, and dietary intake. Existing biomedical knowledge graphs cover these layers in isolation.

**Methods.** We constructed *NuGeMi-KG*, a tri-layer knowledge graph integrating cardiometabolic GWAS associations (GWAS Catalog), microbe–metabolite and microbe–host gene relationships (gutMGene v2.0), and food-composition data (USDA FoodData Central). The KG is implemented in BioCypher, aligned to the Biolink Model, and deployed in Neo4j.

**Results.** NuGeMi-KG contains 55,263 nodes and 85,308 edges across 8 node types and 9 edge types. We define 15 competency questions, of which 14 return biologically meaningful results. The KG supports five-hop cross-layer queries that surface novel nutrigenetic hypotheses (e.g. *Streptococcus salivarius* → PPARG → 45 cardiometabolic SNPs).

**Conclusion.** NuGeMi-KG is the first public KG that integrates all three layers under a single ontology-aligned schema and is openly queryable for hypothesis generation in precision nutrition.

**Keywords:** knowledge graph, cardiometabolic disease, nutrigenetics, gut microbiome, precision nutrition, Biolink, BioCypher, FAIR

---
"""

# (label_for_log, file_under_sections_dir, optional_extra_inserted_content)
SECTIONS = [
    ("§1 Background & Summary",       "1_background.md",        None),
    ("§2 Methods",                    "2_methods.md",           None),
    ("§3 Data Records",               "3_data_records.md",      "table2_artefacts.md"),
    ("§4 Results",                    "4_results.md",           "table4_audit.md"),
    ("§5 Discussion",                 "5_discussion.md",        None),
    ("§6 Conclusion",                 "6_conclusion.md",        None),
    ("§7 Code Availability",          "7_code_availability.md", None),
    ("Figure captions",               "figures.md",             None),
]


def read_required(path: Path) -> str:
    if not path.exists():
        sys.exit(f"ERROR: required section file missing: {path}")
    txt = path.read_text(encoding="utf-8").rstrip()
    if not txt:
        sys.exit(f"ERROR: section file is empty: {path}")
    return txt


def main():
    if not SECTIONS_DIR.exists():
        sys.exit(f"ERROR: sections directory not found: {SECTIONS_DIR}")

    parts = [FRONT_MATTER]

    for label, fname, extra_fname in SECTIONS:
        path = SECTIONS_DIR / fname
        print(f"  including: {label:<32}  {path}")
        parts.append(read_required(path))
        if extra_fname:
            extra_path = SECTIONS_DIR / extra_fname
            print(f"     +table:  {extra_fname}")
            parts.append(read_required(extra_path))

    # Tail material (acks, contributions, competing interests, references)
    tail = """\

---

## Acknowledgments

We thank the curators and developers of the GWAS Catalog (NHGRI–EBI), USDA
FoodData Central, gutMGene v2.0, the Biolink Model, and the BioCypher
framework.

## Author contributions

**S.T.**: conceptualisation, data curation, software, formal analysis,
visualisation, writing — original draft, writing — review and editing.
**V.B.**: supervision, conceptualisation, writing — review and editing.

## Competing interests

The author(s) declare no competing interests.

## Data availability

All data, code, and pre-built knowledge-graph artefacts are publicly
available under CC-BY-4.0; see §3 Data Records and §7 Code Availability for
URLs and DOIs.

## References

1. Sollis E, et al. The NHGRI-EBI GWAS Catalog: knowledge base and deposition resource. *Nucleic Acids Res*. 2023;51(D1):D977–D985. doi:10.1093/nar/gkac1010
2. McKillop KT, Fukagawa NK. USDA FoodData Central: methodology and data quality. *J Food Compos Anal*. 2019. doi:10.1016/j.jfca.2019.103289
3. Qi C, et al. gutMGene v2.0: an updated comprehensive database for target genes of gut microbes and microbial metabolites. *Nucleic Acids Res*. 2025;53(D1):D783–D788. doi:10.1093/nar/gkae1002
4. Chandak P, Huang K, Zitnik M. Building a knowledge graph to enable precision medicine. *Sci Data*. 2023;10:67. doi:10.1038/s41597-023-01960-3
5. Putman T, et al. The Monarch Initiative in 2024: an analytic platform integrating phenotypes, genes and diseases across species. *Nucleic Acids Res*. 2024;52(D1):D938–D949. doi:10.1093/nar/gkad1004
6. Unni DR, et al. Biolink Model: A universal schema for knowledge graphs in clinical, biomedical, and translational science. *Clin Transl Sci*. 2022;15(8):1848–1855. doi:10.1111/cts.13302
7. Lobentanzer S, et al. Democratizing knowledge representation with BioCypher. *Nat Biotechnol*. 2023;41:1056–1059. doi:10.1038/s41587-023-01848-y
8. Vasilevsky NA, et al. Mondo: Unifying diseases for the world, by the world. *medRxiv*. 2022. doi:10.1101/2022.04.13.22273750
"""

    parts.append(tail)

    final = "\n\n".join(parts) + "\n"
    OUT_MD.write_text(final, encoding="utf-8")
    word_count = len(final.split())
    print()
    print(f"  wrote: {OUT_MD}")
    print(f"  total words (incl. headers, tables, captions): {word_count}")

    # Try pandoc -> docx if available
    if shutil.which("pandoc"):
        print()
        print(f"  rendering: {OUT_DOCX}")
        try:
            subprocess.run(
                ["pandoc", str(OUT_MD), "-o", str(OUT_DOCX),
                 "--standalone", "--toc", "--toc-depth=2"],
                check=True,
            )
            size_kb = OUT_DOCX.stat().st_size // 1024
            print(f"  wrote: {OUT_DOCX}  ({size_kb} kB)")
        except subprocess.CalledProcessError as e:
            print(f"  pandoc failed (return code {e.returncode}); skipping docx")
    else:
        print()
        print("  pandoc not found; skipped docx rendering.")
        print("  to enable: sudo apt install -y pandoc")


if __name__ == "__main__":
    main()
