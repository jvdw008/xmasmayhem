# Logging class for debugging/testing
import os, datetime

class Log:
    def __init__(self, settings):
        self.settings = settings
        self.log_size = self.settings.log_size
        self.log_file = self.settings.log_file
        self.dtTime = datetime.datetime.now()
        self.tmpVar = "0"
        initStr = "Log started at <" + str(self.dtTime.year) + "-"
        if (self.dtTime.month < 10):
            initStr += self.tmpVar + str(self.dtTime.month)
        else:
            initStr += str(self.dtTime.month)
        initStr += "-"
        if (self.dtTime.day < 10):
            initStr += self.tmpVar + str(self.dtTime.day)
        else:
            initStr += str(self.dtTime.day)
        initStr += ">\n\n"
        self.log_array = [initStr]
        # Init the log file
        self.clearFile()

    # Write message
    def write(self, message):
        if (self.settings.logging_enabled):            
            dtTime = datetime.datetime.now()
            tmpMessage = "<" 
            if (dtTime.hour < 10):
                tmpMessage += self.tmpVar + str(dtTime.hour)
            else:
                tmpMessage += str(dtTime.hour)
            tmpMessage += ":"

            if (dtTime.minute < 10):
                tmpMessage += self.tmpVar + str(dtTime.minute)
            else:
                tmpMessage += str(dtTime.minute)
            tmpMessage += ":"

            if (dtTime.second < 10):
                tmpMessage += self.tmpVar + str(dtTime.second)
            else:
                tmpMessage += str(dtTime.second)
            tmpMessage += "> " + message + "\n"
            
            # Don't write if already in
            if (len(self.log_array) > 0):
                for i in range(len(self.log_array)):
                    if (tmpMessage == self.log_array[i]):
                        return

            self.log_array.append(tmpMessage)
            
            # Write file immediately for button presses and file loads
            if (self.settings.log_setting < 3):
                self.writeFile()

            else:
                # Keep array size to a configured limit, deleting oldest entries first
                if (len(self.log_array) > self.log_size):
                    # Write to file then reset
                    self.writeFile()

    # Add it to logging text file directly
    def writeFile(self):
        try:
            logFile = open(os.path.join(os.getcwd(), "data", self.log_file), "a+")
            logFile.writelines(self.log_array)
            logFile.close()

            # Clear temp array after writing to file
            self.log_array.clear()
            self.log_array = []

        except IOError:
            print(f"Unable to write to file: {self.log_file}")
            return

    def clearFile(self):
        try:
            logFile = open(os.path.join(os.getcwd(), "data", self.log_file), "w")
            logFile.writelines("")
            logFile.close()

        except IOError:
            print(f"Unable to clear file: {self.log_file}")
            return
