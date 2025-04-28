import matplotlib.pyplot as plt
import os
import sys
import numpy as np
from PIL import Image
from tqdm import tqdm 
from scipy.fftpack import dct


def calc_DCT(img_np: np.ndarray) -> np.array:
	"""
    This function calculates the DCT coefficiets and then flattens the values into a big long 1d array

    Input: np.ndarray img_np which is in the same shape as the image
    Output: np.array which is the 1d array containing the DCT coefficients
	"""

	height, width=img_np.shape
	blocks=[]
    #we calculate it in blocks of 8x8
	#source: https://stackoverflow.com/questions/15978468/using-the-scipy-dct-function-to-create-a-2d-dct-ii
	#source: https://stackoverflow.com/questions/60052848/discrete-cosine-transform-dct-coefficient-distribution
	#source: https://medium.com/analytics-vidhya/what-are-dct-coefficients-and-how-jpeg-compression-works-7f46d1e22b4c
	for i in tqdm(range(0,height,8), desc="Calculating DCT coefficients"):
		for j in range(0,width,8):
			block=img_np[i:i+8, j:j+8]
			block_dct=dct(dct(block.T, norm="ortho").T, norm="ortho") #referenced from stack overflow
			blocks.append(block_dct)
	
	#coefficients, currently in an array of 8x8 blocks
	blocks=[i.flatten() for i in blocks]    
	coefficients=np.concatenate(blocks)     #flattens it out to 1d array (length of heightxwidth)
	print()	

	return coefficients

def sig_fig(val: float) -> int:
	"""
    This function extracts the significant digit of a float value

    Input: float value
    Output: int value ranging from 1-9
	"""

	val=str(val)
	char=val[0]
	
	i=1
	while char=="-" or char=="0" or char==".":      
		if i == len(val):
			return -1
		char=val[i]
		i+=1
	
	return int(char)

def retrieve_sigfig(data: list[float]) -> np.array:
	"""
    This function extracts the significant values for each element in the list

    Input: list[float] data that contains the DCT coeffcietnts
    Output: np.array of sigfigs containing the significant values 
	"""

	sigfigs=[sig_fig(i) for i in tqdm(data, desc="Retrieving Significant Figures")]
	print()

	return np.array(sigfigs)

def calc_distribution(sig_figs: np.array) -> dict[int, float]:
	"""
    This function will calculate the relative abundancies for each sigfig

    Input: np.array sig_figs which containes all the sigfigs in 1d array
    Output: dictionary[int, float] where the keys are sigfig digits 1-9 and the values are the relative proportions
    """

	digits=[1,2,3,4,5,6,7,8,9]
	distribution=[100 * sum(sig_figs == i) / len(sig_figs) for i in tqdm(digits, desc="Calculating Distributions")]
	print()

	return dict(zip(digits, distribution))

def draw_bar(distribution: dict[int, float]):
	"""
    This function will draw a bar plot displaying the relative abundancies for each significant value.
    The plot will also have the expected Benford's distribution plotted above the bars

    Input: dictionary[int, float] with the keys as digits 1-9 and the values as the relative proportions
    Output: None, but a figure of the plot will be saved in the Results directory
    """

    #plot pixel sigfig frequency distributions
	colors={			
		-1:(0, 0, 0),
		1:(0.941, 0.231, 0.231),
		2:(0.941, 0.537, 0.231),
		3:(1, 0.8, 0.2),
		4:(0.133, 0.545, 0.133),
		5:(0.392, 0.584, 0.929),
		6:(0.255, 0.412, 0.882),
		7:(0.482, 0.408, 0.933),
		8:(1, 0.753, 0.796),
		9:(0.823, 0.412, 0.118)
	}

	colors=[colors[x] for x in distribution.keys()]

	bar = [x for x in range(1,10)]
	bars = plt.bar(
		bar,
		height=distribution.values(),
		width=0.75,
		tick_label=distribution.keys(),
		color=colors
	)
    
	#plot benfords stuff
	benfords_dist=[30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]		
	digits=[1,2,3,4,5,6,7,8,9]

	plt.plot(digits, benfords_dist,
		marker="o"
	)
	plt.ylim(0,100)
	plt.ylabel("Percentage (%)")
	#plt.show()
	
	os.makedirs("Results", exist_ok=True)
	plt.title("Distribution Frequency")
	plt.savefig("Results/distribution_freq.png")

