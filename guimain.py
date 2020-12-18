from datetime import datetime
import time, os, sys, serial, subprocess

# Create a log directory if it doesn't already exist
def createLogDir():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    return './logs/'

# Ensure values from GUI are valid
def getSettings(S, log):
    try:
        port = S.port
        baud = int(S.baud)
        DP = int(S.DP)
        HDMI = int(S.HDMI)
    except ValueError as ex:
        log += 'Failure - Invalid input\n'
        log += type(ex).__name__, '\n', ex.args
        save_path = createLogDir()
        logFile = open(save_path + "log_" + datetime.now().strftime("%m.%d.%Y_%H.%M.%S") + ".txt", "x")
        logFile.write(log)
        sys.exit("Invalid input")
    return port, baud, DP, HDMI

# Attempt to get current state
def currentState(log, si):
    try:
        current = subprocess.call(r'ControlMyMonitor.exe /GetValue "\\.\DISPLAY1\Monitor0" 60', startupinfo=si)
    except FileNotFoundError:
        log += "Failure - Could not find ControlMyMonitor.exe\n"
        log += "Add ControlMyMonitor to system's Path and restart"
        save_path = createLogDir()
        logFile = open(save_path + "log_" + datetime.now().strftime("%m.%d.%Y_%H.%M.%S") + ".txt", "x")
        logFile.write(log)
        sys.exit("Could not find ControlMyMonitor.exe")
    return current

# Attempt to connect to arduino
def connect(port, baud, log):
    try:
        arduino = serial.Serial(port, baud, timeout=.1)
    except serial.SerialException:
        log += "Failure - Could not open port " + port
        save_path = createLogDir()
        logFile = open(save_path + "log_" + datetime.now().strftime("%m.%d.%Y_%H.%M.%S") + ".txt", "x")
        logFile.write(log)
        sys.exit("Could not open port " + port)
    log += 'Connecting to Arduino...\n'
    time.sleep(2)   # Arduino resets on new connection, wait 2 seconds before sending data
    return arduino, log

def checkMonitor(DP, HDMI, arduino, current, log):
    if (current == DP):
        log += 'Using Input 1\n'
        arduino.write('1'.encode())
    elif (current == HDMI):
        log += 'Using Input 2\n'
        arduino.write('2'.encode())
    else:
        log += "Failure - Connected monitor isn't using input value " + str(DP) + " or input value " + str(HDMI) + ". Monitor has input value " + str(current)
        save_path = createLogDir()
        logFile = open(save_path + "log_" + datetime.now().strftime("%m.%d.%Y_%H.%M.%S") + ".txt", "x")
        logFile.write(log)
        sys.exit("Connected monitor isn't using input value " + str(DP) + " or input value " + str(HDMI) + ". Monitor has input value " + str(current))
    return log

# Check serial monitor to see if button has been pressed
def serialLoop(arduino, DP, HDMI, log, si):
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

            # Check if there has been an unexpected monitor switch
            # Too annoying to use. See if there is a way to prevent windows wheel from spinning multiple times per second.
            # elif (subprocess.call(r'ControlMyMonitor.exe /GetValue "\\.\DISPLAY1\Monitor0" 60', startupinfo=si) == 15 and current == 17)
            #   or (subprocess.call(r'ControlMyMonitor.exe /GetValue "\\.\DISPLAY1\Monitor0" 60', startupinfo=si) == 17 and current == 15):
            #     if current == HDMI:
            #         arduino.write('1'.encode())
            #         current = DP
            #     elif current == DP:
            #         arduino.write('2'.encode())
            #         current = HDMI
        except serial.SerialException:
            log += 'Failure - Communication to Arduino was interrupted'
            save_path = createLogDir()
            logFile = open(save_path + "log_" + datetime.now().strftime("%m.%d.%Y_%H.%M.%S") + ".txt", "x")
            logFile.write(log)
            sys.exit("Communication to Arduino was interrupted")

def main(args):
    # Silence command prompt
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    log = ''

    # Messy, needs a way to set global variables instead of returning them
    port, baud, input1, input2 = getSettings(args, log)
    current = currentState(log, si)
    arduino, log = connect(port, baud, log)
    log = checkMonitor(input1, input2, arduino, current, log)
    serialLoop(arduino, input1, input2, log, si)