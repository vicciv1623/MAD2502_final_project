import matplotlib.pyplot as plt
import sys
from PIL import Image
import numpy as np

def sig_fig(val: int) -> int:
	val=str(val)
	char=val[0]

	digits=list(range(1,10))
	digits=[str(x) for x in digits]
	
	i=1
	while char not in digits:
		if i == len(val):
			return 0
		char=val[i]
		i+=1
	
	return int(char)

def retrieve_sigfig(data: list[int]) -> list:
	data=[sig_fig(x) for x in data]
	return data

def draw_hist(distribution: dict[int, float]):
	colors={			#will update colors to include all 9 digits
		1:"red",
		2:"orange",
		3:"yellow"
	}
	print(distribution.keys())
	colors=[colors[x] for x in distribution.keys()]

	bar = [1+x for x in range(1,4)]
	bars = plt.bar(
		bar,
		height=distribution.values(),
		width=0.75,
		tick_label=distribution.keys(),
		color=colors
	)
	plt.show()

def main():
	print("hello world")
	if len(sys.argv) > 2:
		print("you added too many arguments")
	print("image file name", sys.argv[1])
	
	'''
	im=Image.open(sys.argv[1])
	print(im.format, im.size, im.mode)

	pixels=list(im.getdata())
	grayscale_pix=[0.299*x[0] + 0.587*x[1] + 0.114*x[2] for x in pixels[:10]]
	print(grayscale_pix[:10])
	
	sigfig_pix=retrieve_sigfig(grayscale_pix)
	print(set(sigfig_pix))
	print(sigfig_pix[:10])'''
	
	temp_distribution={
		1:10.5,
		2:20.5,
		3:40.5
	}
	print(temp_distribution)
	draw_hist(temp_distribution)
	
	

if __name__ == "__main__":
	main()
