"""
GWAS Catalog adapter for cardiometabolic KG.

Filters the full GWAS Catalog to cardiometabolic traits and yields
BioCypher nodes (SNPs, Genes, Phenotypes) and edges (SNP->Gene, SNP->Phenotype).
"""
import csv
import re

# Cardiometabolic trait keywords — substring match on the DISEASE/TRAIT column
CARDIOMETABOLIC_KEYWORDS = [
    "type 2 diabetes", "type ii diabetes", "t2d",
    "fasting glucose", "glycated hemoglobin", "hba1c", "insulin resistance",
    "body mass index", "bmi", "obesity",
    "waist-hip ratio", "waist circumference", "adiposity",
    "ldl cholesterol", "hdl cholesterol", "triglyceride", "total cholesterol",
    "coronary artery disease", "coronary heart disease",
    "myocardial infarction", "cardiovascular disease",
    "hypertension", "blood pressure",
    "metabolic syndrome",
]

# Map each keyword to a canonical MONDO phenotype
KEYWORD_TO_MONDO = {
    "type 2 diabetes": ("MONDO:0005148", "type 2 diabetes mellitus"),
    "type ii diabetes": ("MONDO:0005148", "type 2 diabetes mellitus"),
    "t2d": ("MONDO:0005148", "type 2 diabetes mellitus"),
    "fasting glucose": ("MONDO:0024355", "hyperglycemia"),
    "glycated hemoglobin": ("MONDO:0024355", "hyperglycemia"),
    "hba1c": ("MONDO:0024355", "hyperglycemia"),
    "insulin resistance": ("MONDO:0002909", "insulin resistance"),
    "body mass index": ("MONDO:0011122", "obesity disorder"),
    "bmi": ("MONDO:0011122", "obesity disorder"),
    "obesity": ("MONDO:0011122", "obesity disorder"),
    "waist-hip ratio": ("MONDO:0011122", "obesity disorder"),
    "waist circumference": ("MONDO:0011122", "obesity disorder"),
    "adiposity": ("MONDO:0011122", "obesity disorder"),
    "ldl cholesterol": ("MONDO:0003699", "hypercholesterolemia"),
    "hdl cholesterol": ("MONDO:0003699", "hypercholesterolemia"),
    "total cholesterol": ("MONDO:0003699", "hypercholesterolemia"),
    "triglyceride": ("MONDO:0004790", "hypertriglyceridemia"),
    "coronary artery disease": ("MONDO:0005010", "coronary artery disease"),
    "coronary heart disease": ("MONDO:0005010", "coronary artery disease"),
    "myocardial infarction": ("MONDO:0005068", "myocardial infarction"),
    "cardiovascular disease": ("MONDO:0004995", "cardiovascular disorder"),
    "hypertension": ("MONDO:0005044", "hypertensive disorder"),
    "blood pressure": ("MONDO:0005044", "hypertensive disorder"),
    "metabolic syndrome": ("MONDO:0005137", "metabolic syndrome"),
}


class GWASAdapter:
    def __init__(self, tsv_path="data/raw/gwas/gwas_catalog.tsv",
                 pvalue_cutoff=5e-8):
        self.tsv_path = tsv_path
        self.pvalue_cutoff = pvalue_cutoff
        self._snps = {}
        self._genes = {}
        self._phenotypes = {}
        self._snp_gene_edges = []
        self._snp_phenotype_edges = []
        self._parse()

    def _match_keyword(self, trait_text):
        t = trait_text.lower()
        for kw in CARDIOMETABOLIC_KEYWORDS:
            if kw in t:
                return KEYWORD_TO_MONDO[kw]
        return None

    def _parse(self):
        seen_sp, seen_sg = set(), set()
        with open(self.tsv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                trait = row.get("DISEASE/TRAIT", "").strip()
                rsid = row.get("SNPS", "").strip()
                gene_symbols = row.get("REPORTED GENE(S)", "").strip()
                chrom = row.get("CHR_ID", "").strip()
                pos = row.get("CHR_POS", "").strip()
                risk_allele = row.get("STRONGEST SNP-RISK ALLELE", "").strip()
                pvalue_str = row.get("P-VALUE", "").strip()
                or_beta = row.get("OR or BETA", "").strip()
                pmid = row.get("PUBMEDID", "").strip()

                if not rsid.startswith("rs"):
                    continue
                if any(sep in rsid for sep in [";", ",", " x ", " X "]):
                    continue

                phen = self._match_keyword(trait)
                if not phen:
                    continue

                try:
                    pvalue = float(pvalue_str) if pvalue_str else 1.0
                except ValueError:
                    pvalue = 1.0
                if pvalue > self.pvalue_cutoff:
                    continue

                m = re.search(r"-([ACGT?])", risk_allele)
                allele = m.group(1) if m else "?"

                try:
                    effect = float(or_beta) if or_beta else None
                except ValueError:
                    effect = None

                # SNP node
                if rsid not in self._snps:
                    self._snps[rsid] = {
                        "chromosome": chrom,
                        "position": int(pos) if pos.isdigit() else 0,
                        "risk_allele": allele,
                    }

                # Phenotype node
                mondo_id, mondo_name = phen
                if mondo_id not in self._phenotypes:
                    self._phenotypes[mondo_id] = {
                        "name": mondo_name,
                        "category": "cardiometabolic",
                    }

                # SNP -> Phenotype edge
                k = (rsid, mondo_id)
                if k not in seen_sp:
                    seen_sp.add(k)
                    props = {"p_value": pvalue, "pmid": pmid}
                    if effect is not None:
                        props["effect_size"] = effect
                    self._snp_phenotype_edges.append((rsid, mondo_id, props))

                # Gene nodes + SNP -> Gene edges
                if gene_symbols and gene_symbols not in ("NR", "intergenic", "-"):
                    for sym in re.split(r"[,;]", gene_symbols):
                        sym = sym.strip()
                        if not sym or sym in ("NR", "intergenic", "-"):
                            continue
                        gene_id = f"HGNC:{sym}"
                        if gene_id not in self._genes:
                            self._genes[gene_id] = {"symbol": sym}
                        kg = (rsid, gene_id)
                        if kg not in seen_sg:
                            seen_sg.add(kg)
                            self._snp_gene_edges.append((rsid, gene_id, {}))

    def get_nodes(self):
        for rsid, props in self._snps.items():
            yield (rsid, "snp", props)
        for gene_id, props in self._genes.items():
            yield (gene_id, "gene", props)
        for mondo_id, props in self._phenotypes.items():
            yield (mondo_id, "phenotype", props)

    def get_edges(self):
        for i, (s, t, p) in enumerate(self._snp_gene_edges):
            yield (f"sg_{i}", s, t, "snp_to_gene", p)
        for i, (s, t, p) in enumerate(self._snp_phenotype_edges):
            yield (f"sp_{i}", s, t, "snp_to_phenotype", p)

    def stats(self):
        return {
            "snps": len(self._snps),
            "genes": len(self._genes),
            "phenotypes": len(self._phenotypes),
            "snp_gene_edges": len(self._snp_gene_edges),
            "snp_phenotype_edges": len(self._snp_phenotype_edges),
        }
