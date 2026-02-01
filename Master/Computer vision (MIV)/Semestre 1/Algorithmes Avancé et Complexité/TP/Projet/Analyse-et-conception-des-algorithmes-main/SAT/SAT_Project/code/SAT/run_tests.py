# run_tests.py
import os
import sys
import time
import itertools
import random

# Ajouter le dossier parent au chemin pour pouvoir importer les modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importer les fonctions de solve_SAT
try:
    from solve_SAT import solve_SAT_bruteforce, solve_SAT_backtracking, parse_dimacs
    from verify_SAT import verify_SAT_solution
except ImportError as e:
    print(f"Erreur d'importation: {e}")
    print("Assure-toi que solve_SAT.py et verify_SAT.py sont dans le même dossier.")
    sys.exit(1)

def test_simple_example():
    """Test avec un exemple simple manuel."""
    print("=== Test 1: Exemple manuel simple ===")
    
    variables = ['x1', 'x2', 'x3']
    clauses = [
        [('x1', False), ('x2', True)],   # (x1 ∨ ¬x2)
        [('x1', True), ('x3', False)],   # (¬x1 ∨ x3)
        [('x2', False), ('x3', False)]   # (x2 ∨ x3)
    ]
    
    print(f"Variables: {variables}")
    print(f"Nombre de clauses: {len(clauses)}")
    
    # Test de vérification
    print("\n--- Test de vérification ---")
    assignment_correct = {'x1': True, 'x2': False, 'x3': True}
    is_valid = verify_SAT_solution(variables, clauses, assignment_correct)
    print(f"Affectation testée: {assignment_correct}")
    print(f"Résultat vérification: {is_valid} (attendu: True)")
    
    assignment_wrong = {'x1': False, 'x2': False, 'x3': False}
    is_valid = verify_SAT_solution(variables, clauses, assignment_wrong)
    print(f"\nAffectation testée: {assignment_wrong}")
    print(f"Résultat vérification: {is_valid} (attendu: False)")
    
    # Test de résolution
    print("\n--- Test de résolution ---")
    print("1. Méthode bruteforce:")
    start_time = time.time()
    solution_bf = solve_SAT_bruteforce(variables, clauses)
    elapsed = time.time() - start_time
    print(f"Solution trouvée: {solution_bf}")
    print(f"Temps écoulé: {elapsed:.6f} secondes")
    
    print("\n2. Méthode backtracking:")
    start_time = time.time()
    solution_bt = solve_SAT_backtracking(variables, clauses)
    elapsed = time.time() - start_time
    print(f"Solution trouvée: {solution_bt}")
    print(f"Temps écoulé: {elapsed:.6f} secondes")
    
    return True

def test_from_cnf_file():
    """Test avec un fichier CNF."""
    print("\n\n=== Test 2: Lecture depuis fichier CNF ===")
    
    # Chemin vers le fichier de test
    test_file = os.path.join("..", "data", "test_cases", "sat_tests", "random_3_5.cnf")
    
    if not os.path.exists(test_file):
        print(f"Fichier {test_file} non trouvé!")
        print("Création du fichier de test...")
        
        # Créer le dossier s'il n'existe pas
        os.makedirs(os.path.dirname(test_file), exist_ok=True)
        
        # Créer un fichier CNF simple
        with open(test_file, 'w') as f:
            f.write("c Exemple SAT simple\n")
            f.write("p cnf 3 3\n")
            f.write("1 -2 0\n")
            f.write("-1 3 0\n")
            f.write("2 -3 0\n")
        print(f"Fichier créé: {test_file}")
    
    print(f"Lecture du fichier: {test_file}")
    
    # Parser le fichier
    variables, clauses = parse_dimacs(test_file)
    
    if not variables or not clauses:
        print("Erreur: Impossible de parser le fichier.")
        return False
    
    print(f"Variables trouvées: {variables}")
    print(f"Nombre de clauses: {len(clauses)}")
    print(f"Clauses: {clauses}")
    
    # Tester différentes méthodes
    print("\n--- Résolution du fichier CNF ---")
    
    methods = [
        ("Bruteforce", solve_SAT_bruteforce),
        ("Backtracking", solve_SAT_backtracking)
    ]
    
    for method_name, method_func in methods:
        print(f"\n{method_name}:")
        start_time = time.time()
        solution = method_func(variables, clauses)
        elapsed = time.time() - start_time
        
        if solution:
            print(f"  Solution trouvée: {solution}")
            # Vérifier la solution
            is_valid = verify_SAT_solution(variables, clauses, solution)
            print(f"  Vérification: {is_valid}")
        else:
            print("  Aucune solution trouvée")
        
        print(f"  Temps: {elapsed:.6f} secondes")
    
    return True

