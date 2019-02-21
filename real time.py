import cv2
import numpy.core.multiarray
import numpy as np
import time
import http.client as httplib
import json

## Function to call custom vision in containers
def callCustomVision(frame,cameraWidth,cameraHeight):
    ## deploy your container image and update your endpoint below
    conn = httplib.HTTPConnection('127.0.0.1:8000')
    imencoded = cv2.imencode('.jpg',frame)[1]
    headers = {'Content-type': 'application/octet-stream'}
    conn.request("POST","/image",imencoded.tostring(),headers)
    response = conn.getresponse()
    resjson = json.load(response)
    for predict in resjson['predictions']:
        ## only process probability > 80%
        if predict['probability'] > 0.8:
            x = int(predict['boundingBox']['left'] * cameraWidth)
            y = int(predict['boundingBox']['top'] * cameraHeight)
            w = int(predict['boundingBox']['width'] * cameraWidth)
            h = int(predict['boundingBox']['height'] * cameraHeight)
            ## draw bounding box and text
            cv2.rectangle(frame,(x,y),(x + w, y + h), (0,255,0), 2)
            cv2.putText(frame,predict['tagName'],(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA)
    return frame

## define video source
cap = cv2.VideoCapture(0)

if not(cap.isOpened()):
    cap.open()

## while camera is open
while(cap.isOpened()):
    ret, frame = cap.read()
    cameraWidth = cap.get(3)
    cameraHeight = cap.get(4)
    ## process original frame using custom vision and return frame2
    frame2 = callCustomVision(frame,cameraWidth,cameraHeight)
    cv2.imshow('frame', frame2)
    time.sleep(0.1)
    ## press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

## release camera stream
cap.release()
cv2.destroyAllWindows()