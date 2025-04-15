from PIL import Image

im=Image.open("map00564_20250414_134522.png")
print(im.format, im.size, im.mode)

#im.show()
pixels=list(im.getdata())
width, height = im.size

grayscale_pixels=[0.299*x[0] + 0.587*x[1] + 0.114*x[2] for x in pixels]
#print(grayscale_pixels[:100])
