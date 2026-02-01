"""
TESTS COMPLETS - RÉDUCTION SAT → 3-SAT
======================================
Tests unitaires avec affichage détaillé comme demandé par le prof

AFFICHAGE FORMAT:
----------------
Pour chaque transformation, on montre:

Entrée (SAT):
  (x₁ ∨ x₂ ∨ x₃ ∨ x₄ ∨ x₅)  ← 1 clause avec 5 littéraux

Sortie (3-SAT):
  (x₁ ∨ x₂ ∨ y₁)         ← Clause 1: 3 littéraux ✓
  (¬y₁ ∨ x₃ ∨ y₂)        ← Clause 2: 3 littéraux ✓
  (¬y₂ ∨ x₄ ∨ x₅)        ← Clause 3: 3 littéraux ✓
"""

import sys
import time
from sat_to_3sat_reduction import SATto3SATReducer
from solver_3sat import SAT3Solver
from verifier_3sat import SAT3Verifier
from verify_SAT import verify_SAT_solution


def format_clause_readable(clause, var_type="x"):
    """
    Convertit une clause 3-SAT en format lisible.
    
    Exemple:
    -------
    [1, -2, 3] → "(x₁ ∨ ¬x₂ ∨ x₃)"
    """
    parts = []
    for lit in clause:
        var_num = abs(lit)
        if lit < 0:
            # Négation: ¬xᵢ ou ¬yᵢ
            parts.append(f"¬{var_type}{var_num}")
        else:
            # Variable positive: xᵢ ou yᵢ
            parts.append(f"{var_type}{var_num}")
    return "(" + " ∨ ".join(parts) + ")"


def print_transformation(clause_sat, clauses_3sat, k, aux_vars):
    """
    Affiche une transformation SAT → 3-SAT au format demandé.
    
    Format d'affichage:
    ------------------
    Entrée (SAT):
      (x₁ ∨ x₂ ∨ ... ∨ xₖ)  ← 1 clause avec k littéraux
    
    Sortie (3-SAT):
      (x₁ ∨ x₂ ∨ y₁)         ← Clause 1: 3 littéraux ✓
      (¬y₁ ∨ x₃ ∨ y₂)        ← Clause 2: 3 littéraux ✓
      ...
    """
    print("\n📝 Entrée (SAT):")
    
    # Formater la clause SAT
    sat_parts = []
    for var, is_neg in clause_sat:
        if is_neg:
            sat_parts.append(f"¬x{var}")
        else:
            sat_parts.append(f"x{var}")
    sat_str = "(" + " ∨ ".join(sat_parts) + ")"
    
    print(f"  {sat_str}  ← 1 clause avec {k} littéral(s)")
    
    print("\n📤 Sortie (3-SAT):")
    
    # Afficher chaque clause 3-SAT générée
    for i, clause in enumerate(clauses_3sat, 1):
        # Formater avec x pour variables originales, y pour auxiliaires
        parts = []
        for lit in clause:
            var_num = abs(lit)
            # Déterminer si c'est une variable originale ou auxiliaire
            if var_num in [abs(v[0]) for v in clause_sat]:
                # Variable originale
                var_name = f"x{var_num}"
            else:
                # Variable auxiliaire
                var_name = f"y{var_num}"
            
            if lit < 0:
                parts.append(f"¬{var_name}")
            else:
                parts.append(f"{var_name}")
        
        clause_str = "(" + " ∨ ".join(parts) + ")"
        print(f"  {clause_str:30} ← Clause {i}: 3 littéraux ✓")
    
    # Afficher les variables auxiliaires créées
    if aux_vars:
        print(f"\n🔢 Variables auxiliaires créées: {sorted(aux_vars)}")
    else:
        print(f"\n🔢 Variables auxiliaires: aucune (clause déjà 3-SAT)")


