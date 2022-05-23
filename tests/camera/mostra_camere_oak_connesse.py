import depthai
"""
script che mostra le videocamere connesse della marca OAK, ovvero le videocamere che supportano la libreria depthai. 
"""
for device in depthai.Device.getAllAvailableDevices():
    print(f"\nID VIDEOCAMERA \t\t[ {device.getMxId()} ]  \nNOME VIDEOCAMERA \t[ {device.state} ] \n")
    print("*"*40)
