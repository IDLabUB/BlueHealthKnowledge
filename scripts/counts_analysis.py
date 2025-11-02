#!/usr/bin/env python3
"""
Analyze BlueHealthKnowledge counts.

- Autodetecta *counts_*.p (per defecte: counts_blue_health_activities.p)
- Drop ítems de baixa freqüència (segur)
- Normalitza (dim='A')
- Exporta CSV de scores i JSON de top associacions (A->B i B->A)
"""

from pathlib import Path
import os, json, re, pickle
import numpy as np
import pandas as pd
from lisc.utils import load_object

# --- Config ---
REPO_ROOT = Path(__file__).resolve().parent.parent
COG_BASE  = "counts_blue_health_activities"  # canvia-ho a "..._exposure_metrics" si cal
N_TERMS   = 3
N_DROP    = 100
# --------------

def _slug(s: str) -> str:
    s = re.sub(r"[^\w\s\-\.]", "_", s)
    s = re.sub(r"\s+", "_", s).strip("_")
    return s[:200]

def _resolve_counts_path() -> Path:
    """Troba el fitxer de counts i retorna el Path exacte."""
    candidates = [
        REPO_ROOT / "counts" / f"{COG_BASE}.p",
        REPO_ROOT / "data" / "counts" / f"{COG_BASE}.p",
        REPO_ROOT / "data" / f"{COG_BASE}.p",
    ]
    for p in candidates:
        if p.exists():
            return p
    found = sorted(REPO_ROOT.rglob("counts_*.p"))
    if found:
        print("[info] No s’ha trobat", f"{COG_BASE}.p", "però hi ha aquests fitxers:")
        for fp in found:
            try:
                print("  -", fp.relative_to(REPO_ROOT))
            except Exception:
                print("  -", fp)
        return found[0]
    raise FileNotFoundError("No s’ha trobat cap counts_*.p. Genera’ls amb: python scripts/collect_counts.py")

def _load_counts(counts_path: Path):
    """Carrega el Counts amb compatibilitat ampla (lisc o pickle)."""
    # 1) Intent estàndard lisc (name + directory)
    try:
        return load_object(counts_path.stem, directory=str(counts_path.parent))
    except Exception as e1:
        print(f"[warn] lisc.load_object va fallar: {e1}")
        # 2) Fallback a pickle pur pel path complet
        try:
            with open(counts_path, "rb") as f:
                obj = pickle.load(f)
            print("[info] Carregat via pickle fallback.")
            return obj
        except Exception as e2:
            raise RuntimeError(f"No s’ha pogut carregar {counts_path} ni amb lisc ni amb pickle: {e2}")

def main():
    print("\n\n ANALYZING COUNTS DATA \n")

    counts_path = _resolve_counts_path()
    print("Usant fitxer:", counts_path.resolve())

    counts = _load_counts(counts_path)

    # Preprocés segur
    try:
        nA, nB = counts.counts.shape
        n_drop = min(N_DROP, max(nA - 1, 0), max(nB - 1, 0))
        if n_drop > 0:
            counts.drop_data(n_drop)
    except Exception as e:
        print(f"[warn] drop_data skipped: {e}")

    counts.compute_score('normalize', dim='A')

    A_labels = list(counts.terms['A'].labels)
    B_labels = list(counts.terms['B'].labels)
    score    = np.array(counts.score, copy=False)

    out_dir    = counts_path.parent / "summary"
    assocs_dir = counts_path.parent / "assocs"
    out_dir.mkdir(parents=True, exist_ok=True)
    assocs_dir.mkdir(parents=True, exist_ok=True)

    # Export CSV amb scores normalitzats
    csv_name = "blue_health_activity_scores.csv" if "activities" in counts_path.name else "blue_health_exposure_scores.csv"
    df = pd.DataFrame(score, index=A_labels, columns=B_labels)
    csv_path = out_dir / csv_name
    df.to_csv(csv_path)
    print("Scores ->", csv_path.resolve())
    print("\nSummary stats:\n", df.describe())

    # Top A->B
    for i, a_lab in enumerate(A_labels):
        order = np.argsort(score[i, :])[::-1][:N_TERMS]
        top_b = [B_labels[j] for j in order]
        with open(out_dir / f"{_slug(a_lab)}.json", "w", encoding="utf-8") as f:
            json.dump({"top_assocs": top_b}, f, ensure_ascii=False)

    # Top B->A
    assocs = {}
    for j, b_lab in enumerate(B_labels):
        order = np.argsort(score[:, j])[::-1][:N_TERMS]
        assocs[b_lab] = [A_labels[i] for i in order]
    with open(assocs_dir / "associations.json", "w", encoding="utf-8") as f:
        json.dump(assocs, f, ensure_ascii=False)

    print("\n\n FINISHED ANALYZING COUNTS DATA \n")

if __name__ == "__main__":
    main()
