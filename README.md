# 1. Required Components

- Arduino Nano
- 2x 330Ω resistors
- 2x 10kΩ resistors
- 2 LEDs
- 2 pushbutton switches
- Monitor Switcher PCB (Or soldered breadboard)

View the circuit schematic on TinkerCAD: https://www.tinkercad.com/things/7qLFwGoTEAK

# 2. Installing Software

**A. Arduino Installation**

Currently there isn't an easy way to install my Arduino code to the Arduino except through their software. I am working on a way to install the software through the MonitorInputSwitcher GUI, but for now you will have to install it manually. This means downloading the file 'MonitorSwitch.ino' under /resources and uploading it using Arduino's software: https://www.arduino.cc/en/software

**B. MonitorInputSwitcher**
Download the latest version of MonitorInputSwitcher_GUI (and optionally MonitorInputSwitcher_CMD to run on startup without loading the dialog box each time).

After connecting to the Arduino, run MonitorInputSwitcher_GUI. Windows may say that the program is a virus, however it is not. I'm working on a way to fix this right now, I think it has something to do with the way I compiled the code into an exe file.

If there are any issues, the program will create a log file. If you have any unresolved issues with this program, please post the contents of the log file to the issue tracker and I will try to resolve them.

# 3. PCB and Chassis

The PCB schematic is located in /resources as 'MonitorSwitcher.brd' and can be ordered from any PCB site (OshPark, JLCPCB, etc)

The chassis is a WIP

# 4. Changes and To-do List

To-do:
- Input detector, no need to enter inputs each time
- Support for more than two inputs
- Settings help
- Add automatic installation of Arduino software
