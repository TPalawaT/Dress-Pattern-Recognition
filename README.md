# Dress-Pattern-Recognition
Takes an image of a dress predicts the pattern of the dress

## Overview
main.py file does the initial hardwork by downloading the data and preprocessibg the data.</br>
extract.py is used to extarct features from the image dataset.</br>
download.py downloads the images using urllib.</br>
After the model is one training, we can simply type in location of an image to predict the dress pattern.</br>

## Requirements
Active internet connection on first run of main.py</br>
OpenCV - Version 3.4.2</br>
Numpy - Version 0.24.1</br>
Sklearn - Version 0.20.1</br>
Urllib.request - Version 3.6</br>
Other requirements are usually satisfied with the python package.</br>

## Working
The model first reads the column 'category' and the column containing url from dress_pattern.csv. Then, the model downloads the data using downlod.py.</br>
download.py has a function Download() which takes dataframe as an argument. In this case, it is the dataframe containing the category and url. 150 images for each class are downloaded. This ensures that all the classes are of same number.</br>
After the data is downloaded, the images are extracted from the file extract.py which is called by main.py.</br>
extract.py has a function Extract() which takes path of the image as argument to load that using OpenCV and then goes on to finding part of image enclosed within the contour. If the features of the image can't be extracted, the image is discarded and it won' be used in training dataset.</br>
The image is returned to main.py to do further computations.</br>
After all the images are extracted, all images are then croppped to the minimum sized image.</br>
After that, the images are then classified using Decision Tree Classifier and the resulting model is then saved.</br></br>
The saved model can be used by predict.py to for classification of one image.

## How to use predcit.py
This file can only be predicted after main.py has run and save the model as classifier.sav</br>
When the above condition is saisfied, run the code. It'll first ask for location of the file to classify.</br>
Loading classifier and doing it's own computation, it predicts the pattern on the dress.</br>
It also shows four similar images that match the pattern of our dress.</br>
To close the images that open up, press '0' on the keyboard.

###### Thanks for reading</br>TPT
