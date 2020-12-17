from tkinter import *
from datetime import datetime
import time, os, sys, serial, subprocess

class Settings:
    def __init__(self, top):
        self.port=""
        self.baud=""
        self.DP=""
        self.HDMI=""

        self.t_port = StringVar()
        self.t_baud = StringVar()
        self.t_DP = StringVar()
        self.t_HDMI = StringVar()

        # Settings frame
        settingsFrame = LabelFrame(root, text="Settings", padx=50, pady=20)
        settingsFrame.pack(padx=10, pady=10)

        # Port entry
        Label(settingsFrame, text='Port: ').grid(row=0, column=0)
        portEntry = Entry(settingsFrame, textvariable=self.t_port, width=8)
        portEntry.grid(row=0, column=1)
        portEntry.insert(0, "COM3")

        # Baud entry
        Label(settingsFrame, text='Baud: ').grid(row=1, column=0)
        baudEntry = Entry(settingsFrame, textvariable=self.t_baud, width=8)
        baudEntry.grid(row=1, column=1)
        baudEntry.insert(0, "9600")

        # Input1 entry
        Label(settingsFrame, text='Input 1: ').grid(row=2, column=0)
        inputOneEntry = Entry(settingsFrame, textvariable=self.t_DP, width=8)
        inputOneEntry.grid(row=2, column=1)
        inputOneEntry.insert(0, "15")

        # Input2 entry
        Label(settingsFrame, text='Input 2: ').grid(row=3, column=0)
        inputTwoEntry = Entry(settingsFrame, textvariable=self.t_HDMI, width=8)
        inputTwoEntry.grid(row=3, column=1)
        inputTwoEntry.insert(0, "17")

        # Save button
        saveButton = Button(root, text="Start", command=self.savePress)
        saveButton.pack()

        # Quit button
        quitButton = Button(root, text="Quit", command=self.quitProtocol)
        quitButton.pack()

    def savePress(self):
        self.port = self.t_port.get()
        self.baud = self.t_baud.get()
        self.DP = self.t_DP.get()
        self.HDMI = self.t_HDMI.get()
        root.destroy()

    def quitProtocol(self):
        sys.exit("Program quit")

# GUI
root = Tk()

root.geometry("300x230+100+50")
root.title("Monitor Input Switcher")

S = Settings(root)
root.mainloop()

# Script

# Create log directory
log = ''
if not os.path.exists('logs'):
    os.makedirs('logs')
save_path = './logs/'

try:
    port = S.port
    baud = int(S.baud)
    DP = int(S.DP)
    HDMI = int(S.HDMI)
except ValueError:
    log += 'Fail @Unexpected exit'
    logFile = open(save_path + "log_" + datetime.now().strftime("%m.%d.%Y_%H.%M.%S") + ".txt", "x")
    logFile.write(log)
    sys.exit("Unexpected exit")

# Silence command prompt
si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

# Attempt to get current state
try:
    current = subprocess.call(r'ControlMyMonitor.exe /GetValue "\\.\DISPLAY1\Monitor0" 60', startupinfo=si)
except FileNotFoundError:
    log += "Failure - Could not find ControlMyMonitor.exe\n"
    log += "Add ControlMyMonitor to system's Path and restart"
    logFile = open(save_path + "log_" + datetime.now().strftime("%m.%d.%Y_%H.%M.%S") + ".txt", "x")
    logFile.write(log)
    sys.exit("Could not find ControlMyMonitor.exe")

# Connect to serial monitor
try:
    arduino = serial.Serial(port, baud, timeout=.1)
except serial.SerialException:
    log += "Failure - Could not open port " + port
    logFile = open(save_path + "log_" + datetime.now().strftime("%m.%d.%Y_%H.%M.%S") + ".txt", "x")
    logFile.write(log)
    sys.exit("Could not open port " + port)

print("Connecting to Arduino...")
log += 'Connecting to Arduino...\n'
time.sleep(2)   # Arduino resets on new connection, wait 2 seconds before sending data

if (current == DP):
    log += 'Using Input 1\n'
    arduino.write('1'.encode())
elif (current == HDMI):
    log += 'Using Input 2\n'
    arduino.write('2'.encode())
else:
    log += "Failure - Connected monitor isn't using input value " + str(DP) + " or input value " + str(HDMI) + ". Monitor has input value " + str(current)
    logFile = open(save_path + "log_" + datetime.now().strftime("%m.%d.%Y_%H.%M.%S") + ".txt", "x")
    logFile.write(log)
    sys.exit("Connected monitor isn't using input value " + str(DP) + " or input value " + str(HDMI) + ". Monitor has input value " + str(current))

# Check serial monitor to see if button has been pressed
while True:
    try:
        data = arduino.readline()[:-2]
        if data:
            if data == b'1':
                log += "Switching To Input 1\n"
                subprocess.call(r'ControlMyMonitor.exe /SetValue "\\.\DISPLAY1\Monitor0" 60 ' + str(DP), startupinfo=si)
                current = DP
            if data == b'2':
                log += "Switching To Input 2\n"
                subprocess.call(r'ControlMyMonitor.exe /SetValue "\\.\DISPLAY1\Monitor0" 60 ' + str(HDMI), startupinfo=si)
                current = HDMI

        # Too annoying to use. See if there is a way to prevent windows wheel from spinning multiple times per second.
        # elif (subprocess.call(r'ControlMyMonitor.exe /GetValue "\\.\DISPLAY1\Monitor0" 60', startupinfo=si) == 15 and current == 17)
        #   or (subprocess.call(r'ControlMyMonitor.exe /GetValue "\\.\DISPLAY1\Monitor0" 60', startupinfo=si) == 17 and current == 15):
        #     print("Detected monitor switch")
        #     if current == HDMI:
        #         arduino.write('1'.encode())
        #         current = DP
        #     elif current == DP:
        #         arduino.write('2'.encode())
        #         current = HDMI
    except serial.SerialException:
        log += 'Failure - Communication to Arduino was interrupted'
        logFile = open(save_path + "log_" + datetime.now().strftime("%m.%d.%Y_%H.%M.%S") + ".txt", "x")
        logFile.write(log)
        sys.exit("Communication to Arduino was interrupted")