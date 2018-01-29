
import sys
from logbook import Logger, StreamHandler

StreamHandler(sys.stdout).push_application()
log = Logger('SmartImport')