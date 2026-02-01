# verify_SAT.py
import sys
import os

def evaluate_clause(clause, assignment):
    """
    Évalue une clause avec l'affectation donnée.
    Retourne True si au moins un littéral est vrai.
    """
    for var, neg in clause:
        var_name = f'x{var}'
        val = assignment.get(var_name, False)
        if neg:
            val = not val
        if val:
            return True
    return False

def verify_SAT_solution(variables, clauses, assignment):
    """
    Vérifie si une affectation donnée satisfait toutes les clauses.
    Retourne True si oui, False sinon.
    """
    for clause in clauses:
        if not evaluate_clause(clause, assignment):
            return False
    return True

def parse_dimacs(filepath):
    """
    Lit un fichier DIMACS et retourne (variables, clauses).
    """
    clauses = []
    variables = set()
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('c'):
                    continue
                if line.startswith('p'):
                    continue  # On ignore la ligne d'en-tête pour simplifier
                literals = list(map(int, line.split()))
                if literals:
                    clause = []
                    for lit in literals:
                        if lit == 0:
                            continue
                        var = abs(lit)
                        neg = lit < 0
                        variables.add(f'x{var}')
                        clause.append((var, neg))
                    clauses.append(clause)
    except FileNotFoundError:
        print(f"Erreur: Fichier {filepath} non trouvé.")
        return None, None
    
    variables = sorted(variables, key=lambda x: int(x[1:]))
    return variables, clauses

def main():
    # Exemple de test simple
    print("=== Test de vérification SAT ===")
    
    # Test 1: Exemple manuel
    print("\nTest 1: Exemple manuel")
    variables = ['x1', 'x2', 'x3']
    clauses = [
        [('x1', False), ('x2', True)],   # (x1 ∨ ¬x2)
        [('x1', True), ('x3', False)]    # (¬x1 ∨ x3)
    ]
    
    # Affectation correcte
    assignment_correct = {'x1': True, 'x2': False, 'x3': True}
    result = verify_SAT_solution(variables, clauses, assignment_correct)
    print(f"Affectation correcte: {assignment_correct}")
    print(f"Vérification: {result} (attendu: True)")
    
    # Affectation incorrecte
    assignment_wrong = {'x1': False, 'x2': True, 'x3': False}
    result = verify_SAT_solution(variables, clauses, assignment_wrong)
    print(f"\nAffectation incorrecte: {assignment_wrong}")
    print(f"Vérification: {result} (attendu: False)")
    
    # Test 2: À partir d'un fichier DIMACS
    print("\nTest 2: Lecture depuis un fichier DIMACS")
    
    # Créer un fichier de test simple
    test_file = "data/test_cases/sat_tests/example.cnf"
    os.makedirs(os.path.dirname(test_file), exist_ok=True)
    
    with open(test_file, 'w') as f:
        f.write("c Exemple simple\n")
        f.write("p cnf 3 2\n")
        f.write("1 -2 0\n")
        f.write("-1 3 0\n")
    
    variables, clauses = parse_dimacs(test_file)
    if variables and clauses:
        print(f"Variables trouvées: {variables}")
        print(f"Clauses trouvées: {clauses}")
        
        # Tester avec la même affectation
        result = verify_SAT_solution(variables, clauses, assignment_correct)
        print(f"Affectation {assignment_correct} vérifiée: {result}")

if __name__ == "__main__":
    main()