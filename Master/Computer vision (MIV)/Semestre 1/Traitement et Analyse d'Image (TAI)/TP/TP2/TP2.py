#--------------------------------------------
#1. Opérations arithmétiques et logiques sur une image. 
#--------------------------------------------
import cv2
import matplotlib.pyplot as plt
import numpy as np

img = cv2.imread('lena.jpg', cv2.IMREAD_GRAYSCALE)

hauteur, largeur = img.shape

#image binaire
B = np.zeros((hauteur, largeur), dtype=np.uint8)
x1, y1 = 80, 50      # coin supérieur gauche
x2, y2 = 180, 150   
# Dessiner un rectangle blanc (255)
cv2.rectangle(B, (x1, y1), (x2, y2), color=255, thickness=-1)

#somme 
somme = cv2.add(img, B)

#Soustraction 
soustraction = cv2.subtract(img, B)

# Multiplication
multiplication = cv2.multiply(img, B, scale=1/255.0)

#les operations logique
and_img = cv2.bitwise_and(img, B)
or_img  = cv2.bitwise_or(img, B)
xor_img = cv2.bitwise_xor(img, B)


plt.subplot(3,3,1); plt.imshow(img, cmap='gray'); plt.title("Image Lena"); plt.axis('off')
plt.subplot(3,3,2); plt.imshow(B, cmap='gray'); plt.title("Image Binaire (B)"); plt.axis('off')

# Arithmétiques
plt.subplot(3,3,4); plt.imshow(somme, cmap='gray'); plt.title("Addition Lena + B"); plt.axis('off')
plt.subplot(3,3,5); plt.imshow(soustraction, cmap='gray'); plt.title("Soustraction Lena - B"); plt.axis('off')
plt.subplot(3,3,6); plt.imshow(multiplication, cmap='gray'); plt.title("Multiplication Lena × B"); plt.axis('off')

# Logiques
plt.subplot(3,3,7); plt.imshow(and_img, cmap='gray'); plt.title("AND (Lena ∧ B)"); plt.axis('off')
plt.subplot(3,3,8); plt.imshow(or_img, cmap='gray'); plt.title("OR (Lena ∨ B)"); plt.axis('off')
plt.subplot(3,3,9); plt.imshow(xor_img, cmap='gray'); plt.title("XOR (Lena ⊕ B)"); plt.axis('off')

plt.tight_layout()
plt.show()

#--------------------------------------------
#2. Manipulation de l’histogramme.
#--------------------------------------------
def HISTO(image):
    
    # Initialiser un tableau de 256 cases à 0 (pour niveaux 0→255)
    h = np.zeros(256, dtype=int)

    # Parcourir tous les pixels de l'image
    for i in range(image.shape[0]):        # lignes
        for j in range(image.shape[1]):    # colonnes
            niveau = image[i, j]           # intensité du pixel
            h[niveau] += 1                 # incrémenter le compteur correspondant

    return h

hist = HISTO(img)

plt.figure("Histogramme simple")
plt.subplot(1,2,1)
plt.imshow(img, cmap='gray')
plt.title("Image originale")
plt.axis('off')

plt.subplot(1,2,2)
plt.plot(hist, color='black')
plt.title("Histogramme des niveaux de gris")
plt.xlabel("Niveau de gris (0–255)")
plt.ylabel("Nombre de pixels")
plt.tight_layout()
plt.show()

#TRL (ajoute un constant C)
def TRL(image, C):
    """
    Ajoute une constante C à tous les pixels de l'image.
    Si C > 0 → éclaircissement
    Si C < 0 → assombrissement
    """
    img_trl = image.astype(np.int16) + C   # pour éviter le débordement
    img_trl = np.clip(img_trl, 0, 255)     # limite entre 0 et 255
    return img_trl.astype(np.uint8)

img_plus100 = TRL(img, 100)   # éclaircir
img_moins50 = TRL(img, -50) # assombrir

hist1 = HISTO(img)
hist2 = HISTO(img_plus100)
hist3 = HISTO(img_moins50)

plt.figure("TRL - Translation de niveaux de gris")
plt.subplot(2,3,1)
plt.imshow(img, cmap='gray')
plt.title("Image originale")
plt.axis('off')

plt.subplot(2,3,2)
plt.imshow(img_plus100, cmap='gray')
plt.title("C = +100 (éclaircie)")
plt.axis('off')

plt.subplot(2,3,3)
plt.imshow(img_moins50, cmap='gray')
plt.title("C = -50 (assombrie)")
plt.axis('off')

plt.subplot(2,3,4)
plt.plot(hist1, color='black')
plt.title("hist1")
plt.xlabel("Niveau de gris")
plt.ylabel("Nombre de pixels")

