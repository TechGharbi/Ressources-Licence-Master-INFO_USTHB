"""
ÉTAPE 1 : Calibration de la caméra
====================================
- Lit les images du dossier 'calibration_images/'
- Détecte les coins du chessboard (9x6)
- Calcule la matrice K et les coefficients de distorsion
- Sauvegarde les résultats dans camera_params.npz
"""

import cv2
import numpy as np
import glob
import os

# ─────────────────────────────────────────────
# PARAMÈTRES — à adapter selon votre chessboard
# ─────────────────────────────────────────────
COLS = 9          # coins internes horizontaux
ROWS = 6          # coins internes verticaux
SQUARE_MM = 25.0  # taille d'un carré en mm (mesurez le vôtre)

def calibrate():
    print("=" * 50)
    print("   ÉTAPE 1 — Calibration de la caméra")
    print("=" * 50)

    # Préparer les points 3D du chessboard
    objp = np.zeros((ROWS * COLS, 3), np.float32)
    objp[:, :2] = np.mgrid[0:COLS, 0:ROWS].T.reshape(-1, 2)
    objp *= SQUARE_MM

    objpoints = []  # points 3D réels
    imgpoints = []  # points 2D dans l'image

    images = sorted(glob.glob('Calibration_Images/*.jpg') +
                    glob.glob('Calibration_Images/*.png') +
                    glob.glob('Calibration_Images/*.JPG'))

    print(f"\n {len(images)} images trouvées.\n")
    img_shape = None

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_shape = gray.shape[::-1]

        ret, corners = cv2.findChessboardCorners(gray, (COLS, ROWS), None)

        if ret:
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            objpoints.append(objp)
            imgpoints.append(corners2)

            # Affichage
            cv2.drawChessboardCorners(img, (COLS, ROWS), corners2, ret)
            cv2.imshow('Calibration - appuyez sur une touche', img)
            cv2.waitKey(300)
            
            print(f"    {os.path.basename(fname)} — détecté")
        else:
            print(f"    {os.path.basename(fname)} — échec de détection")

    cv2.destroyAllWindows()

    if len(objpoints) < 5:
        print(f"\n  Seulement {len(objpoints)} images valides. Besoin d'au moins 5.")
        return

    print(f"\n Calibration en cours avec {len(objpoints)} images valides...")
    ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, img_shape, None, None
    )

    # Erreur de reprojection
    total_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], K, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        total_error += error
    mean_error = total_error / len(objpoints)

    print(f"\n Calibration terminée !")
    print(f"   Erreur de reprojection moyenne : {mean_error:.4f} px")
    print(f"(< 1.0 = bonne calibration)")

    print(f"\n📷 Matrice K :\n{K}")
    print("\nMatrice intrinseque K :")
    print(f"  fx = {K[0,0]:.2f} px   (focale horizontale)")
    print(f"  fy = {K[1,1]:.2f} px   (focale verticale)")
    print(f"  cx = {K[0,2]:.2f} px   (centre optique X)")
    print(f"  cy = {K[1,2]:.2f} px   (centre optique Y)")
    
    print(f"\n🔧 Distorsion :\n{dist}")

    # Sauvegarde
    np.savez('camera_params.npz', K=K, dist=dist)
    print("\n Paramètres sauvegardés dans 'camera_params.npz'")

if __name__ == '__main__':
    os.makedirs('Calibration_Images', exist_ok=True)
    calibrate()
