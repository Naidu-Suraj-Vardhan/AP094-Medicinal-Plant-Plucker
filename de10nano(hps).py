import cv2

import os

import time

import json

import subprocess

import requests

import numpy as np

import sys

#pin assignment
 
#1804 - Motor 1 forward
#1805 - Motor 1 backward
#1806 - Motor 2 forward
#1807 - Motor 2 backward
#1808 - signal to arduino-Tx
#1809 - signal from arduino-Rx



#plant detection model using haar cascade
plant_cascade=cv2.CascadeClassifier('CASCADE.xml')


#distance from camera to plant measured in Centimeter
Known_distance = 60

#width of plant in real world or object plane in centimeter
Known_width = 22


#fonts
fonts = cv2.FONT_HERSHEY_COMPLEX

#focal length finder function
def Focal_Length_Finder(measured_distance,real_width,width_in_rf_image):

	focal_length = (width_in_rf_image*measured_distance)/real_width

	return focal_length

#distace estimation function
def Distance_finder(Focal_length,real_plant_width,plant_width_in_frame):

	distance = (real_plant_width*Focal_length)/plant_width_in_frame

	return distance

def plant_data(image):

	plant_width = 0

	plants = plant_cascade.detectMultiScale(image,1.3,5)

	for (x,y,h,w) in plants:

		plant_width = w

	return plant_width

ref_image = cv2.imread('Ref_img')#reference image

ref_image_plant_width = plant_data(ref_image)#find the width of reference image

Focal_length_found = Focal_Length_Finder(Known_distance, Known_width, ref_image_plant_width)#gets focal length


#To Record Camera Vision

filename = 'Vision.avi'

fps = 30.0

res = '480'

def change_res(cap, width, height):

    cap.set(3, width)

    cap.set(4, height)

STD_DIMENSIONS =  {

    "480p": (640, 480),

    "720p": (1280, 720),

    "1080p": (1920, 1080),

    "4k": (3840, 2160),
}

def get_dims(cap, res='1080p'):

    width, height = STD_DIMENSIONS["480p"]

    if res in STD_DIMENSIONS:

        width,height = STD_DIMENSIONS[res]

    change_res(cap, width, height)

    return width, height

