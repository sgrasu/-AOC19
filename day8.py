
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

np.set_printoptions(linewidth=100)
f = open("day8_in","r")
line = list(map(int,list(f.readline().strip())))
num_layers = len(line) // 6 // 25
arr = np.array(line)
image = np.resize(arr,(num_layers,6, 25))
zero_count = np.sum(np.where(image == 0, 1, 0), (1,2))
least_zeros = min(image, key = lambda layer: np.sum(layer == 0))
print(np.sum(least_zeros == 1) * np.sum(least_zeros == 2))
secret = np.zeros((6, 25))
for y in range(6):
    for x in range(25):
        for l in range(num_layers):
            if image[l, y, x] == 2:
                continue
            secret[y, x] = image[l, y, x] 
            break

plt.imshow(secret, cmap="gray")
#plt.show()
decoded = image[0]
for layer in image:
    decoded = np.where(decoded == 2, layer, decoded)
decoded = np.where(decoded == 1, '⬜',' ')
for line in decoded:
    print(*line, sep = '')