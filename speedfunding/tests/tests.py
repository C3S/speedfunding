import unittest
import transaction

from pyramid import testing

from .models import DBSession


class TestMyViewSuccessCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from .models import (
            Base,
            MyModel,
            )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            model = MyModel(name='one', value=55)
            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_passing_view(self):
        from .views import speedfunding_view
        request = testing.DummyRequest()
        info = speedfunding_view(request)
        self.assertTrue('paypal' in info['form'])
        self.assertEqual(info['project'], 'speedfunding')


class TestMyViewFailureCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        #from .models import (
        #    Base,
        #    #MyModel,
        #)
        DBSession.configure(bind=engine)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_failing_view(self):
        from .views import speedfunding_view
        request = testing.DummyRequest()
        info = speedfunding_view(request)
        print(info)
#        self.assertEqual(info.status_int, 500)
