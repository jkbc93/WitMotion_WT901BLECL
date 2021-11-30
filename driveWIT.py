import serial
import time
import struct

cont_packet_data = 0

with serial.Serial('/dev/ttyUSB0', 115200) as Ser:
	star_time = time.time()
	print('star_time',star_time)	
	for data in range(5):
		new_time = time.time()
		s = Ser.read(20)
		#print(s)
		if s[0] == 85:#b'\x55'
			### Data Packet(Default) ###
			if s[1] == 97:#b'\x61'
				'''
				ax =[s[2],s[3]]#[axL,axH]
				ay =[s[4],s[5]]#[ayL,ayH]
				az =[s[6],s[7]]#[azL,azH]
				wx =[s[8],s[9]]#[wxL,wxH]
				wy =[s[10],s[11]]#[wyL,wyH]
				wz =[s[12],s[13]]#[wzL,wzH]
				roll =[s[14],s[15]]#[rollL,rollH]
				pitch =[s[16],s[17]]#[pitchL,pitchH]
				yaw =[s[18],s[19]]#[yawL,yawH]

				###  Acceleration  ###
				Ax = ((ax[1]<<8)|ax[0])/32768 * 16 * 9.8
				Ay = ((ay[1]<<8)|ay[0])/32768 * 16 * 9.8
				Az = ((az[1]<<8)|az[0])/32768 * 16 * 9.8
				
				### Angular velocity ###
				Wx = ((wx[1]<<8)|wx[0])/32768 * 2000
				Wy = ((wy[1]<<8)|wy[0])/32768 * 2000
				Wz = ((wz[1]<<8)|wz[0])/32768 * 2000

				### Angular Calculation ###
				Roll = ((roll[1]<<8)|roll[0])/32768 * 180# (X axis)
				Pitch = ((pitch[1]<<8)|pitch[0])/32768 * 180# (Y axis)
				Yaw = ((yaw[1]<<8)|yaw[0])/32768 * 180# (Z axis)
				print()
				print('forma de la documentacion')
				print('Ax',Ax,'\n','Ay',Ay,'\n','Az',Az)
				print('Wx',Wx,'\n','Wy',Wy,'\n','Wz',Wz)
				print('roll',Roll,'\n','Pitch',Pitch,'\n','Yaw',Yaw)
				'''
				Data_Packet_Default =struct.unpack('<9H',s[2:])

				###  Acceleration  ###
				Ax = Data_Packet_Default[0]/32768 * 16 * 9.8
				Ay = Data_Packet_Default[1]/32768 * 16 * 9.8
				Az = Data_Packet_Default[2]/32768 * 16 * 9.8
				### Angular velocity ###
				Wx = Data_Packet_Default[3]/32768 * 2000
				Wy = Data_Packet_Default[4]/32768 * 2000
				Wz = Data_Packet_Default[5]/32768 * 2000
				### Angular Calculation ###
				Roll = Data_Packet_Default[6]/32768 * 180# (X axis)
				Pitch = Data_Packet_Default[7]/32768 * 180# (Y axis)
				Yaw = Data_Packet_Default[8]/32768 * 180# (Z axis)
				print()				
				print('forma de little-endian')
				print('Ax',Ax,'\n','Ay',Ay,'\n','Az',Az)
				print('Wx',Wx,'\n','Wy',Wy,'\n','Wz',Wz)
				print('roll',Roll,'\n','Pitch',Pitch,'\n','Yaw',Yaw)
				
				cont_packet_data += 1
			
			### Single Return Register Data Packet ###
			elif s[1] == 113:#b'\x71'
				'''
				Single return data packet needs to send register instruction first:
								FF AA 27 XX 00
				--XX is register number. The register number please refer to 6.3. Example as below:
							____________________________________________
							    Function		|	  Instruction
							____________________|_______________________
							Read Magnetic Field |     FF AA 27 3A 00
							____________________|_______________________
							Read Quaternion     |     FF AA 27 51 00
							____________________|_______________________
							Read Temperature    |     FF AA 27 40 00
							____________________|_______________________
				'''
				### Read Magnetic Field ###
				if s[2] == 58:#b'\x3a':
					hx =[s[4],s[5]]#[axL,axH]
					hy =[s[6],s[7]]#[axL,axH]
					hz =[s[8],s[9]]#[axL,axH]
					
					Hx = ((hx[1]<<8)|hx[0])#Magnetic field (X axis)
					Hy = ((hy[1]<<8)|hy[0])#Magnetic field (Y axis)
					Hz = ((hz[1]<<8)|hz[0])#Magnetic field (Z axis)
				### Read Quaternion ###
				elif s[2] == 81:#b'\51':
					q0 =[s[4],s[5]]#[q0L,q0H]
					q1 =[s[6],s[7]]#[q1L,q1H]
					q2 =[s[8],s[9]]#[q2L,q2H]
					q3 =[s[8],s[9]]#[q3L,q3H]
					
					q0 = ((q0[1]<<8)|q0[0])/32768
					q1 = ((q1[1]<<8)|q1[0])/32768
					q2 = ((q2[1]<<8)|q2[0])/32768
					q3 = ((q3[1]<<8)|q3[0])/32768
					
				### Read Temperature ###
				elif s[2] == 64:#b'\40':
					None
				print('llego otro paquete')
				break
		if (new_time - star_time) >= 1.0:
			print('cont_packet_data',cont_packet_data)
			break

				

