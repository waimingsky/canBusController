from ctypes import wintypes
import ctypes
from ctypes import *
import types_define
import numpy as np
from datetime import datetime
import time
import thread

class CANalyser():


	def __init__(self):
	
		try:
			self.cansdk = windll.LoadLibrary('ControlCAN.dll')
			print "load DLL success"
		except Exception as e:
			print"ERROR:Exception in load ControlCan.dll",e
			
		self.deviceType = 4
		self.deviceIndex = 0
		self.canIndex = 0
		
		self.struInitConfig = types_define._INIT_CONFIG()
		self.struInitConfig.AccCode = 0x80000008
		self.struInitConfig.AccMask = 0xFFFFFFFF
		self.struInitConfig.Filter = 1
		self.struInitConfig.Timing0 = 0x01
		self.struInitConfig.Timing1 = 0x1c
		self.struInitConfig.Mode = 0
		
		self.cansdk.VCI_Receive.argtypes = [wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, POINTER(types_define._VCI_CAN_OBJ),c_ulong, c_int32]
			
	def OpenDevice(self):
		
		self.cansdk.VCI_OpenDevice.argtypes = [wintypes.DWORD, wintypes.DWORD, wintypes.DWORD]
		if self.cansdk.VCI_OpenDevice(self.deviceType, self.deviceIndex, 0) == 1:
			print 'Device opened'
		else:
			print 'Device open ERROR'
			
	def CloseDevice(self):
	
		self.cansdk.VCI_CloseDevice.argtypes = [wintypes.DWORD, wintypes.DWORD]
		if self.cansdk.VCI_CloseDevice(self.deviceType, self.deviceIndex) == 1:
			print 'Device closed'
		else:
			print 'Device close ERROR'
			
	def InitDevice(self):
	
		try:
			self.cansdk.VCI_InitCAN.argtypes = [wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, POINTER(types_define._INIT_CONFIG)]
			if self.cansdk.VCI_InitCAN(self.deviceType, self.deviceIndex, self.canIndex, self.struInitConfig) == 1:
				print 'Device init success'
			else:
				print 'Device init fail'
		except  Exception as e:
			print e
			
	def StartCAN(self):
	
		try:
			self.cansdk.VCI_StartCAN.argtypes = [wintypes.DWORD, wintypes.DWORD, wintypes.DWORD]
			if self.cansdk.VCI_StartCAN(self.deviceType, self.deviceIndex, self.canIndex) == 1:
				print 'CAN start success'
				
			else:
				print 'CAN fail to start'
		except Exception as e:
			print e
			
	def ResetCAN(self):
	
		try:
			self.cansdk.VCI_ResetCAN.argtypes = [wintypes.DWORD, wintypes.DWORD, wintypes.DWORD]
			if self.cansdk.VCI_ResetCAN(self.deviceType, self.deviceIndex, self.canIndex) == 1:
				print 'CAN reset success'
			else:
				print 'CAN fail to reset'
		except Exception as e:
			print e
		
	def Transmit(self, InputData):
	
		sendData = types_define._VCI_CAN_OBJ()
		sendData.ID = 0xDA
		sendData.RemoteFlag = 0
		sendData.ExternFlag = 0
		sendData.DataLen = 8 # max is 8 (<=8)
		sendData.Data = InputData #(0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x47)
		
		try:
			self.cansdk.VCI_Transmit.argtypes = [wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, POINTER(types_define._VCI_CAN_OBJ),wintypes.DWORD]
			if self.cansdk.VCI_Transmit(self.deviceType, self.deviceIndex, self.canIndex, sendData, 1) == -1:
				print 'Transmit data fail'
			else:
				print 'Transmit data success'
		except Exception as e:
			print e
			
	def Receive(self):
		
		while(1):
		
			receiveData = types_define._VCI_CAN_OBJ*2500
			receiveDataList = receiveData()
			Message ="Received Message:"
			time.sleep(0.1)
			
			try:
				len = self.cansdk.VCI_Receive(self.deviceType, self.deviceIndex, self.canIndex, receiveDataList, 2500, 200)
				if len <=0:
					pass
					#print 'Received Empty Message'
				else:
					for i in range (len):
						if receiveDataList[i].RemoteFlag == 0:
							ID = receiveDataList[i].ID
							if receiveDataList[i].DataLen > 8:
								receiveDataList[i].DataLen = 8
							for j in range (receiveDataList[i].DataLen):
								Message+= chr(receiveDataList[i].Data[j])
							
							print "ID:", hex(ID) ," ", Message
					
				#ime.sleep(0.1)
					#break
				
				
			except Exception as e:
				print "exception:", e
				break
			
			
		
			
		
			
			
if __name__ == '__main__':
	canControl = CANalyser()
	canControl.OpenDevice()
	canControl.InitDevice()
	canControl.StartCAN()
	#thread.start_new_thread(canControl.Receive(), ())
	canControl.Transmit((0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x47))
	time.sleep(0.1)
	canControl.ResetCAN()
	canControl.CloseDevice()