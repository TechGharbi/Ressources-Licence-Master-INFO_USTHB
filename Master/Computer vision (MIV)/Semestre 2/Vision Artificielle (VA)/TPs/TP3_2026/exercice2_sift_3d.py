"""
========================================================
TP3 - EXERCICE 2 : RECONSTRUCTION 3D PAR SIFT
========================================================
Translation horizontale connue (baseline b)
Etapes :
  1. Charger les deux images stereo
  2. Detecter et matcher les points SIFT
  3. Calculer les coordonnees 3D (triangulation)
  4. Visualiser le nuage de points 3D

Comment executer :
  py exercice2_reconstruction_3d.py
========================================================
"""

import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# -------------------------------------------------------
# PARAMETRES
# -------------------------------------------------------
IMG_LEFT  = 'stereo_images/left.jpg'
IMG_RIGHT = 'stereo_images/right.jpg'
BASELINE  = 0.15    # distance de translation en metres
RATIO_LOWE = 0.75   # ratio test de Lowe

print("="*60)
print("  EXERCICE 2 : RECONSTRUCTION 3D AVEC SIFT")
print("="*60)

# -------------------------------------------------------
# 1. Chargement de K
# -------------------------------------------------------
K_path = 'stereo_images/K.npy'
if os.path.exists('camera_matrix.npy'):
    K = np.load('camera_matrix.npy')
    print("K charge depuis camera_matrix.npy (calibration)")
elif os.path.exists(K_path):
    K = np.load(K_path)
    print("K charge depuis stereo_images/K.npy")
else:
    img_tmp = cv2.imread(IMG_LEFT)
    H_t, W_t = img_tmp.shape[:2]
    f  = float(max(W_t, H_t))
    K  = np.float64([[f,0,W_t/2],[0,f,H_t/2],[0,0,1]])
    print(f"K estime automatiquement : f={f:.0f}")

fx = K[0,0]; cx = K[0,2]; cy = K[1,2]
print(f"  fx={fx:.1f}  cx={cx:.1f}  cy={cy:.1f}")
print(f"  Baseline b = {BASELINE} m")

# -------------------------------------------------------
# 2. Chargement images
# -------------------------------------------------------
img_left_c  = cv2.imread(IMG_LEFT)
img_right_c = cv2.imread(IMG_RIGHT)

if img_left_c is None or img_right_c is None:
    print("ERREUR : images introuvables !")
    exit()

img_left_g  = cv2.cvtColor(img_left_c,  cv2.COLOR_BGR2GRAY)
img_right_g = cv2.cvtColor(img_right_c, cv2.COLOR_BGR2GRAY)
img_left_rgb = cv2.cvtColor(img_left_c, cv2.COLOR_BGR2RGB)

H_img, W_img = img_left_c.shape[:2]
print(f"\nImages : {W_img}x{H_img}")

# -------------------------------------------------------
# 3. Detection SIFT
# -------------------------------------------------------
sift = cv2.SIFT_create()
kp_l, desc_l = sift.detectAndCompute(img_left_g,  None)
kp_r, desc_r = sift.detectAndCompute(img_right_g, None)

print(f"\nKeypoints : gauche={len(kp_l)}  droite={len(kp_r)}")

# -------------------------------------------------------
# 4. Matching + Ratio Test de Lowe
# -------------------------------------------------------
bf      = cv2.BFMatcher(cv2.NORM_L2)
matches = bf.knnMatch(desc_l, desc_r, k=2)
good    = [m for m, n in matches if m.distance < RATIO_LOWE * n.distance]

print(f"Matches valides : {len(good)}")

if len(good) < 5:
    print("ERREUR : pas assez de matches !")
    exit()

pts_left  = np.float32([kp_l[m.queryIdx].pt for m in good])
pts_right = np.float32([kp_r[m.trainIdx].pt for m in good])

# -------------------------------------------------------
# 5. Triangulation - Calcul des coordonnees 3D
# -------------------------------------------------------
disparities = pts_left[:,0] - pts_right[:,0]
disp_mean   = np.mean(disparities)
sign = -1.0 if disp_mean < 0 else 1.0

print(f"Disparite moyenne : {disp_mean:.1f} px")
if disp_mean < 0:
    print("Correction signe automatique (disparite negative)")

points_3d = []
colors_3d = []
rejected  = 0

Z_MIN, Z_MAX = 0.1, 5.0

