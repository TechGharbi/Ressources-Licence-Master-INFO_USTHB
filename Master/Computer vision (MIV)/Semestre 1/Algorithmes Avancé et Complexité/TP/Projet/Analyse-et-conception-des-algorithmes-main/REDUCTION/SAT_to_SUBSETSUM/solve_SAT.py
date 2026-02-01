# solve_SAT.py
import itertools
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importer la fonction d'évaluation depuis verify_SAT
from verify_SAT import evaluate_clause, parse_dimacs, verify_SAT_solution

def solve_SAT_bruteforce(variables, clauses):
    """
    Résout SAT par recherche exhaustive (bruteforce).
    Retourne la première affectation trouvée ou None.
    """
    n = len(variables)
    for bits in itertools.product([False, True], repeat=n):
        assignment = {variables[i]: bits[i] for i in range(n)}
        # Vérification simplifiée avec verify_SAT_solution
        if verify_SAT_solution(variables, clauses, assignment):
            return assignment
    return None

def solve_SAT_backtracking(variables, clauses, assignment=None, index=0):
    """
    Résout SAT par backtracking.
    """
    if assignment is None:
        assignment = {}
    
    if index == len(variables):
        # Vérifier si l'affectation satisfait toutes les clauses
        if verify_SAT_solution(variables, clauses, assignment):
            return assignment.copy()
        else:
            return None
    
    var = variables[index]
    
    # Essayer var = True
    assignment[var] = True
    res = solve_SAT_backtracking(variables, clauses, assignment, index + 1)
    if res is not None:
        return res
    
    # Essayer var = False
    assignment[var] = False
    res = solve_SAT_backtracking(variables, clauses, assignment, index + 1)
    if res is not None:
        return res
    
    # Backtrack
    del assignment[var]
    return None

def main():
    print("=== Solveur SAT ===")
    
    # Test avec un fichier DIMACS
    test_file = "data/test_cases/sat_tests/random_3_5.cnf"
    
    variables, clauses = parse_dimacs(test_file)
    if not variables or not clauses:
        print("Erreur: Impossible de parser le fichier.")
        return
    
    print(f"Instance: {len(variables)} variables, {len(clauses)} clauses")
    print("Clauses parsées :", clauses)
    print("Nombre de clauses :", len(clauses))

    
    # Résolution par bruteforce
    print("\n1. Résolution par bruteforce...")
    solution_bf = solve_SAT_bruteforce(variables, clauses)
    if solution_bf:
        print(f"Solution trouvée: {solution_bf}")
    else:
        print("Aucune solution trouvée.")
    
    # Résolution par backtracking
    print("\n2. Résolution par backtracking...")
    solution_bt = solve_SAT_backtracking(variables, clauses)
    if solution_bt:
        print(f"Solution trouvée: {solution_bt}")
    else:
        print("Aucune solution trouvée.")

if __name__ == "__main__":
    main()