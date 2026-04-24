"""
Load BioCypher output CSVs into Neo4j.
Handles multi-part files (part000, part001, ...) from multiple adapters.
"""
import os
import csv
import glob
from collections import defaultdict
from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "password456"
CSV_DIR = "data/processed/biocypher-out"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))


def clean(val):
    if isinstance(val, str) and len(val) >= 2 and val.startswith("'") and val.endswith("'"):
        return val[1:-1]
    return val


def read_header(path):
    with open(path, newline="") as f:
        row = next(csv.reader(f, delimiter=";"))
    parsed = []
    for cell in row:
        if ":" in cell:
            name, typ = cell.split(":", 1)
        else:
            name, typ = cell, ""
        parsed.append((name.strip(), typ.strip()))
    return parsed


def read_data(path):
    with open(path, newline="") as f:
        return [row for row in csv.reader(f, delimiter=";") if row]


def is_edge_base(base):
    header_path = os.path.join(CSV_DIR, f"{base}-header.csv")
    if not os.path.exists(header_path):
        return False
    types = [t for _, t in read_header(header_path)]
    return "START_ID" in types and "END_ID" in types


def convert(val, typ):
    val = clean(val)
    if val == "":
        return None
    if typ == "int" or typ == "long":
        try:
            return int(val)
        except ValueError:
            return val
    if typ in ("float", "double"):
        try:
            return float(val)
        except ValueError:
            return val
    return val


def discover_bases():
    """Find all unique node/edge type bases (e.g. 'Nutrient', 'SnpToGene')."""
    all_parts = glob.glob(f"{CSV_DIR}/*-part*.csv")
    bases = set()
    for p in all_parts:
        base = os.path.basename(p).split("-part")[0]
        bases.add(base)
    return sorted(bases)


def collect_parts(base):
    """Return all part files for a given base, sorted."""
    pattern = f"{CSV_DIR}/{base}-part*.csv"
    return sorted(glob.glob(pattern))


def load_nodes(session):
    for base in discover_bases():
        if is_edge_base(base):
            continue
        header_path = os.path.join(CSV_DIR, f"{base}-header.csv")
        if not os.path.exists(header_path):
            continue
        headers = read_header(header_path)

        id_idx = next((i for i, (_, t) in enumerate(headers) if t == "ID"), None)
        if id_idx is None:
            continue

        all_rows = []
        for data_path in collect_parts(base):
            for row in read_data(data_path):
                props = {}
                for i, (name, typ) in enumerate(headers):
                    if i >= len(row) or typ == "LABEL":
                        continue
                    key = "id" if typ == "ID" else (name if name else typ)
                    value = convert(row[i], typ)
                    if value is not None:
                        props[key] = value
                all_rows.append(props)

        if not all_rows:
            continue

        # Deduplicate by id, preferring the last occurrence
        by_id = {r["id"]: r for r in all_rows if "id" in r}
        dedup_rows = list(by_id.values())

        query = f"UNWIND $rows AS row MERGE (n:{base} {{id: row.id}}) SET n += row"
        session.run(query, rows=dedup_rows)
        print(f"  {base}: {len(dedup_rows)} nodes")


def load_edges(session):
    for base in discover_bases():
        if not is_edge_base(base):
            continue
        header_path = os.path.join(CSV_DIR, f"{base}-header.csv")
        headers = read_header(header_path)
        src_idx = next(i for i, (_, t) in enumerate(headers) if t == "START_ID")
        tgt_idx = next(i for i, (_, t) in enumerate(headers) if t == "END_ID")
        type_idx = next((i for i, (_, t) in enumerate(headers) if t == "TYPE"), None)

        all_rows = []
        for data_path in collect_parts(base):
            for row in read_data(data_path):
                props = {}
                for i, (name, typ) in enumerate(headers):
                    if i >= len(row) or i in (src_idx, tgt_idx, type_idx) or typ == "LABEL":
                        continue
                    value = convert(row[i], typ)
                    if name and value is not None:
                        props[name] = value
                all_rows.append({
                    "_from": clean(row[src_idx]),
                    "_to": clean(row[tgt_idx]),
                    "props": props,
                })

        if not all_rows:
            continue

        query = (
            "UNWIND $rows AS row "
            "MATCH (a {id: row._from}), (b {id: row._to}) "
            f"CREATE (a)-[r:{base}]->(b) SET r = row.props"
        )
        result = session.run(query, rows=all_rows)
        created = result.consume().counters.relationships_created
        print(f"  {base}: {created} edges (from {len(all_rows)} rows)")


def main():
    with driver.session() as session:
        print("Clearing database...")
        session.run("MATCH (n) DETACH DELETE n")

        print("Loading nodes...")
        load_nodes(session)

        print("Loading edges...")
        load_edges(session)

        n = session.run("MATCH (n) RETURN count(n) AS c").single()["c"]
        e = session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
        print(f"\nTotal nodes in Neo4j: {n}")
        print(f"Total edges in Neo4j: {e}")

    driver.close()
    print("\n✓ Load complete.")


if __name__ == "__main__":
    main()