def benchmark_different_sizes():
    """Benchmark avec différentes tailles d'instances.  """
    print("\n\n=== Test 3: Benchmark avec différentes tailles ===")
    
    # Générer des instances de différentes tailles
    sizes = [
        (3, 5),   # 3 variables, 5 clauses
        (5, 10),  # 5 variables, 10 clauses
        (7, 15),  # 7 variables, 15 clauses
        # (10, 20)  # 10 variables, 20 clauses (peut être long en bruteforce)
    ]
    
    print("Taille (vars, clauses) | Bruteforce (s) | Backtracking (s) | Solution")
    print("-" * 70)
    
    for n_vars, n_clauses in sizes:
        print(f"({n_vars}, {n_clauses})", end="")
        
        # Générer une instance aléatoire
        variables = [f'x{i+1}' for i in range(n_vars)]
        clauses = []
        
        
        for _ in range(n_clauses):
            # Choisir 2-3 variables aléatoires
            k = random.randint(2, 3)
            chosen_vars = random.sample(range(1, n_vars + 1), k)
            clause = []
            for var in chosen_vars:
                neg = random.choice([True, False])
                clause.append((var, neg))
            clauses.append(clause)
        
        # Test bruteforce
        start_time = time.time()
        solution_bf = solve_SAT_bruteforce(variables, clauses)
        time_bf = time.time() - start_time
        
        # Test backtracking
        start_time = time.time()
        solution_bt = solve_SAT_backtracking(variables, clauses)
        time_bt = time.time() - start_time
        
        print(f" | {time_bf:9.6f} | {time_bt:9.6f} | ", end="")
        
        if solution_bf:
            print("Oui")
        else:
            print("Non")
    
    return True

def run_benchmark_and_plots():
    """Exécute le benchmark et génère les graphiques."""
    print("\n" + "=" * 60)
    print("BENCHMARK ET GRAPHIQUES")
    print("=" * 60)
    
    try:
        # Importer le module de benchmark
        from benchmark_SAT import run_benchmark, save_results, plot_performance_comparison
        
        print("Génération des instances de test...")
        from generate_test_instances import generate_test_instances
        generate_test_instances()
        
        print("\nExécution du benchmark...")
        results = run_benchmark(max_vars=10, repetitions=2)
        
        print("\nGénération des graphiques...")
        plot_performance_comparison(results)
        
        print("\n✓ Benchmark et graphiques générés avec succès!")
        print("Les graphiques sont sauvegardés dans report/images/")
        
    except ImportError as e:
        print(f"Erreur: {e}")
        print("Assure-toi que benchmark_SAT.py est dans le même dossier.")
    except Exception as e:
        print(f"Erreur lors du benchmark: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Fonction principale."""
    print("=" * 60)
    print("TEST COMPLET DU MODULE SAT")
    print("=" * 60)
    
    print("\nOptions disponibles:")
    print("1. Tests de base")
    print("2. Benchmark et graphiques")
    
    choice = input("\nChoisissez une option (1 ou 2): ")
    
    if choice == "1":
        # Tests de base (comme avant)
        tests = [
            ("Exemple simple", test_simple_example),
            ("Fichier CNF", test_from_cnf_file),
            ("Benchmark", benchmark_different_sizes)
        ]
        
        all_passed = True
        for test_name, test_func in tests:
            try:
                print(f"\n Exécution du test: {test_name}")
                print("-" * 40)
                if test_func():
                    print(f" Test '{test_name}' réussi")
                else:
                    print(f" Test '{test_name}' échoué")
                    all_passed = False
            except Exception as e:
                print(f" Erreur lors du test '{test_name}': {e}")
                import traceback
                traceback.print_exc()
                all_passed = False
        
        print("\n" + "=" * 60)
        if all_passed:
            print(" TOUS LES TESTS ONT RÉUSSI")
        else:
            print(" CERTAINS TESTS ONT ÉCHOUÉ")
    
    elif choice == "2":
        # Benchmark et graphiques
        run_benchmark_and_plots()
    
    else:
        print("Option invalide. Sélectionnez 1 ou 2.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()