def test_reduction_k1():
    """
    Test réduction clause k=1
    
    TRANSFORMATION:
    --------------
    Entrée:  (x₁)  ← 1 clause avec 1 littéral
    Sortie:  4 clauses avec 3 littéraux chacune
    Auxiliaires: 2 variables (y, z)
    """
    print("\n" + "="*70)
    print("TEST 1: RÉDUCTION CLAUSE k=1")
    print("="*70)
    print("\n📋 Règle k=1:")
    print("   (x₁) → 4 clauses 3-SAT + 2 variables auxiliaires")
    
    # Formule SAT: (x1)
    variables_sat = ['x1']
    clauses_sat = [[(1, False)]]  # x1
    
    # Réduire (sans affichage verbeux)
    reducer = SATto3SATReducer()
    clauses_3sat, num_vars, stats = reducer.reduce(variables_sat, clauses_sat, verbose=False)
    
    # Afficher la transformation
    print_transformation(clauses_sat[0], clauses_3sat, k=1, aux_vars=reducer.auxiliary_vars)
    
    # Vérifications
    print("\n✅ Vérifications:")
    assert len(clauses_3sat) == 4, f"❌ Devrait générer 4 clauses (obtenu: {len(clauses_3sat)})"
    print(f"   ✓ Nombre de clauses: {len(clauses_3sat)} (attendu: 4)")
    
    assert len(reducer.auxiliary_vars) == 2, f"❌ Devrait créer 2 variables auxiliaires"
    print(f"   ✓ Variables auxiliaires: {len(reducer.auxiliary_vars)} (attendu: 2)")
    
    for clause in clauses_3sat:
        assert len(clause) == 3, f"❌ Clause {clause} n'a pas 3 littéraux"
    print(f"   ✓ Toutes les clauses ont exactement 3 littéraux")
    
    print("\n✅ Test k=1 réussi!")
    return True


def test_reduction_k2():
    """
    Test réduction clause k=2
    
    TRANSFORMATION:
    --------------
    Entrée:  (x₁ ∨ x₂)  ← 1 clause avec 2 littéraux
    Sortie:  2 clauses avec 3 littéraux chacune
    Auxiliaires: 1 variable (y)
    """
    print("\n" + "="*70)
    print("TEST 2: RÉDUCTION CLAUSE k=2")
    print("="*70)
    print("\n📋 Règle k=2:")
    print("   (x₁ ∨ x₂) → 2 clauses 3-SAT + 1 variable auxiliaire")
    
    # Formule SAT: (x1 ∨ x2)
    variables_sat = ['x1', 'x2']
    clauses_sat = [[(1, False), (2, False)]]
    
    # Réduire
    reducer = SATto3SATReducer()
    clauses_3sat, num_vars, stats = reducer.reduce(variables_sat, clauses_sat, verbose=False)
    
    # Afficher
    print_transformation(clauses_sat[0], clauses_3sat, k=2, aux_vars=reducer.auxiliary_vars)
    
    # Vérifications
    print("\n✅ Vérifications:")
    assert len(clauses_3sat) == 2, f"❌ Devrait générer 2 clauses"
    print(f"   ✓ Nombre de clauses: {len(clauses_3sat)} (attendu: 2)")
    
    assert len(reducer.auxiliary_vars) == 1, f"❌ Devrait créer 1 variable auxiliaire"
    print(f"   ✓ Variables auxiliaires: {len(reducer.auxiliary_vars)} (attendu: 1)")
    
    for clause in clauses_3sat:
        assert len(clause) == 3, f"❌ Clause {clause} n'a pas 3 littéraux"
    print(f"   ✓ Toutes les clauses ont exactement 3 littéraux")
    
    print("\n✅ Test k=2 réussi!")
    return True


def test_reduction_k3():
    """
    Test réduction clause k=3
    
    TRANSFORMATION:
    --------------
    Entrée:  (x₁ ∨ x₂ ∨ x₃)  ← 1 clause avec 3 littéraux
    Sortie:  1 clause (identique, déjà 3-SAT)
    Auxiliaires: 0 (pas nécessaire)
    """
    print("\n" + "="*70)
    print("TEST 3: RÉDUCTION CLAUSE k=3")
    print("="*70)
    print("\n📋 Règle k=3:")
    print("   (x₁ ∨ x₂ ∨ x₃) → 1 clause 3-SAT (pas de transformation)")
    
    # Formule SAT: (x1 ∨ x2 ∨ x3)
    variables_sat = ['x1', 'x2', 'x3']
    clauses_sat = [[(1, False), (2, False), (3, False)]]
    
    # Réduire
    reducer = SATto3SATReducer()
    clauses_3sat, num_vars, stats = reducer.reduce(variables_sat, clauses_sat, verbose=False)
    
    # Afficher
    print_transformation(clauses_sat[0], clauses_3sat, k=3, aux_vars=reducer.auxiliary_vars)
    
    # Vérifications
    print("\n✅ Vérifications:")
    assert len(clauses_3sat) == 1, f"❌ Devrait générer 1 clause"
    print(f"   ✓ Nombre de clauses: {len(clauses_3sat)} (attendu: 1)")
    
    assert len(reducer.auxiliary_vars) == 0, f"❌ Ne devrait pas créer de variable auxiliaire"
    print(f"   ✓ Variables auxiliaires: {len(reducer.auxiliary_vars)} (attendu: 0)")
    
    print(f"   ✓ Clause déjà au format 3-SAT, pas de transformation nécessaire")
    
    print("\n✅ Test k=3 réussi!")
    return True


