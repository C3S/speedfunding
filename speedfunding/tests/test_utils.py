# -*- coding: utf-8  -*-
import unittest
from pyramid import testing
from pyramid_mailer.message import Message
from speedfunding.models import (
    Speedfundings,
    DBSession,
)
import transaction


class TestUtilities(unittest.TestCase):
    """
    tests for speedfunding/utils.py
    """

    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from speedfunding.models import (
            Base,
        )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            model1 = Speedfundings(  # english
                firstname=u'first',
                lastname=u'last',
                email=u'noreply@c3s.cc',
                address1=u'some',
                address2=u'where',
                postcode=u'98765',
                city=u'over',
                country=u'some country',
                locale=u'en',
                donation=u'3',
                shirt_size=u'3',
                comment=u'some comment.',
            )
            DBSession.add(model1)
        with transaction.manager:
            model2 = Speedfundings(  # german
                firstname=u'first',
                lastname=u'last',
                email=u'noreply@c3s.cc',
                address1=u'some',
                address2=u'where',
                postcode=u'98765',
                city=u'over',
                country=u'some country',
                locale=u'de',
                donation=u'3',
                shirt_size=u'3',
                comment=u'some comment.',
            )
            DBSession.add(model2)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_make_donation_confirmation_emailbody_en(self):
        from speedfunding.utils import make_donation_confirmation_emailbody
        _item = Speedfundings.get_by_id(1)

        result = make_donation_confirmation_emailbody(_item)
        self.assertTrue('your pledge' in result)
        self.assertTrue('appreciate your donation' in result)

    def test_make_donation_confirmation_emailbody_de(self):
        from speedfunding.utils import make_donation_confirmation_emailbody
        _item = Speedfundings.get_by_id(2)
        result = make_donation_confirmation_emailbody(_item)
        self.assertTrue('Deine Spende' in result)
        #print result

    def test_make_shirt_confirmation_email_en(self):
        from speedfunding.utils import make_shirt_confirmation_emailbody
        _item = Speedfundings.get_by_id(1)

        result = make_shirt_confirmation_emailbody(_item)
        self.assertTrue('shirt' in result)
        self.assertTrue('You have chosen a t-shirt' in result)

    def test_make_shirt_confirmation_email_de(self):
        from speedfunding.utils import make_shirt_confirmation_emailbody
        _item = Speedfundings.get_by_id(2)
        result = make_shirt_confirmation_emailbody(_item)
        self.assertTrue(u'Du hast ein T-Shirt gewählt' in result)
        #print result