VIDEO_TYPE = {

    'avi': cv2.VideoWriter_fourcc(*'XVID'),

    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def get_video_type(filename):

    filename, ext = os.path.splitext(filename)

    if ext in VIDEO_TYPE:

      return  VIDEO_TYPE[ext]

    return VIDEO_TYPE['avi']


def read():  #read recieving signal from arduino and act accordingly

	#subprocess.Popen("echo 1809 > /sys/class/gpio/export" ,shell=True,stdout=subprocess.PIPE)

	#subprocess.Popen("echo in > /sys/class/gpio/gpio1809/direction" ,shell=True,stdout=subprocess.PIPE)

	s= subprocess.Popen("cat /sys/class/gpio/gpio1809/value",shell=True,stdout=subprocess.PIPE)

	v=s.stdout.read()

	return int(float(v))



def cloud():   #send image to cloud from board for medicinal plant detection

	cv2.imwrite('image_1.jpg',image)

	url = 'http://104.211.217.182:5000/upload'    #cloud server url

	files = {'image': open("image_1.jpg", 'rb')}

	response = requests.post(url, files=files)

	if response.json()['output']== 1:
		
		return 1
		
		print("Detected Plant is Medicinal")       #if the plant is medicinal the de10 sends signal to arduino giving instruction to pluck
		
		subprocess.Popen("echo 1 > /sys/class/gpio/gpio1808/value",shell=True,stdout=subprocess.PIPE)
	else:
		
		return 0

		print("Detected Plant is not Medicinal")     #if the plant is not medicinal the de10nano acts and moves to next plant

		subprocess.Popen("echo 0 > /sys/class/gpio/gpio1808/value",shell=True,stdout=subprocess.PIPE)



def forward(): #bot control for forward direction

	subprocess.Popen("echo 1 > /sys/class/gpio/gpio1804/value",shell=True,stdout=subprocess.PIPE)

	subprocess.Popen("echo 0 > /sys/class/gpio/gpio1805/value",shell=True,stdout=subprocess.PIPE)

	subprocess.Popen("echo 1 > /sys/class/gpio/gpio1806/value",shell=True,stdout=subprocess.PIPE)

	subprocess.Popen("echo 0 > /sys/class/gpio/gpio1807/value",shell=True,stdout=subprocess.PIPE)

	delay()



def backward():  #bot control for backward direction

	subprocess.Popen("echo 0 > /sys/class/gpio/gpio1804/value",shell=True,stdout=subprocess.PIPE)

	subprocess.Popen("echo 1 > /sys/class/gpio/gpio1805/value",shell=True,stdout=subprocess.PIPE)

	subprocess.Popen("echo 0 > /sys/class/gpio/gpio1806/value",shell=True,stdout=subprocess.PIPE)

	subprocess.Popen("echo 1 > /sys/class/gpio/gpio1807/value",shell=True,stdout=subprocess.PIPE)

	delay()



def right():  #bot control for turning right

	subprocess.Popen("echo 0 > /sys/class/gpio/gpio1804/value",shell=True,stdout=subprocess.PIPE)

	subprocess.Popen("echo 1 > /sys/class/gpio/gpio1805/value",shell=True,stdout=subprocess.PIPE)

	subprocess.Popen("echo 1 > /sys/class/gpio/gpio1806/value",shell=True,stdout=subprocess.PIPE)

	subprocess.Popen("echo 0 > /sys/class/gpio/gpio1807/value",shell=True,stdout=subprocess.PIPE)

	delay()	




def left():  #bot control for turning left

	subprocess.Popen("echo 1 > /sys/class/gpio/gpio1804/value",shell=True,stdout=subprocess.PIPE)

	subprocess.Popen("echo 0 > /sys/class/gpio/gpio1805/value",shell=True,stdout=subprocess.PIPE)

	subprocess.Popen("echo 0 > /sys/class/gpio/gpio1806/value",shell=True,stdout=subprocess.PIPE)

	subprocess.Popen("echo 1 > /sys/class/gpio/gpio1807/value",shell=True,stdout=subprocess.PIPE)

	delay()




def stop():  #bot control to stop

	subprocess.Popen("echo 0 > /sys/class/gpio/gpio1804/value",shell=True,stdout=subprocess.PIPE)

	subprocess.Popen("echo 0 > /sys/class/gpio/gpio1805/value",shell=True,stdout=subprocess.PIPE)

	subprocess.Popen("echo 0 > /sys/class/gpio/gpio1806/value",shell=True,stdout=subprocess.PIPE)

	subprocess.Popen("echo 0 > /sys/class/gpio/gpio1807/value",shell=True,stdout=subprocess.PIPE)
	

	cloud()

	res = cloud()

	if res==0:

		left()

	else:

		while True:
			print("Medicinal plant is Plucking")
			a = read()

			if a==1:

				break

	right()

	delay()


def delay():

	time.sleep(1)	



#accessing GPIO pins of the de10nano 
subprocess.Popen("echo 1804 > /sys/class/gpio/export" ,shell=True,stdout=subprocess.PIPE)

subprocess.Popen("echo out > /sys/class/gpio/gpio1804/direction" ,shell=True,stdout=subprocess.PIPE)


subprocess.Popen("echo 1805 > /sys/class/gpio/export" ,shell=True,stdout=subprocess.PIPE)

subprocess.Popen("echo out > /sys/class/gpio/gpio1805/direction" ,shell=True,stdout=subprocess.PIPE)


subprocess.Popen("echo 1806 > /sys/class/gpio/export" ,shell=True,stdout=subprocess.PIPE)

subprocess.Popen("echo out > /sys/class/gpio/gpio1806/direction" ,shell=True,stdout=subprocess.PIPE)


subprocess.Popen("echo 1807 > /sys/class/gpio/export" ,shell=True,stdout=subprocess.PIPE)

subprocess.Popen("echo out > /sys/class/gpio/gpio1807/direction" ,shell=True,stdout=subprocess.PIPE)


subprocess.Popen("echo 1808 > /sys/class/gpio/export" ,shell=True,stdout=subprocess.PIPE)

subprocess.Popen("echo out > /sys/class/gpio/gpio1808/direction" ,shell=True,stdout=subprocess.PIPE)

subprocess.Popen("echo 1809 > /sys/class/gpio/export" ,shell=True,stdout=subprocess.PIPE)

subprocess.Popen("echo in > /sys/class/gpio/gpio1809/direction" ,shell=True,stdout=subprocess.PIPE)





#turn on camera for processing

cap=cv2.VideoCapture(0)

out = cv2.VideoWriter(filename,get_video_type(filename),25, get_dims(cap,res))

while cap.isOpened():

	_,image=cap.read()

	plant_width_in_frame = plant_data(image)
	
	if plant_width_in_frame!=0:

		Distance = Distance_finder(Focal_length_found, Known_width, plant_width_in_frame)

		gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

		plants=plant_cascade.detectMultiScale(gray,scaleFactor=7.5,minNeighbors=15,minSize=(60,120),flags=cv2.CASCADE_SCALE_IMAGE)

		tup=(0,0,0,0)

		for (x,y,w,h) in plants:

			cv2.rectangle(image,(x,y),(x+w,y+h),(230,255,0),3)
		
			cv2.putText(image,'Plant',(x,y),fonts,1,(0,0,255),1,cv2.LINE_AA)

			cv2.putText(image,f"Distance:{round(Distance,2)}CM",(x+20,y+25),fonts,1,(0,0,255),1)
		
			tup=(x,y,w,h)

		cx=(tup[0]+(tup[0]+tup[2]))/2

		cy=(tup[1]+(tup[1]+tup[3]))/2

		width  = cap.get(3)

		height = cap.get(4)

		framecx=(width)/2

		framecy=(height)

		frheight=260

		frwidth=140

		topx = (int(framecx) - (frwidth) / 2)

		topy = (int(framecy) - (frheight) / 2)

		botx = (int(framecx) + (frwidth / 2))

		boty = (int(framecy) + (frheight) / 2)

		cv2.circle(image, (int(framecx),int(framecy)), 7, (0, 255, 255), -1)

		cv2.rectangle(image, (int(topx), int(topy)), (int(botx), int(boty)), (230, 255, 255), 3)

		centercy=int(cy)

		cv2.circle(image,(int(cx),int(cy)), 7, (0, 0, 255), -1)

		cv2.line(image,(0,int(framecy)),(int(width),int(framecy)),(0,255,0),2)

		cv2.line(image, (int(framecx), int(height)), (int(framecx), 0), (0, 255, 0), 2)

		out.write(image) #camera vision recording VideoWrite

		cv2.imshow('output',image) #displaying camera vision

		if (topy<cy<(topy+frheight)):

			if(topx<cx<(topx+frwidth)):

				stop()

		elif (0<cx<topx):

			left()

			delay()

			print("Move left")

		elif (botx<cx<width):

			right()

			delay()

			print("Move right")

		elif (topx<cx<botx) and (0<cy<topy):

			forward()

			delay()

			print(" Move forward")

		elif (topx<cx<botx) and (boty<cy<height):

			backward()

			delay()

			print("Move Backward")

		else:

			left()
		
			delay()

			print("No Plant is Detected")

	if cv2.waitKey(1) & 0xFF==ord('q'):

		break


#unexporting GPIO pins

subprocess.Popen("echo 1804 > /sys/class/gpio/unexport" ,shell=True,stdout=subprocess.PIPE)

subprocess.Popen("echo 1805 > /sys/class/gpio/unexport" ,shell=True,stdout=subprocess.PIPE)

subprocess.Popen("echo 1806 > /sys/class/gpio/unexport" ,shell=True,stdout=subprocess.PIPE)

subprocess.Popen("echo 1807 > /sys/class/gpio/unexport" ,shell=True,stdout=subprocess.PIPE)

subprocess.Popen("echo 1808 > /sys/class/gpio/unexport" ,shell=True,stdout=subprocess.PIPE)

subprocess.Popen("echo 1809 > /sys/class/gpio/unexport" ,shell=True,stdout=subprocess.PIPE)

cap.release()
out.release()
cv2.destroyAllWindows()