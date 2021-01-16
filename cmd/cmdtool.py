import os, guimain


def getSettings():
    if not os.path.exists('settings/.msettings'):
        log = 'Failure - No settings exist. Please run the GUI program to configure the settings.'
        guimain.createLog(log)
    settingsFile = open('settings/.msettings', 'r+')
    lines = settingsFile.readlines()
    settingsFile.close()
    settings = []
    for line in lines:
        settings.append(line[:-1])
    return settings


class Settings:
    def __init__(self):
        settings = getSettings()

        try:
            self.port = settings[0]
            self.baud = settings[1]
            self.DP = settings[2]
            self.HDMI = settings[3]
            self.monitor = settings[4]
        except IndexError as ex:
            log = 'Failure - Unknown settings file\n'
            log += 'Delete settings file and relaunch\n'
            guimain.createLog(log)

S = Settings()
guimain.main(S)