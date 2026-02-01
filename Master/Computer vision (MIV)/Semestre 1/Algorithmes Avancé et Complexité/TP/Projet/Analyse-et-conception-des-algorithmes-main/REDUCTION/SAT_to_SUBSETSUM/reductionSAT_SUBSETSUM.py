

import sys
import os
from typing import List, Tuple, Dict, Set

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import conditionnel
try:
    from verify_SAT import parse_dimacs
    from solve_SAT import solve_SAT_backtracking
    IMPORTS_OK = True
except ImportError:
    print("⚠️ Modules SAT non trouvés")
    IMPORTS_OK = False


def clauses_to_integers(clauses):
    """
    Convertit les clauses du format (var, neg) vers format entier signé
    """
    result = []
    for clause in clauses:
        int_clause = []
        for var, neg in clause:
            literal = -var if neg else var
            int_clause.append(literal)
        result.append(int_clause)
    return result


def assignment_dict_to_standard(assignment_dict):
    """
    Convertit {'x1': True, 'x2': False} → {1: True, 2: False}
    """
    result = {}
    for key, val in assignment_dict.items():
        if isinstance(key, str) and key.startswith('x'):
            var_num = int(key[1:])
            result[var_num] = val
        elif isinstance(key, int):
            result[key] = val
    return result

def encode_sat_to_subsetsum(formula: List[List[int]]) -> Tuple[List[int], int, Dict]:
    """
    Encode une formule SAT en instance SUBSETSUM
    formula: Liste de clauses, format [[1, -2], [-1, 3], ...] 
    Returne:
        (S, T, mapping) où:
        S: ensemble d'entiers
        T: valeur cible
    """
    if not formula:
        return [], 0, {}
    
    # Identifier toutes les variables
    variables = set()
    for clause in formula:
        for literal in clause:
            variables.add(abs(literal))
    
    n = len(variables)  # nombre de variables
    m = len(formula)    # nombre de clauses
    
    # Base 10 pour éviter les retenues
    base = 10
    
    S = []
    mapping = {}
    index = 0
    
 
    print(f"  Variables: {n}, Clauses: {m}")
    print(f"  Format: [{n} digits vars][{m} digits clauses]")
    
    # Pour chaque variable xi
    for var in sorted(variables):
        # Nombre pour xi = vrai
        num_true = 0
        
        # Digit 1 à la position de la variable (partie gauche)
        num_true += base ** (n + m - var)
        
        # Digit 1 pour chaque clause où xi apparaît positivement
        for j, clause in enumerate(formula):
            if var in clause:
                num_true += base ** (m - j - 1)
        
        S.append(num_true)
        mapping[index] = (var, True)
        index += 1
        
        # Nombre pour xi = faux (¬xi)
        num_false = 0
        
        # Digit 1 à la position de la variable
        num_false += base ** (n + m - var)
        
        # Digit 1 pour chaque clause où ¬xi apparaît
        for j, clause in enumerate(formula):
            if -var in clause:
                num_false += base ** (m - j - 1)
        
        S.append(num_false)
        mapping[index] = (var, False)
        index += 1
    
    # Pour chaque clause Cj, ajouter 2 nombres de slack
    for j in range(m):
        # Premier slack: 1 à la position de la clause
        slack1 = base ** (m - j - 1)
        S.append(slack1)
        mapping[index] = ('slack', j, 1)
        index += 1
        
        # Deuxième slack: 1 à la position de la clause
        slack2 = base ** (m - j - 1)
        S.append(slack2)
        mapping[index] = ('slack', j, 2)
        index += 1
    
    # Calculer la cible T
    T = 0
    # n digits "1" pour les variables
    for i in range(1, n + 1):
        T += base ** (n + m - i)
    # m digits "3" pour les clauses
    for j in range(m):
        T += 3 * (base ** (m - j - 1))
    
    print(f"  Taille de S: {len(S)} nombres")
    print(f"  Cible T: {T}")
    print(f"  Plus grand nombre: {max(S) if S else 0}")
    
    return S, T, mapping


def decode_subsetsum_to_sat(subset_indices: List[int], mapping: Dict, 
                            num_vars: int) -> Dict[int, bool]:
    """
    Décode une solution SUBSETSUM en affectation SAT
    """
    assignment = {}
    
    for idx in subset_indices:
        if idx not in mapping:
            continue
            
        info = mapping[idx]
        
        # Si c'est une variable (pas un slack)
        if isinstance(info, tuple) and len(info) == 2:
            var, value = info
            if isinstance(var, int):
                assignment[var] = value
    
    return assignment

def verify_sat_assignment(formula: List[List[int]], assignment: Dict[int, bool]) -> bool:
    """
    Vérifie si une affectation satisfait la formule SAT
    Returner True si toutes les clauses sont satisfaites
    """
    for clause in formula:
        clause_satisfied = False
        for literal in clause:
            var = abs(literal)
            is_positive = literal > 0
            
            if var in assignment:
                var_value = assignment[var]
                # Littéral positif : vrai si var=True
                # Littéral négatif : vrai si var=False
                if is_positive and var_value:
                    clause_satisfied = True
                    break
                elif not is_positive and not var_value:
                    clause_satisfied = True
                    break
        
        if not clause_satisfied:
            return False
    
    return True


def verify_subsetsum_solution(S: List[int], subset_indices: List[int], T: int) -> bool:
    """
    Vérifie si un sous-ensemble donne la bonne somme
    """
    total = sum(S[i] for i in subset_indices if i < len(S))
    return total == T

