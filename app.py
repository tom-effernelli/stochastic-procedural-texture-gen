import numpy as np
import scipy.stats as stats
from PIL import Image
import matplotlib.pyplot as plt

# Gaussian distribution parameters, see Deliot & Heitz paper for reasons of this choice
GAUSSIAN_AVERAGE = 0.5
GAUSSIAN_STD = 1/36

# Computing T transformation
# input is an np.array object
def Tinput(input):
    Tinput = Image.new('RGB', (len(input[0]), len(input))) # Creating new Image that will have gaussian histogram

    sortedInputValues = []
    for y in range(len(input)):
        for x in range(len(input[0])):
            sortedInputValues.append((x, y, input[y][x]))
    sortedInputValues = sorted(sortedInputValues, key=lambda t:t[2]) # Sorting the list based on channel's color value

    for i in range(len(sortedInputValues)):
        x, y, _ = sortedInputValues[i]
        U = (i + 0.5)/len(sortedInputValues)
        G = stats.norm.ppf(U, loc=GAUSSIAN_AVERAGE, scale=GAUSSIAN_STD)


# Texture file must be named after 'texture.jpg' and must thus be a JPEG format
input_texture = Image.open("texture.jpg").convert('RGB')
input = np.array(input_texture)
channels = [input[:, :, i] for i in range(3)]

# From now we are working on each channel independantly
for c in channels: