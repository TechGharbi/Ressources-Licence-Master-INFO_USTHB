"""
eTAPE 3 CORRIGeE v5 : Reconstruction 3D
- Accepte pts1, pts2 en paramètre optionnel
- Sinon charge matches.npz ou appelle SIFT
- Adapte K, estime R,T, triangulation, mise à l'echelle
- CORRECTION : Utilisation de K adaptee pour la triangulation
"""

import cv2
import numpy as np
import os
import step2_sift_matching as sift_module

BASELINE_MM = 0.10          # 10 cm (translation reelle de la camera)
CALIB_W = 400
CALIB_H = 300
IMG_LEFT = 'MES IMAGES/im2G.png'

def scale_K(K, orig_w, orig_h, calib_w=CALIB_W, calib_h=CALIB_H):
    sx = orig_w / calib_w
    sy = orig_h / calib_h
    K_scaled = K.copy().astype(np.float64)
    K_scaled[0,0] *= sx
    K_scaled[1,1] *= sy
    K_scaled[0,2] *= sx
    K_scaled[1,2] *= sy
    return K_scaled

def reconstruct_3d(pts1=None, pts2=None):
    # Si les points ne sont pas fournis, on essaie de les charger depuis matches.npz
    if pts1 is None or pts2 is None:
        if os.path.exists('matches.npz'):
            with np.load('matches.npz') as data:
                pts1 = data['pts1']
                pts2 = data['pts2']
            print("📂 Correspondances chargees depuis matches.npz")
        else:
            # Sinon, on appelle la detection SIFT (etape 2)
            result = sift_module.detect_and_match()
            if result is None:
                return None
            pts1, pts2 = result[0], result[1]

    # Maintenant on affiche l'en-tête de l'etape 3
    print("\n" + "=" * 50)
    print("   eTAPE 3 — Reconstruction 3D (avec essentielle + echelle)")
    print("=" * 50)

    # 1. Charger calibration
    try:
        data = np.load('camera_params.npz')
        K_calib = data['K']
        dist = data['dist']
        print("✅ Calibration chargee depuis camera_params.npz")
    except FileNotFoundError:
        print(" 'camera_params.npz' introuvable.")
        return

    # 2. Charger les images
    img1 = cv2.imread('MES IMAGES/im2G.png')
    img2 = cv2.imread('MES IMAGES/im1D.png')
    if img1 is None or img2 is None:
        img1 = cv2.imread('MES IMAGES/im2G.jpg')
        img2 = cv2.imread('MES IMAGES/im1D.jpg')
    
    orig_h, orig_w = img1.shape[:2]
    print(f"\n Resolution images : {orig_w} x {orig_h} px")
    
    img_left = cv2.imread(IMG_LEFT)

    img_left_rgb = cv2.cvtColor(img_left, cv2.COLOR_BGR2RGB)
    H_img, W_img = img_left.shape[:2]
    
    # Charger les points bruts pour l'affichage des disparites
    pts_left = np.load('pts1_raw.npy')
    pts_right = np.load('pts2_raw.npy')
    
    # Calcul de la disparite moyenne (pour information seulement)
    disparities = pts_left[:,0] - pts_right[:,0]
    disp_mean = np.mean(disparities)
    print(f" Disparite moyenne (brute) : {disp_mean:.1f} px")

    # Determiner le signe de la disparite
    if disp_mean < 0:
        print("Disparite negative detectee → camera deplacee vers la droite")
        sign = -1.0
    else:
        print("Disparite positive → camera deplacee vers la gauche")
        sign = 1.0
        
    # 3. Adapter K à la resolution
    K = scale_K(K_calib, orig_w, orig_h)
    print(f"\n📷 Matrice K adaptee à la resolution {orig_w}x{orig_h} :")
    print(f"   fx = {K[0,0]:.2f} px")
    print(f"   fy = {K[1,1]:.2f} px")
    print(f"   cx = {K[0,2]:.2f} px")
    print(f"   cy = {K[1,2]:.2f} px")

    if pts1 is None or len(pts1) < 8:
        print(" Pas assez de points SIFT (minimum 8).")
        return
    print(f" {len(pts1)} correspondances brutes")

    # 4. Rectifier la distorsion
    pts1_ud = cv2.undistortPoints(pts1.reshape(-1,1,2), K, dist, P=K).reshape(-1,2)
    pts2_ud = cv2.undistortPoints(pts2.reshape(-1,1,2), K, dist, P=K).reshape(-1,2)

    # 5. Matrice essentielle + RANSAC
    E, mask = cv2.findEssentialMat(pts1_ud, pts2_ud, K,
                                method=cv2.RANSAC, prob=0.999, threshold=1.0)
    inliers = mask.ravel() == 1
    pts1_in = pts1_ud[inliers]
    pts2_in = pts2_ud[inliers]
    print(f"✅ Inliers après RANSAC : {len(pts1_in)} / {len(pts1)}")
    if len(pts1_in) < 8:
        print(" Trop peu d'inliers.")
        return

    # 6. Recuperer pose relative (R, T) à echelle près
    _, R, T, _ = cv2.recoverPose(E, pts1_in, pts2_in, K)
    print(f"\n Rotation R estimee :\n{R}")
    print(f"\n Translation T (direction) :\n{T.T}")

    # 7. Triangulation avec OpenCV
    P1 = K @ np.hstack([np.eye(3), np.zeros((3,1))])
    P2 = K @ np.hstack([R, T])
    pts4d = cv2.triangulatePoints(P1, P2, pts1_in.T, pts2_in.T)
    pts3d_n = (pts4d[:3] / pts4d[3]).T
    
    # 8. Mise à l'echelle avec baseline reelle
    scale = BASELINE_MM / np.linalg.norm(T)
    pts3d_m = pts3d_n * scale
    valid = pts3d_m[:, 2] > 0
    pts3d_m = pts3d_m[valid]
    pts1_v = pts1_in[valid]

    # 9. Filtrage outliers sur Z
    z = pts3d_m[:, 2]
    if len(z) > 10:
        median_z = np.median(z)
        std_z = np.std(z)
        ok = np.abs(z - median_z) < 2 * std_z
        pts3d_m = pts3d_m[ok]
        pts1_v = pts1_v[ok]

    # -------------------------------------------------------
    # TRIANGULATION AVEC K ADAPTeE (Methode alternative)
    # -------------------------------------------------------
    points_3d = []
    colors_3d = []
    rejected = 0

    # Seuils Z raisonnables pour des boîtes sur une table
    Z_MIN = 0.10   # 10 cm minimum
    Z_MAX = 1.00   # 1 mètre maximum

    # Utiliser K adaptee après scale_K
    fx_adapted = K[0, 0]
    cx_adapted = K[0, 2]
    cy_adapted = K[1, 2]

    print(f"\n Paramètres utilises pour la triangulation alternative :")
    print(f"   fx = {fx_adapted:.2f} px (après adaptation)")
    print(f"   cx = {cx_adapted:.2f} px")
    print(f"   cy = {cy_adapted:.2f} px")
    print(f"   Baseline = {BASELINE_MM * 100:.0f} cm")

    for i in range(len(pts_left)):
        xl, yl = pts_left[i]
        xr, yr = pts_right[i]

        # Calcul de la disparite
        d = sign * (xl - xr)

        if abs(d) < 0.5:
            rejected += 1
            continue

        # Calcul du Z avec fx adapte
        Z = (fx_adapted * BASELINE_MM) / d

        if Z < Z_MIN or Z > Z_MAX:
            rejected += 1
            continue

        # Calcul des coordonnees X et Y
        X = (xl - cx_adapted) * Z / fx_adapted
        Y = (yl - cy_adapted) * Z / fx_adapted
        
        points_3d.append([X, Y, Z])

        # Extraction des couleurs
        xi = int(np.clip(xl, 0, W_img-1))
        yi = int(np.clip(yl, 0, H_img-1))
        r, g, b_c = img_left_rgb[yi, xi]
        colors_3d.append([r/255.0, g/255.0, b_c/255.0])

    if points_3d:
        points_3d = np.array(points_3d)
        colors_3d = np.array(colors_3d)
        np.save('points_3d.npy', points_3d)
        np.save('colors_3d.npy', colors_3d)

        print(f"\n Points acceptes (triangulation alternative) : {len(points_3d)}  rejetes : {rejected}")
        print(f" Z : min={points_3d[:,2].min():.2f}m  max={points_3d[:,2].max():.2f}m  moy={points_3d[:,2].mean():.2f}m")
        
        print(f"\n{'#':>3}  {'X':>8}  {'Y':>8}  {'Z':>8}")
        print("-"*32)
        for i in range(min(8, len(points_3d))):
            print(f"{i:>3}  {points_3d[i,0]:>8.3f}  {points_3d[i,1]:>8.3f}  {points_3d[i,2]:>8.3f}")
    else:
        print(f"\n⚠️ 0 points dans la plage [{Z_MIN}m - {Z_MAX}m]")

    # 10. Sauvegarde des resultats principaux (methode OpenCV)
    print(f"\n Points 3D finaux (methode OpenCV) : {len(pts3d_m)}")
    if len(pts3d_m) > 0:
        print(f"   X : [{pts3d_m[:,0].min():.3f}, {pts3d_m[:,0].max():.3f}] m")
        print(f"   Y : [{pts3d_m[:,1].min():.3f}, {pts3d_m[:,1].max():.3f}] m")
        print(f"   Z : [{pts3d_m[:,2].min():.3f}, {pts3d_m[:,2].max():.3f}] m")

    # Sauvegarde des points 3D principaux
    np.save('points3d.npy', pts3d_m)
    img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    colors = []
    for (x, y) in pts1_v.astype(int):
        x = np.clip(x, 0, orig_w - 1)
        y = np.clip(y, 0, orig_h - 1)
        colors.append(img1_rgb[y, x] / 255.0)
    colors = np.array(colors)
    np.save('colors3d.npy', colors)
    print("💾 Sauvegarde : points3d.npy, colors3d.npy")

    # 11. Export PLY (avec fallback)
    try:
        from plyfile import PlyData, PlyElement
        vertex = np.array([(x, y, z, r, g, b) for (x, y, z), (r, g, b) in zip(pts3d_m, colors)],
                          dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
                                 ('red', 'u1'), ('green', 'u1'), ('blue', 'u1')])
        PlyData([PlyElement.describe(vertex, 'vertex')], text=True).write('nuage.ply')
        print("💾 PLY sauvegarde : nuage.ply")
    except ImportError:
        with open('nuage.ply', 'w') as f:
            f.write("ply\nformat ascii 1.0\n")
            f.write(f"element vertex {len(pts3d_m)}\n")
            f.write("property float x\nproperty float y\nproperty float z\n")
            f.write("property uchar red\nproperty uchar green\nproperty uchar blue\n")
            f.write("end_header\n")
            for i in range(len(pts3d_m)):
                x, y, z = pts3d_m[i]
                r, g, b = (colors[i] * 255).astype(np.uint8)
                f.write(f"{x:.6f} {y:.6f} {z:.6f} {r} {g} {b}\n")
        print(" PLY sauvegarde (manuel) : nuage.ply")

    return pts3d_m, colors

if __name__ == '__main__':
    reconstruct_3d()