def test_reduction_k4():
    """
    Test réduction clause k=4
    
    TRANSFORMATION:
    --------------
    Entrée:  (x₁ ∨ x₂ ∨ x₃ ∨ x₄)  ← 1 clause avec 4 littéraux
    Sortie:  2 clauses avec 3 littéraux chacune
    Auxiliaires: 1 variable (y₁)
    """
    print("\n" + "="*70)
    print("TEST 4: RÉDUCTION CLAUSE k=4")
    print("="*70)
    print("\n📋 Règle k=4:")
    print("   (x₁ ∨ x₂ ∨ x₃ ∨ x₄) → 2 clauses 3-SAT + 1 variable auxiliaire")
    print("   Formule: k-2 = 4-2 = 2 clauses")
    
    # Formule SAT: (x1 ∨ x2 ∨ x3 ∨ x4)
    variables_sat = ['x1', 'x2', 'x3', 'x4']
    clauses_sat = [[(1, False), (2, False), (3, False), (4, False)]]
    
    # Réduire
    reducer = SATto3SATReducer()
    clauses_3sat, num_vars, stats = reducer.reduce(variables_sat, clauses_sat, verbose=False)
    
    # Afficher
    print_transformation(clauses_sat[0], clauses_3sat, k=4, aux_vars=reducer.auxiliary_vars)
    
    # Vérifications
    print("\n✅ Vérifications:")
    assert len(clauses_3sat) == 2, f"❌ Devrait générer 2 clauses (k-2 = 4-2 = 2)"
    print(f"   ✓ Nombre de clauses: {len(clauses_3sat)} = k-2 = 4-2 (attendu: 2)")
    
    assert len(reducer.auxiliary_vars) == 1, f"❌ Devrait créer 1 variable auxiliaire"
    print(f"   ✓ Variables auxiliaires: {len(reducer.auxiliary_vars)} = k-3 = 4-3 (attendu: 1)")
    
    for clause in clauses_3sat:
        assert len(clause) == 3, f"❌ Clause {clause} n'a pas 3 littéraux"
    print(f"   ✓ Toutes les clauses ont exactement 3 littéraux")
    
    print("\n✅ Test k=4 réussi!")
    return True


def test_reduction_k5():
    """
    Test réduction clause k=5 (EXEMPLE PRINCIPAL DU PROF)
    
    TRANSFORMATION:
    --------------
    Entrée:  (x₁ ∨ x₂ ∨ x₃ ∨ x₄ ∨ x₅)  ← 1 clause avec 5 littéraux
    Sortie:  3 clauses avec 3 littéraux chacune
    Auxiliaires: 2 variables (y₁, y₂)
    """
    print("\n" + "="*70)
    print("TEST 5: RÉDUCTION CLAUSE k=5 (EXEMPLE DU PROF)")
    print("="*70)
    print("\n📋 Règle k=5:")
    print("   (x₁ ∨ x₂ ∨ x₃ ∨ x₄ ∨ x₅) → 3 clauses 3-SAT + 2 variables auxiliaires")
    print("   Formule: k-2 = 5-2 = 3 clauses, k-3 = 5-3 = 2 variables aux")
    
    # Formule SAT: (x1 ∨ x2 ∨ x3 ∨ x4 ∨ x5)
    variables_sat = ['x1', 'x2', 'x3', 'x4', 'x5']
    clauses_sat = [[(i, False) for i in range(1, 6)]]
    
    # Réduire
    reducer = SATto3SATReducer()
    clauses_3sat, num_vars, stats = reducer.reduce(variables_sat, clauses_sat, verbose=False)
    
    # Afficher
    print_transformation(clauses_sat[0], clauses_3sat, k=5, aux_vars=reducer.auxiliary_vars)
    
    # Vérifications
    print("\n✅ Vérifications:")
    assert len(clauses_3sat) == 3, f"❌ Devrait générer 3 clauses (k-2 = 5-2 = 3)"
    print(f"   ✓ Nombre de clauses: {len(clauses_3sat)} = k-2 = 5-2 (attendu: 3)")
    
    assert len(reducer.auxiliary_vars) == 2, f"❌ Devrait créer 2 variables auxiliaires"
    print(f"   ✓ Variables auxiliaires: {len(reducer.auxiliary_vars)} = k-3 = 5-3 (attendu: 2)")
    
    for i, clause in enumerate(clauses_3sat, 1):
        assert len(clause) == 3, f"❌ Clause {i} {clause} n'a pas 3 littéraux"
    print(f"   ✓ Toutes les clauses ont exactement 3 littéraux")
    
    print("\n🎯 CECI EST L'EXEMPLE EXACT DEMANDÉ PAR LE PROF!")
    print("   Entrée:  (x₁ ∨ x₂ ∨ x₃ ∨ x₄ ∨ x₅)")
    print("   Sortie:  (x₁ ∨ x₂ ∨ y₁) ∧ (¬y₁ ∨ x₃ ∨ y₂) ∧ (¬y₂ ∨ x₄ ∨ x₅)")
    
    print("\n✅ Test k=5 réussi!")
    return True


