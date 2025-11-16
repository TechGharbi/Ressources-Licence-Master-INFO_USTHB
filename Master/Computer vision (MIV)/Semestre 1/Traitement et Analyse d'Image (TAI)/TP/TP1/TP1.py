#--------------------------------------------
#1. Charger une image en niveaux de gris et en couleur. 
#--------------------------------------------
import cv2
import matplotlib.pyplot as plt
import numpy as np

# charge l'image en niveaux de gris 
image_gray = cv2.imread('Lena.jpg',cv2.IMREAD_GRAYSCALE)

# Charger lena en couleur (BGR)
img_color = cv2.imread('lena.jpg', cv2.IMREAD_COLOR)

# affiche l'image en niveaux de gris 
if image_gray is not None or img_color is not None:
    print (image_gray.shape)
    cv2.imshow('Loaded image',image_gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imshow('Loaded image',img_color)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else :
    print("Error loading the image")

#--------------------------------------------
#2. Images Couleurs et conversions 
#--------------------------------------------
img_rgb = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)
plt.title("Image en couleur")
plt.axis("off")
plt.show()

#Separer les canaux 
b, g, r = cv2.split(img_rgb)

#affiche chaque canal
plt.figure(figsize=(10,4))

plt.subplot(1,3,1)
plt.imshow(r, cmap="gray")
plt.title("Canal Rouge")

plt.subplot(1,3,2)
plt.imshow(g, cmap="gray")
plt.title("Canal Vert")

plt.subplot(1,3,3)
plt.imshow(b, cmap="gray")
plt.title("Canal Bleu")

plt.show()

#--------------------------------------------
#3. Conversion en niveaux de gris
#--------------------------------------------
img_gray_cv = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY) 

#    Gray = 0.299*R + 0.587*G + 0.114*B
B, G, R = cv2.split(img_color)

img_gray_math = 0.299 * R + 0.587 * G + 0.114 * B
img_gray_math = np.uint8(img_gray_math)

plt.figure("Comparaison conversion gris")

plt.subplot(1,2,1)
plt.imshow(img_gray_cv, cmap='gray')
plt.title("Gris - OpenCV (cv2.cvtColor)")
plt.axis('off')

plt.subplot(1,2,2)
plt.imshow(img_gray_math, cmap='gray')
plt.title("Gris - Formule mathématique")
plt.axis('off')

plt.show()

#--------------------------------------------
#4. Echantillonnage et Quantification
#--------------------------------------------
#Echantillonnage
img_echantillon = cv2.resize(image_gray,(50,50),interpolation=cv2.INTER_NEAREST)
img_echantillon_agrandie = cv2.resize(img_echantillon, (256, 256), interpolation=cv2.INTER_NEAREST)

plt.figure("Échantillonnage - Réduction de résolution")
plt.subplot(1,2,1)
plt.imshow(image_gray, cmap='gray')
plt.title("Image originale (512x512)")
plt.axis('off')

plt.subplot(1,2,2)
plt.imshow(img_echantillon_agrandie, cmap='gray')
plt.title("Sous-échantillonnée (50x50)")
plt.axis('off')

plt.show()

#Quantification
def quantification(image, K):
    step = 256 / K
    image_float = image.astype(np.float32)
    image_quant = np.floor(image_float / step) * step + step / 2
    image_quant = np.clip(image_quant, 0, 255)
    return image_quant.astype(np.uint8)

Ks = [2, 4, 8, 16, 32, 64]
plt.figure("Quantification - Différents niveaux K")
for i, K in enumerate(Ks):
    img_q = quantification(image_gray, K)
    plt.subplot(2, 3, i + 1)
    plt.imshow(img_q, cmap='gray')
    plt.title(f"K = {K}")
    plt.axis('off')

plt.tight_layout()
plt.show()
