import cv2 as cv
import numpy as np
import os
import matplotlib.pyplot as plt

# =============================================================
# IDENTIFICATION DE PLAQUES PAR SIFT — COULEURS CORRIGÉES
# =============================================================

QUERY_PATH   = r"matricule1.png"
DOSSIER_TRAIN = r"License Plates"   

SEUIL_MATCHES  = 10
RATIO_LOWE     = 0.70
SEUIL_RATIO    = 0.10

# =============================================================
# Chargement
# =============================================================
img_query = cv.imread(QUERY_PATH, cv.IMREAD_GRAYSCALE)
if img_query is None:
    print(f"ERREUR : impossible de charger {QUERY_PATH}")
    exit()

images_train = []
for fichier in os.listdir(DOSSIER_TRAIN):
    if fichier.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        chemin = os.path.join(DOSSIER_TRAIN, fichier)
        img    = cv.imread(chemin, cv.IMREAD_GRAYSCALE)
        if img is not None:
            images_train.append((fichier, img))

print(f"Query chargée, {len(images_train)} images train trouvées\n")

# =============================================================
# Calcul SIFT
# =============================================================
sift = cv.SIFT_create()
kp_query, desc_query = sift.detectAndCompute(img_query, None)
print(f"Keypoints query : {len(kp_query)}")

desc_trains = []
for nom, img in images_train:
    kp, desc = sift.detectAndCompute(img, None)
    desc_trains.append((nom, img, kp, desc))

# =============================================================
# Matching
# =============================================================
bf = cv.BFMatcher(cv.NORM_L2)

meilleur_score       = 0
meilleur_ratio_score = 0
meilleur_nom         = None
meilleur_img         = None
meilleur_kp          = None
meilleurs_matches    = None

print("--- Scores ---")

for nom, img, kp, desc in desc_trains:
    if desc is None or desc_query is None:
        continue
    if len(desc) < 2 or len(desc_query) < 2:
        continue

    matches     = bf.knnMatch(desc_query, desc, k=2)
    bons        = [m for m, n in matches if m.distance < RATIO_LOWE * n.distance]
    ratio_score = len(bons) / len(kp_query) if len(kp_query) > 0 else 0

    print(f"  {nom[:45]:45s} -> {len(bons):3d} matches  ratio={ratio_score:.2f}")

    if len(bons) > meilleur_score:
        meilleur_score       = len(bons)
        meilleur_ratio_score = ratio_score
        meilleur_nom         = nom
        meilleur_img         = img
        meilleur_kp          = kp
        meilleurs_matches    = bons

# =============================================================
# Decision
# =============================================================
print("\n" + "=" * 55)
condition1 = meilleur_score >= SEUIL_MATCHES
condition2 = meilleur_ratio_score >= SEUIL_RATIO

if condition1 and condition2:
    print(f"  CORRESPONDANCE TROUVEE")
    print(f"  Train  : {meilleur_nom}")
    print(f"  Score  : {meilleur_score} matches")
    print(f"  Ratio  : {meilleur_ratio_score:.2f}")
elif condition1 and not condition2:
    print(f"  RESULTAT INCERTAIN")
    print(f"  Score OK ({meilleur_score}) mais ratio faible ({meilleur_ratio_score:.2f})")
else:
    print(f"  AUCUNE CORRESPONDANCE FIABLE")
    print(f"  Score max : {meilleur_score} (seuil={SEUIL_MATCHES})")
print("=" * 55)

# =============================================================
# Affichage avec couleurs correctes
# =============================================================
if meilleur_img is not None and meilleurs_matches:

    if condition1 and condition2:
        couleur_bgr   = (0, 255, 0)   
        couleur_titre = "green"
        statut        = "FIABLE"
    elif condition1:
        couleur_bgr   = (0, 165, 255)  
        couleur_titre = "darkorange"
        statut        = "INCERTAIN"
    else:
        couleur_bgr   = (0, 0, 255)   
        couleur_titre = "red"
        statut        = "NON FIABLE"

    img_result_bgr = cv.drawMatches(
        img_query,    kp_query,
        meilleur_img, meilleur_kp,
        meilleurs_matches[:30],
        None,
        matchColor=couleur_bgr,
        singlePointColor=(150, 150, 150),
        flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )

    # CORRECTION : BGR -> RGB pour matplotlib
    img_result_rgb = cv.cvtColor(img_result_bgr, cv.COLOR_BGR2RGB)

    titre = f"{statut} | Score={meilleur_score} | Ratio={meilleur_ratio_score:.2f} | {meilleur_nom[:40]}"

    plt.figure(figsize=(14, 6))
    plt.imshow(img_result_rgb)   
    plt.title(titre, fontsize=10, color=couleur_titre, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("resultat_matching.png", dpi=120)
    plt.show()