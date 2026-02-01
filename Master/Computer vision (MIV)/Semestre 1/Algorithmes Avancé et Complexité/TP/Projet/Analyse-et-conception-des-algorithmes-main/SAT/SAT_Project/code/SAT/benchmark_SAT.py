# benchmark_SAT.py
import time
import random
import matplotlib.pyplot as plt
import os
import sys
import json
from datetime import datetime
from memory_profiler import memory_usage



# Generer automatiquement des instances SAT
# Comparer deux algorithmes :
# Bruteforce (recherche exhaustive)
# Backtracking (avec coupure intelligente)
# Mesurer le temps d’execution
# Sauvegarder les resultats
# Tracer des graphiques
# Analyser la croissance exponentielle



# Ajouter le dossier courant au path pour importer les modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from solve_SAT import solve_SAT_bruteforce, solve_SAT_backtracking
except ImportError:
    print("Erreur: solve_SAT.py non trouve. Execute depuis le dossier code/SAT/")
    sys.exit(1)

def generate_random_SAT_instance(n_vars, n_clauses, literals_per_clause=3):
    """
    Genère une instance SAT aleatoire.
    
    Args:
        n_vars: nombre de variables
        n_clauses: nombre de clauses
        literals_per_clause: nombre de litteraux par clause
    
        
    Returns:
        (variables, clauses)
    """
    variables = [f'x{i+1}' for i in range(n_vars)]
    clauses = []
    
    for _ in range(n_clauses):
        # Choisir k variables distinctes
        chosen_vars = random.sample(range(1, n_vars + 1), min(literals_per_clause, n_vars))
        clause = []
        for var in chosen_vars:
            neg = random.choice([True, False])  # Avec ou sans negation
            clause.append((var, neg))
        clauses.append(clause)
    
    return variables, clauses

def run_benchmark(max_vars=10, clauses_per_var=2, repetitions=9):
    """
    Execute le benchmark pour differentes tailles.
    
    Args:
        max_vars: nombre maximum de variables à tester
        clauses_per_var: nombre de clauses par variable
        repetitions: nombre de repetitions pour chaque taille
    
    Returns:
        dict: resultats du benchmark

    Boucle sur la taille du problème
    for n_vars in range(3, max_vars + 1):

    On commence à 3 variables (pour le test)
    On augmente progressivement : analyse de la croissance
    Pour chaque combinaison de (bn_var, nb_clause) en test nb_repition fois la performance des fonction BF et BT
      en fonction de temps et l’espace et stocker le resultat dans des list  et calculer la moyen de 
      chaque combinaison et stocker les donner dans le fichier result 

    """
    results = {
        'bruteforce': {'times': [], 'memory': [], 'vars': [], 'clauses': []},
        'backtracking': {'times': [], 'memory': [], 'vars': [], 'clauses': []}
    }

    
    print("=" * 60)
    print("DeMARRAGE DU BENCHMARK SAT")
    print("=" * 60)
    
    for n_vars in range(3, max_vars + 1):
        n_clauses = n_vars * clauses_per_var
        
        print(f"\nTest avec {n_vars} variables et {n_clauses} clauses...")
        
        bf_times = []
        bt_times = []
        bf_memory = []
        bt_memory = []

        
        for rep in range(repetitions):
            # Generer une instance aleatoire
            variables, clauses = generate_random_SAT_instance(n_vars, n_clauses)
           # print("Clauses generer :n", clauses)
            
            # Test bruteforce
            if n_vars <= 10:  # Limiter bruteforce à 10 variables max
                
                start = time.time()
                solve_SAT_bruteforce(variables, clauses)
                bf_time = time.time() - start



                bf_mem = memory_usage(
                    (solve_SAT_bruteforce, (variables, clauses)),
                    interval=0.01,
                    max_usage=True
                )
                

                bf_times.append(bf_time)
                bf_memory.append(bf_mem)

            else:
                bf_times.append(None)
                bf_memory.append(None)
            
            # Test backtracking
            start = time.time()
            solve_SAT_bruteforce(variables, clauses)
            bt_time = time.time() - start
            bt_mem = memory_usage(
                (solve_SAT_backtracking, (variables, clauses)),
                interval=0.01,
                max_usage=True
            )
            

            bt_times.append(bt_time)
            bt_memory.append(bt_mem)

            print(f"  Repetition {rep+1}: BF={bf_time:.4f}s, BT={bt_time:.4f}s")
        
        # Moyenne des temps
        valid_bf_times = [t for t in bf_times if t is not None]
        if valid_bf_times:
            avg_bf = sum(valid_bf_times) / len(valid_bf_times)
        else:
            avg_bf = None
        
        avg_bt = sum(bt_times) / len(bt_times)

        valid_bf_mem = [m for m in bf_memory if m is not None]

        avg_bf_mem = sum(valid_bf_mem) / len(valid_bf_mem) if valid_bf_mem else None
        avg_bt_mem = sum(bt_memory) / len(bt_memory)

        
        # Stocker les resultats
        results['bruteforce']['vars'].append(n_vars)
        results['bruteforce']['clauses'].append(n_clauses)
        results['bruteforce']['times'].append(avg_bf)
        
        results['backtracking']['vars'].append(n_vars)
        results['backtracking']['clauses'].append(n_clauses)
        results['backtracking']['times'].append(avg_bt)

        results['bruteforce']['memory'].append(avg_bf_mem)
        results['backtracking']['memory'].append(avg_bt_mem)

        
        
        print(
            f"  Moyennes: BF={avg_bf:.4f}s, {avg_bf_mem:.2f}MB | "
            f"BT={avg_bt:.4f}s, {avg_bt_mem:.2f}MB"
        )

    return results

