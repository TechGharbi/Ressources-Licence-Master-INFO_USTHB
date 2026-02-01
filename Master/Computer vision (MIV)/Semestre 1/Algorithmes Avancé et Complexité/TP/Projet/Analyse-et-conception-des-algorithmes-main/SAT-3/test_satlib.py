"""
Tests et benchmarks avec les instances SATLIB
Format DIMACS CNF
"""
import time
import os
import sys
from solver_3sat import SAT3Solver
from verifier_3sat import SAT3Verifier
from dimacs_reader import read_dimacs_cnf, read_3sat_dimacs, print_dimacs_info

# Constante pour le dossier des instances
INSTANCES_DIR = "satlib_instances2"

def test_satlib_instance(filename, verbose=True):
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"Test: {os.path.basename(filename)}")
        print('='*70)
    
    # Lire l'instance
    try:
        clauses, num_vars = read_dimacs_cnf(filename)
    except FileNotFoundError:
        print(f"⚠️  Fichier non trouvé: {filename}")
        return None
    except Exception as e:
        print(f"⚠️  Erreur de lecture: {e}")
        return None
    
    if verbose:
        print(f"Variables: {num_vars}")
        print(f"Clauses: {len(clauses)}")
        
        # Vérifier si c'est du 3-SAT
        is_3sat = all(len(c) == 3 for c in clauses)
        if is_3sat:
            print("✓ Instance 3-SAT valide")
        else:
            print("⚠️  Attention: pas une instance 3-SAT stricte")
            # Filtrer pour garder seulement les clauses de taille 3
            clauses = [c for c in clauses if len(c) == 3]
            print(f"→ {len(clauses)} clauses de taille 3 conservées")
    
    # Résoudre
    solver = SAT3Solver(clauses, num_vars)
    
    start_time = time.time()
    try:
        success, assignment, stats = solver.solve()
        elapsed_time = time.time() - start_time
    except Exception as e:
        print(f"⚠️  Erreur lors de la résolution: {e}")
        return None
    
    # Résultats
    if verbose:
        print(f"\nRésultat: {'✓ SATISFIABLE' if success else '✗ INSATISFIABLE'}")
        print(f"Temps d'exécution: {elapsed_time:.4f}s")
        print(f"Nombre de backtracks: {stats['backtrack_count']}")
    
    # Vérifier la solution si trouvée
    verified = False
    if success:
        verifier = SAT3Verifier(clauses)
        is_valid, details = verifier.verify(assignment)
        verified = is_valid
        
        if verbose:
            if is_valid:
                print("✓ Solution vérifiée et validée")
                print(f"  Clauses satisfaites: {details['satisfied_clauses']}/{details['total_clauses']}")
            else:
                print("✗ ERREUR: Solution invalide!")
                print(f"  Clauses insatisfaites: {details['unsatisfied_clauses']}")
    
    return {
        'filename': os.path.basename(filename),
        'num_variables': num_vars,
        'num_clauses': len(clauses),
        'satisfiable': success,
        'time': elapsed_time,
        'backtracks': stats['backtrack_count'],
        'verified': verified
    }


def download_instructions():
    """
    Instructions pour télécharger des instances SATLIB
    """
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║  TÉLÉCHARGER DES INSTANCES SATLIB POUR 3-SAT                        ║
╚══════════════════════════════════════════════════════════════════════╝

📥 ÉTAPE 1: Aller sur SATLIB
   URL: https://www.cs.ubc.ca/~hoos/SATLIB/benchm.html

📦 ÉTAPE 2: Télécharger les instances "Uniform Random-3-SAT"
   
   Instances recommandées pour le projet:
   
   ├─ uf20-91.tar.gz    (20 variables, 91 clauses)   - FACILE
   │  • Bon pour débuter et vérifier que ça marche
   │  • Temps: < 1 seconde
   │
   ├─ uf50-218.tar.gz   (50 variables, 218 clauses)  - MOYEN
   │  • Instances intéressantes pour l'analyse
   │  • Temps: quelques secondes
   │
   ├─ uf75-325.tar.gz   (75 variables, 325 clauses)  - DIFFICILE
   │  • Pour montrer les limites du backtracking
   │  • Temps: peut prendre plusieurs minutes
   │
   └─ uf100-430.tar.gz  (100 variables, 430 clauses) - TRÈS DIFFICILE
      • Optionnel, peut être très long
      • Bon pour démontrer la complexité exponentielle

📂 ÉTAPE 3: Extraire les archives
   $ tar -xzf uf20-91.tar.gz
   $ tar -xzf uf50-218.tar.gz
   $ tar -xzf uf75-325.tar.gz

