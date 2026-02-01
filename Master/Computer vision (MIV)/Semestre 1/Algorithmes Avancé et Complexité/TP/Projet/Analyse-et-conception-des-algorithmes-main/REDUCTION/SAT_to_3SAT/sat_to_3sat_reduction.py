"""
RÉDUCTION SAT → 3-SAT (Complexité Linéaire O(n+m))
=====================================================
Implémente l'algorithme de réduction polynomial SAT vers 3-SAT

PRINCIPE DE LA RÉDUCTION:
-------------------------
Pour chaque clause SAT avec k littéraux, on applique une transformation
qui garantit que TOUTES les clauses résultantes ont EXACTEMENT 3 littéraux.

TRANSFORMATIONS SELON LA TAILLE k:
----------------------------------
• k=1: (x₁) 
  → 4 clauses 3-SAT + 2 variables auxiliaires
  
• k=2: (x₁ ∨ x₂)
  → 2 clauses 3-SAT + 1 variable auxiliaire
  
• k=3: (x₁ ∨ x₂ ∨ x₃)
  → 1 clause 3-SAT (déjà conforme, pas de transformation)
  
• k≥4: (x₁ ∨ x₂ ∨ ... ∨ xₖ)
  → (k-2) clauses 3-SAT + (k-3) variables auxiliaires
  
EXEMPLE k=5:
-----------
Entrée SAT:  (x₁ ∨ x₂ ∨ x₃ ∨ x₄ ∨ x₅)  ← 1 clause, 5 littéraux
Sortie 3-SAT:
  (x₁ ∨ x₂ ∨ y₁)         ← Clause 1: 3 littéraux ✓
  (¬y₁ ∨ x₃ ∨ y₂)        ← Clause 2: 3 littéraux ✓  
  (¬y₂ ∨ x₄ ∨ x₅)        ← Clause 3: 3 littéraux ✓
Résultat: 3 clauses, 2 variables auxiliaires (y₁, y₂)

COMPLEXITÉ:
----------
• Temporelle: O(n + m) où n=nombre de variables, m=nombre de clauses
• Spatiale: O(n + m)
• Linéaire car chaque clause est traitée une seule fois

AUTEUR: [Votre Nom]
DATE: Décembre 2024
"""

import time
import sys
import tracemalloc
from typing import List, Dict, Tuple, Set

# ============================================================================
# IMPORTS DU CODE EXISTANT
# ============================================================================

try:
    # Import du code SAT (pour parser et vérifier)
    from verify_SAT import parse_dimacs as parse_dimacs_sat
    from verify_SAT import evaluate_clause as evaluate_clause_sat
    from solve_SAT import solve_SAT_backtracking, solve_SAT_bruteforce
except ImportError as e:
    print(f"⚠️  ERREUR: Impossible d'importer le code SAT")
    print(f"   {e}")
    print("   Assurez-vous que verify_SAT.py et solve_SAT.py sont accessibles")
    sys.exit(1)

try:
    # Import du code 3-SAT (pour résoudre et vérifier)
    from solver_3sat import SAT3Solver
    from verifier_3sat import SAT3Verifier
except ImportError as e:
    print(f"⚠️  ERREUR: Impossible d'importer le code 3-SAT")
    print(f"   {e}")
    print("   Assurez-vous que solver_3sat.py et verifier_3sat.py sont accessibles")
    sys.exit(1)


# ============================================================================
# CLASSE PRINCIPALE: RÉDUCTEUR SAT → 3-SAT
# ============================================================================

