import ConfigParser
import os

# config file path
CONFIG_FILE = os.path.join(os.path.split(__file__)[0], 'stipule.conf')

def get(key):
    if key.upper() in os.environ:
        return os.environ[key.upper()]
    parser = ConfigParser.RawConfigParser()
    parser.read(CONFIG_FILE)
    return parser.get('general', key)
