import joblib
from extract import Extract
from numpy import clip
import cv2
from numpy import array
import os
import random

loc = input('Enter path of image: ')

model = joblib.load('classifier.sav')

#This function is present in extract.py for preprocessing on images
img = Extract(loc)

if img.any() == False:
	print("Image can't be processed. Try Another")
	exit(0)

#For setting contrast in images
alpha = 1
beta = 0
for b in range(img.shape[0]):
	for g in range(img.shape[1]):
		for r in range(img.shape[2]):
			img[b,g,r] = clip(alpha*img[b,g,r] + beta, 0, 255)

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

h_im, w_im = img.shape

#To read the minimum size of image in training dataset to crop the particular image to that size.
#We would only be able to predict using joblib if this image is of the size of the size of each image in our dataset
f = open('min_value.txt', 'r')
min_h, min_w = f.read().split()
min_h = int(min_h)
min_w = int(min_w)
f.close()

#Code from line 41 to 57 is used to crop images
h_im, w_im = img.shape

h_diff = int((h_im - min_h)/2)
w_diff = int((w_im - min_w)/2)

h_initial = 0 + h_diff
w_initial = 0 + w_diff
h_final = h_im-h_diff
w_final = w_im-w_diff

if (h_final - h_initial) != min_h:
	h_final = h_final - 1
if (w_final - w_initial) != min_w:
	w_final = w_final - 1

#print(h_final, h_initial)
img = img[h_initial : h_final, w_initial : w_final]

#To convert the array into a shape that resembles our training dataset
img = array([img])
img = img.reshape(1,-1)

pred = model.predict(img)


#Code from 67 to 82 used to show similar images to the particular pattern
new_path = 'images\\' + str(pred[0])
os.chdir(new_path)

filename = os.listdir(os.getcwd())

print("The dress pattern is",pred[0])

i = 0
similar_img = []
while i<4:
	file = random.choice(filename)
	filename.remove(file)
	title = "Similar Image " + str(i+1)
	similar_img.append(cv2.imread(file))
	cv2.imshow(title, similar_img[i])
	i = i+1

original_img = cv2.imread(loc)
cv2.imshow('Original Image', original_img)
cv2.waitKey(0)
cv2.destroyAllWindows()