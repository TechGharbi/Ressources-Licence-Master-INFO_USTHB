import cv2
import numpy as np
import os
import glob


DOSSIER = 'images/'         
OUTPUT_FILE = 'panorama_final.jpg'
MIN_MATCH_COUNT = 10
LOWE_RATIO = 0.50  
SHOW_STEPS = True            
WINDOW_W = 900               # <- Largeur des fenêtres d'affichage (pixels)
WINDOW_H = 500               # <- Hauteur des fenêtres d'affichage (pixels)


def imshow_resized(titre, img):
    """Affiche une image dans une fenêtre de taille fixe."""
    cv2.namedWindow(titre, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(titre, WINDOW_W, WINDOW_H)
    cv2.imshow(titre, img)
    cv2.waitKey(0)


def charger_images_depuis_dossier(dossier):
    """Charge toutes les images du dossier, triées par nom de fichier."""
    extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff']
    fichiers = []
    for ext in extensions:
        fichiers.extend(glob.glob(os.path.join(dossier, ext)))
        fichiers.extend(glob.glob(os.path.join(dossier, ext.upper())))

    # Tri par nom de fichier (naturel)
    fichiers = sorted(set(fichiers), key=lambda x: os.path.basename(x).lower())

    if not fichiers:
        print(f"[ERREUR] Aucune image trouvée dans : {dossier}")
        return []

    print(f"[INFO] {len(fichiers)} image(s) trouvée(s) dans '{dossier}' :\n")
    images = []
    for path in fichiers:
        img = cv2.imread(path)
        if img is None:
            print(f"  [!] Impossible de charger : {path}")
            continue
        print(f"  -> {os.path.basename(path)} ({img.shape[1]}x{img.shape[0]})")
        images.append((os.path.basename(path), img))

    return images


def trim(frame):
    """Supprime les bords noirs autour de l'image assemblée."""
    if frame is None or frame.size == 0:
        return frame
    while frame.shape[0] > 0 and not np.sum(frame[0]):
        frame = frame[1:]
    while frame.shape[0] > 0 and not np.sum(frame[-1]):
        frame = frame[:-1]
    while frame.shape[1] > 0 and not np.sum(frame[:, 0]):
        frame = frame[:, 1:]
    while frame.shape[1] > 0 and not np.sum(frame[:, -1]):
        frame = frame[:, :-1]
    return frame


def stitch_two_images(img_l, img_r, etape=0, show=False):
    """Assemble deux images : img_r est warpée sur img_l (gauche fixe)."""
    gray_l = cv2.cvtColor(img_l, cv2.COLOR_BGR2GRAY)
    gray_r = cv2.cvtColor(img_r, cv2.COLOR_BGR2GRAY)

    # Détection SIFT
    sift = cv2.SIFT_create()
    kpl, desl = sift.detectAndCompute(gray_l, None)
    kpr, desr = sift.detectAndCompute(gray_r, None)

    if show:
        imshow_resized(f"[Etape {etape}] Keypoints - Gauche", cv2.drawKeypoints(img_l, kpl, None))
        imshow_resized(f"[Etape {etape}] Keypoints - Droite", cv2.drawKeypoints(img_r, kpr, None))

    # Matching + filtre de Lowe
    matcher = cv2.BFMatcher()
    matches = matcher.knnMatch(desr, desl, k=2)
    good = [m for m, n in matches if m.distance < LOWE_RATIO * n.distance]

    print(f"  Matches retenus : {len(good)} (minimum requis : {MIN_MATCH_COUNT})")

    if show:
        draw_params = dict(matchColor=(0, 255, 0), singlePointColor=None, flags=2)
        match_img = cv2.drawMatches(img_r, kpr, img_l, kpl, good, None, **draw_params)
        imshow_resized(f"[Etape {etape}] Matches", match_img)

    if len(good) < MIN_MATCH_COUNT:
        print(f"  [!] Pas assez de matches. Étape ignorée.")
        return None

    # Homographie
    src_pts = np.float32([kpr[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kpl[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    if M is None:
        print("  [!] Homographie introuvable.")
        return None

    # Warp + fusion
    width = img_l.shape[1] + img_r.shape[1]
    height = img_l.shape[0]
    dst = cv2.warpPerspective(img_r, M, (width, height))

    if show:
        imshow_resized(f"[Etape {etape}] Warp avant fusion", dst)

    dst[0:img_l.shape[0], 0:img_l.shape[1]] = img_l

    if show:
        imshow_resized(f"[Etape {etape}] Apres fusion", dst)

    return dst


def stitch_all(dossier, show=False):
    """Charge les images du dossier et les assemble en panorama."""
    images = charger_images_depuis_dossier(dossier)

    if len(images) < 2:
        print("[ERREUR] Il faut au moins 2 images pour assembler un panorama.")
        return None

    print(f"\n=== Debut de l'assemblage ({len(images)} images) ===\n")

    nom_courant, panorama = images[0]

    for i in range(1, len(images)):
        nom_suivant, img_suivante = images[i]
        print(f"[Etape {i}/{len(images)-1}] {nom_courant}  +  {nom_suivant}")

        result = stitch_two_images(panorama, img_suivante, etape=i, show=show)

        if result is None:
            print(f"  [!] Echec a l'etape {i}. On continue avec le panorama actuel.\n")
            continue

        panorama = trim(result)
        nom_courant = f"panorama_{i}"
        print(f"  -> Taille panorama : {panorama.shape[1]}x{panorama.shape[0]}\n")

        if show:
            imshow_resized(f"[Etape {i}] Panorama partiel (apres trim)", panorama)

    return panorama


if __name__ == '__main__':
    print("=== Assemblage de panorama multi-images ===\n")

    if not os.path.isdir(DOSSIER):
        print(f"[ERREUR] Dossier introuvable : '{DOSSIER}'")
        print("  -> Modifie la variable DOSSIER en haut du script.")
    else:
        panorama = stitch_all(DOSSIER, show=SHOW_STEPS)

        if panorama is not None:
            imshow_resized("=== PANORAMA FINAL ===", panorama)
            cv2.imwrite(OUTPUT_FILE, panorama)
            print(f"\n[OK] Panorama sauvegarde : '{OUTPUT_FILE}'")
            print(f"     Taille finale : {panorama.shape[1]}x{panorama.shape[0]}")
        else:
            print("[ERREUR] Impossible de creer le panorama.")

    cv2.destroyAllWindows()
