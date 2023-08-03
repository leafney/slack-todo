# fix: relative import error: `No module named xxx`
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# fix: requests InsecureRequestWarning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
