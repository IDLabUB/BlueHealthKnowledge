#!/usr/bin/env python3
"""
Analyze BlueHealthKnowledge counts for BOTH categories:
- counts_blue_health_activities.p
- counts_blue_health_exposure_metrics.p

Per a cada categoria:
- Drop d'ítems de baixa freqüència (segur)
- Normalització (dim='A')
- Export CSV de la matriu de scores
- Export JSON de top associacions A->B (un fitxer per terme A)
- Export JSON de top associacions B->A (un sol fitxer)
Les sortides van a subcarpetes pròpies: counts/summary/<cat>/ i counts/assocs/<cat>/
"""

from pathlib import Path
import re, json, pickle
import numpy as np
import pandas as pd
from lisc.utils import load_object

# --- Config ---
REPO_ROOT = Path(__file__).resolve().parent.parent
CATEGORIES = [
    ("activities",         "counts_blue_health_activities"),
    ("exposure_metrics",   "counts_blue_health_exposure_metrics"),
]
N_TERMS = 3
N_DROP  = 100
# --------------

def _slug(s: str) -> str:
    s = re.sub(r"[^\w\s\-\.]", "_", s)
    s = re.sub(r"\s+", "_", s).strip("_")
    return s[:200]

def _find_counts_path(base_name: str) -> Path:
    """Localitza el .p per base_name en ubicacions típiques i, si cal, fa cerca global."""
    candidates = [
        REPO_ROOT / "counts"      / f"{base_name}.p",   # esquema nou
        REPO_ROOT / "data" / "counts" / f"{base_name}.p",
        REPO_ROOT / "data"        / f"{base_name}.p",   # legacy alternatiu
    ]
    for p in candidates:
        if p.exists():
            return p
    # darrer recurs: cerca qualsevol counts_*.p i filtra pel base_name
    found = list(REPO_ROOT.rglob(f"{base_name}.p"))
    if found:
        return found[0]
    raise FileNotFoundError(
        f"No s’ha trobat {base_name}.p. Genera’l amb: python scripts/collect_counts.py"
    )

def _load_counts_safe(p: Path):
    """Carrega Counts des de p amb compatibilitat: lisc (name+directory) -> pickle fallback."""
    # 1) lisc (nom + directori)
    try:
        return load_object(p.stem, directory=str(p.parent))
    except Exception as e1:
        print(f"[warn] lisc.load_object va fallar per {p.name}: {e1}")
        # 2) pickle pur
        try:
            with open(p, "rb") as f:
                obj = pickle.load(f)
            print("[info] Carregat via pickle fallback:", p.name)
            return obj
        except Exception as e2:
            raise RuntimeError(f"No s’ha pogut carregar {p}: {e2}")

def _analyze_one(category_label: str, base_name: str):
    print(f"\n=== ANALYZING: {category_label} ({base_name}) ===")
    counts_path = _find_counts_path(base_name)
    print("Usant fitxer:", counts_path.resolve())

    counts = _load_counts_safe(counts_path)

    # Drop segur (limitem N_DROP segons mides)
    try:
        nA, nB = counts.counts.shape
        n_drop = min(N_DROP, max(nA - 1, 0), max(nB - 1, 0))
        if n_drop > 0:
            counts.drop_data(n_drop)
    except Exception as e:
        print(f"[warn] drop_data omès: {e}")

    counts.compute_score('normalize', dim='A')

    A_labels = list(counts.terms['A'].labels)
    B_labels = list(counts.terms['B'].labels)
    score    = np.array(counts.score, copy=False)

    # Subcarpetes específiques per categoria
    summary_dir = counts_path.parent / "summary" / category_label
    assocs_dir  = counts_path.parent / "assocs"  / category_label
    summary_dir.mkdir(parents=True, exist_ok=True)
    assocs_dir.mkdir(parents=True, exist_ok=True)

    # CSV de scores
    csv_name = "blue_health_activity_scores.csv" if category_label == "activities" \
               else "blue_health_exposure_scores.csv"
    df = pd.DataFrame(score, index=A_labels, columns=B_labels)
    csv_path = summary_dir / csv_name
    df.to_csv(csv_path)
    print("Scores ->", csv_path.resolve())
    print("\nSummary stats:\n", df.describe())

    # Top A->B (un JSON per terme A, dins carpeta de la categoria)
    for i, a_lab in enumerate(A_labels):
        order = np.argsort(score[i, :])[::-1][:N_TERMS]
        top_b = [B_labels[j] for j in order]
        with open(summary_dir / f"{_slug(a_lab)}.json", "w", encoding="utf-8") as f:
            json.dump({"top_assocs": top_b}, f, ensure_ascii=False)

    # Top B->A (un únic JSON per la categoria)
    assocs = {}
    for j, b_lab in enumerate(B_labels):
        order = np.argsort(score[:, j])[::-1][:N_TERMS]
        assocs[b_lab] = [A_labels[i] for i in order]
    with open(assocs_dir / "associations.json", "w", encoding="utf-8") as f:
        json.dump(assocs, f, ensure_ascii=False)

def main():
    print("\n\n ANALYZING COUNTS DATA (activities + exposure) \n")
    for cat_label, base in CATEGORIES:
        _analyze_one(cat_label, base)
    print("\n\n FINISHED ANALYZING BOTH CATEGORIES \n")

if __name__ == "__main__":
    main()
