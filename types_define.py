import ctypes
from ctypes import *
import enum
from ctypes import wintypes


class _VCI_BOARD_INFO(Structure):
	_fields_ =[
			   ('hw_Version', c_ushort),
			   ('fw_Version', c_ushort),
			   ('dr_Version', c_ushort),
			   ('in_Version', c_ushort),
			   ('irq_Num', c_ushort),
			   ('can_Num', c_byte),
			   ('str_Serial_Num', c_char*20),
			   ('str_hw_Type', c_char*40),
			   ('Reserved', c_ushort*4)
			   ]
			   
class _VCI_CAN_OBJ(Structure):
	_fields_ =[
			   ('ID', c_uint),
			   ('TimeStamp', c_uint),
			   ('TimeFlag', c_byte),
			   ('SendType', c_byte),
			   ('RemoteFlag', c_byte),
			   ('ExternFlag', c_byte),
			   ('DataLen', c_byte),
			   ('Data', c_byte*8),
			   ('Reserved', c_byte*3)
			   ]
			   
class _VCI_CAN_STATUS(Structure):
	_fields_ =[
			   ('ErrInterrupt', c_byte),
			   ('regMode', c_byte),
			   ('regStatus', c_byte),
			   ('regALCapture', c_byte),
			   ('regECCapture', c_byte),
			   ('regEWLimit', c_byte),
			   ('regRECounter', c_byte),
			   ('regTECounter', c_byte),
			   ('Reserved', c_uint)
			   ]

class _ERR_INFO(Structure):
	_fields_ =[
			   ('ErrCode', c_uint),
			   ('Passive_ErrData', c_byte*3),
			   ('ArLost_ErrData', c_byte)
			   ]
			   
class _INIT_CONFIG(Structure):
	_fields_ =[
			   ('AccCode', c_uint32),
			   ('AccMask', c_uint32),
			   ('InitFlag', c_uint32),
			   ('Filter', c_byte),
			   ('Timing0', c_byte),
			   ('Timing1', c_byte),
			   ('Mode', c_byte)
			   ]
			   
LPVCI_OpenDevice = WINFUNCTYPE(wintypes.DWORD, wintypes.DWORD, wintypes.DWORD)
LPVCI_CloseDevice = WINFUNCTYPE(wintypes.DWORD, wintypes.DWORD)
LPVCI_InitCan = WINFUNCTYPE(wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, POINTER(_INIT_CONFIG))

LPVCI_ReadBoardInfo = WINFUNCTYPE(wintypes.DWORD, wintypes.DWORD, POINTER(_VCI_BOARD_INFO))
LPVCI_ReadErrInfo = WINFUNCTYPE(wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, POINTER(_ERR_INFO))
LPVCI_ReadCanStatus = WINFUNCTYPE(wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, POINTER(_VCI_CAN_STATUS))

LPVCI_GetReference = WINFUNCTYPE(wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, POINTER(wintypes.BYTE))
LPVCI_SetReference = WINFUNCTYPE(wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, POINTER(wintypes.BYTE))

LPVCI_GetReceiveNum = WINFUNCTYPE(wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD)
LPVCI_ClearBuffer = WINFUNCTYPE(wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD)

LPVCI_StartCAN = WINFUNCTYPE(wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD)
LPVCI_ResetCAN = WINFUNCTYPE(wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD)

LPVCI_Transmit = WINFUNCTYPE(wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, POINTER(_VCI_CAN_OBJ), c_ulong)
LPVCI_Receive = WINFUNCTYPE(wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, POINTER(_VCI_CAN_OBJ), c_ulong, c_int32)





