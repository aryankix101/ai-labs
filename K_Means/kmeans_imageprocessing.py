import urllib.request
import io
from PIL import Image
from random import randint
import sys
import time

URL = sys.argv[1]
f = io.BytesIO(urllib.request.urlopen(URL).read()) # Download the picture at the url as a file object
img = Image.open(f) # You can also use this on a local file; just put the local filename in quotes in place of f.
#img.show() # Send the image to your OS to be displayed as a temporary file
#print(img.size) # A tuple. Note: width first THEN height. PIL goes [x, y] with y counting from the top of the frame.
pix = img.load() # Pix is a pixel manipulation object; we can assign pixel values and img will change as we do so.
#print(pix[2,5]) # Access the color at a specific location; note [x, y] NOT [row, column].
#pix[2,5] = (255, 255, 255) # Set the pixel to white. Note this is called on “pix”, but it modifies “img”.
#img.show() # Now, you should see a single white pixel near the upper left corner
#img.save("my_image.png") # Save the resulting image. Alter your filename as necessary.

K = int(sys.argv[2])
dimensions = img.size

#27-color naïve quantization
"""for x in range(dimensions[0]):
    for y in range(dimensions[1]):
        pix_tuple = pix[x,y]
        temp_list = []
        for rgb_value in pix_tuple:
            if rgb_value<(255//3):
                temp_list.append(0)
            elif rgb_value>((255*2)//3):
                temp_list.append(255)
            else:
                temp_list.append(127)
        pix[x,y] = tuple(temp_list)
img.show()
img.save("27-color_naive.png")

#8-color naive quantization
for x in range(dimensions[0]):
    for y in range(dimensions[1]):
        pix_tuple = pix[x,y]
        temp_list = []
        for rgb_value in pix_tuple:
            if rgb_value<128:
                temp_list.append(0)
            elif rgb_value>=128:
                temp_list.append(255)
        pix[x,y] = tuple(temp_list)
img.show()
img.save("8-color_naive.png")"""

#K-color kmeans
start1 = time.perf_counter()
means = []
for i in range(0, K):
    x, y = randint(0, dimensions[0]), randint(0, dimensions[1])
    means.append(pix[x, y])

pixel_means = [[] for _ in range(K)]
all_means = []
all_means.append(means.copy())

dict_of_pixels = dict()
for i in range(dimensions[0]):
    for j in range(dimensions[1]):
        if pix[i, j] in dict_of_pixels.keys():
            dict_of_pixels[pix[i, j]].append((i, j))
        else:
            dict_of_pixels[pix[i, j]] = [(i, j)]
for k, v in dict_of_pixels.items():
    dict_of_pixels[k] = len(v)
i=0
while True:
    #print(i, means)
    #i+=1
    #Loop through all pixels, find which means it's closest to, place accordingly
    start = time.perf_counter()
    for key, value in dict_of_pixels.items():
        list_of_squared_errors = []
        for mean in means:
            list_of_squared_errors.append(((key[0]-mean[0])**2)+((key[1]-mean[1])**2)+((key[2]-mean[2])**2))
        index = means.index(means[list_of_squared_errors.index(min(list_of_squared_errors))])
        pixel_means[index].append((key, value))
    means.clear()
    #Find average of all groups, make that the new means values
    for pixel_mean in pixel_means:
        t_0_sum, t_1_sum, t_2_sum = 0, 0, 0
        length = 0
        for x in pixel_mean:
            key, values = x[0], x[1]
            length+=values
            t_0_sum+=values*key[0]
            t_1_sum+=values*key[1]
            t_2_sum+=values*key[2]
        updated_means_value = ((t_0_sum/length), (t_1_sum/length), (t_2_sum/length))
        means.append(updated_means_value)
    #Check if means are stable (no mean changes value)
    if means==all_means[-1]:
        break
    else:
        all_means.append(means.copy())
    pixel_means.clear()
    pixel_means = [[] for _ in range(K)]
k_specific_means = all_means[-1]
for x in range(dimensions[0]):
    for y in range(dimensions[1]):
        pix_tuple = pix[x,y]
        list_of_squared_errors = []
        for mean in k_specific_means:
            list_of_squared_errors.append(((pix_tuple[0]-mean[0])**2)+((pix_tuple[1]-mean[1])**2)+((pix_tuple[2]-mean[2])**2))
        updated_pix_unrounded = k_specific_means[list_of_squared_errors.index(min(list_of_squared_errors))]
        t2 = (round(updated_pix_unrounded[0]), round(updated_pix_unrounded[1]), round(updated_pix_unrounded[2]))
        pix[x,y] = t2
#img.show()
img.save("kmeansout.png")