import numpy as np
import scipy.stats as stats
from PIL import Image

# Gaussian distribution parameters, see Deliot & Heitz paper for reasons of this choice
GAUSSIAN_AVERAGE = 0.5
GAUSSIAN_STD = 1/36
LUT_LENGTH = 256 # Look-up-table length, minimum of 256 because intensity levels are 8-bits (0 to 255) but can be more to avoid banding effect

# Computing T transformation
# input is an np.array object of the same size as input_texture (typically R/G/B channel of input_texture)
# the output object is also an np.array of the same size as input_texture
def T(input):
    t_input = np.zeros(input.shape, dtype=np.float32)

    sortedInputValues = []
    for y in range(len(input)):
        for x in range(len(input[0])):
            sortedInputValues.append((x, y, input[y][x]))
    sortedInputValues = sorted(sortedInputValues, key=lambda t:t[2]) # Sorting the list based on channel's color value

    for i in range(len(sortedInputValues)):
        x, y, _ = sortedInputValues[i]
        U = (i + 0.5)/len(sortedInputValues)
        G = stats.norm.ppf(U, loc=GAUSSIAN_AVERAGE, scale=GAUSSIAN_STD)
        t_input[y][x] = G
    
    return t_input

# Computing the inverse of T transformation
# input is an np.array object of the same size as input_texture (typically R/G/B channel of input_texture)
# the output object is also an np.array of size (LUT_LENGTH, 1)
def Tinv(input):
    LUT = np.zeros(LUT_LENGTH)

    sortedInputValues = []
    for y in range(len(input)):
        for x in range(len(input[0])):
            sortedInputValues.append(input[y][x])
    sortedInputValues = sorted(sortedInputValues) # Sorting the list based on channel's color value

    for i in range(LUT_LENGTH):
        G = (i + 0.5)/LUT_LENGTH # Creating gaussian variable z
        U = stats.norm.cdf(G, loc=GAUSSIAN_AVERAGE, scale=GAUSSIAN_STD)
        index = int(np.floor(U * len(sortedInputValues)))
        I = sortedInputValues[index]
        LUT[i] = I

    return LUT

def Tiling(uv):
    uv *= 3.464 # Factor 2*sqrt(3) for proper hexagonal tiling resizing

    gridToSkewedGrid = np.matrix([[1, -0.57735027], [0, 1.15470054]])
    skewedCoord = np.matmul(gridToSkewedGrid, uv)
    baseId = np.floor(skewedCoord)
    temp, _ = np.modf(skewedCoord)
    temp = temp.append(temp, 1 - temp[0] - temp[1])
    if temp[2] > 0:
        return temp[2], temp[1], temp[0], baseId, baseId + np.matrix([[0], [1]]), baseId + np.matrix([[1], [0]])
    else:
        return -temp[2], 1 - temp[1], 1 - temp[0], baseId + np.matrix([[1], [1]]), baseId + np.matrix([[1], [0]]), baseId + np.matrix([[0], [1]])


# Texture file must be named after 'texture.jpg' and must thus be a JPEG format
input_texture = Image.open("texture.jpg").convert('RGB')
input = np.array(input_texture)
channels = [input[:, :, i] for i in range(3)]

# From now we are working on each channel independantly
for c in channels: