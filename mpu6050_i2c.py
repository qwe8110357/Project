#!/usr/bin/env python3


# MPU6050 9-DoF Example Printout
import rospy
from mpu9250_i2c import *
from time import sleep
from std_msgs.msg import String

rospy.init_node('IMU', anonymous=True)
pub=rospy.Publisher('IMUData',String,queue_size=10)
rate=rospy.Rate(10)

time.sleep(1) # delay necessary to allow mpu9250 to settle


  

print('recording data')
while not rospy.is_shutdown():
    try:
        ax,ay,az,wx,wy,wz = mpu6050_conv() # read and convert mpu6050 data
        #mx,my,mz = AK8963_conv() # read and convert AK8963 magnetometer data
    except rospy.ROSInterruptException:
        pass

    print('{}'.format('-'*30)) 
    print('accel [g]: x = {0:2.2f}, y = {1:2.2f}, z = {2:2.2f} '.format(ax,ay,az))
    print('gyro [degree/s]:  x = {0:2.2f}, y = {1:2.2f}, z = {2:2.2f}'.format(wx,wy,wz))
    #print('mag [uT]:   x = {0:2.2f}, y = {1:2.2f}, z = {2:2.2f}'.format(mx,my,mz))
    print('{}'.format('-'*30))
    time.sleep(1)  
    ACCEL=('accel [g]: x = {0:2.2f}, y = {1:2.2f}, z = {2:2.2f}'.format(ax,ay,az))
    GYRO=('gyro [degree/s]:  x = {0:2.2f}, y = {1:2.2f}, z = {2:2.2f}'.format(wx,wy,wz))
    #MAG=('mag [uT]:   x = {0:2.2f}, y = {1:2.2f}, z = {2:2.2f}'.format(mx,my,mz))
    pub.publish(ACCEL)
    pub.publish(GYRO)
    #pub.publish(MAG)
