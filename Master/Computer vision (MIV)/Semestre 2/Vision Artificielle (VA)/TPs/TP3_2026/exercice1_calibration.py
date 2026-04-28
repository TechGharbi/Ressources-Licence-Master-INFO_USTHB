"""
========================================================
TP3 - EXERCICE 1 : CALIBRATION CAMERA (METHODE ZHANG)
========================================================
Utilise des images de damier pour calculer :
  - Matrice intrinseque K (fx, fy, cx, cy)
  - Coefficients de distorsion (k1, k2, p1, p2, k3)
  - Parametres extrinseques (rvecs, tvecs)

Comment executer :
  py exercice1_calibration.py
========================================================
"""

import cv2
import numpy as np
import glob
import os
import matplotlib.pyplot as plt

# -------------------------------------------------------
# PARAMETRES
# -------------------------------------------------------
DOSSIER_IMAGES = 'calibration_images'   # dossier des images
CHECKERBOARD   = (9, 6)                  # coins internes (colonnes-1, lignes-1)
SQUARE_SIZE    = 0.025                   # taille d'un carre en metres (2.5 cm)

# -------------------------------------------------------
# 1. Preparation des points 3D du damier
# -------------------------------------------------------
# Coordonnees 3D des coins dans le repere monde
# Z=0 car le damier est plan (astuce de Zhang)
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0],
                        0:CHECKERBOARD[1]].T.reshape(-1, 2) * SQUARE_SIZE

print("="*60)
print("  EXERCICE 1 : CALIBRATION CAMERA - METHODE ZHANG")
print("="*60)
print(f"\nDamier : {CHECKERBOARD[0]}x{CHECKERBOARD[1]} coins")
print(f"Taille carre : {SQUARE_SIZE*100:.1f} cm")

# -------------------------------------------------------
# 2. Detection des coins dans chaque image
# -------------------------------------------------------
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objpoints = []   # points 3D dans le monde reel
imgpoints = []   # points 2D dans les images
img_size  = None

images = sorted(glob.glob(f'{DOSSIER_IMAGES}/*.jpg') +
                glob.glob(f'{DOSSIER_IMAGES}/*.png'))

if not images:
    print(f"ERREUR : aucune image dans '{DOSSIER_IMAGES}'")
    exit()

print(f"\n{len(images)} images trouvees")
print("\nDetection des coins :")

ok_count = 0
for fname in images:
    img  = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_size = gray.shape[::-1]

    # Recherche des coins du damier
    flags = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, flags)

    if ret:
        ok_count += 1
        objpoints.append(objp)

        # Affinage subpixel (cornerSubPix)
        corners2 = cv2.cornerSubPix(
            gray, corners, (11,11), (-1,-1), criteria
        )
        imgpoints.append(corners2)

        # Dessin des coins
        img_draw = img.copy()
        cv2.drawChessboardCorners(img_draw, CHECKERBOARD, corners2, ret)

        # Sauvegarde image annotee
        out = fname.replace(DOSSIER_IMAGES, DOSSIER_IMAGES+'/detected')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        cv2.imwrite(out, img_draw)
        print(f"  OK  : {os.path.basename(fname)}")
    else:
        print(f"  ECHEC : {os.path.basename(fname)}")

print(f"\nResultat : {ok_count}/{len(images)} images valides")

if ok_count < 3:
    print("ERREUR : besoin d'au moins 3 images valides !")
    exit()

# -------------------------------------------------------
# 3. Calibration - Methode Zhang
# -------------------------------------------------------
print("\nCalibration en cours...")

ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, img_size, None, None
)

# -------------------------------------------------------
# 4. Resultats
# -------------------------------------------------------
print("\n" + "="*60)
print("  RESULTATS DE CALIBRATION")
print("="*60)

print(f"\nErreur de reprojection RMS : {ret:.4f} pixels")
if ret < 0.5:
    print("  Excellente calibration !")
