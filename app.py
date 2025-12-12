import numpy as np
import scipy.stats as stats
from PIL import Image
import matplotlib.pyplot as plt

# Texture file must be named after 'texture.jpg' and must thus be a JPEG format
input_texture = Image.open("texture.jpg").convert('RGB')
width, height = input_texture.size
input_r, input_g, input_b = input_texture.split()