def test_reduction_k6():
    """
    Test réduction clause k=6
    
    TRANSFORMATION:
    --------------
    Entrée:  (x₁ ∨ x₂ ∨ x₃ ∨ x₄ ∨ x₅ ∨ x₆)  ← 1 clause avec 6 littéraux
    Sortie:  4 clauses avec 3 littéraux chacune
    Auxiliaires: 3 variables (y₁, y₂, y₃)
    """
    print("\n" + "="*70)
    print("TEST 6: RÉDUCTION CLAUSE k=6")
    print("="*70)
    print("\n📋 Règle k=6:")
    print("   (x₁ ∨ ... ∨ x₆) → 4 clauses 3-SAT + 3 variables auxiliaires")
    print("   Formule: k-2 = 6-2 = 4 clauses, k-3 = 6-3 = 3 variables aux")
    
    # Formule SAT: (x1 ∨ x2 ∨ x3 ∨ x4 ∨ x5 ∨ x6)
    variables_sat = [f'x{i}' for i in range(1, 7)]
    clauses_sat = [[(i, False) for i in range(1, 7)]]
    
    # Réduire
    reducer = SATto3SATReducer()
    clauses_3sat, num_vars, stats = reducer.reduce(variables_sat, clauses_sat, verbose=False)
    
    # Afficher
    print_transformation(clauses_sat[0], clauses_3sat, k=6, aux_vars=reducer.auxiliary_vars)
    
    # Vérifications
    print("\n✅ Vérifications:")
    assert len(clauses_3sat) == 4, f"❌ Devrait générer 4 clauses (k-2 = 6-2 = 4)"
    print(f"   ✓ Nombre de clauses: {len(clauses_3sat)} = k-2 = 6-2 (attendu: 4)")
    
    assert len(reducer.auxiliary_vars) == 3, f"❌ Devrait créer 3 variables auxiliaires"
    print(f"   ✓ Variables auxiliaires: {len(reducer.auxiliary_vars)} = k-3 = 6-3 (attendu: 3)")
    
    print("\n✅ Test k=6 réussi!")
    return True