for i in range(len(pts_left)):
    xl, yl = pts_left[i]
    xr, yr = pts_right[i]
    d = sign * (xl - xr)

    if abs(d) < 0.5:
        rejected += 1
        continue

    Z = (fx * BASELINE) / d

    if Z < Z_MIN or Z > Z_MAX:
        rejected += 1
        continue

    X = (xl - cx) * Z / fx
    Y = (yl - cy) * Z / fx
    points_3d.append([X, Y, Z])

    xi = int(np.clip(xl, 0, W_img-1))
    yi = int(np.clip(yl, 0, H_img-1))
    r, g, b = img_left_rgb[yi, xi]
    colors_3d.append([r/255., g/255., b/255.])

if not points_3d:
    print("ERREUR : 0 points reconstruits !")
    exit()

points_3d = np.array(points_3d)
colors_3d = np.array(colors_3d)

print(f"\nPoints reconstruits : {len(points_3d)}  rejetes : {rejected}")
print(f"Z min={points_3d[:,2].min():.2f}m  max={points_3d[:,2].max():.2f}m  moy={points_3d[:,2].mean():.2f}m")

print(f"\n{'#':>3}  {'X (m)':>8}  {'Y (m)':>8}  {'Z (m)':>8}")
print("-"*35)
for i in range(min(10, len(points_3d))):
    print(f"{i:>3}  {points_3d[i,0]:>8.3f}  {points_3d[i,1]:>8.3f}  {points_3d[i,2]:>8.3f}")

np.save('points_3d_ex2.npy', points_3d)

# -------------------------------------------------------
# 6. Visualisation
# -------------------------------------------------------
img_matches = cv2.drawMatches(
    img_left_c, kp_l, img_right_c, kp_r,
    good[:40], None,
    matchColor=(0,255,0), singlePointColor=(255,0,0),
    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
)

fig = plt.figure(figsize=(18, 12))

# Matches
ax0 = fig.add_subplot(231)
ax0.imshow(cv2.cvtColor(img_matches, cv2.COLOR_BGR2RGB))
ax0.set_title(f'Matches SIFT : {len(good)} points', fontsize=11)
ax0.axis('off')

# 3D scatter
ax1 = fig.add_subplot(232, projection='3d')
sc = ax1.scatter(points_3d[:,0], points_3d[:,2], -points_3d[:,1],
                  c=points_3d[:,2], cmap='viridis', s=30, alpha=0.9)
ax1.set_xlabel('X (m)'); ax1.set_ylabel('Z (m)'); ax1.set_zlabel('Y (m)')
ax1.set_title('Nuage de points 3D', fontsize=11)
plt.colorbar(sc, ax=ax1, shrink=0.5, label='Z (m)')

# Vue dessus
ax2 = fig.add_subplot(233)
ax2.scatter(points_3d[:,0], points_3d[:,2], c=points_3d[:,2], cmap='viridis', s=30)
ax2.set_xlabel('X (m)'); ax2.set_ylabel('Z (m)')
ax2.set_title('Vue dessus (X-Z)', fontsize=11); ax2.grid(alpha=0.3)

# Vue face
ax3 = fig.add_subplot(234)
ax3.scatter(points_3d[:,0], -points_3d[:,1], c=points_3d[:,2], cmap='plasma', s=30)
ax3.set_xlabel('X (m)'); ax3.set_ylabel('Y (m)')
ax3.set_title('Vue face (X-Y)', fontsize=11); ax3.grid(alpha=0.3)

# Image avec points
ax4 = fig.add_subplot(235)
ax4.imshow(img_left_rgb)
ax4.scatter(pts_left[:,0], pts_left[:,1], c='lime', s=10, alpha=0.7,
            label=f'{len(pts_left)} pts')
ax4.set_title('Points SIFT gauche', fontsize=11)
ax4.legend(fontsize=9); ax4.axis('off')

# Histogram Z
ax5 = fig.add_subplot(236)
ax5.hist(points_3d[:,2], bins=15, color='steelblue', edgecolor='black', alpha=0.8)
ax5.axvline(points_3d[:,2].mean(), color='red', linestyle='--',
             label=f"Moy={points_3d[:,2].mean():.2f} m")
ax5.set_xlabel('Z (m)'); ax5.set_ylabel('Nombre de points')
ax5.set_title('Distribution profondeurs', fontsize=11)
ax5.legend(); ax5.grid(alpha=0.3)

plt.suptitle(f'Exercice 2 : Reconstruction 3D SIFT | b={BASELINE}m | {len(points_3d)} pts',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('exercice2_reconstruction.png', dpi=150, bbox_inches='tight')
print("\nSauvegarde : exercice2_reconstruction.png")
plt.show()
