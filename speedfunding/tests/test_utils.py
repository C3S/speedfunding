# -*- coding: utf-8  -*-
import unittest
from pyramid import testing
from pyramid_mailer.message import Message
from speedfunding.models import (
    Speedfundings,
    DBSession,
)
import transaction
import os


class TestUtilities(unittest.TestCase):
    """
    tests for speedfunding/utils.py
    """

    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite:///test_utils.db')
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
            DBSession.flush()
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
            DBSession.flush()

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()
        try:
            os.remove('test_utils.db')
        except:
            print("file not found: test_utils.db")
            pass

    def test_make_donation_confirmation_emailbody_en(self):
        from speedfunding.utils import make_donation_confirmation_emailbody
        _item = Speedfundings.get_by_id(1)

        result = make_donation_confirmation_emailbody(_item)
        self.assertTrue('your pledge' in result)
        self.assertTrue('appreciate your donation' in result)

    def test_make_donation_confirmation_emailbody_de(self):
        from speedfunding.utils import make_donation_confirmation_emailbody
        _item = Speedfundings.get_by_id(2)
        self.assertIsNotNone(_item)
        result = make_donation_confirmation_emailbody(_item)
        self.assertTrue('Deine Spende' in result)

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

    def test_make_mail_body(self):
        """
        test the mail body preparation function used for mail to accountants
        """
        from speedfunding.utils import make_mail_body
        _item = Speedfundings.get_by_id(1)
        result = make_mail_body(_item)
        self.assertTrue(u'we got some funding through the form' in result)

    def test__accountant_mail(self):
        """
        test the preparation function used for mail to accountants
        """
        from speedfunding.utils import accountant_mail
        _item = Speedfundings.get_by_id(1)
        result = accountant_mail(_item)
        self.assertIsNotNone(_item)
        self.assertIsInstance(result, Message)
        self.assertTrue(u'BEGIN' in result.body)
        print(result)