elif ret < 1.0:
    print("  Bonne calibration")
else:
    print("  Calibration acceptable (ajoutez plus d'images)")

print("\nMatrice intrinseque K :")
print(f"  fx = {K[0,0]:.2f} px   (focale horizontale)")
print(f"  fy = {K[1,1]:.2f} px   (focale verticale)")
print(f"  cx = {K[0,2]:.2f} px   (centre optique X)")
print(f"  cy = {K[1,2]:.2f} px   (centre optique Y)")
print(f"\n  K = \n{K}")

print("\nCoefficients de distorsion :")
print(f"  k1 = {dist[0,0]:.6f}  (distorsion radiale 1)")
print(f"  k2 = {dist[0,1]:.6f}  (distorsion radiale 2)")
print(f"  p1 = {dist[0,2]:.6f}  (distorsion tangentielle 1)")
print(f"  p2 = {dist[0,3]:.6f}  (distorsion tangentielle 2)")
print(f"  k3 = {dist[0,4]:.6f}  (distorsion radiale 3)")

print("\nParametres extrinseques (premiere image) :")
print(f"  rvec (rotation)    : {rvecs[0].T}")
print(f"  tvec (translation) : {tvecs[0].T}")

# -------------------------------------------------------
# 5. Erreur de reprojection par image
# -------------------------------------------------------
print("\nErreur de reprojection par image :")
errors = []
for i in range(len(objpoints)):
    imgpts_proj, _ = cv2.projectPoints(
        objpoints[i], rvecs[i], tvecs[i], K, dist
    )
    err = cv2.norm(imgpoints[i], imgpts_proj, cv2.NORM_L2) / len(imgpts_proj)
    errors.append(err)
    print(f"  Image {i+1:2d} : {err:.4f} px")

# -------------------------------------------------------
# 6. Sauvegarde
# -------------------------------------------------------
np.save('camera_matrix.npy', K)
np.save('dist_coeffs.npy',   dist)
np.savetxt('camera_matrix.txt', K, fmt='%.4f',
           header='Camera Intrinsic Matrix K (fx,fy,cx,cy)')
np.savetxt('dist_coeffs.txt', dist, fmt='%.6f',
           header='Distortion Coefficients (k1,k2,p1,p2,k3)')

print("\nFichiers sauvegardes :")
print("  camera_matrix.npy / .txt")
print("  dist_coeffs.npy   / .txt")

# -------------------------------------------------------
# 7. Visualisation
# -------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Erreurs par image
axes[0].bar(range(1, len(errors)+1), errors, color='steelblue', edgecolor='black')
axes[0].axhline(ret, color='red', linestyle='--', label=f'RMS={ret:.3f} px')
axes[0].set_xlabel('Numero image')
axes[0].set_ylabel('Erreur reprojection (px)')
axes[0].set_title('Erreur par image')
axes[0].legend(); axes[0].grid(alpha=0.3)

# Premiere image avec coins detectes
img_first = cv2.imread(images[0])
img_first = cv2.cvtColor(img_first, cv2.COLOR_BGR2RGB)
axes[1].imshow(img_first)
axes[1].set_title('Premiere image')
axes[1].axis('off')

# Image avec coins detectes si disponible
detected_path = images[0].replace(DOSSIER_IMAGES, DOSSIER_IMAGES+'/detected')
if os.path.exists(detected_path):
    img_det = cv2.cvtColor(cv2.imread(detected_path), cv2.COLOR_BGR2RGB)
    axes[2].imshow(img_det)
    axes[2].set_title('Coins detectes')
    axes[2].axis('off')

plt.suptitle(f'Calibration Zhang | RMS={ret:.3f} px | {ok_count} images valides',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('exercice1_calibration.png', dpi=150, bbox_inches='tight')
print("  exercice1_calibration.png")
plt.show()

print("\n>>> Fermez la fenetre pour terminer")
