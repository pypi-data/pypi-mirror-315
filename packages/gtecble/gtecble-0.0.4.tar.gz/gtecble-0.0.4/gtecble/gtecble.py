import platform
import ctypes
import os
from enum import Enum
import numpy as np
import struct
import sys

class System(Enum):
    Unknown = 1
    Windows = 2
    Linux = 3
    Mac = 4
    iOs = 5
    Android = 6

def get_system():
    systmp = System.Unknown
    system = platform.system()
    if system == 'Darwin':
        systmp = System.Mac
    elif system == 'Linux':
        systmp = System.Linux
        if hasattr(sys, 'getandroidapilevel') == True:
            systmp = System.Android
    elif system == 'Windows':
        systmp = System.Windows
    return systmp

if get_system() == System.Windows:
    platform_folder = 'windows'
    current_architecture = platform.architecture()[0]
    if current_architecture == '32bit':
       architecture_folder = 'Win32'
       library_name = 'libgtecble_Win32.dll'
    elif current_architecture == '64bit':
        architecture_folder = 'x64'
        library_name = 'libgtecble_x64.dll'
    else:
        raise OSError('\'' + str(get_system()) + '\' not supported')
elif get_system() == System.Linux:
    raise OSError('\'' + str(get_system()) + '\' not supported')
elif get_system() == System.Mac:
    platform_folder = 'mac'
    architecture_folder = platform.machine()
    library_name = 'libgtecble_' + platform.machine() +'.dylib'
    if architecture_folder != 'arm64' and architecture_folder != 'x86_64':
        raise OSError('\'' + str(get_system()) + '\' not supported')
elif get_system() == System.iOs:
    raise OSError('\'' + str(get_system()) + '\' not supported')
elif get_system() == System.Android:
    platform_folder = 'android'
    if platform.machine() == 'aarch64':
        architecture_folder = 'arm64-v8a'
        library_name = 'libgtecble_arm64-v8a.so'
    elif platform.machine() == 'armv7l':
        architecture_folder = 'armeabi-v7a'
        library_name = 'libgtecble_armeabi-v7a.so'
    else:
        raise OSError('\'' + str(get_system()) + '\' not supported')
else:
    raise OSError('\'' + str(get_system()) + '\' not supported')

library_path = os.path.join(os.path.dirname(__file__), 'native', platform_folder, architecture_folder, library_name)
lib = ctypes.CDLL(library_path)

GTECBLE_HANDLE = ctypes.c_uint64
GTECBLE_STRING_LENGTH_MAX  = 255
GTECBLE_DEVICENAME_LENGTH_MAX = 15
GTECBLE_NUMBER_OF_CHANNELS_MAX = 64

class GTECBLE_DEVICE_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("modelNumber", ctypes.c_char * GTECBLE_STRING_LENGTH_MAX),
        ("serialNumber", ctypes.c_char * GTECBLE_STRING_LENGTH_MAX),
        ("firmwareRevision", ctypes.c_char * GTECBLE_STRING_LENGTH_MAX),
        ("hardwareRevision", ctypes.c_char * GTECBLE_STRING_LENGTH_MAX),
        ("manufacturerName", ctypes.c_char * GTECBLE_STRING_LENGTH_MAX),
        ("channelTypes", ctypes.c_uint8 * GTECBLE_NUMBER_OF_CHANNELS_MAX),
        ("numberOfAcquiredChannels", ctypes.c_uint16),
        ("samplingRate", ctypes.c_uint16)
    ]

DeviceDiscoveredCallback = ctypes.CFUNCTYPE(None, ctypes.POINTER(ctypes.c_char * GTECBLE_DEVICENAME_LENGTH_MAX), ctypes.c_uint32)
DataAvailableCallback = ctypes.CFUNCTYPE(None, GTECBLE_HANDLE, ctypes.POINTER(ctypes.c_float), ctypes.c_uint32)

lib.GTECBLE_GetApiVersion.restype = ctypes.c_float
lib.GTECBLE_GetLastErrorText.restype = ctypes.c_char_p
lib.GTECBLE_StartScanning.restype = ctypes.c_uint32
lib.GTECBLE_StopScanning.restype = ctypes.c_uint32
lib.GTECBLE_RegisterDeviceDiscoveredCallback.argtypes = [DeviceDiscoveredCallback]
lib.GTECBLE_RegisterDeviceDiscoveredCallback.restype = ctypes.c_int
lib.GTECBLE_OpenDevice.argtypes = [ctypes.c_char_p, ctypes.POINTER(GTECBLE_HANDLE)]
lib.GTECBLE_OpenDevice.restype = ctypes.c_uint32
lib.GTECBLE_CloseDevice.argtypes = [ctypes.POINTER(GTECBLE_HANDLE)]
lib.GTECBLE_CloseDevice.restype = ctypes.c_uint32
lib.GTECBLE_RegisterDataAvailableCallback.argtypes = [GTECBLE_HANDLE, DataAvailableCallback]
lib.GTECBLE_RegisterDataAvailableCallback.restype = ctypes.c_int
lib.GTECBLE_GetDeviceInformation.argtypes = [GTECBLE_HANDLE, ctypes.POINTER(GTECBLE_DEVICE_INFORMATION)]
lib.GTECBLE_GetDeviceInformation.restype = ctypes.c_uint32

