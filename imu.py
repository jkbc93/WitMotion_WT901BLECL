import serial
import time
import struct
import spidev
import time
import rospy
import math
import numpy as np
from time import time
#from MPU9250 import MPU9250
from sensor_msgs.msg import Imu
from DriveWITmotion import Witmotion

def talker():
	pub = rospy.Publisher('imu/data_raw', Imu, queue_size=10)
	rospy.init_node('ros_erle_imu', anonymous=True)
	rate = rospy.Rate(200)

	imu = Witmotion()
	imu.initialize()

	msg = Imu()

	while not rospy.is_shutdown():

		#imu.read_acc()
		
		msg.header.stamp = rospy.get_rostime()
		msg.header.frame_id = 'imu_link'

		m9a, m9g, m9q = imu.WitRead()


		#----------update IMU
		ax = m9a[0]
		ay = m9a[1]
		az = m9a[2]
		gx = m9g[0]
		gy = m9g[1]
		gz = m9g[2]
		q0 = m9q[3] #W
		q1 = m9q[0] #X
		q2 = m9q[1] #Y
		q3 = m9q[2] #Z

		
		#Fill message
		msg.orientation.x = q1
		msg.orientation.y = q2
		msg.orientation.z = q3
		msg.orientation.w = q0
		msg.orientation_covariance[0] = q1 * q1
		msg.orientation_covariance[0] = q2 * q2
		msg.orientation_covariance[0] = q3 * q3		

		msg.angular_velocity.x = m9g[0]
		msg.angular_velocity.y = m9g[1]
		msg.angular_velocity.z = m9g[2]
		msg.angular_velocity_covariance[0] = m9g[0] * m9g[0]
		msg.angular_velocity_covariance[4] = m9g[1] * m9g[1]
		msg.angular_velocity_covariance[8] = m9g[2] * m9g[2]
		
		msg.linear_acceleration.x = m9a[0]
		msg.linear_acceleration.y = m9a[1]
		msg.linear_acceleration.z = m9a[2]
		msg.linear_acceleration_covariance[0] = m9a[0] * m9a[0]
		msg.linear_acceleration_covariance[4] = m9a[1] * m9a[1]
		msg.linear_acceleration_covariance[8] = m9a[2] * m9a[2]
		
		pub.publish(msg)

		rate.sleep()

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass