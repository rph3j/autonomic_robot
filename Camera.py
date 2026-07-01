import cv2
from picamera2 import Picamera2, Preview
from libcamera import Transform
from datetime import datetime

# camera inicjalization
camera = Picamera2()
preview_config = camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (640,480)})
preview_config["transform"] = Transform(hflip=1, vflip=1)

camera.configure(preview_config)
camera.start()

# Function generating frame to video streaming
def generate_frame():
    while True:
        frame = camera.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# Function capturing IMG and saving in indicated document
def capture_file(file_name = ''):
    if len(file_name) == 0:
        data = datetime.now()
        ts = data.timestamp()
        file_name = "test_img_"+str(ts)+".jpg"
    camera.capture_file(file_name)

#Function capturing one frame to procesing
def getIMG():
    frame = camera.capture_array()
    return frame