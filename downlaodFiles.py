import cv2
import base64
import numpy as np
import os
import requests

os.chdir('/home/g00g1y5p4/AP094/yolov5_final/tes/')

def downloadFiles():
	 l = requests.get('http://104.211.217.182:5000/checkFiles')
	 dataList = l.json()['list']
	 getList = os.listdir()
	 for i in dataList:
	 	if i not in getList:
	 		data = requests.post('http://104.211.217.182:5000/downloadFiles',json={'image':i})
	 		de = base64.b64decode(data.content)
	 		nparr = np.fromstring(de,np.uint8)
	 		img = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
	 		cv2.imwrite(i,img)
	 		
downloadFiles()
