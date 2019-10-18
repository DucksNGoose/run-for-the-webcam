import cv2
import base64
import webbrowser
import requests
import json
import datetime
import sys
# Windows dependencies
# - Python 2.7.6: http://www.python.org/download/
# - OpenCV: http://opencv.org/
# - Numpy -- get numpy from here because the official builds don't support x64:
#   http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy

# Mac Dependencies
# - brew install python
# - pip install numpy
# - brew tap homebrew/science
# - brew install opencv

def is_http_status_ok(status_code):
    return status_code == 200

def send_json(body):
    apiUrl = "https://run-ford-future-fiap.herokuapp.com/api/v1/images"
    r = requests.post(apiUrl, json=body)
    if is_http_status_ok(r.status_code):
        print('image sended')
    else:
        print('error to send image [{}]'.format(r.status_code))

def get_requests():
    apiUrl = "https://run-ford-future-fiap.herokuapp.com/api/v1/requests"
    r = requests.get(apiUrl)
    if is_http_status_ok(r.status_code):
        return r.json()['data']
    else:
        return []

def delete_request(id):
    apiUrl = 'https://run-ford-future-fiap.herokuapp.com/api/v1/requests/{}'.format(id)
    print(apiUrl)
    r = requests.delete(apiUrl)
    if is_http_status_ok(r.status_code):
        print('request {} already deleted!'.format(id))
    else:
        print('error to delete request [{}]'.format(r.status_code))
    
def take_photo():
    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
    face_cascade.load('./haarcascade_frontalface_default.xml')
    formatBase64 = 'data:image/png;base64,'
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)    
    rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

    print('analysing image')
    faces = face_cascade.detectMultiScale(gray,1.3, 5)
    print(len(faces))
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    out = cv2.imwrite('capture.jpg', cv2.medianBlur(frame, 3))

    with open("capture.jpg", "rb") as image:
        encoded_string = base64.b64encode(image.read()).decode()
        send_json({'img_name': '{}'.format(datetime.datetime.now()), 'base64_img': '{}{}'.format(formatBase64, encoded_string) })

while(True):
    try:
        for request in get_requests():
            if request['is_processed'] == False:
                take_photo()
                print(request['id'])
                delete_request(request['id'])
    except (KeyboardInterrupt, SystemExit):
        print('cam verify stopped')
        sys.exit()