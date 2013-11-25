# -*- coding: utf-8 -*-
import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    Speedfundings,
    TheTotal,
    C3sStaff,
    Group,
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

    # a speedfunding item
    with transaction.manager:
        speedfunding_item = Speedfundings(
            #speed_id=u"RANDOMCODE",  # is always generated
            firstname=u"karl",
            lastname=u"ranseier",
            email=u"noreply@c3s.cc",
            address1=u"lange straße 123",
            address2=u"hinterhof",
            city=u"hauptort",
            postcode="12345",
            country="CC",
            locale="DE",
            donation=u"4",
            shirt_size=u"2",
            comment=u"no comment ;-)"
        )
        try:
            DBSession.add(speedfunding_item)
            DBSession.flush()
            print("adding speedfunding_item")
        except:
            print("could not add speedfunding_item.")
            # pass
    # a total
    with transaction.manager:
        a_total = TheTotal(
            amount_actual=u'4200',
            amount_promised=u'5000',
            #time='2013-11-20',
            num_shirts='0'
        )
        try:
            DBSession.add(a_total)
            DBSession.flush()
            print("adding a total")
        except:
            print("could not add the total.")
            # pass
    # a group for authorization
    with transaction.manager:
        accountants_group = Group(name=u"staff")
        try:
            DBSession.add(accountants_group)
            DBSession.flush()
            print("adding group staff")
        except:
            print("could not add group staff.")
            # pass

    # staff personnel
    with transaction.manager:
        staffer1 = C3sStaff(
            login=u"rut",
            password=u"berries",
            email=u"noreply@c3s.cc",
        )
        staffer1.groups = [accountants_group]
        try:
            DBSession.add(staffer1)
            print("adding staff rut")
            DBSession.flush()
        except:
            print("it borked! (rut)")
            # pass
