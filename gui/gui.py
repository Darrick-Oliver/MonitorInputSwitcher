from tkinter import *
import os, guimain


def settingsExists():
    if not os.path.exists("settings.txt"):
        settingsFile = open("settings.txt", "w+")
        settingsFile.write("COM3\n")
        settingsFile.write("9600\n")
        settingsFile.write("15\n")
        settingsFile.write("17\n")
        settingsFile.write("0\n")
        settingsFile.close()


def getSettings():
    settingsFile = open("settings.txt", "r+")
    lines = settingsFile.readlines()
    settingsFile.close()
    settings = []
    for line in lines:
        settings.append(line[:-1])
    return settings


def setSettings(port, baud, input1, input2, monitor):
    settingsFile = open("settings.txt", "w+")
    settingsFile.write(port + "\n")
    settingsFile.write(baud + "\n")
    settingsFile.write(input1 + "\n")
    settingsFile.write(input2 + "\n")
    settingsFile.write(monitor + "\n")
    settingsFile.close()


class Settings:
    def __init__(self, top):
        settingsExists()
        settings = getSettings()

        self.start = 0

        self.port = settings[0]
        self.baud = settings[1]
        self.DP = settings[2]
        self.HDMI = settings[3]
        self.monitor = settings[4]

        self.t_port = StringVar()
        self.t_baud = StringVar()
        self.t_DP = StringVar()
        self.t_HDMI = StringVar()
        self.t_monitor = StringVar()

        # Settings frame
        settingsFrame = LabelFrame(root, text="Settings", padx=50, pady=20)
        settingsFrame.pack(padx=10, pady=10)

        # Port entry
        Label(settingsFrame, text='Port: ').grid(row=0, column=0)
        portEntry = Entry(settingsFrame, textvariable=self.t_port, width=8)
        portEntry.grid(row=0, column=1)
        portEntry.insert(0, self.port)

        # Baud entry
        Label(settingsFrame, text='Baud: ').grid(row=1, column=0)
        baudEntry = Entry(settingsFrame, textvariable=self.t_baud, width=8)
        baudEntry.grid(row=1, column=1)
        baudEntry.insert(0, self.baud)

        # Input1 entry
        Label(settingsFrame, text='Input 1: ').grid(row=2, column=0)
        inputOneEntry = Entry(settingsFrame, textvariable=self.t_DP, width=8)
        inputOneEntry.grid(row=2, column=1)
        inputOneEntry.insert(0, self.DP)

        # Input2 entry
        Label(settingsFrame, text='Input 2: ').grid(row=3, column=0)
        inputTwoEntry = Entry(settingsFrame, textvariable=self.t_HDMI, width=8)
        inputTwoEntry.grid(row=3, column=1)
        inputTwoEntry.insert(0, self.HDMI)

        # Monitor entry
        Label(settingsFrame, text='Monitor: ').grid(row=4, column=0)
        monEntry = Entry(settingsFrame, textvariable=self.t_monitor, width=8)
        monEntry.grid(row=4, column=1)
        monEntry.insert(0, self.monitor)

        # Buttons frame
        buttonsFrame = Frame(root)
        buttonsFrame.pack()

        # Save button
        saveButton = Button(buttonsFrame, text="Start", command=self.startProtocol)
        saveButton.pack(side=LEFT, padx=5)

        # Save button
        quitButton = Button(buttonsFrame, text="Save settings", command=self.saveProtocol)
        quitButton.pack(side=LEFT, padx=5)

        # Exit button
        exitButton = Button(buttonsFrame, text="Exit", command=self.exitProtocol)
        exitButton.pack(side=LEFT, padx=5)

        # Version number
        Label(root, text='Version 1.1.0').pack(side=LEFT, padx=5, pady=15)

    def startProtocol(self):
        self.port = self.t_port.get()
        self.baud = self.t_baud.get()
        self.DP = self.t_DP.get()
        self.HDMI = self.t_HDMI.get()
        self.monitor = self.t_monitor.get()
        setSettings(self.port, self.baud, self.DP, self.HDMI, self.monitor)

        self.start = 1
        root.destroy()

    def saveProtocol(self):
        self.port = self.t_port.get()
        self.baud = self.t_baud.get()
        self.DP = self.t_DP.get()
        self.HDMI = self.t_HDMI.get()
        self.monitor = self.t_monitor.get()
        setSettings(self.port, self.baud, self.DP, self.HDMI, self.monitor)

    def exitProtocol(self):
        # if self.port != self.t_port.get() or self.baud != self.t_baud.get() or self.DP != self.t_DP.get() or self.HDMI != self.t_HDMI.get():
        # Use above to check if settings have been changed without saving and add warning
        root.destroy()

# GUI
root = Tk()

root.geometry("270x230+100+50")
root.title("Monitor Input Switcher")

S = Settings(root)
root.mainloop()

if S.start:
    guimain.main(S)