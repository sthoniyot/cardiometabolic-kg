"""
gutMGene adapter for cardiometabolic KG.

Reads the two literature-based association CSVs from gutMGene v2.0 and yields
Microbe nodes plus three edge types:
  - Microbe -> Nutrient (from the metabolite file)
  - Microbe -> Gene (from the host-gene file)
  - Microbe -> Phenotype (derived from DOID column, mapped to MONDO)

Also yields Nutrient and Gene nodes for IDs not already in the graph from
USDA / GWAS, so edges always land on valid nodes.

Filters:
  - human only (drop mouse rows)
  - causal associations only (drop correlational; can be relaxed)
  - non-empty source / target identifiers

PMID forward-fill:
  gutMGene's CSVs occasionally leave the PMID column blank when a row
  belongs to the same `Index` group as a preceding fully-annotated row
  (a manual-curation "fill-down" convention). This adapter forward-fills
  the PMID across rows that share the same Index value.

Edge deduplication:
  When the same (microbe, target) pair is reported in multiple papers,
  only one edge is yielded; subsequent occurrences are dropped (the first
  PMID wins).
"""
import csv
import os

GUTMGENE_DIR = "data/raw/gutmgene"
METAB_FILE = "Gut_Microbe-Microbial_Metabolite.csv"
GENE_FILE = "Gut_Microbe-Host-Gene.csv"

DOID_TO_MONDO = {
    "DOID:9352": "MONDO:0005148",
    "DOID:9351": "MONDO:0005148",
    "DOID:9970": "MONDO:0011122",
    "DOID:3083": "MONDO:0011122",
    "DOID:1287": "MONDO:0004995",
    "DOID:5844": "MONDO:0005068",
    "DOID:3393": "MONDO:0005010",
    "DOID:10763": "MONDO:0005044",
    "DOID:0080600": "MONDO:0005137",
    "DOID:14557": "MONDO:0003699",
    "DOID:2849": "MONDO:0004790",
    "DOID:1026": "MONDO:0024355",
    "DOID:9993": "MONDO:0024355",
    "DOID:0050117": "MONDO:0002909",
}


