"""
Vérificateur pour le problème 3-SAT
Vérifie si une affectation donnée satisfait une formule 3-SAT
"""

class SAT3Verifier:
    def __init__(self, clauses):
        """
        Initialise le vérificateur
        
        Args:
            clauses: Liste de clauses, chaque clause est une liste de 3 littéraux
        """
        self.clauses = clauses
    
    def evaluate_literal(self, literal, assignment):
        """
        Évalue un littéral avec une affectation donnée
        
        Args:
            literal: entier (positif ou négatif)
            assignment: dictionnaire {variable: True/False}
        
        Returns:
            True/False selon l'évaluation du littéral
        """
        var = abs(literal)
        
        if var not in assignment:
            raise ValueError(f"Variable x{var} non affectée dans l'assignment")
        
        value = assignment[var]
        
        # Si littéral positif, retourne la valeur
        # Si littéral négatif, retourne NOT valeur
        return value if literal > 0 else not value
    
    def evaluate_clause(self, clause, assignment):
        """
        Évalue une clause (disjonction de littéraux)
        
        Args:
            clause: liste de 3 littéraux
            assignment: dictionnaire {variable: True/False}
        
        Returns:
            True si au moins un littéral est vrai, False sinon
        """
        for literal in clause:
            if self.evaluate_literal(literal, assignment):
                return True  # Au moins un littéral vrai → clause satisfaite
        
        return False  # Tous les littéraux sont faux
    
    def verify(self, assignment):
        """
        Vérifie si l'affectation satisfait toutes les clauses
        
        Args:
            assignment: dictionnaire {variable: True/False}
        
        Returns:
            tuple: (is_valid, details)
                is_valid: True si toutes les clauses sont satisfaites
                details: dictionnaire avec les détails de vérification
        """
        unsatisfied_clauses = []
        satisfied_clauses = []
        
        for i, clause in enumerate(self.clauses):
            try:
                if self.evaluate_clause(clause, assignment):
                    satisfied_clauses.append(i)
                else:
                    unsatisfied_clauses.append(i)
            except ValueError as e:
                return False, {
                    'error': str(e),
                    'clause_index': i,
                    'clause': clause
                }
        
        is_valid = len(unsatisfied_clauses) == 0
        
        details = {
            'total_clauses': len(self.clauses),
            'satisfied_clauses': len(satisfied_clauses),
            'unsatisfied_clauses': unsatisfied_clauses,
            'success_rate': len(satisfied_clauses) / len(self.clauses) * 100
        }
        
        return is_valid, details
    
    def verify_verbose(self, assignment):
        """
        Vérifie avec affichage détaillé de chaque clause
        
        Args:
            assignment: dictionnaire {variable: True/False}
        
        Returns:
            bool: True si toutes les clauses sont satisfaites
        """
        print("=== Vérification détaillée ===\n")
        
        all_satisfied = True
        
        for i, clause in enumerate(self.clauses, 1):
            print(f"Clause {i}: {clause}")
            
            literals_eval = []
            clause_satisfied = False
            
            for literal in clause:
                var = abs(literal)
                is_negated = literal < 0
                var_value = assignment.get(var)
                
                if var_value is None:
                    print(f"  ERREUR: Variable x{var} non affectée!")
                    all_satisfied = False
                    break
                
                literal_value = (not var_value) if is_negated else var_value
                literals_eval.append(literal_value)
                
                neg_str = "¬" if is_negated else ""
                val_str = "V" if literal_value else "F"
                print(f"  {neg_str}x{var} = {val_str}", end="")
                
                if literal_value:
                    clause_satisfied = True
                    print(" ✓")
                    break
                else:
                    print()
            
            if clause_satisfied:
                print(f"  → Clause SATISFAITE ✓\n")
            else:
                print(f"  → Clause INSATISFAITE ✗\n")
                all_satisfied = False
        
        return all_satisfied


def read_assignment_from_file(filename):
    """
    Lit une affectation depuis un fichier
    
    Format:
    x1 = True
    x2 = False
    x3 = True
    
    ou format court:
    1 0 1  (1=True, 0=False)
    """
    assignment = {}
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Format: x1 = True
        if '=' in line:
            parts = line.split('=')
            var_str = parts[0].strip().replace('x', '')
            value_str = parts[1].strip().lower()
            
            var = int(var_str)
            value = value_str in ['true', 'vrai', '1', 'yes', 'oui']
            
            assignment[var] = value
        
        # Format court: 1 0 1
        else:
            values = line.split()
            for i, val in enumerate(values, 1):
                assignment[i] = (val == '1')
    
    return assignment


def verify_from_files(clauses_file, assignment_file):
    """Vérifie une solution à partir de fichiers"""
    from solver_3sat import read_3sat_from_file
    
    clauses, num_variables = read_3sat_from_file(clauses_file)
    assignment = read_assignment_from_file(assignment_file)
    
    verifier = SAT3Verifier(clauses)
    is_valid, details = verifier.verify(assignment)
    
    return is_valid, details


if __name__ == "__main__":
    print("=== Exemple 3-SAT Verifier ===\n")
    
    # Exemple de l'énoncé
    clauses = [
        [1, -2, 3],   # (x₁ ∨ ¬x₂ ∨ x₃)
        [-1, 2, -3],  # (¬x₁ ∨ x₂ ∨ ¬x₃)
        [1, 2, 3]     # (x₁ ∨ x₂ ∨ x₃)
    ]
    
    # Affectation de l'énoncé: x1=faux, x2=faux, x3=vrai
    assignment_correct = {1: False, 2: False, 3: True}
    
    print("Formule:")
    for i, clause in enumerate(clauses, 1):
        print(f"  C{i}: {clause}")
    
    print(f"\nAffectation à vérifier:")
    for var in sorted(assignment_correct.keys()):
        value = "vrai" if assignment_correct[var] else "faux"
        print(f"  x{var} = {value}")
    
    print()
    
    verifier = SAT3Verifier(clauses)
    
    # Vérification simple
    is_valid, details = verifier.verify(assignment_correct)
    
    print("\nRésultat de vérification:")
    if is_valid:
        print("✓ L'affectation est VALIDE")
    else:
        print("✗ L'affectation est INVALIDE")
    
    print(f"\nDétails:")
    print(f"  Clauses satisfaites: {details['satisfied_clauses']}/{details['total_clauses']}")
    print(f"  Taux de succès: {details['success_rate']:.1f}%")
    
    if details['unsatisfied_clauses']:
        print(f"  Clauses insatisfaites: {details['unsatisfied_clauses']}")
    
    # Vérification verbose
    print("\n" + "="*50)
    verifier.verify_verbose(assignment_correct)
    
    # Test avec une mauvaise affectation
    print("\n" + "="*50)
    print("=== Test avec une affectation incorrecte ===\n")
    
    assignment_wrong = {1: True, 2: True, 3: False}
    
    print("Affectation incorrecte:")
    for var in sorted(assignment_wrong.keys()):
        value = "vrai" if assignment_wrong[var] else "faux"
        print(f"  x{var} = {value}")
    
    print()
    
    is_valid, details = verifier.verify(assignment_wrong)
    
    print("Résultat:")
    if is_valid:
        print("✓ L'affectation est VALIDE")
    else:
        print("✗ L'affectation est INVALIDE")
        print(f"  Clauses insatisfaites: {details['unsatisfied_clauses']}")