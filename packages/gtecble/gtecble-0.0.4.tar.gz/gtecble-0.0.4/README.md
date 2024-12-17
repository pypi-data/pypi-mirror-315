# Gtec.BLE

This python library allows to communicate with Gtec.BLE devices.

## Installation

```pip install gtecble```

## Acquisition Example

This example shows how to setup a data acquisition with a Gtec.BLE device.

``` Python
import gtecble as gble

discovered_devices = []
def on_devices_discovered(devices):
    global discovered_devices
    cnt = 0
    discovered_devices = devices
    for device in discovered_devices:
        print('#' + str(cnt) + ': ' + device)
        cnt = cnt+1

def on_data_available(device, data):
    print(data)

ver = gble.GtecBLE.GetApiVersion()
print('API version: ' + str(ver))

gble.GtecBLE.AddDevicesDiscoveredEventhandler(on_devices_discovered)
gble.GtecBLE.StartScanning()
print('Scanning for devices...')

selectedId = int(input('Select device by id:\n'))

gble.GtecBLE.StopScanning()
gble.GtecBLE.RemoveDevicesDiscoveredEventhandler()
print('Stopped scanning for devices...')

device = gble.GtecBLE(discovered_devices[selectedId])
print('Serial number: ' + device.SerialNumber)
print('ModelNumber: '+ device.ModelNumber)
print('FirmwareRevision: '+ device.FirmwareRevision)
print('HardwareRevision: '+ device.HardwareRevision)
print('ManufacturerName: ' + device.ManufacturerName)
print('NumberOfAcquiredChannels: ' + str(device.NumberOfAcquiredChannels))
print('SamplingRate: ' + str(device.SamplingRate))
print('ChannelTypes: ' + str(device.ChannelTypes))

device.AddDataAvailableEventhandler(on_data_available)
input('Press ENTER to stop acquisition.')
device.RemoveDataAvailableEventhandler()

del device
```