class SATto3SATReducer:
    """
    Classe qui effectue la réduction d'une formule SAT en formule 3-SAT équivalente.
    
    PRINCIPE:
    --------
    Pour chaque clause SAT, on applique une transformation qui garantit que
    toutes les clauses résultantes ont EXACTEMENT 3 littéraux.
    
    ATTRIBUTS:
    ---------
    • next_aux_var: Compteur pour générer des variables auxiliaires uniques
    • auxiliary_vars: Ensemble des variables auxiliaires créées (y₁, y₂, ...)
    • original_vars: Ensemble des variables originales de la formule SAT
    
    COMPLEXITÉ:
    ----------
    • Temporelle: O(n + m) - chaque clause traitée une seule fois
    • Spatiale: O(n + m) - stockage des nouvelles clauses
    """
    
    def __init__(self):
        """Initialise le réducteur"""
        self.next_aux_var = 0           # Prochain numéro de variable auxiliaire
        self.auxiliary_vars = set()     # Variables auxiliaires créées {y₁, y₂, ...}
        self.original_vars = set()      # Variables originales {x₁, x₂, ...}
    
    def _get_auxiliary_var(self, max_original_var: int) -> int:
        """
        Génère une nouvelle variable auxiliaire unique.
        
        PRINCIPE:
        --------
        Les variables auxiliaires ont des numéros > max(variables originales)
        pour éviter les conflits.
        
        Exemple: Si variables originales sont x₁, x₂, x₃ (max=3),
                 alors les variables auxiliaires seront y₁=4, y₂=5, etc.
        
        Args:
            max_original_var: Plus grand numéro de variable originale
            
        Returns:
            int: Numéro de la nouvelle variable auxiliaire
        """
        if self.next_aux_var == 0:
            # Première variable auxiliaire: commence après les originales
            self.next_aux_var = max_original_var + 1
        else:
            # Variables suivantes: incrémenter
            self.next_aux_var += 1
        
        # Enregistrer dans l'ensemble des auxiliaires
        self.auxiliary_vars.add(self.next_aux_var)
        return self.next_aux_var
    
    def _convert_sat_clause_to_literals(self, clause_sat) -> List[Tuple[int, bool]]:
        """
        Convertit une clause SAT en liste de littéraux (numéro, négation).
        
        FORMAT:
        ------
        Entrée SAT: [(var_num, is_negated), ...]
        Sortie: [(var_num, is_negated), ...]
        
        Exemple:
        -------
        [(1, False), (2, True), (3, False)]  → x₁ ∨ ¬x₂ ∨ x₃
        
        Args:
            clause_sat: Clause au format SAT
            
        Returns:
            Liste de tuples (numéro_variable, est_négation)
        """
        literals = []
        for item in clause_sat:
            if isinstance(item, tuple):
                # Format standard: (var_num, is_negated)
                var_num, is_neg = item
            else:
                # Format alternatif: entier signé (-2 signifie ¬x₂)
                var_num = abs(item)
                is_neg = item < 0
            literals.append((var_num, is_neg))
        return literals
    
    def _literals_to_3sat_format(self, literals: List[Tuple[int, bool]]) -> List[int]:
        """
        Convertit des littéraux au format 3-SAT (entiers signés).
        
        FORMAT 3-SAT:
        ------------
        • Entier positif: variable (ex: 1 = x₁)
        • Entier négatif: négation (ex: -2 = ¬x₂)
        
        Exemple:
        -------
        Entrée: [(1, False), (2, True), (3, False)]
        Sortie: [1, -2, 3]  → représente (x₁ ∨ ¬x₂ ∨ x₃)
        
        Args:
            literals: Liste de (numéro, négation)
            
        Returns:
            Liste d'entiers signés pour format 3-SAT
        """
        result = []
        for var, is_neg in literals:
            # Si négation: mettre signe négatif, sinon positif
            result.append(-var if is_neg else var)
        return result
    
    def _reduce_clause_k1(self, literal: Tuple[int, bool], max_var: int) -> List[List[int]]:
        """
        Réduit une clause avec 1 seul littéral (k=1).
        
        TRANSFORMATION k=1:
        ------------------
        Entrée:  (x₁)
        Sortie:  (x₁ ∨ y ∨ z) ∧ 
                 (x₁ ∨ y ∨ ¬z) ∧ 
                 (x₁ ∨ ¬y ∨ z) ∧ 
                 (x₁ ∨ ¬y ∨ ¬z)
        
        RÉSULTAT:
        --------
        • 4 clauses 3-SAT générées (chacune avec 3 littéraux)
        • 2 variables auxiliaires créées (y, z)
        
        POURQUOI ÇA MARCHE:
        ------------------
        Ces 4 clauses forcent x₁ à être VRAI:
        - Si x₁=VRAI → toutes les clauses sont satisfaites ✓
        - Si x₁=FAUX → impossible de satisfaire toutes les clauses ✗
        
        Args:
            literal: Le littéral unique (var_num, is_negated)
            max_var: Plus grand numéro de variable originale
            
        Returns:
            Liste de 4 clauses 3-SAT
        """
        var, is_neg = literal
        
        # Créer 2 variables auxiliaires y et z
        y = self._get_auxiliary_var(max_var)
        z = self._get_auxiliary_var(max_var)
        
        # Convertir le littéral principal au format 3-SAT
        lit_main = -var if is_neg else var
        
        # Générer les 4 clauses avec toutes les combinaisons de y et z
        clauses_3sat = [
            [lit_main, y, z],       # (x₁ ∨ y ∨ z)
            [lit_main, y, -z],      # (x₁ ∨ y ∨ ¬z)
            [lit_main, -y, z],      # (x₁ ∨ ¬y ∨ z)
            [lit_main, -y, -z]      # (x₁ ∨ ¬y ∨ ¬z)
        ]
        
        return clauses_3sat
    
    def _reduce_clause_k2(self, literals: List[Tuple[int, bool]], max_var: int) -> List[List[int]]:
        """
        Réduit une clause avec 2 littéraux (k=2).
        
        TRANSFORMATION k=2:
        ------------------
        Entrée:  (x₁ ∨ x₂)
        Sortie:  (x₁ ∨ x₂ ∨ y) ∧ 
                 (x₁ ∨ x₂ ∨ ¬y)
        
        RÉSULTAT:
        --------
        • 2 clauses 3-SAT générées (chacune avec 3 littéraux)
        • 1 variable auxiliaire créée (y)
        
        POURQUOI ÇA MARCHE:
        ------------------
        Peu importe la valeur de y, l'une des deux clauses force (x₁ ∨ x₂) à être vraie:
        - Si y=VRAI → première clause devient (x₁ ∨ x₂ ∨ VRAI) = VRAI ✓
        - Si y=FAUX → deuxième clause devient (x₁ ∨ x₂ ∨ VRAI) = VRAI ✓
        Donc au moins x₁ ou x₂ doit être VRAI (équivalent à la clause originale)
        
        Args:
            literals: Les 2 littéraux [(var1, neg1), (var2, neg2)]
            max_var: Plus grand numéro de variable originale
            
        Returns:
            Liste de 2 clauses 3-SAT
        """
        # Créer 1 variable auxiliaire y
        y = self._get_auxiliary_var(max_var)
        
        # Convertir les 2 littéraux au format 3-SAT
        lit1 = -literals[0][0] if literals[0][1] else literals[0][0]
        lit2 = -literals[1][0] if literals[1][1] else literals[1][0]
        
        # Générer les 2 clauses avec y et ¬y
        clauses_3sat = [
            [lit1, lit2, y],    # (x₁ ∨ x₂ ∨ y)
            [lit1, lit2, -y]    # (x₁ ∨ x₂ ∨ ¬y)
        ]
        
        return clauses_3sat
    
    def _reduce_clause_k3(self, literals: List[Tuple[int, bool]]) -> List[List[int]]:
        """
        Réduit une clause avec 3 littéraux (k=3).
        
        TRANSFORMATION k=3:
        ------------------
        Entrée:  (x₁ ∨ x₂ ∨ x₃)
        Sortie:  (x₁ ∨ x₂ ∨ x₃)  ← PAS DE CHANGEMENT !
        
        RÉSULTAT:
        --------
        • 1 clause 3-SAT (la clause originale)
        • 0 variable auxiliaire (pas besoin)
        
        POURQUOI:
        --------
        La clause a déjà exactement 3 littéraux, elle est déjà au format 3-SAT.
        On fait juste une conversion de format (tuple → entier signé).
        
        Args:
            literals: Les 3 littéraux [(var1, neg1), (var2, neg2), (var3, neg3)]
            
        Returns:
            Liste d'1 clause 3-SAT
        """
        # Simplement convertir au format 3-SAT (pas de transformation nécessaire)
        clause_3sat = self._literals_to_3sat_format(literals)
        return [clause_3sat]
    
    def _reduce_clause_k_geq_4(self, literals: List[Tuple[int, bool]], max_var: int) -> List[List[int]]:
        """
        Réduit une clause avec k≥4 littéraux.
        
        TRANSFORMATION k≥4:
        ------------------
        Entrée:  (x₁ ∨ x₂ ∨ ... ∨ xₖ)  ← 1 clause avec k littéraux
        
        Sortie:  (x₁ ∨ x₂ ∨ y₁) ∧              ← Clause 1: 3 littéraux
                 (¬y₁ ∨ x₃ ∨ y₂) ∧             ← Clause 2: 3 littéraux
                 (¬y₂ ∨ x₄ ∨ y₃) ∧             ← Clause 3: 3 littéraux
                 ...
                 (¬yₖ₋₃ ∨ xₖ₋₁ ∨ xₖ)           ← Clause finale: 3 littéraux
        
        RÉSULTAT:
        --------
        • (k-2) clauses 3-SAT générées
        • (k-3) variables auxiliaires créées (y₁, y₂, ..., yₖ₋₃)
        
        EXEMPLE k=5:
        -----------
        Entrée:  (x₁ ∨ x₂ ∨ x₃ ∨ x₄ ∨ x₅)  ← 1 clause, 5 littéraux
        
        ÉTAPE 1: Première clause
          Prendre: x₁, x₂, y₁
          Résultat: (x₁ ∨ x₂ ∨ y₁)
        
        ÉTAPE 2: Clause intermédiaire (UNE SEULE pour k=5)
          Prendre: ¬y₁, x₃, y₂
          Résultat: (¬y₁ ∨ x₃ ∨ y₂)
        
        ÉTAPE 3: Dernière clause
          Prendre: ¬y₂, x₄, x₅
          Résultat: (¬y₂ ∨ x₄ ∨ x₅)
        
        Total: 3 clauses (k-2 = 5-2 = 3) ✓
        Variables auxiliaires: y₁, y₂ (k-3 = 5-3 = 2) ✓
        
        LOGIQUE GÉNÉRALE:
        ----------------
        Pour k littéraux:
        - Clause 1: (l₁ ∨ l₂ ∨ y₁)
        - Clauses 2 à k-3: (¬yᵢ ∨ lᵢ₊₂ ∨ yᵢ₊₁) pour i=1 à k-4
        - Clause k-2: (¬yₖ₋₃ ∨ lₖ₋₁ ∨ lₖ)
        
        Nombre de clauses intermédiaires: (k-3) - 1 = k-4
        Total clauses: 1 + (k-4) + 1 = k-2 ✓
        
        POURQUOI ÇA MARCHE:
        ------------------
        Les variables auxiliaires "chaînent" les littéraux:
        - Si la clause originale est vraie, on peut choisir les yᵢ pour satisfaire toutes les clauses
        - Si la clause originale est fausse, au moins une clause 3-SAT sera fausse
        
        Args:
            literals: Les k littéraux (k≥4)
            max_var: Plus grand numéro de variable originale
            
        Returns:
            Liste de (k-2) clauses 3-SAT
        """
        k = len(literals)  # Nombre de littéraux dans la clause
        clauses_3sat = []  # Liste des clauses 3-SAT à générer
        
        # Convertir tous les littéraux au format 3-SAT (entiers signés)
        lits = [(-lit[0] if lit[1] else lit[0]) for lit in literals]
        
        # ÉTAPE 1: Première clause (x₁ ∨ x₂ ∨ y₁)
        # On prend les 2 premiers littéraux + une variable auxiliaire
        y_prev = self._get_auxiliary_var(max_var)
        clauses_3sat.append([lits[0], lits[1], y_prev])
        
        # ÉTAPE 2: Clauses intermédiaires (¬yᵢ₋₁ ∨ xᵢ₊₁ ∨ yᵢ)
        # CORRECTION: range(2, k-2) au lieu de range(2, k-1)
        # Pour k=5: range(2, 3) = [2] → 1 itération ✓
        for i in range(2, k - 2):
            y_curr = self._get_auxiliary_var(max_var)
            clauses_3sat.append([-y_prev, lits[i], y_curr])
            y_prev = y_curr  # La variable actuelle devient la précédente
        
        # ÉTAPE 3: Dernière clause (¬yₖ₋₃ ∨ xₖ₋₁ ∨ xₖ)
        # On prend la dernière variable auxiliaire + les 2 derniers littéraux
        clauses_3sat.append([-y_prev, lits[k-2], lits[k-1]])
        
        # Vérification: on doit avoir généré exactement (k-2) clauses
        assert len(clauses_3sat) == k - 2, f"Erreur: {len(clauses_3sat)} clauses au lieu de {k-2}"
        
        return clauses_3sat
    
    def reduce(self, variables_sat: List[str], clauses_sat: List, verbose: bool = True) -> Tuple[List[List[int]], int, Dict]:
        """
        Réduit une formule SAT complète en formule 3-SAT équivalente.
        
        ALGORITHME:
        ----------
        Pour chaque clause SAT:
          1. Déterminer sa taille k (nombre de littéraux)
          2. Appliquer la transformation appropriée:
             - k=1 → _reduce_clause_k1
             - k=2 → _reduce_clause_k2
             - k=3 → _reduce_clause_k3
             - k≥4 → _reduce_clause_k_geq_4
          3. Ajouter les clauses 3-SAT générées au résultat
        
        COMPLEXITÉ:
        ----------
        • Temporelle: O(n + m) - chaque clause traitée une fois
        • Spatiale: O(n + m) - stockage des clauses générées
        
        Args:
            variables_sat: Liste des variables SAT ['x1', 'x2', ...]
            clauses_sat: Liste de clauses SAT [[(var, neg), ...], ...]
            verbose: Afficher les détails ou non
            
        Returns:
            tuple: (clauses_3sat, num_variables_3sat, statistiques)
        """
        if verbose:
            print(f"\n{'='*70}")
            print("RÉDUCTION SAT → 3-SAT")
            print(f"{'='*70}")
        
        # Démarrer les mesures de performance
        tracemalloc.start()
        start_time = time.time()
        
        # Réinitialiser les variables auxiliaires
        self.auxiliary_vars.clear()
        self.next_aux_var = 0
        
        # Extraire les numéros des variables originales
        self.original_vars = set()
        for var_name in variables_sat:
            var_num = int(var_name.replace('x', ''))
            self.original_vars.add(var_num)
        
        max_var = max(self.original_vars) if self.original_vars else 0
        
        # Initialiser les statistiques
        stats = {
            'original_vars': len(variables_sat),
            'original_clauses': len(clauses_sat),
            'clauses_k1': 0,      # Nombre de clauses avec 1 littéral
            'clauses_k2': 0,      # Nombre de clauses avec 2 littéraux
            'clauses_k3': 0,      # Nombre de clauses avec 3 littéraux
            'clauses_k4plus': 0,  # Nombre de clauses avec 4+ littéraux
            'total_3sat_clauses': 0
        }
        
        if verbose:
            print(f"\nFormule SAT originale:")
            print(f"  Variables: {stats['original_vars']}")
            print(f"  Clauses: {stats['original_clauses']}")
        
        # Liste pour stocker toutes les clauses 3-SAT générées
        all_3sat_clauses = []
        
        # BOUCLE PRINCIPALE: Traiter chaque clause SAT
        for i, clause_sat in enumerate(clauses_sat):
            # Convertir la clause en format interne
            literals = self._convert_sat_clause_to_literals(clause_sat)
            k = len(literals)  # Nombre de littéraux dans cette clause
            
            # Appliquer la transformation appropriée selon k
            if k == 1:
                stats['clauses_k1'] += 1
                new_clauses = self._reduce_clause_k1(literals[0], max_var)
            elif k == 2:
                stats['clauses_k2'] += 1
                new_clauses = self._reduce_clause_k2(literals, max_var)
            elif k == 3:
                stats['clauses_k3'] += 1
                new_clauses = self._reduce_clause_k3(literals)
            else:  # k >= 4
                stats['clauses_k4plus'] += 1
                new_clauses = self._reduce_clause_k_geq_4(literals, max_var)
            
            # Ajouter les nouvelles clauses au résultat
            all_3sat_clauses.extend(new_clauses)
        
        # Calculer le nombre total de variables (originales + auxiliaires)
        num_variables_3sat = max_var + len(self.auxiliary_vars)
        
        # Mesures finales de performance
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Compléter les statistiques
        stats['new_vars'] = num_variables_3sat
        stats['new_clauses'] = len(all_3sat_clauses)
        stats['auxiliary_vars'] = len(self.auxiliary_vars)
        stats['time'] = end_time - start_time
        stats['memory_kb'] = peak / 1024
        stats['total_3sat_clauses'] = len(all_3sat_clauses)
        
        if verbose:
            print(f"\nTransformations appliquées:")
            print(f"  k=1: {stats['clauses_k1']} clause(s) → {stats['clauses_k1']*4} clauses 3-SAT")
            print(f"  k=2: {stats['clauses_k2']} clause(s) → {stats['clauses_k2']*2} clauses 3-SAT")
            print(f"  k=3: {stats['clauses_k3']} clause(s) → {stats['clauses_k3']} clauses 3-SAT")
            if stats['clauses_k4plus'] > 0:
                print(f"  k≥4: {stats['clauses_k4plus']} clause(s) → ... clauses 3-SAT")
            
            print(f"\nFormule 3-SAT résultante:")
            print(f"  Variables: {num_variables_3sat} (+{stats['auxiliary_vars']} auxiliaires)")
            print(f"  Clauses: {len(all_3sat_clauses)}")
            print(f"  Facteur d'expansion: {len(all_3sat_clauses)/len(clauses_sat):.2f}x")
            
            print(f"\nPerformance:")
            print(f"  Temps: {stats['time']:.6f}s")
            print(f"  Mémoire: {stats['memory_kb']:.2f} KB")
            print(f"  Complexité: O(n + m) ✓")
        
        return all_3sat_clauses, num_variables_3sat, stats
    
    def convert_solution_3sat_to_sat(self, solution_3sat: Dict[int, bool]) -> Dict[str, bool]:
        """
        Convertit une solution 3-SAT en solution SAT.
        
        PRINCIPE:
        --------
        On retire simplement les variables auxiliaires (yᵢ) de la solution
        et on garde uniquement les variables originales (xᵢ).
        
        Args:
            solution_3sat: {var_num: True/False} incluant auxiliaires
            
        Returns:
            {var_name: True/False} sans auxiliaires
        """
        solution_sat = {}
        
        # Ne garder que les variables originales
        for var_num, value in solution_3sat.items():
            if var_num in self.original_vars:
                var_name = f'x{var_num}'
                solution_sat[var_name] = value
        
        return solution_sat


