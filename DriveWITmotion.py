import serial
import time
import struct
import sys
import numpy as np
#import rospy
#from tf.transformations import euler_from_quaternion, quaternion_from_euler
#from scipy.spatial.transform import Rotation
#602 4853530


class Witmotion:

	def initialize(self):
		self.cont_packet_data = 0
		self.Ser = serial.Serial('/dev/ttyUSB0', 115200)
		while True:
			if self.Ser.read(1) == b'\x55':
				if self.Ser.read(1) == b'\x61':  
					pp = self.Ser.read(18)
					break
		self.Ser.write(b'\xff\xaa\x03\x0b\x00')
		print(self.WitRead())
		time.sleep(0.5)
		self.Ser.write(b'\xff\xaa\x00\x00\x00')
		print(self.WitRead())
		time.sleep(0.5)

	def quaternion_from_euler(self,roll, pitch, yaw):
		qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
		qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
		qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
		qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

		return [qx, qy, qz, qw]

	#def WitRead(inputSer):#, flagbytes= b'\x55\x61'
	def WitRead(self):#, flagbytes= b'\x55\x61'
		inputSer = self.Ser
		PI = 3.141592654
		s = inputSer.read(20)
		#print(s[0],s[1],s[2],s)
		if s[0] == 85:#b'\x55'
			### Data Packet(Default) ###
			if s[1] == 97:#b'\x61'
				Data_Packet_Default = struct.unpack('<9H',s[2:])

				###  Acceleration  ###
				Ax = Data_Packet_Default[0]/32768 * 16 * 9.8
				Ay = Data_Packet_Default[1]/32768 * 16 * 9.8
				Az = Data_Packet_Default[2]/32768 * 16 * 9.8
				### Angular velocity ###
				Wx = Data_Packet_Default[3]/32768 * 2000
				Wy = Data_Packet_Default[4]/32768 * 2000
				Wz = Data_Packet_Default[5]/32768 * 2000
				### Angular Calculation ###
				Roll = Data_Packet_Default[6]/32768 * (PI)# (X axis)
				Pitch = Data_Packet_Default[7]/32768 * (PI)# (Y axis)
				Yaw = Data_Packet_Default[8]/32768  * (PI)# (Z axis)
				quat = self.quaternion_from_euler (Roll, Pitch, Yaw)
				#print('Ax',Ax,'\n','Ay',Ay,'\n','Az',Az)
				#print('Wx',Wx,'\n','Wy',Wy,'\n','Wz',Wz)
				#print('Roll',Roll*180/PI,'\n','Pitch',Pitch*180/PI,'\n','Yaw',Yaw*180/PI,'\n')
				return [Ax, Ay, Az], [Wx, Wy, Wz], [quat[0], quat[1], quat[2], quat[3]]
				
			'''			
			### Single Return Register Data Packet ###
			elif s[1] == 113:#b'\x71'
				
				#Single return data packet needs to send register instruction first:
				#				FF AA 27 XX 00
				#--XX is register number. The register number please refer to 6.3. Example as below:
				#			____________________________________________
				#				Function		|	  Instruction
				#			____________________|_______________________
				#			Read Magnetic Field |     FF AA 27 3A 00
				#			____________________|_______________________
				#			Read Quaternion     |     FF AA 27 51 00
				#			____________________|_______________________
				#			Read Temperature    |     FF AA 27 40 00
				#			____________________|_______________________
				
				### Read Magnetic Field ###
				if s[2] == 58:#b'\x3a':
					print('entro Magnetic Field')
					Data_Magnetic_field = struct.unpack('<3H',s[4:10])
					Hx = Data_Magnetic_field[0]#Magnetic field (X axis)
					Hy = Data_Magnetic_field[1]#Magnetic field (Y axis)
					Hz = Data_Magnetic_field[2]#Magnetic field (Z axis)
					return [Hx, Hy, Hz]
					
				### Read Quaternion ###
				elif s[2] == 81:#b'\x51':
					print('entro quaternion')
					Data_Quaternion = struct.unpack('<4H',s[4:12])
					Q0 = Data_Quaternion[0]/32768
					Q1 = Data_Quaternion[1]/32768
					Q2 = Data_Quaternion[2]/32768
					Q3 = Data_Quaternion[3]/32768
					return [Q0, Q1, Q2, Q3]
					
				### Read Temperature ###
				elif s[2] == 64:#b'\x40':
					print('entro Temperature')
					Data_Temperature = struct.unpack('<H',s[4:6])
					Temp = Data_Temperature[0]/100
					return [Temp]
				else:
					print('no se que sucedio',s)
					return 'sos'
			'''


if __name__ == '__main__':
	imu = Witmotion()
	imu.initialize()
	while True:
		m9a, m9w, m9q = imu.WitRead()

	'''
	cont_packet_data = 0
	with serial.Serial('/dev/ttyUSB0', 115200) as Ser:
		Ser.write(b'\xff\xaa\x03\x0b\x00')
		print(WitRead(Ser))
		Ser.write(b'\xff\xaa\x00\x00\x00')
		print(WitRead(Ser))
		#time.sleep(2)
		star_time = time.time()
		print('star_time',star_time)	
		while True:
			pp = []
			new_time = time.time()
			cont_packet_data += 1
			PPP = WitRead(Ser)

			
			#if pp == 'sos':
			#	break
			
			#if (new_time - star_time) >= 1:
			#	Ser.write(b'\xff\xaa\x27\x3a\x00')
			#	print(WitRead(Ser))
			#	Ser.write(b'\xff\xaa\x27\x51\x00')
			#	print(WitRead(Ser))
			#	Ser.write(b'\xff\xaa\x27\x40\x00')
			#	print(WitRead(Ser))
			#	star_time = time.time()	
			#	print('cont_packet_data',cont_packet_data)
			#	cont_packet_data = 0
			#	break
			
	'''