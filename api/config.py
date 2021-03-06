import os
import yaml

basedir = os.path.abspath(os.path.dirname(__file__))

env = os.getenv('HOSTENV') or 'development'

config_file = basedir + '/config/' + env + '.yml'

with open(config_file, 'r') as f:
    CONFIG = yaml.safe_load(f)


DATABASE_URL = CONFIG["mysql"]["connection"]
LOG_FILE = CONFIG["logfile"]
LOG_FILE_ERROR = CONFIG["errorlogfile"]
