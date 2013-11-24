# -*- coding: utf-8  -*-
import unittest
from pyramid import testing
from pyramid_mailer.message import Message

mock_appstruct = {
    'speed_id': 'SPEED_ID_FOO',
    'firstname': u'Anne',
    'lastname': u'Gilles',
    'email': u'devnull@c3s.cc',
    'address1': 'addr one',
    'address2': 'addr two',
    'postcode': u'54321',
    'city': u'Müsterstädt',
    'country': u'some country',
    'locale': u'EN',
    'shirt_size': '3',
    'donation': '1234',
    'date_of_submission': '2013-09-09 08:44:47.251588',
}


class TestUtilities(unittest.TestCase):
    """
    tests for speedfunding/utils.py
    """

    def setUp(self):
        self.config = testing.setUp()

    def test_make_confirmation_email_en(self):
        from speedfunding.utils import make_confirmation_email

        result = make_confirmation_email(mock_appstruct)
        self.assertTrue(isinstance(result, Message))
        #print dir(result)
        self.assertTrue('your pledge' in result.body)

    def test_make_confirmation_email_de(self):
        from speedfunding.utils import make_confirmation_email

        _mock_appstruct_DE = mock_appstruct
        _mock_appstruct_DE['locale'] = u'DE'
        result = make_confirmation_email(_mock_appstruct_DE)
        self.assertTrue(isinstance(result, Message))
        print result.body
