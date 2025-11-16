# Importing Image from PIL package
from PIL import Image
import imageio as iio

# creating a image object
im = Image.open(r"im1.bmp")
px = im.load()
print (px[4, 4])
px[4, 4] = (0, 0, 0)
print (px[4, 4])
coordinate = x, y = 150, 59

# using getpixel method
print (im.getpixel(coordinate));

width, height = im.size
  
for x in range(height):
    im.putpixel( (x, x), (0, 0, 0, 255) )
  
im.show()

# Python program to read an write an image

# read an image
img = iio.imread("im1.bmp")

# write it in a new format
iio.imwrite("im1.jpg", img)
