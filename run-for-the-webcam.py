import cv2
import base64
import webbrowser
import requests
import json
import datetime
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
def send_json(body):
    apiUrl = "https://run-ford-future-fiap.herokuapp.com/api/v1/images"
    r = requests.post(apiUrl, json=body)
    print(r.status_code)

cap = cv2.VideoCapture(0)
formatBase64 = 'data:image/png;base64,'
while(True):
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    cv2.imshow('frame', rgb)
    
    out = cv2.imwrite('capture.jpg', frame)
    
    with open("capture.jpg", "rb") as image:
        encoded_string = base64.b64encode(image.read()).decode()
        webbrowser.open('{}{}'.format(formatBase64, encoded_string))
        send_json({'img_name': '{}'.format(datetime.datetime.now()), 'base64_img': '{}{}'.format(formatBase64, encoded_string) })
    
    break
cap.release()
cv2.destroyAllWindows()