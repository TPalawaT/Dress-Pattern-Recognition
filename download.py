import os
import urllib.request

def Download(df):
	#This function is used to download images from the internet
	#Due to data limit, only 150 images were allowed
	#Unintentionally, it also limited made all classes of almost equal sizes since many classes don't even have 20 images
	os.chdir('F:\\Tushar\\Pyhton Scripts\\Dress Pattern')

	if not os.path.exists('images'):
		os.mkdir('images')
	os.chdir('images')
	#os.chdir('..')

	x = 0
	downloaded = [] #To include the class which fulfiled it's limit of 150 images in it
	for i in df.itertuples():
		x = x+1
		print(x)

		#If a class does not have 150 images, then only will further downloads be available
		if i[1] not in downloaded:
			if not os.path.exists(i[1]):
				os.mkdir(i[1])
			os.chdir(i[1])

			file = str(x) + '.png'
			urllib.request.urlretrieve(i[2], file)

			files = os.listdir(os.getcwd())
			if len(files)>=150:
				downloaded.append(i[1])

			os.chdir('..')