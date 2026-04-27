import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# -------------------------------
# 1. Chargement des données
# -------------------------------
data = {
    "Ville": [f"V{i}" for i in range(1, 21)],
    "H. Ball": [1881.9, 3369.8, 4467.4, 1862.1, 3499.8, 3903.2, 2620.7, 3678.4, 3840.5, 2170.2,
                3920.4, 2599.6, 2828.5, 2498.7, 2685.1, 2739.3, 1662.1, 2469.9, 2350.7, 3177.7],
    "B. Ball": [96.8, 96.8, 138.2, 83.2, 287.0, 170.7, 129.5, 157.0, 187.9, 140.5,
                128.0, 39.6, 211.3, 123.2, 41.2, 100.7, 81.1, 142.9, 38.7, 292.1],
    "Tennis": [14.2, 10.8, 9.5, 8.8, 11.5, 6.3, 4.2, 6.0, 10.2, 11.7,
               7.2, 5.5, 9.9, 7.4, 2.3, 6.6, 10.1, 15.5, 2.4, 8.0],
    "Gym": [25.2, 51.6, 34.2, 27.6, 49.4, 42.0, 16.8, 24.9, 39.6, 31.1,
            25.5, 19.4, 21.8, 26.5, 10.6, 22.0, 19.1, 30.9, 13.5, 34.8],
    "Natation": [1135.5, 1331.7, 2346.1, 972.6, 2139.4, 1935.2, 1346.0, 1682.6, 1859.9, 1351.1,
                 1911.5, 1050.8, 1085.0, 1086.2, 812.5, 1270.4, 872.2, 1165.5, 1253.1, 1400.0],
    "F. Ball": [278.3, 284.0, 312.3, 203.4, 358.0, 292.9, 131.8, 194.2, 449.1, 256.5,
                64.1, 172.5, 209.0, 153.5, 89.8, 180.5, 123.3, 335.5, 170.0, 358.9]
}

df = pd.DataFrame(data)
individus = df["Ville"].values
variables = df.columns[1:].values
X = df[variables].values

# -------------------------------
# 2. ACP
# -------------------------------
scaler = StandardScaler()
X_centred_reduit = scaler.fit_transform(X)
pca = PCA()
scores = pca.fit_transform(X_centred_reduit)  # coordonnées des individus
loadings = pca.components_.T * np.sqrt(pca.explained_variance_)  # coordonnées des variables
inertie = pca.explained_variance_ratio_
valeurs_propres = pca.explained_variance_

# -------------------------------
# 3. Distance au centre du nuage (carré) dans sous-espace factoriel
# -------------------------------
# On prend les 3 premiers axes
scores_3d = scores[:, :3]
dist_carrees = np.sum(scores_3d**2, axis=1)

print("=== 1) Carré de la distance de chaque individu au centre dans sous-espace factoriel (3 axes) ===")
for i, d in enumerate(dist_carrees):
    print(f"Individu {individus[i]} : {d:.4f}")

print(f"\nSomme des distances : {np.sum(dist_carrees):.4f}")
print("\nDéduction : La somme des distances au centre dans l'espace factoriel = inertie totale projetée sur ces axes.")
print("C'est aussi la somme des valeurs propres des axes retenus.\n")

# -------------------------------
# 4. Qualité de représentation (cos²)
# -------------------------------
cos2 = np.zeros((len(individus), 3))
for i in range(3):
    cos2[:, i] = scores[:, i]**2 / np.sum(scores**2, axis=1)

print("=== 4) Qualité de représentation des individus (cos²) ===")
table_cos2 = pd.DataFrame(cos2, index=individus, columns=[f"Axe {i+1}" for i in range(3)])
print(table_cos2.round(4))
print("\nInterprétation : Plus cos² est proche de 1, mieux l'individu est représenté sur l'axe.")
print("Les individus avec cos² faible sur les 3 axes sont mal représentés dans le plan factoriel.\n")

# -------------------------------
# 5. Contribution des individus à l'inertie des axes
# -------------------------------
contrib_ind = np.zeros((len(individus), 3))
for j in range(3):
    contrib_ind[:, j] = (scores[:, j]**2) / (len(individus) * valeurs_propres[j]) * 100

print("=== 5) Contribution des individus à l'inertie de chaque axe (%) ===")
table_contrib_ind = pd.DataFrame(contrib_ind, index=individus, columns=[f"Axe {i+1}" for i in range(3)])
print(table_contrib_ind.round(2))
print("\nInterprétation : Un individu avec forte contribution participe beaucoup à la construction de l'axe.")
print("Généralement, on examine les contributions > moyenne (100/n_individus = 5%).\n")

# -------------------------------
# 6. Individus mal représentés
# -------------------------------
print("=== 6) Individus mal représentés (cos² < 0.5) ===")
for i in range(3):
    print(f"\nAxe {i+1} :")
    mal_representes = [(individus[j], cos2[j, i], np.sign(scores[j, i])) for j in range(len(individus)) if cos2[j, i] < 0.5]
    for ind, cos, signe in mal_representes:
        print(f"  {ind} : cos²={cos:.4f}, signe sur axe = {signe}")

# -------------------------------
# 7. Coordonnées des variables
# -------------------------------
print("\n=== B) Analyse des variables ===")
print("1) Coordonnées des variables sur les axes principaux (3 axes) :")
coord_var = pd.DataFrame(loadings[:, :3], index=variables, columns=[f"Axe {i+1}" for i in range(3)])
print(coord_var.round(4))