def save_results(results, filename="benchmark_results.json"):
    """Sauvegarde les resultats dans un fichier JSON."""
    # Creer le dossier de resultats s'il n'existe pas
    results_dir = os.path.join("data", "results")
    os.makedirs(results_dir, exist_ok=True)
    
    filepath = os.path.join(results_dir, filename)
    
    # Convertir les resultats en format serialisable
    serializable_results = {
        'timestamp': datetime.now().isoformat(),
        'bruteforce': results['bruteforce'],
        'backtracking': results['backtracking']
    }
    
    with open(filepath, 'w') as f:
        json.dump(serializable_results, f, indent=2)
    
    print(f"\nResultats sauvegardes dans: {filepath}")
    return filepath

def load_results(filename="benchmark_results.json"):
    """Charge les resultats depuis un fichier JSON."""
    filepath = os.path.join("data", "results", filename)
    
    if not os.path.exists(filepath):
        print(f"Fichier {filepath} non trouve. Executez d'abord le benchmark.")
        return None
    
    with open(filepath, 'r') as f:
        results = json.load(f)
    
    print(f"Resultats charges depuis: {filepath}")
    print(f"Date du benchmark: {results['timestamp']}")
    
    return results

def plot_performance_comparison(results):
    """
    Cree des graphiques comparant les performances.
    
    Args:
        results: dict contenant les resultats du benchmark
    """
    
    # 1. Graphique: Temps d'execution vs Nombre de variables
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    
    # Filtrer les valeurs None pour bruteforce
    bf_vars = results['bruteforce']['vars']
    bf_times = results['bruteforce']['times']
    valid_indices = [i for i, t in enumerate(bf_times) if t is not None]
    
    if valid_indices:
        bf_vars_filtered = [bf_vars[i] for i in valid_indices]
        bf_times_filtered = [bf_times[i] for i in valid_indices]
        plt.plot(bf_vars_filtered, bf_times_filtered, 'ro-', linewidth=2, markersize=8, label='Bruteforce')
    
    # Backtracking
    plt.plot(results['backtracking']['vars'], 
             results['backtracking']['times'], 
             'bs-', linewidth=2, markersize=8, label='Backtracking')
    
    plt.xlabel('Nombre de variables', fontsize=12)
    plt.ylabel('Temps d\'execution (secondes)', fontsize=12)
    plt.title('Temps d\'execution vs Nombre de variables', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.yscale('log')  # echelle logarithmique pour mieux voir les differences
    
    # 2. Graphique: Temps d'execution vs Nombre de clauses
    plt.subplot(1, 2, 2)
    
    if valid_indices:
        bf_clauses_filtered = [results['bruteforce']['clauses'][i] for i in valid_indices]
        plt.plot(bf_clauses_filtered, bf_times_filtered, 'ro-', linewidth=2, markersize=8, label='Bruteforce')
    
    plt.plot(results['backtracking']['clauses'], 
             results['backtracking']['times'], 
             'bs-', linewidth=2, markersize=8, label='Backtracking')
    
    plt.xlabel('Nombre de clauses', fontsize=12)
    plt.ylabel('Temps d\'execution (secondes)', fontsize=12)
    plt.title('Temps d\'execution vs Nombre de clauses', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.yscale('log')
    
    plt.tight_layout()
    
    # Sauvegarder le graphique
    plots_dir = os.path.join("report", "images")
    os.makedirs(plots_dir, exist_ok=True)
    plot_file = os.path.join(plots_dir, "SAT_performance_comparison.png")
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"\nGraphique sauvegarde dans: {plot_file}")
    
    plt.show()

def plot_growth_rate(results):
    """Affiche le taux de croissance des algorithmes."""
    
    plt.figure(figsize=(10, 6))
    
    # Calculer le taux de croissance theorique
    vars_list = results['backtracking']['vars']
    
    # Theorique: O(2^n) pour bruteforce, O(1.8^n) pour backtracking (approximation)
    theoretical_bf = [0.001 * (2 ** n) for n in vars_list]  # Facteur d'echelle
    theoretical_bt = [0.001 * (1.8 ** n) for n in vars_list]  # Facteur d'echelle
    
    # Experimentale (normalisee)
    max_time = max([t for t in results['backtracking']['times'] if t is not None])
    normalized_bt = [t / max_time for t in results['backtracking']['times']]
    
    plt.plot(vars_list, theoretical_bf, 'r--', linewidth=2, label='Theorique: O(2ⁿ) (Bruteforce)')
    plt.plot(vars_list, theoretical_bt, 'b--', linewidth=2, label='Theorique: O(1.8ⁿ) (Backtracking)')
    plt.plot(vars_list, normalized_bt, 'go-', linewidth=3, markersize=8, 
             label='Experimental (Backtracking normalise)')
    
    plt.xlabel('Nombre de variables (n)', fontsize=12)
    plt.ylabel('Temps normalise', fontsize=12)
    plt.title('Taux de croissance theorique vs experimental', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.yscale('log')
    
    # Ajouter des annotations
    plt.annotate('Croissance exponentielle', 
                 xy=(8, theoretical_bf[5]), 
                 xytext=(6, theoretical_bf[5] * 5),
                 arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                 fontsize=10, color='red')
    
    # Sauvegarder
    plots_dir = os.path.join("report", "images")
    os.makedirs(plots_dir, exist_ok=True)
    plot_file = os.path.join(plots_dir, "SAT_growth_rate.png")
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"Graphique de croissance sauvegarde dans: {plot_file}")
    
    plt.show()

def plot_memory_usage(results):
    """Trace l'usage memoire mesure."""
    vars_list = results['backtracking']['vars']

    memory_bf = results['bruteforce']['memory']
    memory_bt = results['backtracking']['memory']



    plt.figure(figsize=(10, 6))
    
   

    
    plt.plot(vars_list, memory_bf, 'ro-', linewidth=2, markersize=8, 
             label='Bruteforce (pire cas)')
    plt.plot(vars_list, memory_bt, 'bs-', linewidth=2, markersize=8, 
             label='Backtracking')
    
    plt.xlabel('Nombre de variables', fontsize=12)
    plt.ylabel('Usage memoire (MB)', fontsize=12)
    plt.title('Usage memoire vs Taille du problème', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Sauvegarder
    plots_dir = os.path.join("report", "images")
    os.makedirs(plots_dir, exist_ok=True)
    plot_file = os.path.join(plots_dir, "SAT_memory_usage.png")
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"Graphique memoire sauvegarde dans: {plot_file}")
    
    plt.show()

def generate_summary_table(results):
    """Genère un tableau recapitulatif des resultats avec usage memoire minimalement ajoute."""
    
    print("\n" + "=" * 90)
    print("TABLEAU ReCAPITULATIF DES PERFORMANCES (Temps + Memoire)")
    print("=" * 90)
    print(f"{'Variables':<12} {'Clauses':<12} {'Bruteforce (s)':<15} {'Backtracking (s)':<15} "
          f"{'BF Memoire(MB)':<15} {'BT Memoire(MB)':<15} {'Acceleration':<12}")
    print("-" * 90)
    
    for i in range(len(results['backtracking']['vars'])):
        n_vars = results['backtracking']['vars'][i]
        n_clauses = results['backtracking']['clauses'][i]
        time_bt = results['backtracking']['times'][i]
        time_bf = results['bruteforce']['times'][i]
        mem_bf = results['bruteforce']['memory'][i]
        mem_bt = results['backtracking']['memory'][i]
        
        if time_bf and time_bf > 0:
            speedup = time_bf / time_bt if time_bt > 0 else float('inf')
            speedup_str = f"{speedup:.2f}x"
        else:
            speedup_str = "N/A"
            time_bf = 0
        
        time_bf_str = f"{time_bf:.4f}" if time_bf != 0 else "N/A"
        time_bt_str = f"{time_bt:.4f}" if time_bt else "N/A"
        mem_bf_str = f"{mem_bf:.2f}" if mem_bf else "N/A"
        mem_bt_str = f"{mem_bt:.2f}" if mem_bt else "N/A"
        
        print(f"{n_vars:<12} {n_clauses:<12} {time_bf_str:<15} {time_bt_str:<15} "
              f"{mem_bf_str:<15} {mem_bt_str:<15} {speedup_str:<12}")
    
    print("=" * 90)


def main():
    """Fonction principale."""
    print("BENCHMARK SAT - ANALYSE DE PERFORMANCE")
    print("Ce script va :")
    print("1. Generer des instances SAT de differentes tailles")
    print("2. Mesurer le temps d'execution des algorithmes")
    print("3. Generer des graphiques de performance")
    print("4. Sauvegarder les resultats")
    print("\nLe benchmark peut prendre quelques minutes...")
    

    
    # Option: Charger des resultats existants ou en generer de nouveaux
    load_existing = input("\nCharger des resultats existants ? car la generation de nouveaux resultats prend un temps , et les reesultas existant son des resultat d'une execution precedent .(o/n): ")
    
    if load_existing.lower() == 'o':
        results = load_results()
        if not results:
            print("Generation de nouveaux resultats...")
            results = run_benchmark(max_vars=10, repetitions=3)
            save_results(results)
    else:
        # Executer le benchmark
        results = run_benchmark(max_vars=10, repetitions=3)
        save_results(results)
    
    # Generer les graphiques
    print("\n" + "=" * 60)
    print("GeNeRATION DES GRAPHIQUES")
    print("=" * 60)
    
    plot_performance_comparison(results)
    plot_growth_rate(results)
    plot_memory_usage(results)
    
    # Afficher le tableau recapitulatif
    generate_summary_table(results)
    
    print("\n" + "=" * 60)
    print("BENCHMARK TERMINe AVEC SUCCÈS")
    print("=" * 60)
    print("\nFichiers generes :")
    print("1. data/results/benchmark_results.json - Donnees brutes")
    print("2. report/images/SAT_performance_comparison.png - Comparaison")
    print("3. report/images/SAT_growth_rate.png - Taux de croissance")
    print("4. report/images/SAT_memory_usage.png - Usage memoire")

if __name__ == "__main__":
    main()
