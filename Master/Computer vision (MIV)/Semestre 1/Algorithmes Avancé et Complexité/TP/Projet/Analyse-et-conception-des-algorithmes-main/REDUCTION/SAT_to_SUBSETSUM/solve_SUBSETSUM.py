def solve_SUBSETSUM_DP(S, T):

    """
    Résout le problème du Subset Sum avec programmation dynamique.

    Args:
        S (list[int]): liste des entiers
        T (int): somme cible

    Returns:
        (bool, list[int] | None):
            - True et le sous-ensemble dont la somme = T
            - False et None si aucune solution
    """
    
    n = len(S)

    # T = 0
    if T == 0:
        return True, []

    # Initialisation de la table DP

    # dp[i][j] = True si on peut obtenir la somme j avec les i premiers éléments
    dp = [[False] * (T + 1) for _ in range(n + 1)]

    # somme 0 vraie pour tout i
    for i in range(n + 1):
        dp[i][0] = True

    # Remplissage de la table DP
    for i in range(1, n + 1):

        for j in range(1, T + 1):

            # On peut faire la somme j sans le i-ème élément
            dp[i][j] = dp[i - 1][j]

            # Ou en utilisant le i-ème élément si possible
            if S[i - 1] <= j:

                dp[i][j] = dp[i][j] or dp[i - 1][j - S[i - 1]]

    # Si la somme cible n’est pas atteignable
    if not dp[n][T]:
        return False, None

    # backtracking pour retrouver les éléments utilisés d'apres le sous ensemble obtenu
    solution = []
    i, j = n, T
    while i > 0 and j > 0:

        # Si la somme j n’était pas possible sans S[i-1], alors on prend S[i-1]
        if not dp[i - 1][j]:
            solution.append(S[i - 1])
            j -= S[i - 1]
        i -= 1

    # On inverse pour obtenir l’ordre original
    solution.reverse()
    return True, solution

# tests simples
if __name__ == "__main__":
    # Liste de tests simples
    tests = [
        ([3, 4, 5, 2], 9),
        ([1, 2, 3, 4], 6),
        ([1, 2, 3, 4, 5], 15),
        ([2, 3, 7], 5),
    ]

    for S, T in tests:
        res, sol = solve_SUBSETSUM_DP(S, T)
        if res:
            print(f"S={S}, T={T} -> Solution: {sol}, somme={sum(sol)}")
        else:
            print(f"S={S}, T={T} -> Pas de solution")