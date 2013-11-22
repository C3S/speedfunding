# -*- coding: utf-8 -*-
import unittest
import transaction

from pyramid import testing

from speedfunding.models import DBSession


class TestSpeedfundingsSuccessCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from speedfunding.models import (
            Base,
            Speedfundings,
        )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            model = Speedfundings(
                firstname='first',
                lastname='last',
                email='noreply@c3s.cc',
                address1='some',
                address2='where',
                postcode='98765',
                city='over',
                country='CC',
                locale='AT',
                donation='',
                shirt_size='',
                comment='some comment.',
            )
            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_passing_view(self):
        from speedfunding.views import speedfunding_view
        request = testing.DummyRequest()
        info = speedfunding_view(request)
        self.assertTrue('paypal' in info['form'])
        self.assertEqual(info['project'], 'speedfunding')


class TestMyViewFailureCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from speedfunding.models import (
            Base,
            #Speedfundings,
            #Group,
            #C3sStaff,
            #TheTotal
        )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        self.initialize_db()

    def initialize_db(self):
        from speedfunding.models import (
            Speedfundings,
            Group,
            C3sStaff,
            TheTotal
        )
        # a speedfunding item
        with transaction.manager:
            speedfunding_item = Speedfundings(
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

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_failing_view(self):
        from speedfunding.views import speedfunding_view
        request = testing.DummyRequest()
        info = speedfunding_view(request)
        print(info)
#        self.assertEqual(info.status_int, 500)
