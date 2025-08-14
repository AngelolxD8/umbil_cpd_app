# storage.py
import csv
import os

CPD_FILE = "cpd_log.csv"
PDP_FILE = "pdp_goals.csv"

def load_cpd():
    if not os.path.exists(CPD_FILE):
        return []
    rows = []
    with open(CPD_FILE, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            # parse list-like tags
            tags = row.get("Tags", "")
            row["Tags"] = [t.strip() for t in tags.split("|") if t.strip()] if "|" in tags else eval(tags) if tags.startswith("[") else []
            rows.append(row)
    return rows

def save_cpd(entries):
    if not entries:
        with open(CPD_FILE, "w", newline="", encoding="utf-8") as f:
            f.write("")
        return
    keys = ["Timestamp", "Query", "Response", "Reflection", "Tags"]
    with open(CPD_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for e in entries:
            out = e.copy()
            out["Tags"] = "|".join(e.get("Tags", []))
            w.writerow(out)

def load_pdp():
    if not os.path.exists(PDP_FILE):
        return []
    rows = []
    with open(PDP_FILE, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        rows.extend(r)
    return rows

def save_pdp(goals):
    if not goals:
        with open(PDP_FILE, "w", newline="", encoding="utf-8") as f:
            f.write("")
        return
    keys = ["Topic", "Created"]
    with open(PDP_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for g in goals:
            w.writerow(g)
