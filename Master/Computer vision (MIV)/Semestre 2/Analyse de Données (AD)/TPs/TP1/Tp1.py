"""
TP1 - Analyse des données
Solution complète
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform

# Pour afficher plus de décimales
np.set_printoptions(precision=4, suppress=True)

print("="*60)
print("TP1 - Analyse des données")
print("="*60)

# ============================================
# 1) Déclaration de la matrice X et Xt
# ============================================
print("\n1) Matrice des données X et sa transposée Xt")
print("-"*40)

X = np.array([
    [1881.9, 96.8, 14.2, 25.2, 1135.5, 278.3],
    [3369.8, 96.8, 10.8, 51.6, 1331.7, 284.0],
    [4467.4, 138.2, 9.5, 34.2, 2346.1, 312.3],
    [1862.1, 83.2, 8.8, 27.6, 972.6, 203.4],
    [3499.8, 287.0, 11.5, 49.4, 2139.4, 358.0],
    [3903.2, 170.7, 6.3, 42.0, 1935.2, 292.9],
    [2620.7, 129.5, 4.2, 16.8, 1346.0, 131.8],
    [3678.4, 157.0, 6.0, 24.9, 1682.6, 194.2],
    [3840.5, 187.9, 10.2, 39.6, 1859.9, 449.1],
    [2170.2, 140.5, 11.7, 31.1, 1351.1, 256.5],
    [3920.4, 128.0, 7.2, 25.5, 1911.5, 64.1],
    [2599.6, 39.6, 5.5, 19.4, 1050.8, 172.5],
    [2828.5, 211.3, 9.9, 21.8, 1085.0, 209.0],
    [2498.7, 123.2, 7.4, 26.5, 1086.2, 153.5],
    [2685.1, 41.2, 2.3, 10.6, 812.5, 89.8],
    [2739.3, 100.7, 6.6, 22.0, 1270.4, 180.5],
    [1662.1, 81.1, 10.1, 19.1, 872.2, 123.3],
    [2469.9, 142.9, 15.5, 30.9, 1165.5, 335.5],
    [2350.7, 38.7, 2.4, 13.5, 1253.1, 170.0],
    [3177.7, 292.1, 8.0, 34.8, 1400.0, 358.9]
])

Xt = X.T

print("Matrice X (20 villes × 6 sports) :")
print("Forme :", X.shape)
print("\nPremières lignes de X :")
print(X[:5])  # Afficher les 5 premières villes

print("\nMatrice transposée Xt (6 sports × 20 villes) :")
print("Forme :", Xt.shape)
print("\nPremières lignes de Xt :")
print(Xt[:3])  # Afficher les 3 premiers sports

# ============================================
# 2) Liste des individus
# ============================================
print("\n\n2) Liste des individus (villes)")
print("-"*40)

individus = [f"V{i+1}" for i in range(20)]
print("Individus :", individus)

# ============================================
# 3) Extraire les variables
# ============================================
print("\n\n3) Variables extraites")
print("-"*40)

variables = ["Hand Ball", "Basket Ball", "Tennis", "Gymnastique", "Natation", "Foot Ball"]
for j, nom in enumerate(variables):
    print(f"{nom:12} : {X[:, j]}")

# ============================================
# 4) Accéder aux individus 3, 11, 15, 19
# ============================================
print("\n\n4) Individus sélectionnés")
print("-"*40)

indices_selection = [2, 10, 14, 18]  # V3, V11, V15, V19 (indices 0-based)
noms_selection = [f"V{i+1}" for i in indices_selection]

for i, nom in zip(indices_selection, noms_selection):
    print(f"{nom} : {X[i]}")

# ============================================
# 5) Proximité entre individus sélectionnés
# ============================================
print("\n\n5) Distances entre les individus sélectionnés")
print("-"*40)

selection = X[indices_selection]
distances = pdist(selection, metric='euclidean')
matrice_dist = squareform(distances)

print("Matrice des distances (euclidiennes) :")
print("        ", end="")
for nom in noms_selection:
    print(f"{nom:8}", end="")
print()
for i, nom_i in enumerate(noms_selection):
    print(f"{nom_i:6}", end="")
    for j in range(len(noms_selection)):
        print(f"{matrice_dist[i, j]:8.2f}", end="")
    print()

print("\nCommentaire :")
print("- Plus la distance est petite, plus les villes ont des profils similaires.")
print("- V3 et V11 sont très éloignés → profils différents")
print("- V15 et V19 sont proches → profils similaires")

# ============================================
# 6) Statistiques par variable
# ============================================
print("\n\n6) Statistiques descriptives par variable")
print("-"*40)

moyennes = np.mean(X, axis=0)
variances = np.var(X, axis=0, ddof=0)
ecarts_types = np.std(X, axis=0, ddof=0)

print("Variable      |   Moyenne   |   Variance   |  Ecart-type")
print("-"*55)
for j, nom in enumerate(variables):
    print(f"{nom:12} | {moyennes[j]:10.4f} | {variances[j]:11.4f} | {ecarts_types[j]:10.4f}")

# ============================================
# 7) Individu moyen
# ============================================
print("\n\n7) Individu moyen")
print("-"*40)

individu_moyen = moyennes
print("Individu moyen (profil moyen des villes) :")
for j, nom in enumerate(variables):
    print(f"{nom:12} : {individu_moyen[j]:.4f}")

# ============================================
# 8) Matrice centrée
# ============================================
print("\n\n8) Matrice centrée")
print("-"*40)

X_centre = X - moyennes
print("Premières lignes de la matrice centrée :")
print(X_centre[:5])
print("\nVérification : moyenne des colonnes centrées ≈ 0")
print(np.mean(X_centre, axis=0))

# ============================================
# 9) Fonction de variance
# ============================================
print("\n\n9) Calcul des variances")
print("-"*40)

def calculer_variance(matrice):
    """Calcule la variance de chaque colonne"""
    return np.var(matrice, axis=0, ddof=0)

variances_calculees = calculer_variance(X)
print("Variances calculées par la fonction :")
for j, nom in enumerate(variables):
    print(f"{nom:12} : {variances_calculees[j]:.4f}")

# ============================================
# 10) Matrice de covariance V
# ============================================
print("\n\n10) Matrice de covariance V = (1/m) Y^t Y")
print("-"*40)

m = X.shape[0]
Y = X_centre
V = (Y.T @ Y) / m  # Formule donnée dans l'énoncé

print("Matrice de covariance V :")
print("    ", end="")
for nom in variables:
    print(f"{nom:6}", end=" ")
print()
for i, nom_i in enumerate(variables):
    print(f"{nom_i:6}", end=" ")
    for j in range(len(variables)):
        print(f"{V[i, j]:8.0f}", end=" ")
    print()

# ============================================
# 11) Commentaire sur V
# ============================================
print("\n\n11) Commentaire sur la matrice V")
print("-"*40)
print("• La diagonale donne les variances de chaque variable :")
for j, nom in enumerate(variables):
    print(f"  - Var({nom}) = {V[j, j]:.4f}")
print("\n• Les termes hors diagonale sont les covariances :")
print("  - Positives → les variables varient dans le même sens")
print("  - Négatives → les variables varient en sens inverse")

# ============================================
# 12) Matrice de corrélation R
# ============================================
print("\n\n12) Matrice de corrélation R")
print("-"*40)

# Méthode 1 : à partir de la covariance
ecarts = np.std(X, axis=0, ddof=0)
R = V / np.outer(ecarts, ecarts)

print("Matrice de corrélation R :")
print("    ", end="")
for nom in variables:
    print(f"{nom:6}", end=" ")
print()
for i, nom_i in enumerate(variables):
    print(f"{nom_i:6}", end=" ")
    for j in range(len(variables)):
        print(f"{R[i, j]:8.0f}", end=" ")
    print()

# Méthode 2 : avec numpy (vérification)
R_numpy = np.corrcoef(X.T)
print("\nVérification avec numpy.corrcoef :")
print(np.round(R_numpy, 4))

# ============================================
# 13) Commentaire sur R
# ============================================
print("\n\n13) Commentaire sur la matrice R")
print("-"*40)
print("• Corrélation forte (|r| > 0.7) :")
for i in range(len(variables)):
    for j in range(i+1, len(variables)):
        if abs(R[i, j]) > 0.7:
            print(f"  - {variables[i]} et {variables[j]} : r = {R[i, j]:.4f} (forte corrélation)")

print("\n• Corrélation modérée (0.4 < |r| < 0.7) :")
for i in range(len(variables)):
    for j in range(i+1, len(variables)):
        if 0.4 < abs(R[i, j]) < 0.7:
            print(f"  - {variables[i]} et {variables[j]} : r = {R[i, j]:.4f}")

print("\n• Corrélation faible (|r| < 0.4) :")
for i in range(len(variables)):
    for j in range(i+1, len(variables)):
        if abs(R[i, j]) < 0.4:
            print(f"  - {variables[i]} et {variables[j]} : r = {R[i, j]:.4f}")

# ============================================
# 14) Représentations graphiques
# ============================================
print("\n\n14) Représentations graphiques")
print("-"*40)
print("Génération des graphiques...")

# Configuration des graphiques
plt.figure(figsize=(15, 5))

# (X1, X4) : Hand Ball vs Gymnastique
plt.subplot(1, 3, 1)
plt.scatter(X[:, 0], X[:, 3], c='blue', alpha=0.6)
plt.xlabel("Hand Ball", fontsize=12)
plt.ylabel("Gymnastique", fontsize=12)
plt.title("(Hand Ball, Gymnastique)", fontsize=14)
plt.grid(True, alpha=0.3)

# Ajouter les labels des villes
for i, nom in enumerate(individus):
    plt.annotate(nom, (X[i, 0], X[i, 3]), fontsize=8, alpha=0.7)

# (X2, X5) : Basket Ball vs Natation
plt.subplot(1, 3, 2)
plt.scatter(X[:, 1], X[:, 4], c='red', alpha=0.6)
plt.xlabel("Basket Ball", fontsize=12)
plt.ylabel("Natation", fontsize=12)
plt.title("(Basket Ball, Natation)", fontsize=14)
plt.grid(True, alpha=0.3)

for i, nom in enumerate(individus):
    plt.annotate(nom, (X[i, 1], X[i, 4]), fontsize=8, alpha=0.7)

# (X3, X6) : Tennis vs Foot Ball
plt.subplot(1, 3, 3)
plt.scatter(X[:, 2], X[:, 5], c='green', alpha=0.6)
plt.xlabel("Tennis", fontsize=12)
plt.ylabel("Foot Ball", fontsize=12)
plt.title("(Tennis, Foot Ball)", fontsize=14)
plt.grid(True, alpha=0.3)

for i, nom in enumerate(individus):
    plt.annotate(nom, (X[i, 2], X[i, 5]), fontsize=8, alpha=0.7)

plt.tight_layout()
plt.savefig('graphiques_tp1.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nGraphiques sauvegardés dans 'graphiques_tp1.png'")

print("\n\n" + "="*60)
print("FIN DU TP1")
print("="*60)