"""Build the cardiometabolic KG using all available adapters."""
from biocypher import BioCypher
from adapters.gwas_adapter import GWASAdapter

bc = BioCypher(
    biocypher_config_path="config/biocypher_config.yaml",
    schema_config_path="config/schema_config.yaml",
)

print("Running GWAS adapter...")
gwas = GWASAdapter()
print(f"  Stats: {gwas.stats()}")

print("Writing nodes...")
bc.write_nodes(gwas.get_nodes())

print("Writing edges...")
bc.write_edges(gwas.get_edges())

bc.write_import_call()
bc.summary()
print("\n✓ Build complete.")
