import cv2
from numpy import mean
from numpy import array

def Extract(path):
	#This function is used to read an image from the path provided and return only the dresss in the image
	print(path)
	img = cv2.imread(path)
	img = cv2.bilateralFilter(img, 9, 50, 50)

	#We use minval and maxval as the parameter in canny edge detection
	m = mean(img)
	minval = 0.66*m
	maxval = 1.33*m
	edged = cv2.Canny(img, minval, maxval)

	#The next two lines are used to find the contours in an image.
	#In this code, we want to find the part of image enclosed in red rectangle
	ret,thresh = cv2.threshold(edged,127,255,0)
	im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	height, width, channel = img.shape

	#The images dataset we have is very noisy and has multiple contours and to only get red box, we use the below code.
	x_list = [] #Stores x value of a contour i.e the top left point
	y_list = []	#Stores y value of the contour
	h_list = []	#Stores height of a contour
	w_list = [] #Stores width of a contour
	h_ratio_list = []	#Stores the value of height of contour divided by total height of image
	w_ratio_list = []	#Stores the value of width of contour divided by total height of image

	'''
	The below code is explained here.
	The image is very noisy and there are multiple contours forming.
	To only get just the one contour, I did this.
	After doing multiple computations and seeing what height, width of a contour gives us the image bounded by rectangle and
	storing it in a variable. I made a list of all the associated height of contour, it's width and the height and
	width of image.
	Dividing each h_contour and w_contour by image height, width gave us the mean values 0.47 and 0.27 for height 
	and width respectively with a standard deviation of 0.3 for both of them
	Since, 95% data falls within two standard deviation, I decided to that h_ratio should lie between 0.40 and 0.60.
	Width ratio between 0.30 and 0.50.
	All other contours will be rejected.
	Now, if there are multiple contours even in this range, we choose the value which is the closest to the the mean
	height_ratio which is listed below. 
	'''


	for c in contours:
		x,y,w,h = cv2.boundingRect(c)

		h_ratio = h/height
		w_ratio = w/width

		if h_ratio>0.40 and h_ratio<0.60 and w_ratio>0.30 and w_ratio<0.50:
			#x = x+1
			x_list.append(x)
			y_list.append(y)
			h_list.append(h)
			w_list.append(w)
			h_ratio_list.append(h_ratio)
			w_ratio_list.append(w_ratio)
			new_img = img[y:y+h,x:x+w]


	'''
		if len(h_list)>1:
			h_list = [x-0.4978503375378032 for m in h_list]
			h_list = [abs(x) for m in h_list]
	'''

	#Multiple contours even within the range
	if len(h_ratio_list)>1:
		h_ratio_list = [m - 0.4978503375378032 for m in h_ratio_list]
		h_ratio_list = [abs(m) for m in h_ratio_list]
		min_loc = h_ratio_list.index(min(h_ratio_list))
		new_x = x_list[min_loc]
		new_y = y_list[min_loc]
		new_h = h_list[min_loc]
		new_w = w_list[min_loc]

		new_img = img[new_y:new_y+new_h, new_x:new_x+new_w]

	#Only one contour in the range, so we select this
	elif len(h_ratio_list) == 1:
		new_x = x_list[0]
		new_y = y_list[0]
		new_h = h_list[0]
		new_w = w_list[0]

		new_img = img[new_y:new_y+new_h, new_x:new_x+new_w]

	else:
		#If there is no contour within this range, we reject this image
		new_img = [False]
		new_img = array(new_img)

	return new_img