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

# Takes uv 2-dimensionnal vector as input (coordinates on the 3D to-be-textured-surface)
# Returns w1, w2, w3, vertex1, vertex2, vertex3 (wi are the barycentric coordinates, vertexes are the triangles ends)
def Tiling(uv):
    uv = np.array(uv, dtype=np.float32)
    uv *= 3.464 # Factor 2*sqrt(3) for proper hexagonal tiling resizing

    gridToSkewedGrid = np.array([[1, -0.57735027], [0, 1.15470054]])
    skewedCoord = gridToSkewedGrid @ uv
    baseId = np.floor(skewedCoord).astype(int)
    temp_val = skewedCoord - np.floor(skewedCoord)
    
    x_frac = temp_val[0]
    y_frac = temp_val[1]
    z_frac = 1.0 - x_frac - y_frac
    if z_frac > 0:
        v1 = baseId
        v2 = baseId + np.array([0, 1])
        v3 = baseId + np.array([1, 0])
        return z_frac, y_frac, x_frac, v1, v2, v3
    else:
        v1 = baseId + np.array([1, 1])
        v2 = baseId + np.array([1, 0])
        v3 = baseId + np.array([0, 1])
        return -z_frac, 1.0 - y_frac, 1.0 - x_frac, v1, v2, v3

# Texture file must be named after 'texture.jpg' and must thus be a JPEG format
input_texture = Image.open("texture.jpg").convert('RGB')
input = np.array(input_texture)
channels = [input[:, :, i] for i in range(3)]

# From now we are working on each channel independantly
for c in channels: