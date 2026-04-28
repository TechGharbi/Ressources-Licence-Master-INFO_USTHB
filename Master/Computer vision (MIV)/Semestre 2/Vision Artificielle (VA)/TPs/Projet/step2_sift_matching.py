"""
ÉTAPE 2 : Détection SIFT et mise en correspondance (version ultra-améliorée)
=============================================================================
- Paramètres SIFT optimisés pour plus de points
- Masque pour ignorer les bordures
- Ratio test plus strict
- Filtrage RANSAC avec seuil adapté
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

def detect_and_match():
    print("=" * 50)
    print("   ÉTAPE 2 — SIFT + mise en correspondance (optimisée)")
    print("=" * 50)

    # -------------------------------------------------------
    # PARAMETRES OPTIMISES
    # -------------------------------------------------------
    MIN_MATCHES = 10        
    RATIO_LOWE = 0.80                                                                                                                                                                                                                                                                                                        
    
    # Paramètres SIFT améliorés
    SIFT_NFEATURES = 0       # 0 = pas de limite
    SIFT_N_OCTAVE_LAYERS = 4 # Plus de couches (détecte plus de points)
    SIFT_CONTRAST_THRESH = 0.02  # Plus bas = plus de points sur surfaces peu texturées
    SIFT_EDGE_THRESH = 15    # Plus haut = garde plus de points sur les bords
    SIFT_SIGMA = 1.6         # Sigma du flou initial
    
    # -------------------------------------------------------
    # 1. Chargement des images
    # -------------------------------------------------------
    img1 = cv2.imread('MES IMAGES/im2G.png')
    img2 = cv2.imread('MES IMAGES/im1D.png')
    
    if img1 is None or img2 is None:
        img1 = cv2.imread('MES IMAGES/im2G.jpg')
        img2 = cv2.imread('MES IMAGES/im1D.jpg')
    
    if img1 is None or img2 is None:
        print(" Images introuvables!")
        return None, None

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    print(f"\n Image gauche : {img1.shape[1]}x{img1.shape[0]} px")
    print(f" Image droite : {img2.shape[1]}x{img2.shape[0]} px")

    # -------------------------------------------------------
    # 2. Detection SIFT avec paramètres optimisés
    # -------------------------------------------------------
    sift = cv2.SIFT_create(
        nfeatures=SIFT_NFEATURES,
        nOctaveLayers=SIFT_N_OCTAVE_LAYERS,
        contrastThreshold=SIFT_CONTRAST_THRESH,
        edgeThreshold=SIFT_EDGE_THRESH,
        sigma=SIFT_SIGMA
    )
    
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)
    
    print(f"\n Keypoints détectés :")
    print(f"   Image gauche  : {len(kp1)} points")
    print(f"   Image droite  : {len(kp2)} points")

    # -------------------------------------------------------
    # 3. Masque pour éliminer les bords de l'image
    #    (les bords ne contiennent pas de boîtes)
    # -------------------------------------------------------
    h, w = gray1.shape
    margin = 30  # marge en pixels à ignorer
    
    mask = np.zeros(gray1.shape, dtype=np.uint8)
    mask[margin:h-margin, margin:w-margin] = 255
    
    # Appliquer le masque aux keypoints de l'image gauche
    indices1 = [i for i, kp in enumerate(kp1) 
                if mask[int(kp.pt[1]), int(kp.pt[0])] == 255]
    kp1 = [kp1[i] for i in indices1]
    des1 = des1[indices1] if des1 is not None else None
    
    # Appliquer le masque aux keypoints de l'image droite
    indices2 = [i for i, kp in enumerate(kp2) 
                if mask[int(kp.pt[1]), int(kp.pt[0])] == 255]
    kp2 = [kp2[i] for i in indices2]
    des2 = des2[indices2] if des2 is not None else None
    
    print(f"   Après masque (sans bordures) :")
    print(f"   Image gauche  : {len(kp1)} points")
    print(f"   Image droite  : {len(kp2)} points")

    if des1 is None or des2 is None or len(kp1) < 10 or len(kp2) < 10:
        print(" Pas assez de keypoints après masquage!")
        return None, None

    # -------------------------------------------------------
    # 4. Matching avec FLANN + Ratio Test de Lowe
    # -------------------------------------------------------
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)

    # Ratio test avec seuil plus strict
    good_matches = []
    for m, n in matches:
        if m.distance < RATIO_LOWE * n.distance:
            good_matches.append(m)

    print(f"\n✅ Matches après ratio test ({RATIO_LOWE}) : {len(good_matches)}")

    # -------------------------------------------------------
    # 5. Extraction des coordonnées
    # -------------------------------------------------------    
    pts1_raw = np.float32([kp1[m.queryIdx].pt for m in good_matches])
    pts2_raw = np.float32([kp2[m.trainIdx].pt for m in good_matches])

    # Filtrage géométrique par matrice fondamentale (RANSAC)
    # ransacReprojThreshold plus petit = plus strict
    F, mask = cv2.findFundamentalMat(pts1_raw, pts2_raw, cv2.FM_RANSAC,
                                    ransacReprojThreshold=0.8, confidence=0.99)
    
    if mask is not None:
        inliers = mask.ravel() == 1
        pts1 = pts1_raw[inliers]
        pts2 = pts2_raw[inliers]
        good_matches_final = [good_matches[i] for i in range(len(good_matches)) if inliers[i]]
        print(f"✅ Après filtrage RANSAC : {len(pts1)} matches géométriquement cohérents")
    else:
        print("⚠️  Pas de matrice fondamentale trouvée, on garde tous les matches")
        pts1, pts2 = pts1_raw, pts2_raw
        good_matches_final = good_matches
        
    # Affichage des 8 premiers points
    print("\n📊 Coordonnées des 8 premiers points appariés :")
    print(f"{'#':>3}  {'Gauche (x,y)':>20}  {'Droite (x,y)':>20}  {'Disparité':>10}")
    print("-" * 65)
    for i in range(min(8, len(good_matches))):
        xl, yl = pts1_raw[i]
        xr, yr = pts2_raw[i]
        d = xl - xr
        print(f"{i:>3}  ({xl:6.1f}, {yl:6.1f})    ({xr:6.1f}, {yr:6.1f})    {d:>8.1f} px")

    # -------------------------------------------------------
    # 6. Sauvegarde
    # -------------------------------------------------------
    np.savez('matches.npz', pts1=pts1, pts2=pts2)
    np.save('pts1_raw.npy', pts1_raw)
    np.save('pts2_raw.npy', pts2_raw)
    print("\n💾 Points sauvegardés dans 'matches.npz'")

    # -------------------------------------------------------
    # 7. Visualisations
    # -------------------------------------------------------
    # Keypoints sur les deux images
    img1_kp = cv2.drawKeypoints(img1, kp1, None,
                                flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    img2_kp = cv2.drawKeypoints(img2, kp2, None,
                                flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    plt.figure(figsize=(14, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(img1_kp, cv2.COLOR_BGR2RGB))
    plt.title(f'Image gauche — {len(kp1)} keypoints SIFT')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(img2_kp, cv2.COLOR_BGR2RGB))
    plt.title(f'Image droite — {len(kp2)} keypoints SIFT')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('result_sift_keypoints.png', dpi=150)
    plt.show()
    print("💾 Sauvegardé : result_sift_keypoints.png")

    # Matches bruts
    img_matches_raw = cv2.drawMatches(
        img1, kp1, img2, kp2, good_matches[:80], None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    plt.figure(figsize=(18, 7))
    plt.imshow(cv2.cvtColor(img_matches_raw, cv2.COLOR_BGR2RGB))
    plt.title(f'Matches bruts (avant RANSAC) — {len(good_matches)} matches')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('result_sift_matches_raw.png', dpi=150)
    plt.show()
    print("💾 Sauvegardé : result_sift_matches_raw.png")

    # Matches filtrés
    img_matches_filtered = cv2.drawMatches(
        img1, kp1, img2, kp2, good_matches_final[:80], None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    plt.figure(figsize=(18, 7))
    plt.imshow(cv2.cvtColor(img_matches_filtered, cv2.COLOR_BGR2RGB))
    plt.title(f'Matches filtrés (RANSAC) — {len(pts1)} matches')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('result_sift_matches_filtered.png', dpi=150)
    plt.show()
    print("💾 Sauvegardé : result_sift_matches_filtered.png")
    

    return pts1, pts2


if __name__ == '__main__':
    pts1, pts2 = detect_and_match()
    if pts1 is not None:
        print(f"\n✅ Prêt pour l'étape 3 (triangulation). {len(pts1)} points disponibles.")