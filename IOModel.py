#python filename.py

import Jetson.GPIO as GPIO
import jetson.inference
import jetson.utils
import botActions


#Handles setting up camera and model link
net = jetson.inference.detectNet('ssd-mobilenet-v2', threshold=0.5)
camera = jetson.utils.gstCamera(1280, 720, '/dev/video0')
display = jetson.utils.glDisplay()

bot = botActions(motor_pin=20)

#Loops infinitely while the GUI is open
while display.IsOpen():
    
    #Handles inference processing
    img, width, height = camera.CaptureRGBA()
    detections = net.Detect(img, width, height)
    display.RenderOnce(img, width, height)
    display.SetTitle("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
    
    
    
    #Checks if there is a racoon to shoot
    if 'racoon' in detections and not bot.is_shooting(): #Probably needs to parse detections better
        bot.threaded_shoot_racoon()
    
bot.clean()
del bot