class GtecBLE():
    CHANNELTYPE_EXG = 1
    CHANNELTYPE_ACC = 2
    CHANNELTYPE_GYR = 3
    CHANNELTYPE_BAT = 4
    CHANNELTYPE_CNT = 5
    CHANNELTYPE_LINK = 6
    CHANNELTYPE_SATURATION = 7
    CHANNELTYPE_FLAG = 8
    CHANNELTYPE_VALID = 9
    CHANNELTYPE_OTHER = 10

    GTECBLE_ERROR_SUCCESS = 0
    GTECBLE_ERROR_INVALID_HANDLE = 1
    GTECBLE_ERROR_BLUETOOTHADAPTER = 2
    GTECBLE_ERROR_BLUETOOTHDEVICE = 3
    GTECBLE_ERROR_GENERAL_ERROR	= 4294967295

    __deviceDiscoveredEventHandler = None
    __deviceDiscoveredCallbackInternal = None

    @staticmethod
    def __handle_error__(errorCode):
        if errorCode != GtecBLE.GTECBLE_ERROR_SUCCESS:
            error_text = lib.GTECBLE_GetLastErrorText()
            error_text_str = error_text.decode('utf-8')
            raise ValueError(error_text_str)
        
    @staticmethod 
    def __on_devices_discovered_internal(devices, number_of_devices):
        device_list = [devices[i].value.decode("utf-8") for i in range(number_of_devices)]
        if GtecBLE.__deviceDiscoveredCallbackInternal is not None:
             GtecBLE.__deviceDiscoveredEventHandler(device_list)

    @staticmethod
    def GetApiVersion():  
        return np.frombuffer(struct.pack('f', lib.GTECBLE_GetApiVersion()), dtype=np.float32)[0]
    
    @staticmethod
    def StartScanning():
        GtecBLE.__handle_error__(lib.GTECBLE_StartScanning())
    
    @staticmethod
    def StopScanning():
        GtecBLE.__handle_error__(lib.GTECBLE_StopScanning())
    
    @staticmethod
    def AddDevicesDiscoveredEventhandler(handler):
        GtecBLE.__deviceDiscoveredCallbackInternal = DeviceDiscoveredCallback(GtecBLE.__on_devices_discovered_internal)
        GtecBLE.__handle_error__(lib.GTECBLE_RegisterDeviceDiscoveredCallback(GtecBLE.__deviceDiscoveredCallbackInternal))
        GtecBLE.__deviceDiscoveredEventHandler = handler

    @staticmethod
    def RemoveDevicesDiscoveredEventhandler():       
        GtecBLE.__handle_error__(lib.GTECBLE_RegisterDeviceDiscoveredCallback(ctypes.cast(None, DeviceDiscoveredCallback)))
        GtecBLE.__deviceDiscoveredEventHandler = None
        GtecBLE.__deviceDiscoveredCallbackInternal = None

    def __init__(self, serial):
        self.__dataAvailableHandler = None
        self.__dataAvailableCallbackInternal = None

        self.__hDevice = GTECBLE_HANDLE() 
        GtecBLE.__handle_error__(lib.GTECBLE_OpenDevice(serial.encode('utf-8'), ctypes.byref(self.__hDevice)))

        self.__device_info = GTECBLE_DEVICE_INFORMATION()
        GtecBLE.__handle_error__(lib.GTECBLE_GetDeviceInformation(self.__hDevice, ctypes.byref(self.__device_info )))

    def __del__(self):
        try:
            lib.GTECBLE_CloseDevice( ctypes.byref(self.__hDevice))
        except:
            pass #do nothing/destructor must not fail

    def AddDataAvailableEventhandler(self, dataAvailableHandler):
        self.__dataAvailableHandler = dataAvailableHandler
        self.__dataAvailableCallbackInternal = DataAvailableCallback(self.__dataAvailableInternal)
        GtecBLE.__handle_error__(lib.GTECBLE_RegisterDataAvailableCallback(self.__hDevice, self.__dataAvailableCallbackInternal))

    def RemoveDataAvailableEventhandler(self):
        GtecBLE.__handle_error__(lib.GTECBLE_RegisterDataAvailableCallback(self.__hDevice, ctypes.cast(None, DataAvailableCallback)))
        self.__dataAvailableHandler = None
        self.__dataAvailableCallbackInternal = None

    @property
    def ModelNumber(self):
        return self.__device_info.modelNumber.decode('utf-8')
    
    @property
    def SerialNumber(self):
        return self.__device_info.serialNumber.decode('utf-8')
    
    @property
    def FirmwareRevision(self):
        return self.__device_info.firmwareRevision.decode('utf-8')
    
    @property
    def HardwareRevision(self):
        return self.__device_info.hardwareRevision.decode('utf-8')
    
    @property
    def ManufacturerName(self):
        return self.__device_info.manufacturerName.decode('utf-8')
    
    @property
    def ChannelTypes(self):
        return [num for num in self.__device_info.channelTypes if num != 0]
    
    @property
    def NumberOfAcquiredChannels(self):
        return self.__device_info.numberOfAcquiredChannels
    
    @property
    def SamplingRate(self):
        return self.__device_info.samplingRate
    
    @property
    def Handle(self):
        return self.__hDevice.value

    def __dataAvailableInternal(self, hDevice, sample, sample_size):
        sample_array = np.fromiter(sample, dtype=np.float32, count=sample_size)
        if self.__dataAvailableHandler is not None:
            self.__dataAvailableHandler(self, sample_array)