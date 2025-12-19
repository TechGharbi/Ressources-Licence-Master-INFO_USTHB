import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('asma.jpg')

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

gray = cv2.imread('asma.jpg', cv2.IMREAD_GRAYSCALE)

_, binary1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

blur = cv2.GaussianBlur(binary, (5, 5), 0)

binary2 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 5)

combined_binary = cv2.bitwise_or(binary1, binary2)

# Réduire la taille du noyau pour préserver plus de détails fins
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))

opened = cv2.morphologyEx(blur, cv2.MORPH_OPEN, kernel)

closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

_, binary3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

opened1 = cv2.morphologyEx(binary3, cv2.MORPH_OPEN, kernel)

closed1 = cv2.morphologyEx(opened1, cv2.MORPH_CLOSE, kernel)

# Utiliser RETR_LIST pour récupérer tous les contours, y compris internes, pour capturer plus de détails
#contours, hierarchy = cv2.findContours(closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

edges = cv2.Canny(closed, 50, 150, apertureSize=3, L2gradient=True)
edges = cv2.dilate(edges, cv2.getStructuringElement(cv2.MORPH_RECT, (3,3)))
contours, hierarchy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# Filtrer les contours par aire minimale, mais réduire le seuil pour inclure des détails plus fins
min_area = 100  # Réduit pour capturer des contours plus petits comme les détails de la plante
valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

mask = np.zeros_like(closed)
for cnt in valid_contours:
    cv2.fillPoly(mask, [cnt], 255)

result = cv2.bitwise_and(img_rgb, img_rgb, mask=mask)

# Lissage léger
gauss = cv2.GaussianBlur(gray, (5, 5), 0)
gauss1 = cv2.GaussianBlur(binary, (5, 5), 0)

_, binaryG = cv2.threshold(gauss1, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Canny seul
edges = cv2.Canny(gauss, 50, 150)

# Inverser pour obtenir fond blanc + dessin noir
result1 = cv2.bitwise_or(edges , binaryG)

plt.figure(figsize=(12, 6))

plt.subplot(3, 4, 1)
plt.title("Image originale")
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(3, 4, 2)
plt.imshow(gray, cmap='gray')
plt.title('Niveaux de Gris')
plt.axis('off')

plt.subplot(3, 4, 3)
plt.title("noir&blanc")
plt.imshow(binary, cmap='gray')
plt.axis('off')

plt.subplot(3, 4, 4)
plt.imshow(combined_binary, cmap='gray')
plt.title('Binaire Combiné')
plt.axis('off')

plt.subplot(3, 4, 5)
plt.title("ouverture")
plt.imshow(opened, cmap='gray')
plt.axis('off')

plt.subplot(3, 4, 6)
plt.title("ouverture + fermeture")
plt.imshow(closed, cmap='gray')
plt.axis('off')

plt.subplot(3, 4, 7)
plt.title("ouverture1")
plt.imshow(opened1, cmap='gray')
plt.axis('off')

plt.subplot(3, 4, 8)
plt.title("ouverture1 + fermeture1")
plt.imshow(closed1, cmap='gray')
plt.axis('off')

plt.subplot(3, 4, 9)
plt.imshow(mask, cmap='gray')
plt.title('Masque')
plt.axis('off')

plt.subplot(3, 4, 10)
plt.title("(objet)")
plt.imshow(result)
plt.axis('off')

plt.subplot(3, 4, 11)
plt.title("Superposition sur l'original")
overlay = img.copy()
for cnt in valid_contours:
    cv2.drawContours(overlay, [cnt], -1, (0, 255, 0), 2)
plt.imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(3, 4, 12)
plt.title("(objet par Canny seul)")
plt.imshow(result1 , cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()
