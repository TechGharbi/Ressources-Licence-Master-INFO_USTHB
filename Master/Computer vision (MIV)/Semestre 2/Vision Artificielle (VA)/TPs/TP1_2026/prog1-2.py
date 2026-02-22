import cv2

img_path = "im1.jpg"
image_c = cv2.imread(img_path)
image = cv2.cvtColor(image_c, cv2.COLOR_BGR2GRAY)

# Number of iterations for the Gaussian blur filter
n = 5  

# Parameters for Gaussian blur
ksize = (3, 3)
sigma = 2
border_type = cv2.BORDER_DEFAULT

# Apply initial Gaussian blur: g(x,y) = f(x,y) * G_σ
blur_img = cv2.GaussianBlur(image, (3, 3), 2, 0, border_type)

# Apply Gaussian blur iteratively n times: g(x,y) = g(x,y) * G_σ
for i in range(n):
    blur_img = cv2.GaussianBlur(blur_img, ksize, sigma, 0, border_type)

cv2.imshow('Iterative Gaussian Blur (n={})'.format(n), blur_img)
cv2.waitKey(0)

cv2.imwrite("im1_iterative_blur.png", blur_img)
cv2.waitKey(0)