class GutMGeneAdapter:
    def __init__(self, gutmgene_dir=GUTMGENE_DIR,
                 human_only=True, causal_only=True):
        self.gutmgene_dir = gutmgene_dir
        self.human_only = human_only
        self.causal_only = causal_only
        self._microbes = {}
        self._extra_nutrients = {}
        self._extra_genes = {}
        self._microbe_nutrient_edges = []
        self._microbe_gene_edges = []
        self._microbe_phenotype_edges = set()
        self._seen_mn = set()
        self._seen_mg = set()
        self._parse()

    # ------------------------------------------------------------------
    # CSV reading with encoding fallback + PMID forward-fill
    # ------------------------------------------------------------------
    def _read_csv(self, filename):
        path = os.path.join(self.gutmgene_dir, filename)
        for encoding in ("utf-8", "latin-1"):
            try:
                with open(path, newline="", encoding=encoding) as f:
                    rows = list(csv.DictReader(f))
                self._forward_fill_pmid(rows)
                return rows
            except UnicodeDecodeError:
                continue
        raise RuntimeError(f"Could not decode {path}")

    @staticmethod
    def _forward_fill_pmid(rows):
        """
        gutMGene CSVs sometimes leave PMID blank for follow-up rows in the
        same Index group. We propagate the most recent non-empty PMID
        forward within the same Index value.

        Mutates rows in place.
        """
        last_pmid_by_index = {}
        for row in rows:
            idx = (row.get("Index") or "").strip()
            pmid = (row.get("PMID") or "").strip()
            if not idx:
                continue
            if pmid:
                last_pmid_by_index[idx] = pmid
            elif idx in last_pmid_by_index:
                row["PMID"] = last_pmid_by_index[idx]

    # ------------------------------------------------------------------
    # Filters and node helpers
    # ------------------------------------------------------------------
    def _passes_filters(self, row):
        if self.human_only and row.get("human/mouse", "").strip().lower() != "human":
            return False
        mode = row.get("Associative mode", "").strip().lower()
        if self.causal_only and "caus" not in mode:
            return False
        return True

    def _add_microbe(self, row):
        taxid = row.get("Gut Microbiota NCBI ID", "").strip()
        name = row.get("Gut Microbiota", "").strip()
        rank = row.get("Rank", "").strip()
        if not taxid or not name:
            return None
        node_id = f"NCBITaxon:{taxid}"
        if node_id not in self._microbes:
            self._microbes[node_id] = {"name": name, "rank": rank}
        return node_id

    def _add_nutrient(self, chebi_id, name):
        if chebi_id not in self._extra_nutrients:
            self._extra_nutrients[chebi_id] = {
                "name": name or chebi_id,
                "compound_class": "microbial_metabolite",
            }

    def _add_gene(self, symbol):
        if not symbol:
            return None
        gene_id = f"HGNC:{symbol}"
        if gene_id not in self._extra_genes:
            self._extra_genes[gene_id] = {"symbol": symbol}
        return gene_id

    def _add_phenotype_edge(self, microbe_id, doid, tier):
        doid = (doid or "").strip()
        if not doid or doid not in DOID_TO_MONDO:
            return
        mondo_id = DOID_TO_MONDO[doid]
        self._microbe_phenotype_edges.add((microbe_id, mondo_id, tier))

    # ------------------------------------------------------------------
    # File parsers
    # ------------------------------------------------------------------
    def _parse_metabolite_file(self):
        for row in self._read_csv(METAB_FILE):
            if not self._passes_filters(row):
                continue
            microbe_id = self._add_microbe(row)
            if not microbe_id:
                continue
            chebi = row.get("Metabolite ChEBI", "").strip()
            name = row.get("Metabolite", "").strip()
            if not chebi or not chebi.startswith("CHEBI:"):
                continue
            self._add_nutrient(chebi, name)
            pmid = row.get("PMID", "").strip()
            condition = row.get("Condition", "").strip()
            tier = row.get("Associative mode", "").strip()
            key = (microbe_id, chebi)
            if key in self._seen_mn:
                continue
            self._seen_mn.add(key)
            self._microbe_nutrient_edges.append((
                microbe_id, chebi,
                {"evidence_tier": tier, "pmid": pmid, "condition": condition},
            ))
            self._add_phenotype_edge(microbe_id, row.get("DOID", ""), tier)

    def _parse_gene_file(self):
        for row in self._read_csv(GENE_FILE):
            if not self._passes_filters(row):
                continue
            microbe_id = self._add_microbe(row)
            if not microbe_id:
                continue
            gene_symbol = row.get("Gene", "").strip()
            if not gene_symbol:
                continue
            gene_id = self._add_gene(gene_symbol)
            pmid = row.get("PMID", "").strip()
            tier = row.get("Associative mode", "").strip()
            key = (microbe_id, gene_id)
            if key in self._seen_mg:
                continue
            self._seen_mg.add(key)
            self._microbe_gene_edges.append((
                microbe_id, gene_id,
                {"evidence_tier": tier, "pmid": pmid},
            ))
            self._add_phenotype_edge(microbe_id, row.get("DOID", ""), tier)

    def _parse(self):
        self._parse_metabolite_file()
        self._parse_gene_file()

    # ------------------------------------------------------------------
    # BioCypher emit interface
    # ------------------------------------------------------------------
    def get_nodes(self):
        for microbe_id, props in self._microbes.items():
            yield (microbe_id, "microbe", props)
        for chebi_id, props in self._extra_nutrients.items():
            yield (chebi_id, "nutrient", props)
        for gene_id, props in self._extra_genes.items():
            yield (gene_id, "gene", props)

    def get_edges(self):
        for i, (s, t, p) in enumerate(self._microbe_nutrient_edges):
            yield (f"mn_{i}", s, t, "microbe_to_nutrient", p)
        for i, (s, t, p) in enumerate(self._microbe_gene_edges):
            yield (f"mg_{i}", s, t, "microbe_to_gene", p)
        for i, (s, t, tier) in enumerate(self._microbe_phenotype_edges):
            yield (f"mp_{i}", s, t, "microbe_to_phenotype",
                   {"evidence_tier": tier})

    def stats(self):
        # Count edges that have a non-empty PMID (after forward-fill)
        mn_pmid = sum(1 for (_, _, p) in self._microbe_nutrient_edges if p.get("pmid"))
        mg_pmid = sum(1 for (_, _, p) in self._microbe_gene_edges if p.get("pmid"))
        return {
            "microbes": len(self._microbes),
            "extra_nutrients": len(self._extra_nutrients),
            "extra_genes": len(self._extra_genes),
            "microbe_nutrient_edges": len(self._microbe_nutrient_edges),
            "microbe_nutrient_edges_with_pmid": mn_pmid,
            "microbe_gene_edges": len(self._microbe_gene_edges),
            "microbe_gene_edges_with_pmid": mg_pmid,
            "microbe_phenotype_edges": len(self._microbe_phenotype_edges),
        }
