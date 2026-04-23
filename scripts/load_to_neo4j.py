"""
Load BioCypher output CSVs into Neo4j.
- Uses the `id` column (BioCypher 0.8 default).
- Strips BioCypher's single-quote wrapping from string values.
"""
import os
import csv
import glob
from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "password456"   # your actual password
CSV_DIR = "data/processed/biocypher-out"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))


def clean(val):
    """Strip BioCypher's single-quote wrapping: \"'rs7903146'\" -> 'rs7903146'."""
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


def is_edge_file(filename):
    base = os.path.basename(filename).split("-part")[0]
    header_path = os.path.join(CSV_DIR, f"{base}-header.csv")
    if not os.path.exists(header_path):
        return False
    types = [t for _, t in read_header(header_path)]
    return "START_ID" in types and "END_ID" in types


def convert(val, typ):
    """Convert value based on BioCypher column type."""
    val = clean(val)
    if val == "":
        return None
    if typ == "int":
        try:
            return int(val)
        except ValueError:
            return val
    if typ == "float" or typ == "double":
        try:
            return float(val)
        except ValueError:
            return val
    return val


def load_nodes(session):
    node_files = [f for f in glob.glob(f"{CSV_DIR}/*-part000.csv") if not is_edge_file(f)]
    total = 0
    for data_path in sorted(node_files):
        base = os.path.basename(data_path).split("-part")[0]
        header_path = os.path.join(CSV_DIR, f"{base}-header.csv")
        headers = read_header(header_path)
        data = read_data(data_path)

        id_idx = next((i for i, (_, t) in enumerate(headers) if t == "ID"), None)
        if id_idx is None:
            print(f"  {base}: SKIPPED (no :ID column)")
            continue

        rows = []
        for row in data:
            props = {}
            for i, (name, typ) in enumerate(headers):
                if i >= len(row):
                    continue
                if typ == "LABEL":
                    continue
                key = "id" if typ == "ID" else (name if name else typ)
                value = convert(row[i], typ)
                if value is not None:
                    props[key] = value
            rows.append(props)

        query = f"UNWIND $rows AS row CREATE (n:{base}) SET n = row"
        session.run(query, rows=rows)
        print(f"  {base}: {len(rows)} nodes")
        total += len(rows)
    return total


def load_edges(session):
    edge_files = [f for f in glob.glob(f"{CSV_DIR}/*-part000.csv") if is_edge_file(f)]
    total = 0
    for data_path in sorted(edge_files):
        base = os.path.basename(data_path).split("-part")[0]
        header_path = os.path.join(CSV_DIR, f"{base}-header.csv")
        headers = read_header(header_path)
        data = read_data(data_path)

        src_idx = next(i for i, (_, t) in enumerate(headers) if t == "START_ID")
        tgt_idx = next(i for i, (_, t) in enumerate(headers) if t == "END_ID")
        type_idx = next((i for i, (_, t) in enumerate(headers) if t == "TYPE"), None)

        rows = []
        for row in data:
            props = {}
            for i, (name, typ) in enumerate(headers):
                if i >= len(row) or i in (src_idx, tgt_idx, type_idx) or typ == "LABEL":
                    continue
                value = convert(row[i], typ)
                if name and value is not None:
                    props[name] = value
            rows.append({
                "_from": clean(row[src_idx]),
                "_to": clean(row[tgt_idx]),
                "props": props,
            })

        query = (
            "UNWIND $rows AS row "
            "MATCH (a {id: row._from}), (b {id: row._to}) "
            f"CREATE (a)-[r:{base}]->(b) SET r = row.props"
        )
        result = session.run(query, rows=rows)
        created = result.consume().counters.relationships_created
        print(f"  {base}: {created} edges (from {len(rows)} rows)")
        total += created
    return total


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
