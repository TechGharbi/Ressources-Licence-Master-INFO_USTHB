import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# --- 1. Chargement des images ---
img_query = cv.imread('matricule1.png')
img_train = cv.imread('voit1.jpg')

# Conversion en niveaux de gris 
gray_query = cv.cvtColor(img_query, cv.COLOR_BGR2GRAY)
gray_train = cv.cvtColor(img_train, cv.COLOR_BGR2GRAY)

# --- 2. Creation du detecteur/descripteur SIFT ---
sift = cv.SIFT_create()

# detectAndCompute retourne :
#   kp   : liste de KeyPoint (points détectés)
#   desc : matrice (N x 128) des descripteurs — une ligne par keypoint
kp_query, desc_query = sift.detectAndCompute(gray_query, None)
kp_train, desc_train = sift.detectAndCompute(gray_train, None)

print(f"Nombre de keypoints — Query : {len(kp_query)}, Train : {len(kp_train)}")
print(f"Taille descripteurs  — Query : {desc_query.shape}, Train : {desc_train.shape}")

# On affiche les attributs des 5 premiers keypoints de la query
print("\n========== ATTRIBUTS DES KEYPOINTS (Query) ==========")
for i, kp in enumerate(kp_query[:5]):
    print(f"\n--- Keypoint {i} ---")
    print(f"  Position (x, y)  : {kp.pt}")          # coordonnées dans l'image
    print(f"  Taille (diamètre): {kp.size:.4f}")     # taille de la région caractéristique
    print(f"  Orientation      : {kp.angle:.4f}°")   # orientation dominante du gradient
    print(f"  Réponse (force)  : {kp.response:.6f}") # score de saillance du point
    print(f"  Octave           : {kp.octave}")        # niveau de la pyramide d'échelle
    print(f"  Descripteur[0:8] : {desc_query[i, :8]}") # aperçu des 8 premières valeurs / 128

# Affichage complet du descripteur du premier keypoint
print("\n========== DESCRIPTEUR COMPLET DU KEYPOINT 0 (Query) ==========")
print(f"Vecteur de {desc_query.shape[1]} dimensions :")
print(desc_query[0])

# DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS : dessine le cercle + l'orientation
img_kp_query = cv.drawKeypoints(
    gray_query, kp_query, None,
    flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
)
img_kp_train = cv.drawKeypoints(
    gray_train, kp_train, None,
    flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

axes[0].imshow(cv.cvtColor(img_kp_query, cv.COLOR_BGR2RGB))
axes[0].set_title(f'Query — {len(kp_query)} keypoints', fontsize=13)
axes[0].axis('off')

axes[1].imshow(cv.cvtColor(img_kp_train, cv.COLOR_BGR2RGB))
axes[1].set_title(f'Train — {len(kp_train)} keypoints', fontsize=13)
axes[1].axis('off')

plt.suptitle('Détection SIFT — Keypoints avec orientation et échelle', fontsize=14)
plt.tight_layout()
plt.show()

# Le descripteur SIFT est un vecteur de 128 valeurs organisé en
# 16 blocs (4x4) × 8 orientations = 128 dimensions
fig2, ax = plt.subplots(figsize=(14, 4))
ax.bar(range(128), desc_query[0], color='steelblue', width=0.8)
ax.set_title('Descripteur SIFT du keypoint 0 (Query) — 128 dimensions', fontsize=13)
ax.set_xlabel('Dimension (16 blocs × 8 orientations)')
ax.set_ylabel('Valeur')
ax.set_xticks(range(0, 128, 8))
ax.grid(axis='y', alpha=0.3)

# Délimiteurs visuels entre les 16 blocs
for i in range(0, 128, 8):
    ax.axvline(x=i, color='red', linewidth=0.5, alpha=0.5)

plt.tight_layout()
plt.show()
