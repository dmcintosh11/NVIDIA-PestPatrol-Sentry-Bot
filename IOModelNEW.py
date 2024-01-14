#python filename.py

import Jetson.GPIO as GPIO
import jetson.inference
import jetson.utils
from botActions import botActions
import time

#Handles setting up camera and model link
net = jetson.inference.detectNet(model='/home/dylan/Desktop/jetson-inference/python/training/detection/ssd/models/raccoon2/ssd-mobilenet.onnx', labels='/home/dylan/Desktop/jetson-inference/python/training/detection/ssd/models/raccoon2/labels.txt', input_blob='input_0', output_cvg='scores', output_bbox='boxes', threshold=0.8)
camera = jetson.utils.gstCamera(1280, 720, '/dev/video0')
# display = jetson.utils.glDisplay()

bot = botActions(motor_pin=32)

#Loops infinitely while the GUI is open
# while display.IsOpen():
try:
    while True:
        #Handles inference processing
        img, width, height = camera.CaptureRGBA()
        detections = net.Detect(img, width, height)
        # display.RenderOnce(img, width, height)
        # display.SetTitle("Object Detection | Network {:.0f} FPS".format(net.GeetNetworkFPS()))

        if detections:
            print('Raccoon Detected!!!')
            if not bot.is_shooting():
                print('Starting shooting')
                bot.threaded_shoot_racoon(duration=0.7)
        #classIDs = [detection.ClassID for detection in detections]
        #print(classIDs)


        #print()
        #print('Length of detections: ' + str(len(detections)))
        #print(f'First index of detections: {detections[0].ClassID}')
        
        #Checks if there is a racoon to shoot
    #if 'racoon' in detections and not bot.is_shooting(): #Probably needs to parrse detections better
    #   bot.threaded_shoot_racoon()
except KeyboardInterrupt:
    print('Program interrupted')
finally:
    print('Cleanup starting...')
    bot.clean()
    del bot
    print('Cleanup finished!')