📁 ÉTAPE 4: Organiser les fichiers
   Créer un dossier 'satlib_instances/' et y placer les .cnf
   
   Structure attendue:
   satlib_instances/
   ├── uf20-01.cnf
   ├── uf20-02.cnf
   ├── ...
   ├── uf50-01.cnf
   ├── uf50-02.cnf
   └── ...

🚀 ÉTAPE 5: Relancer ce script
   $ python test_satlib.py

════════════════════════════════════════════════════════════════════════

💡 ALTERNATIVE RAPIDE (pour tester):
   Ce script peut générer des instances de test locales si vous n'avez
   pas encore téléchargé SATLIB. Lancez:
   
   $ python test_satlib.py --generate

════════════════════════════════════════════════════════════════════════
""")


def generate_test_instances():
    """
    Génère des instances de test locales
    """
    from test_3sat import generate_random_3sat
    from dimacs_reader import write_dimacs_cnf
    
    os.makedirs(INSTANCES_DIR, exist_ok=True)
    
    print("\n" + "="*70)
    print("GÉNÉRATION D'INSTANCES DE TEST")
    print("="*70 + "\n")
    
    test_configs = [
        (10, 42, "local_uf10", 5),   # 5 instances de 10 vars
        (15, 63, "local_uf15", 5),   # 5 instances de 15 vars
        (20, 84, "local_uf20", 5),   # 5 instances de 20 vars
    ]
    
    total = 0
    for num_vars, num_clauses, prefix, count in test_configs:
        print(f"Génération: {count} instances avec {num_vars} variables...")
        
        for i in range(1, count + 1):
            clauses = generate_random_3sat(num_vars, num_clauses, seed=i)
            filename = f"{INSTANCES_DIR}/{prefix}-{i:02d}.cnf"
            
            comments = [
                f"Instance 3-SAT générée localement",
                f"Variables: {num_vars}, Clauses: {num_clauses}",
                f"Ratio: {num_clauses/num_vars:.2f}"
            ]
            
            write_dimacs_cnf(clauses, num_vars, filename, comments)
            total += 1
        
        print(f"  ✓ {count} fichiers créés")
    
    print(f"\n✓ Total: {total} instances générées dans '{INSTANCES_DIR}/'")
    print("="*70 + "\n")
    
    return total


def list_existing_instances():
    """
    Liste les instances existantes dans le dossier
    """
    if not os.path.exists(INSTANCES_DIR):
        return []
    
    cnf_files = []
    for file in os.listdir(INSTANCES_DIR):
        if file.endswith('.cnf'):
            cnf_files.append(os.path.join(INSTANCES_DIR, file))
    
    cnf_files.sort()
    return cnf_files


def show_instances_menu():
    """
    Affiche un menu pour choisir entre instances existantes ou générer
    """
    print("\n" + "="*70)
    print("MENU PRINCIPAL - CHOIX DES INSTANCES")
    print("="*70)
    
    # Vérifier si des instances existent déjà
    existing_instances = list_existing_instances()
    
    if existing_instances:
        print(f"\n📁 Instances existantes trouvées ({len(existing_instances)} fichiers):")
        print("-" * 70)
        
        # Grouper par type d'instance
        instances_by_type = {}
        for file in existing_instances:
            name = os.path.basename(file)
            if name.startswith("local_"):
                instance_type = name.split("-")[0]  # local_uf10, local_uf15, etc.
            elif name.startswith("uf"):
                instance_type = name.split("-")[0]  # uf20, uf50, etc.
            else:
                instance_type = "autres"
            
            if instance_type not in instances_by_type:
                instances_by_type[instance_type] = []
            instances_by_type[instance_type].append(name)
        
        # Afficher par type
        for inst_type, files in instances_by_type.items():
            print(f"  {inst_type}: {len(files)} fichiers")
            for i, f in enumerate(files[:3], 1):
                print(f"    {i}. {f}")
            if len(files) > 3:
                print(f"    ... et {len(files)-3} autres")
            print()
    
    else:
        print("\n📁 Aucune instance trouvée dans le dossier.")
        print("  Vous pouvez générer des instances locales ou télécharger SATLIB")
    
    print("\nOptions disponibles:")
    print("="*70)
    print("1. Utiliser les instances existantes")
    print("2. Générer de nouvelles instances locales")
    print("3. Télécharger des instances SATLIB (instructions)")
    print("4. Quitter")
    print("-" * 70)
    
    while True:
        choice = input("Votre choix (1-4): ").strip()
        
        if choice == "1":
            if not existing_instances:
                print("\n⚠️  Aucune instance existante. Choisissez une autre option.")
                continue
            return "use_existing"
        
        elif choice == "2":
            return "generate"
        
        elif choice == "3":
            download_instructions()
            input("\nAppuyez sur Entrée pour revenir au menu...")
            continue
        
        elif choice == "4":
            return "quit"
        
        else:
            print("Choix invalide. Veuillez entrer 1, 2, 3 ou 4.")


def run_benchmark_with_choice():
    """
    Lance le benchmark avec le choix de l'utilisateur
    """
    choice = show_instances_menu()
    
    if choice == "quit":
        print("\nAu revoir!")
        return
    
    if choice == "generate":
        print("\n" + "="*70)
        print("GÉNÉRATION DE NOUVELLES INSTANCES")
        print("="*70)
        
        # Demander confirmation si des instances existent déjà
        existing = list_existing_instances()
        if existing:
            print(f"\n⚠️  Attention: {len(existing)} instances existent déjà.")
            print("La génération va ajouter de nouvelles instances aux existantes.")
            confirm = input("Continuer? (o/n): ").lower()
            if confirm != 'o':
                print("Annulé.")
                return
        
        num_generated = generate_test_instances()
        if num_generated == 0:
            print("Aucune instance générée.")
            return
        
        # Demander si on veut exécuter le benchmark maintenant
        print("\n" + "="*70)
        run_now = input("Voulez-vous exécuter le benchmark maintenant? (o/n): ").lower()
        if run_now != 'o':
            print("\nInstances générées. Vous pourrez les utiliser plus tard.")
            return
    
    # Récupérer la liste des instances (existantes ou nouvellement générées)
    instances = list_existing_instances()
    
    if not instances:
        print("\n❌ Aucune instance disponible pour le benchmark.")
        return
    
    print(f"\n📊 {len(instances)} instances disponibles pour le benchmark")
    
    # Demander le nombre d'instances à tester
    while True:
        try:
            max_input = input(f"Nombre d'instances à tester (max {len(instances)}, 0 pour toutes): ").strip()
            if max_input == "":
                max_instances = min(10, len(instances))
                break
            max_instances = int(max_input)
            if max_instances == 0:
                max_instances = None
                break
            if 1 <= max_instances <= len(instances):
                break
            print(f"Veuillez entrer un nombre entre 1 et {len(instances)}")
        except ValueError:
            print("Veuillez entrer un nombre valide")
    
    # Demander la limite de temps
    while True:
        try:
            time_input = input("Temps limite par instance en secondes (défaut: 60): ").strip()
            if time_input == "":
                time_limit = 60
                break
            time_limit = float(time_input)
            if time_limit > 0:
                break
            print("Veuillez entrer un nombre positif")
        except ValueError:
            print("Veuillez entrer un nombre valide")
    
    # Lancer le benchmark
    run_satlib_benchmark(instances, max_instances, time_limit)


def run_satlib_benchmark(instances_list, max_instances=None, time_limit=60):
    """
    Benchmark complet sur instances SATLIB
    
    Args:
        instances_list: liste des fichiers .cnf à tester
        max_instances: nombre maximum d'instances à tester (None = toutes)
        time_limit: temps limite par instance en secondes
    """
    
    if not instances_list:
        print("❌ Aucune instance à tester.")
        return
    
    # Limiter le nombre d'instances si demandé
    if max_instances and len(instances_list) > max_instances:
        print(f"\nℹ️  Limitation à {max_instances} instances sur {len(instances_list)} disponibles")
        instances_list = instances_list[:max_instances]
    
    print("\n" + "="*70)
    print("BENCHMARK 3-SAT")
    print("="*70)
    print(f"Instances à tester: {len(instances_list)}")
    print(f"Temps limite par instance: {time_limit}s")
    print("="*70)
    
    results = []
    skipped = 0
    
    for i, file in enumerate(instances_list, 1):
        print(f"\n[{i}/{len(instances_list)}] ", end="")
        
        result = test_satlib_instance(file, verbose=True)
        
        if result:
            results.append(result)
            
            # Vérifier si on dépasse le temps limite
            if result['time'] > time_limit:
                print(f"\n⚠️  Temps limite dépassé ({result['time']:.1f}s > {time_limit}s)")
                print("   Arrêt du benchmark pour éviter les instances trop longues")
                skipped = len(instances_list) - i
                break
        else:
            skipped += 1
        
        # Pause optionnelle entre les instances
        if i < len(instances_list):
            continue_test = input("\nAppuyez sur Entrée pour continuer (ou 'q' pour quitter): ").strip()
            if continue_test.lower() == 'q':
                print("Benchmark interrompu par l'utilisateur.")
                skipped = len(instances_list) - i
                break
    
    # Tableau récapitulatif
    if results:
        print("\n" + "="*70)
        print("RÉSUMÉ DES RÉSULTATS")
        print("="*70)
        print(f"{'Fichier':<25} {'Vars':>6} {'Clauses':>8} {'Temps':>10} {'Backtracks':>12} {'Résultat':>10}")
        print("-"*70)
        
        total_time = 0
        satisfiable_count = 0
        
        for r in results:
            total_time += r['time']
            if r['satisfiable']:
                satisfiable_count += 1
            
            result_str = "SAT ✓" if r['satisfiable'] else "UNSAT ✗"
            
            print(f"{r['filename']:<25} {r['num_variables']:>6} {r['num_clauses']:>8} "
                  f"{r['time']:>9.4f}s {r['backtracks']:>12} {result_str:>10}")
        
        print("-"*70)
        print(f"Instances testées: {len(results)}")
        print(f"Satisfiables: {satisfiable_count} ({satisfiable_count/len(results)*100:.1f}%)")
        print(f"Insatisfiables: {len(results)-satisfiable_count} ({(len(results)-satisfiable_count)/len(results)*100:.1f}%)")
        print(f"Temps total: {total_time:.2f}s")
        print(f"Temps moyen: {total_time/len(results):.3f}s")
        
        if skipped > 0:
            print(f"\nInstances ignorées/non terminées: {skipped}")
        
        # Sauvegarder les résultats
        save_results = input("\nVoulez-vous sauvegarder les résultats? (o/n): ").lower()
        if save_results == 'o':
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            results_file = f"benchmark_results_{timestamp}.csv"
            with open(results_file, 'w') as f:
                f.write("filename,num_variables,num_clauses,satisfiable,time,backtracks,verified\n")
                for r in results:
                    f.write(f"{r['filename']},{r['num_variables']},{r['num_clauses']},"
                           f"{r['satisfiable']},{r['time']},{r['backtracks']},{r['verified']}\n")
            print(f"✓ Résultats sauvegardés dans: {results_file}")
        
        print("="*70)
        
        return results
    else:
        print("\n⚠️  Aucun résultat à afficher")
        return []


def analyze_specific_instance(filename):
    """
    Analyse détaillée d'une instance spécifique
    """
    print("\n" + "="*70)
    print("ANALYSE DÉTAILLÉE D'UNE INSTANCE")
    print("="*70)
    
    # Afficher les informations
    print_dimacs_info(filename)
    
    # Tester
    result = test_satlib_instance(filename, verbose=True)
    
    if result and result['satisfiable']:
        print("\n" + "="*70)
        print("AFFECTATION TROUVÉE")
        print("="*70)
        
        # Relire et résoudre pour afficher l'affectation
        clauses, num_vars = read_dimacs_cnf(filename)
        solver = SAT3Solver(clauses, num_vars)
        success, assignment, stats = solver.solve()
        
        # Afficher quelques variables
        print("\nPremières 20 variables:")
        for var in sorted(assignment.keys())[:20]:
            value = "vrai" if assignment[var] else "faux"
            print(f"  x{var} = {value}")
        
        if num_vars > 20:
            print(f"  ... ({num_vars - 20} variables supplémentaires)")


if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == "--help" or arg == "-h":
            print(__doc__)
            download_instructions()
        
        elif arg == "--generate" or arg == "-g":
            generate_test_instances()
        
        elif arg == "--info" or arg == "-i":
            if len(sys.argv) > 2:
                print_dimacs_info(sys.argv[2])
            else:
                print("Usage: python test_satlib.py --info <fichier.cnf>")
        
        elif arg == "--analyze" or arg == "-a":
            if len(sys.argv) > 2:
                analyze_specific_instance(sys.argv[2])
            else:
                print("Usage: python test_satlib.py --analyze <fichier.cnf>")
        
        elif arg.endswith('.cnf'):
            # Test d'un fichier spécifique
            test_satlib_instance(arg, verbose=True)
        
        elif arg == "--menu" or arg == "-m":
            # Mode menu interactif
            run_benchmark_with_choice()
        
        else:
            print(f"Option inconnue: {arg}")
            print("Utilisez --help pour voir les options disponibles")
    
    else:
        # Mode menu interactif par défaut
        print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    BENCHMARK 3-SAT - MENU INTERACTIF                ║
╚══════════════════════════════════════════════════════════════════════╝

Options disponibles:
  python test_satlib.py                  → Menu interactif (défaut)
  python test_satlib.py --menu           → Menu interactif
  python test_satlib.py --generate       → Générer des instances
  python test_satlib.py --help           → Aide et instructions
  python test_satlib.py fichier.cnf      → Tester un fichier spécifique
  python test_satlib.py --analyze file   → Analyse détaillée
  python test_satlib.py --info file      → Informations sur un fichier

════════════════════════════════════════════════════════════════════════
""")
        
        run_benchmark_with_choice()
    

    print("\nFin du programme.")
