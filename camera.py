from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import cv2

record_time = 15

camera_resolution = [640,480]
camera_framerate = 20

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
video = cv2.VideoWriter('monitor.avi', fourcc, camera_framerate, tuple(camera_resolution))

camera = PiCamera()
camera.resolution = tuple(camera_resolution)
camera.framerate = camera_framerate
rawCapture = PiRGBArray(camera, size=tuple(camera_resolution))

start_time = time.time()

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    video.write(image)
    #clear stream for next frame
    rawCapture.truncate(0)

    if time.time() - start_time > record_time:
        break

video.release()