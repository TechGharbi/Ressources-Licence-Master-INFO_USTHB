class SAT3Solver:
    def __init__(self, clauses, num_variables):
        self.clauses = clauses
        self.num_variables = num_variables
        self.assignment = {}  # Affectation courante: {var: True/False}
        self.solutions_found = []
        self.backtrack_count = 0  # Pour les statistiques
        
    def evaluate_literal(self, literal):
        """Évalue un littéral avec l'affectation courante"""
        var = abs(literal)
        if var not in self.assignment:
            return None  # Variable non encore affectée
        
        value = self.assignment[var]
        # Si literal positif, retourne la valeur; si négatif, retourne NOT valeur
        return value if literal > 0 else not value
    
    def evaluate_clause(self, clause):
        """
        Évalue une clause (disjonction de littéraux)
        Retourne: True si satisfaite, False si insatisfaite, None si indéterminée
        """
        has_true = False
        has_unassigned = False
        
        for literal in clause:
            val = self.evaluate_literal(literal)
            if val is True:
                return True  # Au moins un littéral vrai → clause satisfaite
            elif val is None:
                has_unassigned = True
        
        if has_unassigned:
            return None  # Clause indéterminée
        return False  # Tous les littéraux sont faux → clause insatisfaite
    
    def is_satisfied(self):
        """Vérifie si toutes les clauses sont satisfaites"""
        for clause in self.clauses:
            if self.evaluate_clause(clause) != True:
                return False
        return True
    
    def has_conflict(self):
        """Vérifie s'il y a un conflit (une clause insatisfaite)"""
        for clause in self.clauses:
            if self.evaluate_clause(clause) == False:
                return True
        return False
    
    def select_variable(self):
        """
        Sélectionne la prochaine variable non affectée
        Stratégie simple: prend la première non affectée
        """
        for var in range(1, self.num_variables + 1):
            if var not in self.assignment:
                return var
        return None
    
    def backtrack(self):
        """
        Algorithme de backtracking récursif
        Retourne True si une solution est trouvée, False sinon
        """
        self.backtrack_count += 1
        
        # Cas de base: toutes les variables sont affectées
        if len(self.assignment) == self.num_variables:
            if self.is_satisfied():
                return True
            return False
        
        # Détection précoce de conflit
        if self.has_conflict():
            return False
        
        # Sélectionner la prochaine variable
        var = self.select_variable()
        if var is None:
            return self.is_satisfied()
        
        # Essayer var = True
        self.assignment[var] = True
        if self.backtrack():
            return True
        
        # Essayer var = False
        self.assignment[var] = False
        if self.backtrack():
            return True
        
        # Backtrack: retirer l'affectation
        del self.assignment[var]
        return False
    
    def solve(self):
        """
        Lance la résolution
        
        Returns:
            tuple: (success, assignment, stats)
                success: True si solution trouvée
                assignment: dictionnaire {variable: valeur} ou None
                stats: dictionnaire avec statistiques
        """
        self.assignment = {}
        self.backtrack_count = 0
        
        success = self.backtrack()
        
        stats = {
            'backtrack_count': self.backtrack_count,
            'num_variables': self.num_variables,
            'num_clauses': len(self.clauses)
        }
        
        if success:
            return True, dict(self.assignment), stats
        else:
            return False, None, stats
    
    def solve_all(self, max_solutions=10):
        """
        Trouve toutes les solutions (ou jusqu'à max_solutions)
        
        Returns:
            list: Liste des affectations solutions
        """
        self.solutions_found = []
        self._backtrack_all(max_solutions)
        return self.solutions_found
    
    def _backtrack_all(self, max_solutions):
        """Backtracking pour trouver toutes les solutions"""
        if len(self.solutions_found) >= max_solutions:
            return
        
        if len(self.assignment) == self.num_variables:
            if self.is_satisfied():
                self.solutions_found.append(dict(self.assignment))
            return
        
        if self.has_conflict():
            return
        
        var = self.select_variable()
        if var is None:
            return
        
        # Essayer var = True
        self.assignment[var] = True
        self._backtrack_all(max_solutions)
        
        # Essayer var = False
        self.assignment[var] = False
        self._backtrack_all(max_solutions)
        
        # Backtrack
        del self.assignment[var]


