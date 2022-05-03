#!/usr/bin/env python3
import rospy
import numpy as np 
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
import RPi.GPIO as GPIO
import time
import math
import statistics

radius = 0.040  # m
gearRatio = 74.83
statesPerRotation = 48
cpro = 0.25 * gearRatio * statesPerRotation
micro = 6.00e6
circum= 2*math.pi*radius

GPIO.setmode(GPIO.BCM)

#####Left Side Encoders######

RightYellow = 26
RightWhite = 20

GPIO.setup(RightYellow, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RightWhite, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#####Right Side Encoder######

#############################

 # direction designated for the left encoder

def speed_calc():
    t=0
    countl=0

    tic=time.perf_counter()
    for i in range(190000):
        if GPIO.event_detected(RightYellow):
            countl=countl+1

        else:
            pass
  
        i=i+1
    toc=time.perf_counter()    
    t=toc-tic    
    relv=countl/1812.75
    rps=relv/t
    vel=rps*circum          
    return vel
def Speed_dir():
    td=0
    counter=0
    
    ALastState=GPIO.input(RightYellow)  
    j=0
    for j in range(190000):
        AState=GPIO.input(RightYellow)
        BState=GPIO.input(RightWhite)
        if AState !=ALastState:
            if BState!=AState:
                counter-=1
            else:
                counter+=1
        if counter<0:
            counter=-1
        elif counter>0:
            counter=1
        else:        
            counter=0
        ALastState=AState   
  
        j=j+1
    d=counter          
    return d       

if __name__ == '__main__':
    
    rospy.init_node('right_encoder_count', anonymous=True)
    pub = rospy.Publisher('right_encoder', Float32, queue_size=10)   
    rate=rospy.Rate(10)
    GPIO.add_event_detect(RightYellow,GPIO.BOTH)  
    try:

        #GPIO.wait_for_edge(LeftYellow,GPIO.BOTH)
        
        while not rospy.is_shutdown():         
            Speed=[]
            while np.size(Speed)<10:
                V=speed_calc()
                Speed.append(V)
            AverageSpeed=statistics.mean(Speed)
            d=Speed_dir()
            AverageSpeed=AverageSpeed*d            
            pub.publish(AverageSpeed)
            
            print(AverageSpeed)
            


    except rospy.ROSInterruptException:
        pass

    finally:
        GPIO.cleanup()



