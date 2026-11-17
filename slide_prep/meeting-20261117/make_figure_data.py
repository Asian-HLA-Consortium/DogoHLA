#!/usr/bin/env python3
"""Write the small data tables used by slides.tex (pgfplots) from the stage result files.

Only group-level summary numbers are read and written; no donor rows or donor IDs.
Usage: python3 make_figure_data.py
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVID = ROOT.parent / "scientist" / "evidence"
DOSE = EVID / "dose-response-20261114" / "results" / "figure_ready_dose_response.tsv"
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)

rows = [r for r in csv.DictReader(DOSE.open(), delimiter="\t") if r["metric"] == "absent_exact_any"]
cell = {(r["group"], r["cell"]): r for r in rows}
steps = [("n0", 0), ("match_n05", 5), ("match_n10", 10), ("match_n20", 20), ("match_n40", 40)]
groups = ["ME", "EAS", "SAS"]

with (OUT / "dose_matched.dat").open("w") as f:
    f.write("n " + " ".join(groups) + "\n")
    for name, n in steps:
        f.write(f"{n} " + " ".join(cell[(g, name)]["pct"] for g in groups) + "\n")

with (OUT / "dose_nonasian40.dat").open("w") as f:
    f.write("n " + " ".join(groups) + "\n")
    f.write("40 " + " ".join(cell[(g, "x_NONASIAN_n40")]["pct"] for g in groups) + "\n")

with (OUT / "dose_check.txt").open("w") as f:
    for g in groups:
        for name, n in steps + [("x_NONASIAN_n40", 40)]:
            r = cell[(g, name)]
            f.write(f"{g}\t{name}\t{r['k']}/{r['n']}\t{r['pct']}%\tdrawn={r['mean_n_drawn']}\n")

# Thin-data numbers: real reads, arm A (IPD reference), rule "first listed allele".
# Copied from thin-data-20261114/REPORT.md tables (two-field accuracy; ambiguity share).
thin = [("full", 99.0, 0.8), ("1/2", 98.5, 2.4), ("1/4", 95.8, 10.5), ("1/8", 83.6, 31.2), ("1/16", 74.9, 50.8)]
with (OUT / "thin_real.dat").open("w") as f:
    f.write("i acc tie\n")
    for i, (_, acc, tie) in enumerate(thin):
        f.write(f"{i} {acc} {tie}\n")
print(open(OUT / "dose_check.txt").read())
