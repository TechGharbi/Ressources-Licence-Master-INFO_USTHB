import cv2
import numpy as np
import matplotlib.pyplot as plt

#-----------------------
# 1. Gradients 
#-----------------------
# Nous lisons l'image en niveaux de gris (Grayscale) car la detection des contours fonctionne sur un seul canal
I = cv2.imread('catty.jpg', cv2.IMREAD_GRAYSCALE)

# Convertir le type de donnees en float32 pour eviter les problemes de precision lors des operations
I = I.astype(np.float32)

# Definition des filtres de Sobel (Noyaux de Sobel)
# Gx (filtre horizontal) : detecte les contours verticaux
# → car il mesure le changement dans la direction horizontale (de gauche a droite)

# Gy (filtre vertical) : detecte les contours horizontaux
# → car il mesure le changement dans la direction verticale (de haut en bas)
Gx = np.array([[-1, 0, 1],
               [-2, 0, 2],
               [-1, 0, 1]], dtype=np.float32)

Gy = np.array([[-1, -2, -1],
               [ 0,  0,  0],
               [ 1,  2,  1]], dtype=np.float32)

# Application de la convolution avec cv2.filter2D
# borderType=cv2.BORDER_CONSTANT ajoute des bordures nulles autour de l'image
grad_x = cv2.filter2D(I, -1, Gx, borderType=cv2.BORDER_CONSTANT)
grad_y = cv2.filter2D(I, -1, Gy, borderType=cv2.BORDER_CONSTANT)

# Calcul de la magnitude du gradient
# Formule : G = √(Gx² + Gy²)
magnitude = np.sqrt(grad_x**2 + grad_y**2)

# Normaliser l'image pour qu'elle soit comprise entre 0 et 255 pour l'affichage
def normalize(img):
    img_min = img.min()
    img_max = img.max()
    if img_max - img_min > 0:
        return ((img - img_min) / (img_max - img_min) * 255).astype(np.uint8)
    else:
        return np.zeros_like(img, dtype=np.uint8)

magnitude_norm = normalize(magnitude)

plt.figure(figsize=(13, 5))

plt.subplot(2, 3, 1)
plt.title('Image originale')
plt.imshow(I, cmap='gray')
plt.axis('off')

plt.subplot(2, 3, 2)
plt.title('Gradient horizontal Gx')
plt.imshow(normalize(grad_x), cmap='gray')
plt.axis('off')

plt.subplot(2, 3, 3)
plt.title('Gradient vertical Gy')
plt.imshow(normalize(grad_y), cmap='gray')
plt.axis('off')

plt.subplot(2, 3, 4)
plt.title('Amplitude de la derivee')
plt.imshow(magnitude_norm, cmap='gray')
plt.axis('off')


# - Magnitude : combine les deux → met en evidence tous les contours forts

#-----------------------
# 2. Le filtre Laplacien 
#-----------------------
#Le Laplacien detecte les zones où le gradient change rapidement en utilisant la seconde derivee.
L = np.array([[ 0, -1,  0],
              [-1,  4, -1],
              [ 0, -1,  0]], dtype=np.float32)

laplacian = cv2.filter2D(I, -1, L, borderType=cv2.BORDER_CONSTANT)

laplacian_norm = normalize(laplacian)

# Remarque : Le laplacien donne des valeurs positives et negatives (points de passage par zero = contours)
# mais pour l'affichage, nous utilisons la normalisation

# Appliquer d'abord le filtre gaussien (pour reduire le bruit)
I_blurred = cv2.GaussianBlur(I, (5, 5), 0)

laplacian_blurred = cv2.filter2D(I_blurred, -1, L, borderType=cv2.BORDER_CONSTANT)

laplacian_blurred_norm = normalize(laplacian_blurred)

# Nous utilisons CV_32F pour conserver les valeurs negatives
laplacian_cv = cv2.Laplacian(I, cv2.CV_32F) 
laplacian_cv_norm = normalize(laplacian_cv)

plt.subplot(2, 3, 5)
plt.title('Laplacien (manuel)')
plt.imshow(laplacian_norm, cmap='gray')
plt.axis('off')

plt.subplot(2, 3, 6)
plt.title('Laplacien apres Gauss')
plt.imshow(laplacian_blurred_norm, cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()

print("="*60)
print("Analyse de Laplacien :")
print("="*60)
print("1. Le Laplacien montre les contours comme des points de passage par zero (de positif a negatif)")
print("2. Sans Gauss : tres sensible au bruit → beaucoup de contours indesirables")
print("3. Avec Gauss : resultats plus propres et precis")
print("4. OpenCV utilise le meme principe mais avec des ameliorations internes")
#-----------------------
# 3. Detecteur de Canny
#-----------------------
#Le detecteur de Canny est un detecteur de contours avance utilise pour identifier les 
#transitions d’intensite dans une image. Il est considere comme l’un des meilleurs 
#detecteurs de contours
thresholds = [
    (100, 50),   
    (50, 100),   
    (30, 150),
    (70, 200),
]

plt.figure(figsize=(14, 6))

# Image originale
plt.subplot(2, 3, 1)
plt.title('Image originale')
plt.imshow(I, cmap='gray')
plt.axis('off')

# Canny avec les valeurs donnees (meme si elles sont inversees)
canny_wrong = cv2.Canny(I.astype(np.uint8), 100, 50)

plt.subplot(2, 3, 2)
plt.title('Canny (100, 50) - inverse')
plt.imshow(canny_wrong, cmap='gray')
plt.axis('off')

idx = 3
for t1, t2 in thresholds[1:]:  
    canny = cv2.Canny(I.astype(np.uint8), t1, t2)
    plt.subplot(2, 3, idx)
    plt.title(f'Canny ({t1}, {t2})')
    plt.imshow(canny, cmap='gray')
    plt.axis('off')
    idx += 1

plt.tight_layout()
plt.show()

results = {
    'Original': I.astype(np.uint8),
    'Sobel Magnitude': magnitude_norm,
    'Laplacian (manual)': laplacian_norm,
    'Laplacian + Gaussian': laplacian_blurred_norm,
    'Canny (50,100)': cv2.Canny(I.astype(np.uint8), 50, 100),
    'Canny (70,200)': cv2.Canny(I.astype(np.uint8), 70, 200)
}

plt.figure(figsize=(18, 12))
for i, (title, img) in enumerate(results.items(), 1):
    plt.subplot(2, 3, i)
    plt.title(title, fontsize=14)
    plt.imshow(img, cmap='gray')
    plt.axis('off')

plt.suptitle('Comparaison des methodes de detection des contours', fontsize=16, y=0.98)
plt.tight_layout()
plt.show()