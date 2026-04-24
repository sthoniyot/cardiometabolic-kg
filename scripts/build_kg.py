"""Build the cardiometabolic KG using all available adapters."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from biocypher import BioCypher
from adapters.gwas_adapter import GWASAdapter
from adapters.usda_adapter import USDAAdapter
from adapters.gutmgene_adapter import GutMGeneAdapter

bc = BioCypher(
    biocypher_config_path="config/biocypher_config.yaml",
    schema_config_path="config/schema_config.yaml",
)

print("Running GWAS adapter...")
gwas = GWASAdapter()
print(f"  Stats: {gwas.stats()}")

print("Running USDA adapter...")
usda = USDAAdapter()
print(f"  Stats: {usda.stats()}")

print("Running gutMGene adapter...")
gutmgene = GutMGeneAdapter()
print(f"  Stats: {gutmgene.stats()}")

print("Writing nodes...")
bc.write_nodes(gwas.get_nodes())
bc.write_nodes(usda.get_nodes())
bc.write_nodes(gutmgene.get_nodes())

print("Writing edges...")
bc.write_edges(gwas.get_edges())
bc.write_edges(usda.get_edges())
bc.write_edges(gutmgene.get_edges())

bc.write_import_call()
bc.summary()
print("\n✓ Build complete.")
