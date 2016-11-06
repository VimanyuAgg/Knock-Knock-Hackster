import argparse
import base64
import time
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from PIL import Image
from PIL import ImageDraw
from selenium import webdriver
import json
import os
import json
import numpy as np


from pprint import pprint

import math


def get_vision_service():
    credentials = GoogleCredentials.get_application_default()
    return discovery.build('vision', 'v1', credentials=credentials)



def detect_face(face_file, max_results,output_filename):
    image_content = face_file.read()
    batch_request = [{
        'image': {
            'content': base64.b64encode(image_content).decode('utf-8')
            },
        'features': [{
            'type': 'FACE_DETECTION',
            'maxResults': max_results,
            }]
        }]

    service = get_vision_service()
    request = service.images().annotate(body={
        'requests': batch_request,
        })
    response = request.execute()

    print response
    json_str = json.dumps(response)
    data = json.loads(json_str)
    file_name='live_datasets/'+output_filename[:13]+'.json'
    #file_name='json_datasets/sparsh_family/live_feed30.json'

    with open(file_name, 'w+') as f:
        json.dump(data, f)

    return response['responses'][0]['faceAnnotations']


def highlight_faces(image, faces, output_filename):
    im = Image.open(image)
    draw = ImageDraw.Draw(im)

    for face in faces:
        box = [(v.get('x', 0.0), v.get('y', 0.0))
               for v in face['fdBoundingPoly']['vertices']]
        draw.line(box + [box[0]], width=5, fill='#00ff00')

    im.save(output_filename)


def main(input_filename, output_filename, max_results):

    with open(input_filename, 'rb') as image:
 
        faces = detect_face(image, max_results, output_filename)
        print('Found {} face{}'.format(
            len(faces), '' if len(faces) == 1 else 's'))

        output_addr="output-images/"+output_filename

        print('Writing to file {}'.format(output_addr))
        # Reset the file pointer, so we can read the file again
        image.seek(0)
        highlight_faces(image, faces, output_addr)


def lineCalc(x1,y1,z1,x2,y2,z2):
	return math.sqrt((float(x2)-float(x1))**2+(float(y2)-float(y1))**2+(float(z2)-float(z1))**2)

def delAB(upper,lower):
	return upper-lower


def diff():
	for each in range(2,len(jsonstats['sparsh'])-1):
		abs(jsonstats['sparsh'][each] - jsonstats['sparsh2'][each])



Facejson = {}

def facefoldertraversal():
	for eachpersonname in os.listdir(os.getcwd()+"/json_datasets"):
		if str(eachpersonname).startswith('.'):
			continue
		Facejson[eachpersonname]=[]
		for eachjson in os.listdir(os.getcwd()+"/json_datasets/"+eachpersonname):
			with open(os.getcwd()+"/json_datasets/"+eachpersonname+"/"+eachjson) as jsonfile:
				fullobj = json.load(jsonfile)
			try:
				reqobject = fullobj['responses'][0]['faceAnnotations'][0]['landmarks']
				Facejson[eachpersonname].append(jsonarrayval(reqobject))
			except Exception, e:
				print "Error in JSON"
		
			

def facefoldertraveltest():
	for eachpersonname in os.listdir(os.getcwd()+"/json_datasets"):
		print eachpersonname


def jsonarrayval(jsonobject):
	jsoncalcuated = []
	for i in range(0,len(jsonobject)-1):
		x = lineCalc(jsonobject[i]['position']['x'],jsonobject[i]['position']['y'],jsonobject[i]['position']['z'],jsonobject[i+1]['position']['x'],jsonobject[i+1]['position']['y'],jsonobject[i+1]['position']['z'])
		jsoncalcuated.append(x)
	return jsoncalcuated




#print("len  " + str(len(jsonstats['sparsh'])))

if __name__ == '__main__':
	facefoldertraversal()
	driver = webdriver.Firefox()
	driver.get('http://ssjsparsh.local:8080/')
	driver.maximize_window()
	time.sleep(1) # delays for 5 seconds
	driver.save_screenshot('captured-images/captured-from-door-1.png')
	driver.save_screenshot('captured-images/captured-from-door-2.png')
	# driver.save_screenshot('captured-from-door-3.png')
	# driver.save_screenshot('captured-from-door-4.png')
	# #driver.save_screenshot('captured-from-door-5.png')
	driver.quit()
	main('captured-images/captured-from-door-1.png', 'output_face_1.jpg', 4)
	main('captured-images/captured-from-door-2.png', 'output_face_2.jpg', 4)
	data=[]
	with open("live_Datasets/output_face_1.json") as data_file:
		json_data = json.load(data_file)
		#print json_data
		data = json_data['responses'][0]['faceAnnotations'][0]['landmarks']
		#print data
	

	with open("live_Datasets/output_face_2.json") as data_file:
		json_data = json.load(data_file)
		#print json_data
		data1 = json_data['responses'][0]['faceAnnotations'][0]['landmarks']
		#print data1
	livedataarrays = []
	livedataarrays.append(jsonarrayval(data))
	livedataarrays.append(jsonarrayval(data1))
	resultcounter = {}
	matchcounterlist={}
	for eachlivearray in livedataarrays:
		for eachstoredarraylistkey in Facejson:
			resultcounter[eachstoredarraylistkey] = 0
			matchcounterlist[eachstoredarraylistkey] = []
			for eachstoredarray in Facejson[eachstoredarraylistkey]:
				counter =0
				lenoflist  = len(eachstoredarray)
				for i in range(0,lenoflist-1):
					if abs(delAB(eachstoredarray[i],eachlivearray[i]))<20:
						counter+=1
				matchcounterlist[eachstoredarraylistkey].append([float(counter)/float(lenoflist)])
	print matchcounterlist

	for key in matchcounterlist:
		print key
		print np.mean(matchcounterlist[key])




