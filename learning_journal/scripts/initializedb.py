import os
import sys
import transaction

from ..models import DBSession, MyModel, Entry, Base

from sqlalchemy import engine_from_config

from cryptacular.pbkdf2 import PBKDF2PasswordManager as Manager
from ..models import User

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    MyModel,
    Base,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        # replace the code to create a MyModel instance
        manager = Manager()
        password = manager.encode(u'admin')
        admin = User(name=u'admin', password=password)
        DBSession.add(admin)
