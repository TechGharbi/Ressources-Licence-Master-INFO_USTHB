"""
========================================================
TP3 - EXERCICE 3 : CARTE DE DISPARITE (DISPARITY MAP)
========================================================
Calcule la carte de disparite pour une paire d'images
stereo avec translation axiale (mouvement avant/arriere)

Utilise les donnees Middlebury ou vos propres images.

Comment executer :
  py exercice3_disparity_map.py

Telechargez des images Middlebury ici :
  https://vision.middlebury.edu/stereo/data/
========================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# -------------------------------------------------------
# PARAMETRES
# -------------------------------------------------------
IMG_LEFT  = 'middlebury/left.png'
IMG_RIGHT = 'middlebury/right.png'

# Parametres StereoBM (algorithme rapide)
NUM_DISPARITIES = 64   # multiple de 16
BLOCK_SIZE      = 15   # impair entre 5 et 255

# Parametres StereoSGBM (algorithme de qualite)
USE_SGBM = True        # True = SGBM, False = BM simple

print("="*60)
print("  EXERCICE 3 : CARTE DE DISPARITE")
print("="*60)

# -------------------------------------------------------
# 1. Chargement des images
# -------------------------------------------------------
img_left  = cv2.imread(IMG_LEFT)
img_right = cv2.imread(IMG_RIGHT)

if img_left is None or img_right is None:
    print(f"ERREUR : images introuvables dans 'middlebury/'")
    print("Telechargez les images depuis :")
    print("  https://vision.middlebury.edu/stereo/data/")
    exit()

gray_left  = cv2.cvtColor(img_left,  cv2.COLOR_BGR2GRAY)
gray_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2GRAY)
H, W = gray_left.shape
print(f"Images : {W}x{H}")

# -------------------------------------------------------
# 2. Calcul de la disparite
# -------------------------------------------------------
algo_name = "SGBM" if USE_SGBM else "BM"
print(f"Algorithme : Stereo{algo_name}")

if USE_SGBM:
    # StereoSGBM - meilleure qualite
    stereo = cv2.StereoSGBM_create(
        minDisparity   = 0,
        numDisparities = NUM_DISPARITIES,
        blockSize      = BLOCK_SIZE,
        P1 = 8  * 3 * BLOCK_SIZE**2,
        P2 = 32 * 3 * BLOCK_SIZE**2,
        disp12MaxDiff  = 1,
        uniquenessRatio = 10,
        speckleWindowSize = 100,
        speckleRange      = 32,
        mode = cv2.STEREO_SGBM_MODE_SGBM_3WAY
    )
else:
    # StereoBM - plus rapide
    stereo = cv2.StereoBM_create(
        numDisparities = NUM_DISPARITIES,
        blockSize      = BLOCK_SIZE
    )

# Calcul
disparity = stereo.compute(gray_left, gray_right).astype(np.float32) / 16.0

# -------------------------------------------------------
# 3. Post-traitement
# -------------------------------------------------------
# Masquer les regions invalides (disparite <= 0)
disp_valid = np.copy(disparity)
disp_valid[disp_valid <= 0] = np.nan

# Normalisation pour affichage
disp_norm = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
disp_color = cv2.applyColorMap(disp_norm, cv2.COLORMAP_JET)

print(f"\nDisparite :")
valid_mask = disparity > 0
if valid_mask.any():
    print(f"  Min  : {disparity[valid_mask].min():.1f} px")
    print(f"  Max  : {disparity[valid_mask].max():.1f} px")
    print(f"  Moy  : {disparity[valid_mask].mean():.1f} px")
    print(f"  Pixels valides : {valid_mask.sum()}/{H*W} ({100*valid_mask.mean():.1f}%)")

# -------------------------------------------------------
# 4. Sauvegarde
# -------------------------------------------------------
cv2.imwrite('disparity_map_color.png', disp_color)
cv2.imwrite('disparity_map_gray.png', disp_norm)
np.save('disparity_map.npy', disparity)
print("\nSauvegardes :")
print("  disparity_map_color.png")
print("  disparity_map_gray.png")
print("  disparity_map.npy")

# -------------------------------------------------------
# 5. Visualisation
# -------------------------------------------------------
fig, axes = plt.subplots(2, 3, figsize=(18, 10))

axes[0,0].imshow(cv2.cvtColor(img_left, cv2.COLOR_BGR2RGB))
axes[0,0].set_title('Image gauche (reference)', fontsize=11)
axes[0,0].axis('off')

axes[0,1].imshow(cv2.cvtColor(img_right, cv2.COLOR_BGR2RGB))
axes[0,1].set_title('Image droite (decalee)', fontsize=11)
axes[0,1].axis('off')

im = axes[0,2].imshow(disparity, cmap='jet',
                       vmin=0, vmax=NUM_DISPARITIES)
axes[0,2].set_title(f'Carte de disparite ({algo_name})', fontsize=11)
axes[0,2].axis('off')
plt.colorbar(im, ax=axes[0,2], shrink=0.8, label='Disparite (px)')

axes[1,0].imshow(cv2.cvtColor(disp_color, cv2.COLOR_BGR2RGB))
axes[1,0].set_title('Disparite coloree (JET)', fontsize=11)
axes[1,0].axis('off')

# Histogramme
valid_disp = disparity[disparity > 0].flatten()
if len(valid_disp) > 0:
    axes[1,1].hist(valid_disp, bins=30, color='steelblue',
                   edgecolor='black', alpha=0.8)
    axes[1,1].set_xlabel('Disparite (pixels)')
    axes[1,1].set_ylabel('Nombre de pixels')
    axes[1,1].set_title('Distribution des disparites', fontsize=11)
    axes[1,1].axvline(valid_disp.mean(), color='red', linestyle='--',
                       label=f"Moy={valid_disp.mean():.1f} px")
    axes[1,1].legend(); axes[1,1].grid(alpha=0.3)

# Profondeur estimee (si K connue)
K_path = 'camera_matrix.npy'
if os.path.exists(K_path):
    K = np.load(K_path)
    fx = K[0,0]
    BASELINE = 0.05  # estimation 5cm pour translation axiale
    depth_map = np.zeros_like(disparity)
    mask = disparity > 0.5
    depth_map[mask] = (fx * BASELINE) / disparity[mask]
    depth_map[depth_map > 10] = 0  # filtrer valeurs aberrantes

    im2 = axes[1,2].imshow(depth_map, cmap='plasma', vmin=0, vmax=3)
    axes[1,2].set_title('Carte de profondeur Z (m)', fontsize=11)
    axes[1,2].axis('off')
    plt.colorbar(im2, ax=axes[1,2], shrink=0.8, label='Z (m)')
    print(f"\nCarte de profondeur estimee (b=5cm)")
else:
    axes[1,2].imshow(disp_norm, cmap='gray')
    axes[1,2].set_title('Disparite niveaux gris', fontsize=11)
    axes[1,2].axis('off')

plt.suptitle(f'Exercice 3 : Carte de Disparite Stereo | Algo={algo_name}\n'
             f'numDisparities={NUM_DISPARITIES}  blockSize={BLOCK_SIZE}',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('exercice3_disparity.png', dpi=150, bbox_inches='tight')
print("  exercice3_disparity.png")
plt.show()

# -------------------------------------------------------
# 6. Discussion des resultats
# -------------------------------------------------------
print("\n" + "="*60)
print("  DISCUSSION DES RESULTATS")
print("="*60)
print("""
- Pixels BLANCS/JAUNES : objets PROCHES (grande disparite)
- Pixels BLEUS/NOIRS   : objets LOIN    (petite disparite)

Relation disparite-profondeur :
  Z = (fx * baseline) / disparite

Problemes courants :
  - Regions lisses (fond blanc) : disparite nulle (invalide)
  - Occlusions : zones masquees dans une image
  - Bruit : filtrage par speckle et uniqueness ratio

Pour ameliorer :
  - Augmenter numDisparities si les objets semblent tronques
  - Reduire blockSize pour plus de details (mais plus de bruit)
  - Utiliser USE_SGBM = True pour meilleure qualite
""")