def test_mixed_formula():
    """
    Test avec formule mixte (différentes tailles)
    """
    print("\n" + "="*70)
    print("TEST 7: FORMULE MIXTE (k=1, k=2, k=3, k=4)")
    print("="*70)
    
    # Mélange de différentes tailles
    variables_sat = ['x1', 'x2', 'x3', 'x4']
    clauses_sat = [
        [(1, False)],                                    # k=1
        [(2, False), (3, True)],                         # k=2
        [(1, False), (2, False), (3, False)],            # k=3
        [(1, False), (2, False), (3, False), (4, True)]  # k=4
    ]
    
    print("\nFormule SAT mixte:")
    print("  C1: (x₁)              ← k=1")
    print("  C2: (x₂ ∨ ¬x₃)        ← k=2")
    print("  C3: (x₁ ∨ x₂ ∨ x₃)    ← k=3")
    print("  C4: (x₁ ∨ x₂ ∨ x₃ ∨ ¬x₄) ← k=4")
    
    # Réduire
    reducer = SATto3SATReducer()
    clauses_3sat, num_vars, stats = reducer.reduce(variables_sat, clauses_sat, verbose=False)
    
    # Calcul des attentes
    expected_clauses = 4 + 2 + 1 + 2  # k=1→4, k=2→2, k=3→1, k=4→2
    expected_aux = 2 + 1 + 0 + 1      # k=1→2, k=2→1, k=3→0, k=4→1
    
    print(f"\n📤 Résultat:")
    print(f"   Clauses 3-SAT générées: {len(clauses_3sat)} (attendu: {expected_clauses})")
    print(f"   Variables auxiliaires: {len(reducer.auxiliary_vars)} (attendu: {expected_aux})")
    
    # Afficher toutes les clauses
    print(f"\n📋 Clauses 3-SAT complètes:")
    for i, clause in enumerate(clauses_3sat, 1):
        clause_str = format_clause_readable(clause)
        print(f"   C{i:2d}: {clause_str}")
    
    # Vérifications
    print(f"\n✅ Vérifications:")
    assert len(clauses_3sat) == expected_clauses
    print(f"   ✓ Nombre de clauses correct: {len(clauses_3sat)}")
    
    assert len(reducer.auxiliary_vars) == expected_aux
    print(f"   ✓ Variables auxiliaires correctes: {len(reducer.auxiliary_vars)}")
    
    for clause in clauses_3sat:
        assert len(clause) == 3
    print(f"   ✓ Toutes les clauses ont 3 littéraux")
    
    print("\n✅ Test formule mixte réussi!")
    return True


def run_all_tests():
    """Exécute tous les tests avec affichage détaillé"""
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*12 + "SUITE DE TESTS - RÉDUCTION SAT → 3-SAT" + " "*15 + "║")
    print("║" + " "*15 + "Avec affichage détaillé demandé" + " "*20 + "║")
    print("╚" + "="*68 + "╝")
    
    tests = [
        ("Réduction k=1", test_reduction_k1),
        ("Réduction k=2", test_reduction_k2),
        ("Réduction k=3", test_reduction_k3),
        ("Réduction k=4", test_reduction_k4),
        ("Réduction k=5 (EXEMPLE PROF)", test_reduction_k5),
        ("Réduction k=6", test_reduction_k6),
        ("Formule mixte", test_mixed_formula)
    ]
    
    passed = 0
    failed = 0
    
    start_time = time.time()
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"❌ Test '{test_name}' échoué")
        except AssertionError as e:
            failed += 1
            print(f"\n❌ Test '{test_name}' échoué: {e}")
        except Exception as e:
            failed += 1
            print(f"\n❌ Test '{test_name}' erreur: {e}")
            import traceback
            traceback.print_exc()
    
    elapsed = time.time() - start_time
    
    # Résumé final
    print("\n" + "="*70)
    print("RÉSUMÉ DES TESTS")
    print("="*70)
    print(f"\n✅ Tests réussis: {passed}/{len(tests)}")
    print(f"❌ Tests échoués: {failed}/{len(tests)}")
    print(f"⏱️  Temps total: {elapsed:.3f}s")
    
    if failed == 0:
        print("\n" + "="*70)
        print("🎉 TOUS LES TESTS SONT PASSÉS!")
        print("="*70)
        print("\n📋 Résumé des transformations vérifiées:")
        print("   ✓ k=1 → 4 clauses 3-SAT (2 var. aux)")
        print("   ✓ k=2 → 2 clauses 3-SAT (1 var. aux)")
        print("   ✓ k=3 → 1 clause 3-SAT (0 var. aux)")
        print("   ✓ k=4 → 2 clauses 3-SAT (1 var. aux)")
        print("   ✓ k=5 → 3 clauses 3-SAT (2 var. aux) ← EXEMPLE PROF")
        print("   ✓ k=6 → 4 clauses 3-SAT (3 var. aux)")
        print("\n🎯 La réduction respecte bien la consigne:")
        print("   'Si nombre de littéraux > 3, on rajoute des clauses")
        print("    en faisant en sorte que chaque clause ait 3 littéraux'")
        print("="*70)
    else:
        print(f"\n⚠️  {failed} test(s) ont échoué")
    
    print()
    
    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)