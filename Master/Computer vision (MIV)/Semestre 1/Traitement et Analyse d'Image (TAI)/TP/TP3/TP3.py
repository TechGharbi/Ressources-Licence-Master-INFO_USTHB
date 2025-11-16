#------------------------------------
#Part1. Convolution avec OpenCV
#------------------------------------
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Charger l'image bruitée
img = cv2.imread('lena_noise.jpg', cv2.IMREAD_GRAYSCALE)

#--------------------------------------------
# 1. Filtre moyen (flou uniforme)
#--------------------------------------------
def filtre_moyen(image, k):
    return cv2.blur(image, (k, k))

#--------------------------------------------
# 2. Filtre médian
#--------------------------------------------
def filtre_median(image, k):
    return cv2.medianBlur(image, k)

#--------------------------------------------
# 3. Application des filtres pour K = 3, 5, 7, 11
#--------------------------------------------
tailles = [3, 5, 7, 11]

plt.figure("Filtres - OpenCV")

for i, k in enumerate(tailles):
    mean = filtre_moyen(img, k)
    median = filtre_median(img, k)
    
    plt.subplot(2, len(tailles), i+1)
    plt.imshow(mean, cmap='gray')
    plt.title(f"Filtre moyen {k}x{k}")
    plt.axis('off')

    plt.subplot(2, len(tailles), len(tailles)+i+1)
    plt.imshow(median, cmap='gray')
    plt.title(f"Filtre médian {k}x{k}")
    plt.axis('off')

plt.tight_layout()
plt.show()

#--------------------------------------------
# 4. Creer et appliquer un noyau personnalise
#--------------------------------------------
kernel = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])   # Filtre de renforcement 
img_filtre = cv2.filter2D(img, -1, kernel)

plt.figure("Filtre personnalise")
plt.subplot(1,2,1); plt.imshow(img, cmap='gray'); plt.title("Originale"); plt.axis('off')
plt.subplot(1,2,2); plt.imshow(img_filtre, cmap='gray'); plt.title("Apres filtre custom"); plt.axis('off')
plt.show()

#------------------------------------
#Part2. Convolution « from scratch ».
#------------------------------------
#corrige :
#Erreur 1 — Le noyau n’est pas symetrique ni normalise
#Erreur 2 — Manque de normalisation des résultats
#Erreur 4 — Noyau mal appliqué ou non retourné

def convolution(image, kernel):

    H, W = image.shape
    h, w = kernel.shape
    p_h, p_w = h // 2, w // 2

    # Retourner le noyau (propriété de la convolution)
    kernel = np.flipud(np.fliplr(kernel))

    # Ajouter un padding de zéros autour de l'image
    padded = np.pad(image, ((p_h, p_h), (p_w, p_w)), mode='constant')

    # Image résultat
    output = np.zeros_like(image, dtype=np.float32)

    # Balayer toute l'image
    for i in range(H):
        for j in range(W):
            region = padded[i:i+h, j:j+w]
            output[i, j] = np.sum(region * kernel)

    # Normaliser dans [0,255]
    output = np.clip(output, 0, 255)
    return output.astype(np.uint8)

kernel = np.ones((3,3), np.float32) / 9

# Appliquer la convolution manuelle
result = convolution(img, kernel)

# Résultat OpenCV pour comparaison
result_cv = cv2.filter2D(img, -1, kernel)

plt.figure("Test de la fonction Convolution")
plt.subplot(1,3,1)
plt.imshow(img, cmap='gray')
plt.title("Image originale")
plt.axis('off')

plt.subplot(1,3,2)
plt.imshow(result, cmap='gray')
plt.title("Convolution manuelle")
plt.axis('off')

plt.subplot(1,3,3)
plt.imshow(result_cv, cmap='gray')
plt.title("Convolution OpenCV")
plt.axis('off')

plt.tight_layout()
plt.show()

#-----------------------------------
def convolution(image, kernel):
    k = kernel.shape[0]
    p = k // 2  # padding

    # Inverser le noyau sur les deux axes (propriété de la convolution)
    kernel = np.flipud(np.fliplr(kernel))

    # Padding de zéros
    padded = np.pad(image, ((p, p), (p, p)), mode='constant', constant_values=0)
    output = np.zeros_like(image)

    # Appliquer la convolution
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            region = padded[i:i+k, j:j+k]
            output[i, j] = np.sum(region * kernel)
    
    # Normaliser pour rester dans [0,255]
    output = np.clip(output, 0, 255)
    return output.astype(np.uint8)

# Exemple de noyau
kernel = np.ones((3,3), np.float32) / 9  # Filtre moyen 3x3
result = convolution(img, kernel)

plt.subplot(1,2,1); plt.imshow(img, cmap='gray'); plt.title("Originale"); plt.axis('off')
plt.subplot(1,2,2); plt.imshow(result, cmap='gray'); plt.title("Convolution manuelle"); plt.axis('off')
plt.show()

#------------------------------------
#Part3. Filtre Gaussien.
#------------------------------------
def filtre_gaussien(sigma, k):
    ax = np.linspace(-(k-1)/2, (k-1)/2, k)
    xx, yy = np.meshgrid(ax, ax)
    noyau = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    noyau = noyau / np.sum(noyau)
    return noyau

# Exemple
G = filtre_gaussien(sigma=1, k=3)
print("Noyau gaussien (K=3, σ=1):\n", G)

# Appliquer la convolution avec ce filtre
result = convolution(img, G)

plt.figure("Filtre Gaussien")
plt.subplot(1,2,1); plt.imshow(img, cmap='gray'); plt.title("Image originale"); plt.axis('off')
plt.subplot(1,2,2); plt.imshow(result, cmap='gray'); plt.title("Flou gaussien (σ=1, K=3)"); plt.axis('off')
plt.show()

# Tester différentes tailles et σ
params = [(3,0.5), (3,1), (5,1), (7,2)]
plt.figure("Différents filtres Gaussiens")

for i, (k, s) in enumerate(params):
    G = filtre_gaussien(s, k)
    result = convolution(img, G)
    plt.subplot(2,2,i+1)
    plt.imshow(result, cmap='gray')
    plt.title(f"K={k}, σ={s}")
    plt.axis('off')

plt.tight_layout()
plt.show()