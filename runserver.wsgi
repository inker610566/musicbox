import sys
sys.path.insert(0, "/home/mbox/www/musicbox")
from werkzeug.debug import DebuggedApplication
from musicbox import app as applicationx
application = DebuggedApplication(applicationx, True)

