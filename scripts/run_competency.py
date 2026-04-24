"""
Run all competency queries. Prints to console AND writes a structured
Markdown report suitable for the paper's supplementary material.
"""
import os
import glob
import time
import json
from datetime import datetime
from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "password456"
QUERY_DIR = "queries/competency"
REPORT_PATH = "queries/competency/results.md"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))


def load_query(path):
    with open(path) as f:
        lines = f.readlines()
    question = ""
    if lines and lines[0].strip().startswith("//"):
        question = lines[0].lstrip("/").strip()
    body = "\n".join(l for l in lines if not l.strip().startswith("//"))
    return question, body.strip().rstrip(";")


def run_one(session, cypher):
    start = time.time()
    result = session.run(cypher)
    rows = [dict(r) for r in result]
    elapsed_ms = (time.time() - start) * 1000
    return rows, elapsed_ms


def compact(value, width=80):
    s = str(value)
    return s if len(s) <= width else s[: width - 3] + "..."


def run_all():
    files = sorted(glob.glob(f"{QUERY_DIR}/*.cypher"))
    print(f"Running {len(files)} competency queries\n" + "=" * 80)

    report = []
    report.append(f"# Competency Question Results\n")
    report.append(f"_Generated: {datetime.now().isoformat()}_  ")
    report.append(f"_KG: Neo4j at {NEO4J_URI}_\n")

    summary_rows = []

    with driver.session() as session:
        for path in files:
            name = os.path.basename(path).replace(".cypher", "")
            question, cypher = load_query(path)
            try:
                rows, elapsed = run_one(session, cypher)
                status = "PASS" if rows else "EMPTY"
                print(f"\n### {name} [{status}]")
                print(f"Q: {question}")
                print(f"Result: {len(rows)} rows in {elapsed:.1f} ms")
                for r in rows[:3]:
                    print(f"   {compact(r, 100)}")
                if len(rows) > 3:
                    print(f"   ... ({len(rows) - 3} more rows)")

                # Markdown report
                report.append(f"\n## {name}  `[{status}]`")
                report.append(f"**Question:** {question}\n")
                report.append(f"**Rows:** {len(rows)} · **Time:** {elapsed:.1f} ms\n")
                report.append("```cypher")
                report.append(cypher)
                report.append("```")
                if rows:
                    report.append(f"\n**Example rows (first 5):**\n")
                    report.append("```json")
                    for r in rows[:5]:
                        report.append(json.dumps(r, default=str))
                    report.append("```")
                    if len(rows) > 5:
                        report.append(f"\n_({len(rows) - 5} additional rows not shown)_")
                else:
                    report.append("\n_No rows returned._")

                summary_rows.append((name, status, len(rows), f"{elapsed:.1f}"))
            except Exception as e:
                print(f"\n### {name} [ERROR]")
                print(f"Q: {question}")
                print(f"ERROR: {e}")
                report.append(f"\n## {name}  `[ERROR]`")
                report.append(f"**Question:** {question}\n")
                report.append(f"```")
                report.append(str(e))
                report.append("```")
                summary_rows.append((name, "ERROR", 0, "-"))

    driver.close()

    # summary table at top (append, then move to top)
    summary = ["\n## Summary\n",
               "| Query | Status | Rows | Time (ms) |",
               "|---|---|---|---|"]
    for name, status, n, t in summary_rows:
        summary.append(f"| {name} | {status} | {n} | {t} |")
    # write: header, summary, detail
    with open(REPORT_PATH, "w") as f:
        f.write("\n".join(report[:3]))
        f.write("\n".join(summary))
        f.write("\n\n---\n")
        f.write("\n".join(report[3:]))

    print("\n" + "=" * 80)
    print(f"Done. Report written to {REPORT_PATH}")


if __name__ == "__main__":
    run_all()
