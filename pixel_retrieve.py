from PIL import Image
import numpy as np

im=Image.open("marston.jpg")
print(im.format, im.size, im.mode)

#im.show()
pixels=list(im.getdata())
width, height = im.size

grayscale_pixels=[0.299*x[0] + 0.587*x[1] + 0.114*x[2] for x in pixels]
#print(grayscale_pixels[:100])

def retrieve_digits(num_digits: int, data: list)->list:
	data=[str(i) for i in data]
	digits=[int(i[:num_digits]) for i in data]
	return digits

sig_figs=retrieve_digits(1, grayscale_pixels)
sig_figs=np.array(sig_figs)
print(sig_figs[:10])

print(set(sig_figs))

distribution=[sum(sig_figs == i) / len(sig_figs) for i in set(sig_figs)]
for ind, i in enumerate(distribution):
	print(ind,": ",i*100,"%")
print("\nsum of distributions is", sum(distribution))

