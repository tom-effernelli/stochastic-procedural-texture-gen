import numpy as np
import scipy.stats as stats
from PIL import Image
import matplotlib.pyplot as plt

# Computing T transformation
# input is an np.array object
def Tinput(input):
    Tinput = Image.new('RGB', (len(input[0]), len(input))) # Creating new Image that will have gaussian histogram
    sortedInputValues = []
    for y in range(len(input)):
        for x in range(len(input[0])):
            sortedInputValues.append((x, y, input[y][x]))

# Texture file must be named after 'texture.jpg' and must thus be a JPEG format
input_texture = Image.open("texture.jpg").convert('RGB')
input = np.array(input_texture)
channels = [input[:, :, i] for i in range(3)]

# From now we are working on each channel independantly
for c in channels: