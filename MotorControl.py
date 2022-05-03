#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import RPi.GPIO as GPIO
from time import sleep

LeftMotorPin=12
RightMotorPin=13
EnLeft=5
EnRight=6

GPIO.setmode(GPIO.BCM)
GPIO.setup(LeftMotorPin,GPIO.OUT)
GPIO.setup(EnLeft,GPIO.OUT)
GPIO.setup(RightMotorPin,GPIO.OUT)
GPIO.setup(EnRight,GPIO.OUT)

GPIO.output(EnLeft,GPIO.LOW)
GPIO.output(EnRight,GPIO.LOW)

l=GPIO.PWM(LeftMotorPin,10)
r=GPIO.PWM(RightMotorPin,10)

r.start(0)
l.start(0)

global GoingforwardSpeed

def Forward():
	rospy.init_node('motor', anonymous=True)
	pub=rospy.Publisher('motor',String,queue_size=10)
	rate=rospy.Rate(10)
	run='running! %s' %rospy.get_time()
	pub.publish(run)
	rospy.loginfo(run)
	Goingforward='Going Forward'
	rospy.loginfo(Goingforward)
	GoingforwardSpeed=input('Enter Motor speed 0 to 100 percent')
	rospy.loginfo(GoingforwardSpeed)
	# Response=input()
	while not rospy.is_shutdown():
		PWM_Percent=int(GoingforwardSpeed)
		r.ChangeDutyCycle(PWM_Percent)
		l.ChangeDutyCycle(PWM_Percent)
		GPIO.output(EnLeft,GPIO.HIGH)
		GPIO.output(EnRight,GPIO.HIGH)
		rate.sleep()
		direction= input('Enter the direction')
		if direction=='w':
			Forward()
		elif direction=='s':
			Backward()
		elif direction=='a':
			Left()
		elif direction=='d':
			Right()		
def Backward():
	rospy.init_node('motor', anonymous=True)
	pub=rospy.Publisher('motor',String,queue_size=10)
	rate=rospy.Rate(10)
	run='running! %s' %rospy.get_time()
	pub.publish(run)
	rospy.loginfo(run)
	Goingforward='Going Backward'
	rospy.loginfo(Goingforward)
	GoingforwardSpeed=input('Enter Motor speed 0 to 100 percent')
	rospy.loginfo(GoingforwardSpeed)
	# Response=input()
	while not rospy.is_shutdown():
		PWM_Percent=int(GoingforwardSpeed)
		r.ChangeDutyCycle(PWM_Percent)
		l.ChangeDutyCycle(PWM_Percent)
		GPIO.output(EnLeft,GPIO.LOW)
		GPIO.output(EnRight,GPIO.LOW)
		rate.sleep()

		direction= input('Enter the direction')
		if direction=='w':
			Forward()
		elif direction=='s':
			Backward()
		elif direction=='a':
			Left()
		elif direction=='d':
			Right()		
def Left():
	rospy.init_node('motor', anonymous=True)
	pub=rospy.Publisher('motor',String,queue_size=10)
	rate=rospy.Rate(10)
	run='running! %s' %rospy.get_time()
	pub.publish(run)
	rospy.loginfo(run)
	Goingforward='Going Left'
	rospy.loginfo(Goingforward)
	GoingforwardSpeed=input('Enter Motor speed 0 to 100 percent')
	rospy.loginfo(GoingforwardSpeed)
	# Response=input()
	while not rospy.is_shutdown():
		PWM_Percent=int(GoingforwardSpeed)
		r.ChangeDutyCycle(PWM_Percent)
		l.ChangeDutyCycle(0.75*PWM_Percent)
		GPIO.output(EnLeft,GPIO.HIGH)
		GPIO.output(EnRight,GPIO.HIGH)
		rate.sleep()
		direction= input('Enter the direction')
		if direction=='w':
			Forward()
		elif direction=='s':
			Backward()
		elif direction=='a':
			Left()
		elif direction=='d':
			Right()		
def Right():
	rospy.init_node('motor', anonymous=True)
	pub=rospy.Publisher('motor',String,queue_size=10)
	rate=rospy.Rate(10)
	run='running! %s' %rospy.get_time()
	pub.publish(run)
	rospy.loginfo(run)
	Goingforward='Going Right'
	rospy.loginfo(Goingforward)
	GoingforwardSpeed=input('Enter Motor speed 0 to 100 percent')
	rospy.loginfo(GoingforwardSpeed)
	# Response=input()
	while not rospy.is_shutdown():
		PWM_Percent=int(GoingforwardSpeed)
		r.ChangeDutyCycle(0.75*PWM_Percent)
		l.ChangeDutyCycle(PWM_Percent)
		GPIO.output(EnLeft,GPIO.HIGH)
		GPIO.output(EnRight,GPIO.HIGH)
		rate.sleep()
		direction= input('Enter the direction')
		if direction=='w':
			Forward()
		elif direction=='s':
			Backward()
		elif direction=='a':
			Left()
		elif direction=='d':
			Right()			


if __name__ == '__main__':

		
	try:
		direction= input('Enter the direction')
		if direction=='w':
			Forward()
		elif direction=='s':
			Backward()
		elif direction=='a':
			Left()
		elif direction=='d':
			Right()
	except rospy.ROSInterruptException:
		pass

	finally:
		GPIO.cleanup()		


		
