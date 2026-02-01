import os
import csv
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RESULTS_DIR = os.path.join(BASE_DIR, "tests")

# dossier où on va stocker les tableaux de performance
PERF_DIR = os.path.join(BASE_DIR, "performance")

# créer le dossier performance s'il n'existe pas
os.makedirs(PERF_DIR, exist_ok=True)

# fichiers résultats
DP_FILE = os.path.join(RESULTS_DIR, "results_dp.csv")
BACKTRACKING_FILE = os.path.join(RESULTS_DIR, "results_backtracking.csv")
VERIFY_FILE = os.path.join(RESULTS_DIR, "results_verify.csv")
 
# lire un fichier csv et retourner toutes les lignes
def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

#calculer la moyenne d'une liste
def average(values):
    return sum(values) / len(values) if values else 0

#moyenne par n et type
def average_by_n_and_type(data, algo_name):
   
    
    # regrouper par type puis par n
    grouped = defaultdict(lambda: defaultdict(list))
    
    for row in data:
        type_cat = row["type"]
        n = int(row["n"])
        grouped[type_cat][n].append(row)
    
    # préparer les résultats
    results = []
    
    for type_cat in grouped.keys():
        for n in sorted(grouped[type_cat].keys()):
            times = [float(r["temps_ms"]) for r in grouped[type_cat][n]]
            memories = [float(r["memoire_kb"]) for r in grouped[type_cat][n]]
            
            results.append({
                "type": type_cat,
                "n": n,
                "avg_time_ms": average(times),
                "avg_memory_kb": average(memories)
            })
    
    # fichier de sortie
    out_file = os.path.join(PERF_DIR, f"{algo_name}_avg_by_n_and_type.csv")

    with open(out_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["type", "n", "avg_time_ms", "avg_memory_kb"])
        
        for r in results:
            writer.writerow([r["type"], r["n"], r["avg_time_ms"], r["avg_memory_kb"]])

    return out_file


# MOYENNE PAR TYPE DE DATASET
def average_by_type(data, algo_name):
    
    grouped = defaultdict(list)

    for row in data:
        grouped[row["type"]].append(row)
    
    # préparer les résultats
    results = []
    for t in grouped.keys():
        times = [float(r["temps_ms"]) for r in grouped[t]]
        memories = [float(r["memoire_kb"]) for r in grouped[t]]
        results.append({
            "type": t,
            "avg_time_ms": average(times),
            "avg_memory_kb": average(memories)
        })
    
    # fichier de sortie
    out_file = os.path.join(PERF_DIR, f"{algo_name}_avg_by_type.csv")

    with open(out_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["type", "avg_time_ms", "avg_memory_kb"])
        
        for r in results:
            writer.writerow([r["type"], r["avg_time_ms"], r["avg_memory_kb"]])

    return out_file


# COMPARAISON DP vs BACKTRACKING
def compare_dp_backtracking(dp_data, bt_data):
    
    merged = {}

    # stocker les résultats DP
    for row in dp_data:
        merged[row["dataset"]] = {
            "dataset": row["dataset"],
            "n": int(row["n"]),
            "type": row["type"],
            "dp_time": float(row["temps_ms"]),
            "dp_memory": float(row["memoire_kb"]),
        }

    # ajouter les résultats Backtracking
    for row in bt_data:
        if row["dataset"] in merged:
            merged[row["dataset"]]["bt_time"] = float(row["temps_ms"])
            merged[row["dataset"]]["bt_memory"] = float(row["memoire_kb"])

   
    out_file = os.path.join(PERF_DIR, "compare_dp_backtracking.csv")

    with open(out_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "dataset", "type", "n",
            "dp_time_ms", "bt_time_ms",
            "dp_memory_kb", "bt_memory_kb"
        ])

        for data in merged.values():
            if "bt_time" in data:
                writer.writerow([
                    data["dataset"], data["type"], data["n"],
                    data["dp_time"], data["bt_time"],
                    data["dp_memory"], data["bt_memory"]
                ])

    return out_file

 

def main():
    
    
    dp = read_csv(DP_FILE)
    bt = read_csv(BACKTRACKING_FILE)
    vf = read_csv(VERIFY_FILE)

    # moyennes par type et taille n
    print( average_by_n_and_type(dp, "dp"))
    print(average_by_n_and_type(bt, "backtracking"))
    print( average_by_n_and_type(vf, "verify"))


    # moyennes par type global
    print( average_by_type(dp, "dp"))
    print( average_by_type(bt, "backtracking"))
    print( average_by_type(vf, "verify"))

if __name__ == "__main__":
    main()