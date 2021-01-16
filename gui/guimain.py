from datetime import datetime
from ctypes import windll
import time, os, sys, serial, moncontrol


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
        monitor = int(S.monitor)
    except ValueError as ex:
        log += 'Failure - Invalid input\n'
        log += type(ex).__name__, '\n', ex.args
        createLog(log)
    return port, baud, DP, HDMI, monitor


# Attempt to connect to arduino
def connect(port, baud, log):
    try:
        arduino = serial.Serial(port, baud, timeout=.1)
    except serial.SerialException:
        log += 'Failure - Could not open port ' + port
        createLog(log)
    log += 'Connecting to Arduino...\n'
    time.sleep(2)   # Arduino resets on new connection, wait 2 seconds before sending data
    return arduino, log


# Figure out which monitor is connected and tell the Arduino
def checkMonitor(DP, HDMI, arduino, current, log):
    if (current == DP):
        log += 'Using Input 1\n'
        arduino.write('1'.encode())
    elif (current == HDMI):
        log += 'Using Input 2\n'
        arduino.write('2'.encode())
    else:
        log += 'Failure - Connected monitor isn\'t using input value ' + str(DP) + ' or input value ' + str(HDMI) + '. Monitor has input value ' + str(current)
        createLog(log)
    return log


# Check serial monitor to see if button has been pressed
def serialLoop(arduino, DP, HDMI, log, current, monitor):
    while True:
        handles = []
        for handle in moncontrol.iter_physical_monitors(False):
            handles.append(handle)

        try:
            data = arduino.readline()[:-2]
            currMon = moncontrol.get_monitor_input(handles[monitor], 0x60)
            if data:
                if data == b'1':
                    log += 'Switching To Input 1\n'
                    moncontrol.set_vcp_feature(handles[monitor], 0x60, DP)
                    # current = DP
                if data == b'2':
                    log += 'Switching To Input 2\n'
                    moncontrol.set_vcp_feature(handles[monitor], 0x60, HDMI)
                    # current = HDMI

            # Check if there has been an unexpected monitor switch
            elif (currMon == DP and current == HDMI) or (currMon == HDMI and current == DP):
                if current == HDMI:
                    arduino.write('1'.encode())
                    current = DP
                elif current == DP:
                    arduino.write('2'.encode())
                    current = HDMI
                else:
                    log += 'Failure - Unknown current input'
                    destroyHandles(handles)
                    createLog(log)
        except serial.SerialException:
            log += 'Failure - Communication to Arduino was interrupted'
            destroyHandles(handles)
            createLog(log)

        destroyHandles(handles)


def destroyHandles(handles):
    for handle in handles:
        windll.dxva2.DestroyPhysicalMonitor(handle)


def createLog(log):
    save_path = createLogDir()
    logFile = open(save_path + 'log_' + datetime.now().strftime('%m.%d.%Y_%H.%M.%S') + '.txt', 'x')
    logFile.write(log)
    logFile.close()
    sys.exit()


def main(args):
    log = ''
    try:
        port, baud, input1, input2, monitor = getSettings(args, log)

        handles = []
        for handle in moncontrol.iter_physical_monitors(False):
            handles.append(handle)
        current = moncontrol.get_monitor_input(handles[monitor], 0x60)
        destroyHandles(handles)

        arduino, log = connect(port, baud, log)
        log = checkMonitor(input1, input2, arduino, current, log)
        serialLoop(arduino, input1, input2, log, current, monitor)
    except Exception as ex:
        log += 'Failure - Unknown fail\n'
        log += type(ex).__name__, '\n', ex.args
        createLog(log)