def read_3sat_from_file(filename, format='auto'):
    """
    Lit une instance 3-SAT depuis un fichier
    Supporte les formats: simple, DIMACS CNF
    
    Args:
        filename: nom du fichier
        format: 'simple', 'dimacs', ou 'auto' (détection automatique)
    
    Format simple:
    3
    3
    1 -2 3
    -1 2 -3
    1 2 3
    
    Format DIMACS CNF:
    c Commentaires
    p cnf 3 3
    1 -2 3 0
    -1 2 -3 0
    1 2 3 0
    """
    # Détection automatique du format
    if format == 'auto':
        with open(filename, 'r') as f:
            first_line = f.readline().strip()
            if first_line.startswith('c') or first_line.startswith('p'):
                format = 'dimacs'
            else:
                format = 'simple'
    
    if format == 'dimacs':
        # Utiliser le lecteur DIMACS
        try:
            from dimacs_reader import read_dimacs_cnf
            clauses, num_variables = read_dimacs_cnf(filename)
            
            # Filtrer pour ne garder que les clauses de taille 3
            clauses_3sat = [c for c in clauses if len(c) == 3]
            if len(clauses_3sat) < len(clauses):
                print(f"⚠️  {len(clauses) - len(clauses_3sat)} clauses ignorées (pas 3 littéraux)")
            
            return clauses_3sat, num_variables
        except ImportError:
            print("⚠️  Module dimacs_reader non trouvé, utilisation du format simple")
            format = 'simple'
    
    if format == 'simple':
        # Format simple original
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        num_variables = int(lines[0].strip())
        num_clauses = int(lines[1].strip())
        
        clauses = []
        for i in range(2, 2 + num_clauses):
            literals = list(map(int, lines[i].strip().split()))
            if len(literals) != 3:
                raise ValueError(f"Clause {i-1} n'a pas exactement 3 littéraux: {literals}")
            clauses.append(literals)
        
        return clauses, num_variables


def write_solution_to_file(filename, success, assignment, stats):
    """Écrit la solution dans un fichier"""
    with open(filename, 'w') as f:
        if success:
            f.write("SATISFIABLE\n")
            f.write("Affectation:\n")
            for var in sorted(assignment.keys()):
                value = "vrai" if assignment[var] else "faux"
                f.write(f"  x{var} = {value}\n")
        else:
            f.write("INSATISFIABLE\n")
        
        f.write("\nStatistiques:\n")
        f.write(f"  Nombre de backtracks: {stats['backtrack_count']}\n")
        f.write(f"  Nombre de variables: {stats['num_variables']}\n")
        f.write(f"  Nombre de clauses: {stats['num_clauses']}\n")


if __name__ == "__main__":
    # Exemple d'utilisation
    print("=== Exemple 3-SAT Solver ===\n")
    
    # Exemple de l'énoncé: F = (x₁ ∨ ¬x₂ ∨ x₃) ∧ (¬x₁ ∨ x₂ ∨ ¬x₃) ∧ (x₁ ∨ x₂ ∨ x₃)
    clauses = [
        [1, -2, 3],   # (x₁ ∨ ¬x₂ ∨ x₃)
        [-1, 2, -3],  # (¬x₁ ∨ x₂ ∨ ¬x₃)
        [1, 2, 3]     # (x₁ ∨ x₂ ∨ x₃)
    ]
    num_variables = 3
    
    print("Formule:")
    for i, clause in enumerate(clauses, 1):
        print(f"  C{i}: {clause}")
    
    solver = SAT3Solver(clauses, num_variables)
    success, assignment, stats = solver.solve()
    
    print("\nRésultat:")
    if success:
        print("✓ SATISFIABLE")
        print("\nAffectation trouvée:")
        for var in sorted(assignment.keys()):
            value = "vrai" if assignment[var] else "faux"
            print(f"  x{var} = {value}")
    else:
        print("✗ INSATISFIABLE")
    
    print(f"\nStatistiques:")
    print(f"  Backtracks: {stats['backtrack_count']}")
    print(f"  Variables: {stats['num_variables']}")
    print(f"  Clauses: {stats['num_clauses']}")