def solve_subsetsum_dp(S: List[int], T: int) -> Tuple[bool, List[int]]:
    """
    Résout SUBSETSUM par programmation dynamique
    """
    n = len(S)
    
    if T == 0:
        return True, []
    
    if T < 0 or n == 0:
        return False, []
    
    # DP table
    dp = [[False] * (T + 1) for _ in range(n + 1)]
    
    # Somme 0 toujours possible
    for i in range(n + 1):
        dp[i][0] = True
    
    # Remplir la table
    for i in range(1, n + 1):
        for j in range(1, T + 1):
            # Sans prendre S[i-1]
            dp[i][j] = dp[i-1][j]
            
            # En prenant S[i-1] si possible
            if S[i-1] <= j:
                dp[i][j] = dp[i][j] or dp[i-1][j - S[i-1]]
    
    # Pas de solution
    if not dp[n][T]:
        return False, []
    
    # Backtracking pour retrouver les indices
    solution_indices = []
    i, j = n, T
    
    while i > 0 and j > 0:
        # Si on ne pouvait pas faire j sans S[i-1], alors on l'a pris
        if not dp[i-1][j]:
            solution_indices.append(i - 1)  # Index dans S
            j -= S[i-1]
        i -= 1
    
    solution_indices.reverse()
    return True, solution_indices

def reduce_and_solve(cnf_file: str):
    """
    Pipeline complet: SAT → SUBSETSUM → Solution SAT
    """

    if not IMPORTS_OK:
        return
    
    # 1. Parser le fichier DIMACS
    print(f"\n1️ Lecture: {cnf_file}")
    variables, clauses = parse_dimacs(cnf_file)
    
    if not variables or not clauses:
        return
    
    print(f" {len(variables)} variables, {len(clauses)} clauses")
    
    # Convertir au format entier
    formula_int = clauses_to_integers(clauses)
    print(f"   Format original {clauses[0] if clauses else 'vide'}")
    print(f"   Format entier {formula_int[0] if formula_int else 'vide'}")
    
    # Résoudre SAT avec backtracking
    sat_solution_dict = solve_SAT_backtracking(variables, clauses)
    
    if sat_solution_dict:
        sat_solution = assignment_dict_to_standard(sat_solution_dict)
     
        print(f"   Solution SAT: {sat_solution}")
    else:
        sat_solution = None
        
    
    # Réduction SAT → SUBSETSUM
    S, T, mapping = encode_sat_to_subsetsum(formula_int)
    
    print(f"\n   Instance SUBSETSUM générée:")
    print(f"   S = {S[:6]}{'...' if len(S) > 6 else ''}")
    print(f"   T = {T}")
    
    #  Résoudre SUBSETSUM

    success, subset_indices = solve_subsetsum_dp(S, T)
    
    if success:
      
        print(f"   Sous-ensemble: {len(subset_indices)} éléments")
        
        # Vérifier la somme
        total = sum(S[i] for i in subset_indices)
        print(f"   Vérification somme: {total} = {T} ? {total == T}")
        
        #Décoder en solution SAT
     
        decoded_sat = decode_subsetsum_to_sat(subset_indices, mapping, len(variables))
        print(f"   Solution décodée: {decoded_sat}")
        
        #Vérifier que la solution décodée satisfait SAT
        
        is_valid = verify_sat_assignment(formula_int, decoded_sat)
        print(f"   Solution valide pour SAT: {is_valid}")
        
        if is_valid:
            print(f"CORRECTE")
        else:
            print(f"Problème de décodage")
        
    else:
        print(f" SUBSETSUM INSATISFAISABLE")
        if sat_solution:
            print(f"   INCOHÉRENCE: SAT satisfaisable mais SUBSETSUM non")

def test_simple_examples():
   # Tests avec exemples simples
   
 
    
    # Formule satisfaisable simple
    print("\n[Test 1] (x1 ∨ ¬x2) ∧ (¬x1 ∨ x3) ∧ (x2 ∨ x3)")
    formula1 = [[1, -2], [-1, 3], [2, 3]]
    
    S, T, mapping = encode_sat_to_subsetsum(formula1)
    success, indices = solve_subsetsum_dp(S, T)
    
    if success:
        decoded = decode_subsetsum_to_sat(indices, mapping, 3)
        is_valid = verify_sat_assignment(formula1, decoded)
        print(f"Solution: {decoded}")
        print(f"Valide: {is_valid} " if is_valid else "❌")
    
    #  Formule UNSAT
    print("\n[Test 2] (x1) ∧ (¬x1)")
    formula2 = [[1], [-1]]
    
    S2, T2, mapping2 = encode_sat_to_subsetsum(formula2)
    success2, indices2 = solve_subsetsum_dp(S2, T2)
    
    print(f"SUBSETSUM satisfaisable: {success2}")
    print(f"Attendu: False " if not success2 else "❌")

def main():
   
    
    # Tests simples
    test_simple_examples()
    
    # Test avec fichier DIMACS
    test_file = "random_3_5.cnf"
    
    if os.path.exists(test_file):
        print("\n[Pipeline complet avec fichier DIMACS]")
        reduce_and_solve(test_file)
    else:
        print(f"\n Fichier {test_file} non trouvé")
      
    
    print("\nTests terminés!")


if __name__ == "__main__":
    main()