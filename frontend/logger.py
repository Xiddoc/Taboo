"""
Logging! We love it.
"""
import logging
from time import time

# Create the logger we will use
log = logging.getLogger("")
log.setLevel(logging.INFO)

# Level config
levels = {
    logging.DEBUG: "[+]",
    logging.INFO: "[+]",
    logging.WARN: "[!]",
    logging.ERROR: "[X]",
}

# Set the level names
for level, level_text in levels.items():
    logging.addLevelName(level, level_text)


# noinspection PyMissingOrEmptyDocstring,PySameParameterValue
class RelativeSeconds(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Assign function like this, because PyCharm will
        # hang itself if you try to override it directly
        self.format = self.format_override

    def format_override(self, record):
        record.relativeCreated //= 1000
        return super().format(record)


# Reset the timer
logging._startTime = time()
# Use our new formatted seconds
logFormatter = RelativeSeconds('[%(relativeCreated)4ds] %(levelname)s %(message)s')

# Create console handler and add it to the logger
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
log.addHandler(consoleHandler)
