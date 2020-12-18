# 1. Required components

- Arduino Uno (Soon to be Arduino Nano)
- 2x 330Ω Resistors
- 2x 10kΩ Resistors
- 2 LEDs
- 2 Pushbuttons
- Monitor Switcher PCB (Or soldered breadboard)

Find out how to build the circuit from the circuit diagram ("*circuit_diagram.png*") or view it on TinkerCAD: https://www.tinkercad.com/things/6FZK49Luh5o

# 2. Installing software

**A. Arduino Installation**

Currently there isn't an easy way to install my Arduino code to the Arduino except through their software. I am working on a way to install the software through the MonitorInputSwitcher GUI, but for now you will have to install it manually. This means downloading the file "*MonitorSwitch.ino*" and uploading it using Arduino's software: https://www.arduino.cc/en/software

**B. ControlMyMonitor**

The only dependency for this program is ControlMyMonitor which can be downloaded here: https://www.nirsoft.net/utils/control_my_monitor.html 

Install it in your Program Files and add it to the command prompt path. For a more detailed explanation of how to do so, follow along with this Imgur album I made: https://imgur.com/a/4GtlqDX

**C. MonitorInputSwitcher**

You have the choice of downloading the GUI version or Command Prompt version from the "dist" folder. **The GUI version is recommended**, as I am not updating the Command Prompt version right now. The only difference between the two versions is that the GUI version allows the user to change the settings before running the program.

After connecting the Arduino, you should be able to run the MonitorInputSwitcher program. If there are any issues, the program will store it in a log file. If you have any issues with the program, please post the contents of the log file to the issue tracker and I will try to resolve them

Something funny I noticed is that Windows thinks the GUI executable is a virus. I'll figure out how to fix this later.

# 3. PCB and Chassis

The PCB schematic is located in the files as "*MonitorSwitcher.brd*" and can be ordered from any PCB site (OshPark, JLCPCB, etc)

The chassis is a WIP
