import time, os, sys, serial

port = 'COM3'
baud = 9600
DP = 15
HDMI = 17

try:
    current = os.system(r'ControlMyMonitor.exe /GetValue "\\.\DISPLAY1\Monitor0" 60')
except:
    sys.exit("Add ControlMyMonitor to system's Path and restart")

arduino = serial.Serial(port, baud, timeout=.1)

print("Connecting to Arduino...")
time.sleep(2)   #Arduino resets on new connection, wait 2 seconds before sending data

if (current == DP):
    print("Using DisplayPort input")
    arduino.write('1'.encode())
elif (current == HDMI):
    print("Using HDMI input")
    arduino.write('2'.encode())
else:
    sys.exit("Connected monitor isn't supported (Add support by changing value of DP or HDMI)")

while True:
    try:
        data = arduino.readline()[:-2]
        if data:
            if data == b'1':
                print("Switching To DisplayPort")
                os.system(r'ControlMyMonitor.exe /SetValue "\\.\DISPLAY1\Monitor0" 60 15')
                current = DP
            if data == b'2':
                print("Switching To HDMI")
                os.system(r'ControlMyMonitor.exe /SetValue "\\.\DISPLAY1\Monitor0" 60 17')
                current = HDMI
        elif (os.system(r'ControlMyMonitor.exe /GetValue "\\.\DISPLAY1\Monitor0" 60') == 15 and current == 17) or (os.system(r'ControlMyMonitor.exe /GetValue "\\.\DISPLAY1\Monitor0" 60') == 17 and current == 15):    # Check if monitor has changed
            print("Detected monitor switch")
            if current == HDMI:
                arduino.write('1'.encode())
                current = DP
            elif current == DP:
                arduino.write('2'.encode())
                current = HDMI
    except:
        sys.exit("Communication to Arduino was interrupted")