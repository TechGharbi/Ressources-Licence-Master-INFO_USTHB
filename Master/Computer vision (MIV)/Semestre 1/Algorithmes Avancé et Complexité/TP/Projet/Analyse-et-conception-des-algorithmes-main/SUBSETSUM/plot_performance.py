import os
import csv
from collections import defaultdict
import matplotlib.pyplot as plt


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# dossier où se trouvent les fichiers de performance
PERF_DIR = os.path.join(BASE_DIR, "performance")

# dossier où on va sauvegarder les graphes
PLOTS_DIR = os.path.join(BASE_DIR, "plots")

# créer le dossier plots s'il n'existe pas
os.makedirs(PLOTS_DIR, exist_ok=True)



CATEGORY_ORDER = ["MEILLEUR", "PIRE"]
CATEGORY_COLORS = {
    "MEILLEUR": "#2ecc71",   
    "PIRE": "#e74c3c"         
}


# lire fichier csv 
def read_csv(file_path):
    """Lit un fichier CSV et retourne toutes les lignes"""
    with open(file_path, newline="") as f:
        return list(csv.DictReader(f))


def read_avg_by_n_and_type(file_path):
   
    # Lit le fichier de moyennes par type et n
   
   
    rows = read_csv(file_path)
    
    data_by_type = defaultdict(list)
    
    for row in rows:
        type_cat = row["type"]
        data_by_type[type_cat].append({
            "n": int(row["n"]),
            "time": float(row["avg_time_ms"]),
            "memory": float(row["avg_memory_kb"])
        })
    
    return data_by_type

def read_avg_by_type(file_path):
    rows = read_csv(file_path)
    
    result = {}
    for row in rows:
        type_cat = row["type"]
        result[type_cat] = {
            "time": float(row["avg_time_ms"]),
            "memory": float(row["avg_memory_kb"])
        }
    
    return result


# Graphe par catégorie 
def plot_time_by_category(data_dict, algo_name, file_name):
    """Graphe du temps d'exécution avec 2 courbes (MEILLEUR vs PIRE)"""
    
    plt.figure(figsize=(10, 6))
    
    for category in CATEGORY_ORDER:
        if category in data_dict:
            data = data_dict[category]
            n_values = [d["n"] for d in data]
            times = [d["time"] for d in data]
            
            plt.plot(n_values, times, 
                    marker="o", 
                    label=category,
                    color=CATEGORY_COLORS[category],
                    linewidth=2.5,
                    markersize=8)
    
    plt.xlabel("Taille de l'ensemble (n)", fontsize=13)
    plt.ylabel("Temps d'exécution (ms)", fontsize=13)
    plt.title(f"Temps d'exécution : MEILLEUR vs PIRE - {algo_name}", 
             fontsize=15, fontweight='bold')
    plt.legend(title="Catégorie", fontsize=12, loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, file_name), dpi=300)
    plt.close()

def plot_memory_by_category(data_dict, algo_name, file_name):

    plt.figure(figsize=(10, 6))
    
    for category in CATEGORY_ORDER:
        if category in data_dict:
            data = data_dict[category]
            n_values = [d["n"] for d in data]
            memories = [d["memory"] for d in data]
            
            plt.plot(n_values, memories, 
                    marker="o", 
                    label=category,
                    color=CATEGORY_COLORS[category],
                    linewidth=2.5,
                    markersize=8)
    
    plt.xlabel("Taille de l'ensemble (n)", fontsize=13)
    plt.ylabel("Mémoire utilisée (KB)", fontsize=13)
    plt.title(f"Mémoire utilisée : MEILLEUR vs PIRE - {algo_name}", 
             fontsize=15, fontweight='bold')
    plt.legend(title="Catégorie", fontsize=12, loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, file_name), dpi=300)
    plt.close()


# COMPARAISON ENTRE DEUX ALGOS
def plot_comparison_by_category(data1_dict, data2_dict, key, y_label, title, 
                                file_name, label1, label2):
    
    
    # Couleurs pour DP vs Backtracking
    DP_COLORS = {
        "MEILLEUR": "#3498db",   
        "PIRE": "#9b59b6"         
    }
    
    BT_COLORS = {
        "MEILLEUR": "#e67e22",    
        "PIRE": "#e74c3c"         
    }
    
    plt.figure(figsize=(12, 7))
    
    for category in CATEGORY_ORDER:
        if category in data1_dict and category in data2_dict:
            data1 = data1_dict[category]
            data2 = data2_dict[category]
            
            n1 = [d["n"] for d in data1]
            v1 = [d[key] for d in data1]
            
            n2 = [d["n"] for d in data2]
            v2 = [d[key] for d in data2]
            
            # Ligne continue pour algo1 (DP)
            plt.plot(n1, v1, 
                    marker="o", 
                    label=f"{label1} - {category}",
                    color=DP_COLORS[category],
                    linewidth=2.5,
                    linestyle="-",
                    markersize=7)
            
            # Ligne pointillée pour algo2 (Backtracking)
            plt.plot(n2, v2, 
                    marker="s", 
                    label=f"{label2} - {category}",
                    color=BT_COLORS[category],
                    linewidth=2.5,
                    linestyle="--",
                    alpha=0.7,
                    markersize=7)
    
    plt.xlabel("Taille de l'ensemble (n)", fontsize=13)
    plt.ylabel(y_label, fontsize=13)
    plt.title(title, fontsize=15, fontweight='bold')
    plt.legend(fontsize=11, loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, file_name), dpi=300)
    plt.close()

def main():
    # Charger les données
    dp_by_cat = read_avg_by_n_and_type(os.path.join(PERF_DIR, "dp_avg_by_n_and_type.csv"))
    bt_by_cat = read_avg_by_n_and_type(os.path.join(PERF_DIR, "backtracking_avg_by_n_and_type.csv"))
    vf_by_cat = read_avg_by_n_and_type(os.path.join(PERF_DIR, "verify_avg_by_n_and_type.csv"))
   

    # Graphes du temps par catégorie
    plot_time_by_category(dp_by_cat, "DP", "dp_time.png")
    plot_time_by_category(bt_by_cat, "Backtracking", "backtracking_time.png")
    plot_time_by_category(vf_by_cat, "Verify", "verify_time.png")

    # Graphes de la mémoire par catégorie
    plot_memory_by_category(dp_by_cat, "DP", "dp_memory.png")
    plot_memory_by_category(bt_by_cat, "Backtracking", "backtracking_memory.png")
    plot_memory_by_category(vf_by_cat, "Verify", "verify_memory.png")
  
    # Comparaison DP vs Backtracking uniquement
  
    plot_comparison_by_category(
        dp_by_cat, bt_by_cat,
        key="time",
        y_label="Temps (ms)",
        title="Comparaison du temps : DP vs Backtracking (MEILLEUR/PIRE)",
        file_name="compare_dp_bt_time.png",
        label1="DP",
        label2="Backtracking"
    )
    
    plot_comparison_by_category(
        dp_by_cat, bt_by_cat,
        key="memory",
        y_label="Mémoire (KB)",
        title="Comparaison de la mémoire : DP vs Backtracking (MEILLEUR/PIRE)",
        file_name="compare_dp_bt_memory.png",
        label1="DP",
        label2="Backtracking"
    )
    print(f" {PLOTS_DIR}")
  
   

if __name__ == "__main__":
    main()
    print(f"terminer")