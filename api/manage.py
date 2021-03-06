from gevent.monkey import patch_all; patch_all()

import os
from app import create_app
from flask_script import Manager
from flask_script import Server
from app.log import setup_logging
from app.src.sqlalchemydb import AlchemyDB

basedir = os.path.abspath(os.path.dirname(__file__))
env = os.getenv('HOSTENV') or 'development'
new_relic_cfg = basedir + '/config/' + env + '_newrelic.ini'

# import newrelic.agent
# newrelic.agent.initialize(new_relic_cfg)

app = create_app()
manager = Manager(app)
setup_logging()
AlchemyDB.init()
manager.add_command("runserver", Server(host="localhost", port=9056))

if __name__ == '__main__':
    manager.run()