# -------------------------------
# 8. Cercle de corrélation (axes 1-2)
# -------------------------------
plt.figure(figsize=(8, 8))
for i, var in enumerate(variables):
    plt.arrow(0, 0, loadings[i, 0], loadings[i, 1], head_width=0.05, head_length=0.05, fc='red', ec='red')
    plt.text(loadings[i, 0]*1.1, loadings[i, 1]*1.1, var, fontsize=12)
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
circle = plt.Circle((0, 0), 1, color='blue', fill=False, linestyle='--')
plt.gca().add_artist(circle)
plt.xlabel(f"Axe 1 ({inertie[0]*100:.2f}%)")
plt.ylabel(f"Axe 2 ({inertie[1]*100:.2f}%)")
plt.title("Cercle de corrélation (axes 1-2)")
plt.grid()
plt.show()

# -------------------------------
# 9. Cercle de corrélation (axes 1-3)
# -------------------------------
plt.figure(figsize=(8, 8))
for i, var in enumerate(variables):
    plt.arrow(0, 0, loadings[i, 0], loadings[i, 2], head_width=0.05, head_length=0.05, fc='red', ec='red')
    plt.text(loadings[i, 0]*1.1, loadings[i, 2]*1.1, var, fontsize=12)
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
circle = plt.Circle((0, 0), 1, color='blue', fill=False, linestyle='--')
plt.gca().add_artist(circle)
plt.xlabel(f"Axe 1 ({inertie[0]*100:.2f}%)")
plt.ylabel(f"Axe 3 ({inertie[2]*100:.2f}%)")
plt.title("Cercle de corrélation (axes 1-3)")
plt.grid()
plt.show()

# -------------------------------
# 10. Qualité de représentation des variables
# -------------------------------
cos2_var = loadings**2
print("\n=== 5) Qualité de représentation des variables (cos²) ===")
table_cos2_var = pd.DataFrame(cos2_var[:, :3], index=variables, columns=[f"Axe {i+1}" for i in range(3)])
print(table_cos2_var.round(4))

# -------------------------------
# 11. Contribution des variables à l'inertie des axes
# -------------------------------
contrib_var = (loadings**2 / np.sum(loadings**2, axis=0)) * 100
print("\n=== 6) Contribution des variables à l'inertie de chaque axe (%) ===")
table_contrib_var = pd.DataFrame(contrib_var[:, :3], index=variables, columns=[f"Axe {i+1}" for i in range(3)])
print(table_contrib_var.round(2))

# -------------------------------
# 12. Graphe des individus et variables séparés
# -------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Individus
ax1.scatter(scores[:, 0], scores[:, 1], c='blue', alpha=0.7)
for i, ville in enumerate(individus):
    ax1.annotate(ville, (scores[i, 0], scores[i, 1]), fontsize=8)
ax1.axhline(0, color='black', linewidth=0.5)
ax1.axvline(0, color='black', linewidth=0.5)
ax1.set_xlabel(f"Axe 1 ({inertie[0]*100:.2f}%)")
ax1.set_ylabel(f"Axe 2 ({inertie[1]*100:.2f}%)")
ax1.set_title("Graphe des individus")
ax1.grid()

# Variables
for i, var in enumerate(variables):
    ax2.arrow(0, 0, loadings[i, 0], loadings[i, 1], head_width=0.05, head_length=0.05, fc='red', ec='red')
    ax2.text(loadings[i, 0]*1.1, loadings[i, 1]*1.1, var, fontsize=12)
ax2.set_xlim(-1, 1)
ax2.set_ylim(-1, 1)
ax2.axhline(0, color='black', linewidth=0.5)
ax2.axvline(0, color='black', linewidth=0.5)
circle = plt.Circle((0, 0), 1, color='blue', fill=False, linestyle='--')
ax2.add_artist(circle)
ax2.set_xlabel(f"Axe 1 ({inertie[0]*100:.2f}%)")
ax2.set_ylabel(f"Axe 2 ({inertie[1]*100:.2f}%)")
ax2.set_title("Cercle de corrélation")
ax2.grid()
plt.tight_layout()
plt.show()

# -------------------------------
# 13. Biplot (individus + variables superposés)
# -------------------------------
plt.figure(figsize=(10, 10))
# Individus
plt.scatter(scores[:, 0], scores[:, 1], c='blue', alpha=0.6, label='Individus')
for i, ville in enumerate(individus):
    plt.annotate(ville, (scores[i, 0], scores[i, 1]), fontsize=8, color='blue')
# Variables
for i, var in enumerate(variables):
    plt.arrow(0, 0, loadings[i, 0], loadings[i, 1], head_width=0.05, head_length=0.05, fc='red', ec='red')
    plt.text(loadings[i, 0]*1.1, loadings[i, 1]*1.1, var, fontsize=12, color='red')
plt.xlim(-4, 6)
plt.ylim(-3, 5)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.xlabel(f"Axe 1 ({inertie[0]*100:.2f}%)")
plt.ylabel(f"Axe 2 ({inertie[1]*100:.2f}%)")
plt.title("Biplot ACP - Individus et variables")
plt.legend()
plt.grid()
plt.show()

print("\nInterprétation des axes :")
print("- Axe 1 : fortement corrélé à H. Ball, Natation, F. Ball (sports collectifs et aquatiques).")
print("- Axe 2 : oppositions entre Tennis/Gym et B. Ball (sports de raquette/gymnastique vs basket).")
print("- Les variables proches du cercle unité sont bien représentées.")
print("- Les individus proches des variables pratiquent davantage ces sports.")