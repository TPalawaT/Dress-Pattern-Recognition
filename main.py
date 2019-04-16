import urllib.request
import pandas as pd
import os
from download import Download
from extract import Extract
import joblib
import cv2
import numpy as np
from sklearn.tree import DecisionTreeClassifier

os.chdir('F:\\Tushar\\Pyhton Scripts\\Dress Pattern')

df = pd.read_csv('dress_patterns.csv', usecols=[1,3])

#This code to check if we need to download images
folder = os.listdir(os.getcwd())
if len(folder) == 0:
	Download(df)
if len(folder) == 17:
	pass
else:
	print("Delete all folders in images/ and try again")

os.chdir('F:\\Tushar\\Pyhton Scripts\\Dress Pattern')

#This will be our lables and also the values the names of direcorty where images are stored
datafolder = ['ikat', 'plain', 'polka dot', 'geometry', 'floral', 'squares', 'scales',
 'animal', 'OTHER', 'stripes', 'tribal', 'houndstooth', 'cartoon', 'chevron',
 'stars', 'letter_numb', 'skull']

x =[]  #Stores Images
y = []	#Stores lables
height = [] #Stores height of image
width = []	#Stores width of image


#The first if statement means that we have extracted the features from images and also saved them.
#This will save time in future when we need to computer features
#This was done for when I was testng the code. Now, it does not serve much purpose since we already have a
#model to predict values

if os.path.exists('edited_images'):
	os.chdir('edited_images')

	filename = [os.listdir(f) for f in datafolder]
	file_dict = dict(zip(datafolder, filename))

	for data_key, file_list in file_dict.items():
		for filename in file_list:
			loc = str(data_key) + '\\' + str(filename)
			print(loc)
			img = cv2.imread(loc)

			h,w,c = img.shape
			height.append(h)
			width.append(w)

			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

			x.append(img)
			y.append(data_key)
	os.chdir('..')

else:
	os.chdir('images')
	filename = [os.listdir(f) for f in datafolder]
	file_dict = dict(zip(datafolder, filename))
	os.chdir('..')

	for data_key, file_list in file_dict.items():
		for filename in file_list:
			loc = 'images\\' + str(data_key) + '\\' + str(filename)
			#This is the function in extract.py
			img = Extract(loc)

			#If we can't extract features from image, we discard that image
			if img.any() != False:
				alpha = 1 #Value to increase contrast in our images
				beta = 0 #Value to change brightness in image

				h, w, c = img.shape
				height.append(h)
				width.append(w)

				#Traversing over BGR to set contrast
				for b in range(img.shape[0]):
					for g in range(img.shape[1]):
						for r in range(img.shape[2]):
							img[b,g,r] = np.clip(alpha*img[b,g,r] + beta, 0, 255)

				img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

				#To save the edit images
				if not os.path.exists('edited_images'):
					os.mkdir('edited_images')
				os.chdir('edited_images')

				#Data key is made a directory and it further stores the images
				if not os.path.exists(data_key):
					os.mkdir(data_key)
				os.chdir(data_key)

				cv2.imwrite(filename, img)
				#This takes is back to our main directory where the directory images/ is stored
				os.chdir('..\\..')
				print(os.getcwd())

				#img.resize((256, 140))
				x.append(img)
				y.append(data_key)


#Code from line 119 to 141 is written to make all images of equal size
#Images will be cropped to the size of minimum sized image in the dataset
min_h = min(height)
min_w = min(width)

for i in range(len(x)):
	h_im, w_im = x[i].shape
	
	#The difference between the minimum sized and the particular image
	#The image will be cropped from all sides and that's why we divide it by 2
	h_diff = int((h_im - min_h)/2)
	w_diff = int((w_im - min_w)/2)

	h_initial = 0 + h_diff 	#Top portion of image
	w_initial = 0 + w_diff 	#Bottom portion of image
	h_final = h_im-h_diff 	#Left portion of image
	w_final = w_im-w_diff 	#Right portion of image

	#After the computations are done, height of images come out either as 241 or 242 and the width is either 121 or 122
	if (h_final - h_initial) != min_h:
		h_final = h_final - 1
	if (w_final - w_initial) != min_w:
		w_final = w_final - 1

	#Image is cropped here
	x[i] = x[i][h_initial : h_final, w_initial : w_final]
	img_h, img_w = x[i].shape
	print(img_h, img_w)

#To make the array 2d
size = len(x)
x = np.array(x)
x = x.reshape(size,-1)

values = str(min_h)+' '+str(min_w)

#We need these minimum values to predict values using saved model
f = open('min_value.txt', 'w+')
f.write(values)
f.close()

clf = DecisionTreeClassifier(min_samples_split=9).fit(x, y)

joblib.dump(clf, 'classifier.sav')
print("File created")

print("Now you can use the predict.py file to see predcitions for image of your choice")