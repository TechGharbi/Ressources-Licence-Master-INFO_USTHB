import os
import time
import csv
from memory_profiler import memory_usage

from solve_SUBSETSUM_dp import solve_SUBSETSUM_DP
from solve_SUBSETSUM import solve_subsetsum_backtracking_recursif
from verify_SUBSETSUM import verifier_solution

# Dossier du projet (racine SUBSETSUM)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Dossier contenant les datasets
DATA = os.path.join(BASE_DIR, "data")

# Dossier où on sauvegarde les résultats
RESULTS = os.path.join(BASE_DIR, "tests")

# Créer les dossiers s’ils n’existent pas
os.makedirs(DATA, exist_ok=True)
os.makedirs(RESULTS, exist_ok=True)


def readDataset(id):
    """Lit un dataset complet : S, T, V, TYPE"""

    with open(os.path.join(DATA, f"dataset_{id}_S.txt")) as f:
        S = list(map(int, f.read().split()))

    with open(os.path.join(DATA, f"dataset_{id}_T.txt")) as f:
        T = int(f.read())

    vPath = os.path.join(DATA, f"dataset_{id}_V.txt")
    if os.path.exists(vPath):
        with open(vPath) as f:
            V = list(map(int, f.read().split()))
    else:
        V = None

    typePath = os.path.join(DATA, f"dataset_{id}_TYPE.txt")
    if os.path.exists(typePath):
        with open(typePath) as f:
            dtype = f.read().strip()
    else:
        dtype = "unknown"

    return S, T, V, dtype


def runAlgo(algo, S, T):
    """Exécute un algorithme SUBSETSUM et mesure temps et mémoire"""

    start = time.time()
    mem = memory_usage((algo, (S, T)), max_iterations=1)
    end = time.time()

    found, solution = algo(S, T)

    timeMs = (end - start) * 1000
    memKb = max(mem) * 1024

    return found, solution, timeMs, memKb


def runVerify(S, V, T):
    """Mesure temps et mémoire pour la fonction verifier_solution"""
    
    start = time.time()
    mem = memory_usage((verifier_solution, (S, V, T)), max_iterations=1)
    end = time.time()

    valid = verifier_solution(S, V, T)

    timeMs = (end - start) * 1000
    memKb = max(mem) * 1024

    return valid, timeMs, memKb


def main():
    """
    Parcourt tous les datasets :
    - DP
    - Backtracking
    - Verify
    Mesure temps et mémoire
    Sauvegarde les résultats en CSV
    """

    files = os.listdir(DATA)
    ids = sorted(int(f.split("_")[1]) for f in files if f.endswith("_S.txt"))

    dpFile = os.path.join(RESULTS, "results_dp.csv")
    bfFile = os.path.join(RESULTS, "results_backtracking.csv")
    verifyFile = os.path.join(RESULTS, "results_verify.csv")

    with open(dpFile, "w", newline="") as dp, \
         open(bfFile, "w", newline="") as bf, \
         open(verifyFile, "w", newline="") as vf:

        dpWriter = csv.writer(dp)
        bfWriter = csv.writer(bf)
        vfWriter = csv.writer(vf)

        dpWriter.writerow(["dataset", "type", "n", "T", "temps_ms", "memoire_kb", "trouve"])
        bfWriter.writerow(["dataset", "type", "n", "T", "temps_ms", "memoire_kb", "trouve"])
        vfWriter.writerow(["dataset", "type", "n", "temps_ms", "memoire_kb", "solution_valide"])

        for id in ids:
            S, T, V, dtype = readDataset(id)
            n = len(S)

            # --- DP ---
            ok, sol, t, m = runAlgo(solve_SUBSETSUM_DP, S, T)
            dpWriter.writerow([id, dtype, n, T, f"{t:.3f}", f"{m:.1f}", ok])

            # --- Backtracking ---
            ok, sol, t, m = runAlgo(solve_subsetsum_backtracking_recursif, S, T)
            bfWriter.writerow([id, dtype, n, T, f"{t:.3f}", f"{m:.1f}", ok])

            # --- Verify ---
            if V is not None:
                valid, t, m = runVerify(S, V, T)
            else:
                valid, t, m = True, 0.0, 0.0

            vfWriter.writerow([id, dtype, n, f"{t:.3f}", f"{m:.1f}", valid])

    print("\n✔ DP results           →", dpFile)
    print("✔ Backtracking results →", bfFile)
    print("✔ Verify results       →", verifyFile)


if __name__ == "__main__":
    main()
