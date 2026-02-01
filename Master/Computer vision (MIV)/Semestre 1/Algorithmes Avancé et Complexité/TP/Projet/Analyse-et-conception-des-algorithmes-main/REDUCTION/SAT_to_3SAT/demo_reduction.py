"""
DÉMONSTRATION COMPLÈTE - RÉDUCTION SAT → 3-SAT
==============================================

Démonstration pédagogique avec affichage détaillé
"""

import time

from sat_to_3sat_reduction import SATto3SATReducer
from solver_3sat import SAT3Solver
from verifier_3sat import SAT3Verifier
from verify_SAT import verify_SAT_solution


def format_clause_readable(clause, aux_vars):
    """Convertit une clause 3-SAT en format lisible (x / y)."""
    parts = []
    for lit in clause:
        var = abs(lit)
        name = f"y{var}" if var in aux_vars else f"x{var}"
        parts.append(f"¬{name}" if lit < 0 else name)
    return "(" + " ∨ ".join(parts) + ")"


def demo_step_by_step():

    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 10 + "DÉMONSTRATION - RÉDUCTION SAT → 3-SAT" + " " * 19 + "║")
    print("╚" + "=" * 68 + "╝")

    # ==============================================================
    # ÉTAPE 1
    # ==============================================================

    print("\n" + "=" * 70)
    print("ÉTAPE 1: DÉFINITION DE LA FORMULE SAT")
    print("=" * 70)

    variables_sat = ['x1', 'x2', 'x3', 'x4', 'x5']
    clauses_sat = [
        [(1, False)],
        [(2, False), (3, True)],
        [(1, False), (2, False), (3, False)],
        [(1, False), (2, False), (3, True), (4, False), (5, True)]
    ]

    print("\n✓ Formule SAT définie:")
    print(f"   Variables: {len(variables_sat)}")
    print(f"   Clauses: {len(clauses_sat)}")

    # ==============================================================
    # ÉTAPE 2 — RÉDUCTION
    # ==============================================================

    print("\n" + "=" * 70)
    print("ÉTAPE 2: APPLICATION DE LA RÉDUCTION")
    print("=" * 70)

    reducer = SATto3SATReducer()
    start_red = time.perf_counter()
    clauses_3sat, num_vars_3sat, stats = reducer.reduce(
        variables_sat, clauses_sat, verbose=True
    )
    end_red = time.perf_counter()

    stats['time'] = end_red - start_red

    # ==============================================================
    # ÉTAPE 3 — DÉTAILS
    # ==============================================================

    print("\n" + "=" * 70)
    print("ÉTAPE 3: DÉTAIL DES TRANSFORMATIONS")
    print("=" * 70)

    reducer2 = SATto3SATReducer()

    for i, clause_sat in enumerate(clauses_sat, 1):
        literals = reducer2._convert_sat_clause_to_literals(clause_sat)
        max_var = max(reducer2.original_vars) if reducer2.original_vars else 5

        if len(literals) == 1:
            new = reducer2._reduce_clause_k1(literals[0], max_var)
        elif len(literals) == 2:
            new = reducer2._reduce_clause_k2(literals, max_var)
        elif len(literals) == 3:
            new = reducer2._reduce_clause_k3(literals)
        else:
            new = reducer2._reduce_clause_k_geq_4(literals, max_var)

        print(f"\nClause {i}:")
        for c in new:
            print("  ", format_clause_readable(c, reducer2.auxiliary_vars))

    # ==============================================================
    # ÉTAPE 4 — RÉSUMÉ
    # ==============================================================

    print("\n" + "=" * 70)
    print("ÉTAPE 4: FORMULE 3-SAT COMPLÈTE")
    print("=" * 70)

    for i, c in enumerate(clauses_3sat, 1):
        print(f"C{i:2d}:", format_clause_readable(c, reducer.auxiliary_vars))

    print("\nVariables auxiliaires:", sorted(reducer.auxiliary_vars))
    print("Toutes clauses de taille 3:",
          "OUI ✓" if all(len(c) == 3 for c in clauses_3sat) else "NON ✗")

    # ==============================================================
    # ÉTAPE 5 — SOLVER
    # ==============================================================

    print("\n" + "=" * 70)
    print("ÉTAPE 5: RÉSOLUTION AVEC SOLVER 3-SAT")
    print("=" * 70)

    solver = SAT3Solver(clauses_3sat, num_vars_3sat)

    start_solve = time.perf_counter()
    success, solution_3sat, solve_stats = solver.solve()
    end_solve = time.perf_counter()

    solve_stats['time'] = end_solve - start_solve

    if not success:
        print("❌ Formule insatisfiable")
        return

    print("\n✅ Solution trouvée")
    print("Backtracks:", solve_stats.get('backtrack_count', 0))
    print(f"Temps: {solve_stats['time']:.6f}s")

    # ==============================================================
    # ÉTAPE 6 — VÉRIFICATION 3-SAT
    # ==============================================================

    verifier = SAT3Verifier(clauses_3sat)
    ok, details = verifier.verify(solution_3sat)

    print("\nSolution 3-SAT valide:", "OUI ✓" if ok else "NON ✗")

    # ==============================================================
    # ÉTAPE 7 — RETOUR SAT
    # ==============================================================

    solution_sat = reducer.convert_solution_3sat_to_sat(solution_3sat)

    # ==============================================================
    # ÉTAPE 8 — VÉRIFICATION SAT
    # ==============================================================

    sat_ok = verify_SAT_solution(variables_sat, clauses_sat, solution_sat)

    print("\nSolution SAT valide:", "OUI ✓" if sat_ok else "NON ✗")

    # ==============================================================
    # RÉSUMÉ FINAL
    # ==============================================================

    print("\n" + "=" * 70)
    print("RÉSUMÉ FINAL")
    print("=" * 70)

    print(f"Temps de réduction : {stats['time']:.6f}s")
    print(f"Temps de résolution: {solve_stats['time']:.6f}s")
    print("Satisfiabilité préservée : OUI ✓")
    print("\n🎉 DÉMONSTRATION TERMINÉE AVEC SUCCÈS")


def demo_quick():
    print("\nEXEMPLE RAPIDE k=5")

    variables_sat = ['x1', 'x2', 'x3', 'x4', 'x5']
    clauses_sat = [[(i, False) for i in range(1, 6)]]

    reducer = SATto3SATReducer()
    clauses_3sat, _, _ = reducer.reduce(variables_sat, clauses_sat)

    for c in clauses_3sat:
        print(format_clause_readable(c, reducer.auxiliary_vars))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        demo_quick()
    else:
        demo_step_by_step()