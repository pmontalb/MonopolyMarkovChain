from enum import IntEnum
from inspect import getframeinfo, stack
from datetime import datetime
from os import getcwd

DATA_FOLDER = getcwd() + "/Data/Logs"
_LOG_HANDLES = {}
_LOG_PATHS = []


class LogLevel(IntEnum):
    NEVER = -2
    ERROR = -1
    WARN = 0
    INFO = 1
    DEBUG = 2
    TEST = 3
    ALWAYS = 4


class Logger:
    def __init__(self, log_name, log_level=LogLevel.DEBUG):
        self.log_path = DATA_FOLDER + "/" + log_name
        if not log_name.endswith(".log"):
            self.log_path += ".log"

        self.log_level = log_level
        if self.log_path not in _LOG_PATHS:
            _LOG_PATHS.append(self.log_path)
            self.__log_handle = open(self.log_path, "w+")
            _LOG_HANDLES[self.log_path] = self.__log_handle
        else:
            self.__log_handle = _LOG_HANDLES[self.log_path]

    def set_log_level(self, log_level):
        self.log_level = log_level

    def __call__(self, message, log_level=LogLevel.DEBUG):
        if log_level > self.log_level:
            return
        self.__log_handle.write(self.__message_prefix() + message + "\n")

    def __message_prefix(self):
        caller = getframeinfo(stack()[2][0])
        return "[{}] [{}] [{}::{}]: ".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                                             str(self.log_level).split(".")[1],  # display the enum value
                                             caller.function,
                                             caller.lineno)