import matplotlib.pyplot as plt
import os
import sys
from PIL import Image
import numpy as np
from tqdm import tqdm 

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

	bar = [x for x in range(1,4)]
	bars = plt.bar(
		bar,
		height=distribution.values(),
		width=0.75,
		tick_label=distribution.keys(),
		color=colors
	)

	benfords_dist=[30.1, 17.6, 12.5]		#will update distributions
	digits=[1,2,3]
	plt.plot(digits, benfords_dist,
		marker="o"
	)
	#plt.show()
	
	os.makedirs("Results", exist_ok=True)
	plt.title("Distribution Frequency")
	plt.savefig("Results/distribution_freq.png")

def statistical_testing(distribution: dict[int, float]):
	#Anderson-Darling Test
	with open("Results/Statistical_Analysis.txt", "w") as file:
		file.write("DIGIT                    FREQUENCY\n")
		file.write("----------------------------------\n")
		for digit, prob in distribution.items():
			file.write(f"{digit}:                 {prob}%\n")

	#source: https://real-statistics.com/non-parametric-tests/goodness-of-fit-tests/goodness-of-fit-benford-distribution/
	qi=np.array(list(distribution.values())) / 100
	pi=[0.301, 0.176, 0.125] #, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]	#benfords distributions
	sum_qi=[qi[0]]
	sum_pi=[pi[0]]

	for i in range(1,3):
		sum_qi.append(qi[i] + sum_qi[i-1])
		sum_pi.append(pi[i] + sum_pi[i-1])

	ad_stat=[((pi[x] + pi[x+1])*(sum_qi[x] - sum_pi[x])**2) / (sum_pi[x]*(1-sum_pi[x])) for x in range(2)]
	print(ad_stat)
	ad_stat=sum(ad_stat)
	print(ad_stat * 1.5)
	return 0	

def main():
	print("hello world")
	if len(sys.argv) > 2:
		raise Exception("you added too many arguments")
	elif not os.path.exists(sys.argv[1]):
		raise FileNotFoundError("File does not exist")
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
		1:10.1,
		2:57.6,
		3:12.5
	}
	print(temp_distribution)
	draw_hist(temp_distribution)
	
	for i in tqdm(range(100), desc="Passing"):
		pass	
	
	statistical_testing(temp_distribution)

if __name__ == "__main__":
	main()