# ============================================================================
# FONCTIONS DE TEST SIMPLE
# ============================================================================

def test_simple():
    """Test basique pour vérifier que le code fonctionne"""
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*20 + "TEST SIMPLE - RÉDUCTION" + " "*23 + "║")
    print("╚" + "="*68 + "╝")
    
    # Formule SAT: (x1) ∧ (x2 ∨ x3) ∧ (x1 ∨ x2 ∨ x3)
    variables_sat = ['x1', 'x2', 'x3']
    clauses_sat = [
        [(1, False)],                         # k=1: x1
        [(2, False), (3, False)],             # k=2: x2 ∨ x3
        [(1, False), (2, False), (3, False)]  # k=3: x1 ∨ x2 ∨ x3
    ]
    
    print("\nFormule SAT:")
    print("  C1: (x1)")
    print("  C2: (x2 ∨ x3)")
    print("  C3: (x1 ∨ x2 ∨ x3)")
    
    # Réduire
    reducer = SATto3SATReducer()
    clauses_3sat, num_vars_3sat, stats = reducer.reduce(variables_sat, clauses_sat)
    
    print(f"\n✅ Réduction terminée avec succès!")
    print(f"   {len(clauses_sat)} clauses SAT → {len(clauses_3sat)} clauses 3-SAT")


if __name__ == "__main__":
    test_simple()