import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('bini.jpg', cv2.IMREAD_GRAYSCALE)

# Binarisation stricte (au cas où l'image n'est pas parfaitement binaire)
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

#L’érosion est une opération qui réduit (thinning) les contours des objets dans une image 
#binaire à l’aide d’un élément structurant (SE). L’érosion permet d’affiner les contours et de 
#supprimer le bruit. La dilatation est la fonction inverse elle permet d’élargir les contours et de 
#remplir les petits trous dans une image binaire. 
# ===================================================================
# 2. Definition des elements structurants demandes
# ===================================================================
# getStructuringElement(shape, ksize) → shape peut être :
# cv2.MORPH_RECT, cv2.MORPH_ELLIPSE, cv2.MORPH_CROSS

kernel_3x3_rect   = cv2.getStructuringElement(cv2.MORPH_RECT,   (3, 3))
kernel_5x5_rect   = cv2.getStructuringElement(cv2.MORPH_RECT,   (5, 5))
kernel_5x5_ellipse= cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5, 5))
kernel_5x5_cross  = cv2.getStructuringElement(cv2.MORPH_CROSS,  (5, 5))

kernels = {
    'Rectangle 3×3'    : kernel_3x3_rect,
    'Rectangle 5×5'    : kernel_5x5_rect,
    'Ellipse 5×5'      : kernel_5x5_ellipse,
    'Croix 5×5'        : kernel_5x5_cross
}

# ===================================================================
# 3. erosion avec chaque element structurant
# ===================================================================
erosions = {}
for name, kernel in kernels.items():
    erosions[name] = cv2.erode(binary, kernel, iterations=1)

# ===================================================================
# 4. Dilatation avec chaque element structurant
# ===================================================================
dilations = {}
for name, kernel in kernels.items():
    dilations[name] = cv2.dilate(binary, kernel, iterations=1)

# ===================================================================
# 5. Ouverture et Fermeture (avec le meme element structurant)
#L’ouverture d’une image binaire est simplement l’application d’une érosion suivie d’une 
#dilatation. La fermeture d’une image binaire est à l’inverse l’application d’une dilatation suivie 
#d'une érosion. 
# ===================================================================
# On peut les faire manuellement ou avec morphologyEx (plus rapide)
opening_rect5  = cv2.morphologyEx(binary, cv2.MORPH_OPEN,  kernel_5x5_rect)
closing_rect5  = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel_5x5_rect)

opening_ellipse = cv2.morphologyEx(binary, cv2.MORPH_OPEN,  kernel_5x5_ellipse)
closing_ellipse = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel_5x5_ellipse)

# ===================================================================
# 6. Affichage des resultats 
# ===================================================================
plt.figure(figsize=(16, 10))

plt.subplot(3, 5, 1)
plt.title("Image binaire originale", fontsize=12)
plt.imshow(binary, cmap='gray')
plt.axis('off')

# erosions
idx = 2
for name, eroded in erosions.items():
    plt.subplot(3, 5, idx)
    plt.title(f"erosion\n{name}")
    plt.imshow(eroded, cmap='gray')
    plt.axis('off')
    idx += 1

# Dilatations
idx = 7
for name, dilated in dilations.items():
    plt.subplot(3, 5, idx)
    plt.title(f"Dilatation\n{name}")
    plt.imshow(dilated, cmap='gray')
    plt.axis('off')
    idx += 1

# Ouvertures et fermetures
plt.subplot(3, 5, 6)
plt.title("Ouverture\n(Rect 5×5)")
plt.imshow(opening_rect5, cmap='gray')
plt.axis('off')

plt.subplot(3, 5, 11)
plt.title("Fermeture\n(Rect 5×5)")
plt.imshow(closing_rect5, cmap='gray')
plt.axis('off')

plt.subplot(3, 5, 12)
plt.title("Ouverture\n(Ellipse 5×5)")
plt.imshow(opening_ellipse, cmap='gray')
plt.axis('off')

plt.subplot(3, 5, 13)
plt.title("Fermeture\n(Ellipse 5×5)")
plt.imshow(closing_ellipse, cmap='gray')
plt.axis('off')

plt.suptitle("TP5 - Morphologie Mathematique : erosion, Dilatation, Ouverture, Fermeture", 
             fontsize=16, y=0.98)
plt.tight_layout()
plt.show()

# ===================================================================
# 7. Deuxième partie : Image FPR.jpg (empreinte digitale)
# ===================================================================
fpr = cv2.imread('FPR.jpg', cv2.IMREAD_GRAYSCALE)
if fpr is None:
    print("Attention : 'FPR.jpg' non trouvee → partie 2 ignoree")
else:
    _, fpr_bin = cv2.threshold(fpr, 127, 255, cv2.THRESH_BINARY)

    # elements structurants adaptes aux empreintes
    se_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    se_big   = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))

    # Operations utiles pour nettoyer une empreinte digitale
    opened   = cv2.morphologyEx(fpr_bin, cv2.MORPH_OPEN,  se_small, iterations=2)  # enlève petits bruits
    closed   = cv2.morphologyEx(opened,   cv2.MORPH_CLOSE, se_big,   iterations=3)  # comble les trous
    final    = cv2.morphologyEx(closed,   cv2.MORPH_OPEN,  se_small, iterations=1)  # nettoyage final

    plt.figure(figsize=(15, 8))
    plt.subplot(2, 4, 1)
    plt.title("FPR.jpg originale")
    plt.imshow(fpr_bin, cmap='gray')
    plt.axis('off')

    plt.subplot(2, 4, 2)
    plt.title("Ouverture (3×3 ellipse ×2)")
    plt.imshow(opened, cmap='gray')
    plt.axis('off')

    plt.subplot(2, 4, 3)
    plt.title("Fermeture (9×9 ellipse ×3)")
    plt.imshow(closed, cmap='gray')
    plt.axis('off')

    plt.subplot(2, 4, 4)
    plt.title("Resultat final\n(Nettoyage complet)")
    plt.imshow(final, cmap='gray')
    plt.axis('off')

    plt.suptitle("Application sur FPR.jpg (empreinte digitale) - Nettoyage optimal", fontsize=16)
    plt.tight_layout()
    plt.show()

    print("\nFPR.jpg : La meilleure sequence est :")
    print("   1. Ouverture (petit SE) → enlève les petits points de bruit")
    print("   2. Fermeture (grand SE) → comble les trous dans les crêtes")
    print("   3. Petite ouverture finale → nettoyage supplementaire")

