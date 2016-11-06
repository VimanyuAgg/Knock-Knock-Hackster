import argparse
import base64
import time
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from PIL import Image
from PIL import ImageDraw
from selenium import webdriver


def get_vision_service():
    credentials = GoogleCredentials.get_application_default()
    return discovery.build('vision', 'v1', credentials=credentials)

import json



def detect_face(face_file, max_results=4):
    """Uses the Vision API to detect faces in the given file.

    Args:
        face_file: A file-like object containing an image with faces.

    Returns:
        An array of dicts with information about the faces in the picture.
    """
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
    with open('family_sparsh_live.json', 'w') as f:
        json.dump(data, f)

    return response['responses'][0]['faceAnnotations']





def highlight_faces(image, faces, output_filename):
    """Draws a polygon around the faces, then saves to output_filename.

    Args:
      image: a file containing the image with the faces.
      faces: a list of faces found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the
          faces have polygons drawn around them.
    """
    im = Image.open(image)
    draw = ImageDraw.Draw(im)

    for face in faces:
        box = [(v.get('x', 0.0), v.get('y', 0.0))
               for v in face['fdBoundingPoly']['vertices']]
        draw.line(box + [box[0]], width=5, fill='#00ff00')

    im.save(output_filename)


def main(input_filename, output_filename, max_results):

    with open(input_filename, 'rb') as image:
        print "I am in"
        faces = detect_face(image, max_results)
        print('Found {} face{}'.format(
            len(faces), '' if len(faces) == 1 else 's'))

        print('Writing to file {}'.format(output_filename))
        # Reset the file pointer, so we can read the file again
        image.seek(0)
        highlight_faces(image, faces, output_filename)



import json


if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get('http://ssjsparsh.local:8080/')
    driver.maximize_window()
    time.sleep(2) # delays for 5 seconds
    driver.save_screenshot('captured-from-door.png')
    driver.quit()

    main('captured-from-door.png', 'output_face.jpg', 4)


    # parser = argparse.ArgumentParser(
    #     description='Detects faces in the given image.')
    # parser.add_argument(
    #     'input_image', dest='captured-from-door.png',help='the image you\'d like to detect faces in.')
    

    # parser.add_argument(
    #     '--out', dest='output', default='out.jpg',
    #     help='the name of the output file.')
    # parser.add_argument(
    #     '--max-results', dest='max_results', default=4,
    #     help='the max results of face detection.')
    # args = parser.parse_args()
    
        
    
    #main(args.input_image, args.output, args.max_results)

    




