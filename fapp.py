
import RPI.GPIO as GPIO
from time import sleep
from flask import Flask, render_template, Response, request
from camera import VideoCamera
import time
import threading
import os

pi_camera = VideoCamera(flip=False) # flip pi camera 


app = Flask(__name__)

def SetElbowAngle(angle): #control the servo angle 
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.OUT)
        pwm=GPIO.PWM(7,50)
        pwm.start(0)
        
        duty = angle / 18 + 2
        
        GPIO.output(7, True)
        pwm.ChangeDutyCycle(duty)
        sleep(2)
        GPIO.output(7,False)
        pwm.ChangeDutyCycle(0)
        
        

        
        

@app.route('/')
def index():
    return render_template('index.html') 
    
    


def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False)
    


pwm.stop()
GPIO.cleanup()
GPIO.setwarnings(False)