def statistical_testing(distribution: dict[int, float]):
	"""
	This function calculates how much the sigfig distributions are deviant from the expected
	values by using the Anderson-Darling test. It outputs the results in a saved text file.
	The text file also holds information about the relative proportions for each digit as well as
	list the critical values for each significance level.

	Input: dict[int, float] containing the keyts as sigfigs 1-9 and values of their proportions
	Ouput: a saved text file in the Results directory
	"""

	#Anderson-Darling Test
	with open("Results/Statistical_Analysis.txt", "w") as file:
		file.write("DIGIT                    FREQUENCY\n")
		file.write("----------------------------------\n")
		for digit, prob in distribution.items():
			prob = int(prob*100)/100
			file.write(f"{digit}:                       {prob}%\n")

	#source: https://real-statistics.com/non-parametric-tests/goodness-of-fit-tests/goodness-of-fit-benford-distribution/
	qi=np.array(list(distribution.values())) / 100
	pi=[0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]	#benfords distributions
	sum_qi=[qi[0]]
	sum_pi=[pi[0]]

	for i in range(1,9):
		sum_qi.append(qi[i] + sum_qi[i-1])
		sum_pi.append(pi[i] + sum_pi[i-1])

	#calculate the test statistic
	ad_stat=[((pi[x] + pi[x+1])*(sum_qi[x] - sum_pi[x])**2) / (sum_pi[x]*(1-sum_pi[x])) for x in range(8)]
	ad_stat=4.5 * sum(ad_stat)
	ad_stat=int(ad_stat*10000)/10000
	
	with open("Results/Statistical_Analysis.txt", "a") as file:
		file.write("\n\nAnderson-Darling Test\n")
		file.write(f"Test statistic value: {ad_stat}\n\n")
		file.write("Alpha level:    0.01    0.025    0.05    0.1    0.25    0.5\n")
		file.write("Critical value: 3.688   2.89     2.304   1.743  1.060   0.596\n")
		file.write("\nThere is a significant result when the statistic value is greater than the critical value at the corresponding alpha level.\n")

def colorcoding(pixels, sigfigs: np.ndarray):
	"""
    This function basically replaces each pixel in the image with a corresponding color for its significant value.
    For example, a pixel with significant value of 1 will be colored red
    
    Input: pixels object, np.ndarray sigfigs (in the same shape as the image)
    Output: newly modified pixels object 
	"""
	colors={
		-1:(0, 0, 0),			
		1:(240, 59, 59),
		2:(240, 137, 59),
		3:(255, 204, 51),
		4:(34,139,34),
		5:(100,149,237),
		6:(65,105,225),
		7:(123,104,238),
		8:(255,192,203),
		9:(210,105,30)
	}
	
	height, width = sigfigs.shape
	
	for i in tqdm(range(height), desc="Colorcoding the original image"):
		for j in range(width):
			pixels[j, i] = colors[sigfigs[i, j]]
	print()
	
	return pixels

def main():
	if len(sys.argv) > 2:
		raise Exception("You added too many arguments. Please provide only one file path!")
	elif not os.path.exists(sys.argv[1]):
		raise FileNotFoundError("Uh-oh! I can't find your file; it appears it does not exist.")
	print(f"Found {sys.argv[1]}!")
	
	im=Image.open(sys.argv[1]).convert("L") #converts into grayscale
	im_np=np.array(im)   #convert into numpy for easier arithmetic manipulation

	print(f"Image basic information: {im.format}, {im.size}\n")

	height, width=im_np.shape

	#make sure im_np dimensions are divisible by 8
	im_np=im_np[:height-height%8, :width-width%8]
	dct_coefficients=calc_DCT(im_np)

	sigfigs=retrieve_sigfig(dct_coefficients)

	distributions=calc_distribution(sigfigs)

	draw_bar(distributions)
	print("Histogram completed. Plot saved.\n")
	
	statistical_testing(distributions)
	print("Statistical analysis completed. Text file saved.\n")

	im=im.convert("RGB")
	pixels=im.load()	
	sigfigs=np.reshape(sigfigs, (height-height%8, width-width%8))
	new_pixels=colorcoding(pixels, sigfigs)
	
	print("Generating colorcoded image...")
	im.save("Results/Colorcoded_image.png", format="png")
	print("Image saved!")
	print("\nAll done! You can check results in the Results directory.")

if __name__ == "__main__":
	main()