plt.subplot(2,3,5)
plt.plot(hist2, color='black')
plt.title("hist2")
plt.xlabel("Niveau de gris")

plt.subplot(2,3,6)
plt.plot(hist3, color='black')
plt.title("hist3")
plt.xlabel("Niveau de gris")

plt.tight_layout()
plt.show()

#--------------------------------------------
# Inversion de l’image
#--------------------------------------------
# Méthode 1 : formule mathématique
inversion = 255 - img

# Méthode 2 (alternative OpenCV)
# inversion = cv2.bitwise_not(img)

hist_original = HISTO(img)
hist_inverse = HISTO(inversion)

plt.figure("Inversion d'image")

# Ligne 1 : Images
plt.subplot(2,2,1)
plt.imshow(img, cmap='gray')
plt.title("Image originale")
plt.axis('off')

plt.subplot(2,2,2)
plt.imshow(inversion, cmap='gray')
plt.title("Image inversée (255 - I)")
plt.axis('off')

# Ligne 2 : Histogrammes
plt.subplot(2,2,3)
plt.plot(hist_original, color='black')
plt.title("Histogramme original")
plt.xlabel("Niveau de gris")
plt.ylabel("Nombre de pixels")

plt.subplot(2,2,4)
plt.plot(hist_inverse, color='black')
plt.title("Histogramme après inversion")
plt.xlabel("Niveau de gris")

plt.tight_layout()
plt.show()

def etirement_contraste(image):
    """
    Applique un étirement linéaire pour améliorer le contraste :
    I'(x, y) = (I(x, y) - Imin) / (Imax - Imin) * 255
    """
    Imin = np.min(image)
    Imax = np.max(image)
    
    print(f"Valeurs min = {Imin}, max = {Imax}")
    
    # Éviter la division par zéro
    if Imax == Imin:
        return image.copy()
    
    I_norm = (image - Imin) / (Imax - Imin) * 255
    return I_norm.astype(np.uint8)

alex = cv2.imread('alex.jpg', cv2.IMREAD_GRAYSCALE)

lena_exp = etirement_contraste(img)
alex_exp = etirement_contraste(alex)

plt.figure("Expansion de contraste - Lena")
plt.subplot(2,2,1)
plt.imshow(img, cmap='gray')
plt.title("Lena originale")
plt.axis('off')

plt.subplot(2,2,2)
plt.imshow(lena_exp, cmap='gray')
plt.title("Lena étirée")
plt.axis('off')

plt.subplot(2,2,3)
plt.plot(HISTO(img), color='black')
plt.title("Histogramme original")

plt.subplot(2,2,4)
plt.plot(HISTO(lena_exp), color='black')
plt.title("Histogramme étiré")
plt.tight_layout()
plt.show()

plt.figure("Expansion de contraste - Alex")
plt.subplot(2,2,1)
plt.imshow(alex, cmap='gray')
plt.title("Alex originale")
plt.axis('off')

plt.subplot(2,2,2)
plt.imshow(alex_exp, cmap='gray')
plt.title("Alex étirée")
plt.axis('off')

plt.subplot(2,2,3)
plt.plot(HISTO(alex), color='black')
plt.title("Histogramme original")

plt.subplot(2,2,4)
plt.plot(HISTO(alex_exp), color='black')
plt.title("Histogramme étiré")
plt.tight_layout()
plt.show()

#--------------------------------------------
# 17. Appliquer un seuillage simple
#--------------------------------------------
_, lena_thresh = cv2.threshold(lena_exp, 120, 255, cv2.THRESH_BINARY)
_, alex_thresh = cv2.threshold(alex_exp, 120, 255, cv2.THRESH_BINARY)

plt.figure("Seuillage simple (t=120)")
plt.subplot(1,2,1)
plt.imshow(lena_thresh, cmap='gray')
plt.title("Lena seuillée (t=120)")
plt.axis('off')

plt.subplot(1,2,2)
plt.imshow(alex_thresh, cmap='gray')
plt.title("Alex seuillée (t=120)")
plt.axis('off')
plt.show()

#--------------------------------------------
# 18. Appliquer le seuillage d’Otsu
#--------------------------------------------
_, lena_otsu = cv2.threshold(lena_exp, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
_, alex_otsu = cv2.threshold(alex_exp, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

plt.figure("Seuillage d'Otsu")
plt.subplot(1,2,1)
plt.imshow(lena_otsu, cmap='gray')
plt.title("Otsu sur Lena")
plt.axis('off')

plt.subplot(1,2,2)
plt.imshow(alex_otsu, cmap='gray')
plt.title("Otsu sur Alex")
plt.axis('off')
plt.show()