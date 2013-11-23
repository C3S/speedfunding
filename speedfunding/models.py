from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Index,
    Integer,
    Boolean,
    DateTime,
    Unicode
)
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    synonym,
)
import cryptacular.bcrypt
from zope.sqlalchemy import ZopeTransactionExtension
from datetime import datetime

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()
crypt = cryptacular.bcrypt.BCRYPTPasswordManager()


def make_random_string():
    """
    used as email confirmation code
    """
    import random
    import string
    return u''.join(
        random.choice(
            string.ascii_uppercase + string.digits
        ) for x in range(10))


class Speedfundings(Base):
    """
    submissions to the speedfunding
    """
    __tablename__ = 'speedfundings'
    id = Column(Integer, primary_key=True)
    speed_id = Column(Unicode(255), unique=True)
    firstname = Column(Unicode(255))
    lastname = Column(Unicode(255))
    email = Column(Unicode(255))
    address1 = Column(Unicode(255))
    address2 = Column(Unicode(255))
    postcode = Column(Unicode(255))
    city = Column(Unicode(255))
    country = Column(Unicode(255))
    locale = Column(Unicode(255))
    donation = Column(Unicode(255))
    shirt_size = Column(Integer())
    comment = Column(Unicode(255))
    date_of_submission = Column(DateTime(), nullable=False)
    payment_received = Column(Boolean, default=False)
    payment_received_date = Column(
        DateTime(), default=datetime(1970, 1, 1))

    def __init__(self,
                 #speed_id,
                 firstname, lastname, email,
                 address1, address2, postcode, city, country,
                 locale,
                 donation, shirt_size, comment,):
        """
        a new entry is persisted this way
        """
        self.speed_id = make_random_string()
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.address1 = address1
        self.address2 = address2
        self.postcode = postcode
        self.city = city
        self.country = country
        self.locale = locale
        self.donation = donation
        self.shirt_size = shirt_size
        self.comment = comment
        self.date_of_submission = datetime.now()
        self.payment_received = False

    @classmethod
    def get_number(cls):
        """
        how much entries do we have?
        """
        return DBSession.query(cls).count()

    @classmethod
    def get_by_id(cls, _id):
        """
        find a dataset by speedfunding id

        this is needed when a user returns from reading her email
        and clicking on a link containing the confirmation code.
        as the code is unique, one record is returned.
        """
        return DBSession.query(cls).filter(
            cls.id == _id).first()

    @classmethod
    def get_by_code(cls, code):
        """
        find a dataset by speedfunding id

        this is needed when a user returns from reading her email
        and clicking on a link containing the confirmation code.
        as the code is unique, one record is returned.
        """
        return DBSession.query(cls).filter(
            cls.speed_id == code).first()

    @classmethod
    def check_for_existing_speed_id(cls, _code):
        """
        check if a code is already present
        """
        check = DBSession.query(cls).filter(
            cls.speed_id == _code).first()
        if check:  # pragma: no cover
            return True
        else:
            return False

    @classmethod
    def speed_listing(cls, order_by, how_many=10, offset=0):
        #print("offset: %s" % offset)
        _how_many = int(offset) + int(how_many)
        _offset = int(offset)
        q = DBSession.query(cls).all()[_offset:_how_many]
        #return q.order_by(order_by)[:how_many]
        return q


Index('speedfunding_index',
      Speedfundings.speed_id,
      unique=True,
      mysql_length=255)


class TheTotal(Base):
    """
    records about how much money we got when
    """
    __tablename__ = 'totals'
    id = Column(Integer, primary_key=True)
    amount_actual = Column(Unicode(255))
    amount_promised = Column(Unicode(255))
    num_shirts = Column(Unicode(255))
    time = Column(DateTime)

    def __init__(self, amount_actual, amount_promised, num_shirts):
        self.amount_actual = amount_actual
        self.amount_promised = amount_promised
        self.num_shirts = num_shirts
        self.time = func.current_timestamp()

    @classmethod
    def get_by_id(cls, _id):
        """
        find a dataset by speedfunding id

        this is needed when a user returns from reading her email
        and clicking on a link containing the confirmation code.
        as the code is unique, one record is returned.
        """
        return DBSession.query(cls).filter(
            cls.id == _id).first()

    @classmethod
    def get_total(cls):
        """
        how much money do we have?
        """
        _id = DBSession.query(cls).count()
        print("_id: %s" % _id)
        # return
        return TheTotal.get_by_id(_id)
        #pass  # read the total from the last entry...

    # @classmethod
    # def get_listing(cls, order_by, how_many=5, offset=0):
    #     """
    #     get the five last entries
    #     """
    #     _we_have = DBSession.query(cls).count()
    #     print("there are %s entries in TheTotal" % _we_have)
    #     _how_many = how_many
    #     _offset = _we_have - 5
    #     print("the offset: %s" % _offset)
    #     q = DBSession.query(cls).all()[_offset:_how_many]
    #     return q
    @classmethod
    def get_listing(cls, order_by):
        """
        get all entries
        """
        return DBSession.query(cls).all()

# machinery and data model for accountants


def hash_password(password):
    return unicode(crypt.encode(password))


class Group(Base):
    """
    groups aka roles for users
    """
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Unicode(30), unique=True, nullable=False)

    def __str__(self):
        return 'group:%s' % self.name

    def __init__(self, name):
        self.name = name

# table for relation between staffers and groups
staff_groups = Table(
    'staff_groups', Base.metadata,
    Column(
        'staff_id', Integer, ForeignKey('staff.id'),
        primary_key=True, nullable=False),
    Column(
        'group_id', Integer, ForeignKey('groups.id'),
        primary_key=True, nullable=False)
)


class C3sStaff(Base):
    """
    C3S staff may login and do things
    """
    __tablename__ = 'staff'
    id = Column(Integer, primary_key=True)
    login = Column(Unicode(255))
    _password = Column('password', Unicode(60))
    last_password_change = Column(
        DateTime,
        default=func.current_timestamp())
    email = Column(Unicode(255))
    groups = relationship(
        Group,
        secondary=staff_groups,
        backref="staff")

    def _init_(self, login, password, email):  # pragma: no cover
        self.login = login
        self.password = password
        #self.last_password_change = datetime.now()
        self.last_password_change = func.current_timestamp()
        self.email = email

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = hash_password(password)

    password = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password)

    @classmethod
    def get_by_login(cls, login):
        #dbSession = DBSession()
        return DBSession.query(cls).filter(cls.login == login).first()

    @classmethod
    def check_password(cls, login, password):
        #dbSession = DBSession()
        staffer = cls.get_by_login(login)
        #if staffer is None:  # ?
        #    return False
        #if not staffer:  # ?
        #    return False
        return crypt.check(staffer.password, password)

    # this one is used by RequestWithUserAttribute
    @classmethod
    def check_user_or_None(cls, login):
        """
        check whether a user by that username exists in the database.
        if yes, return that object, else None.
        returns None if username doesn't exist
        """
        login = cls.get_by_login(login)  # is None if user not exists
        return login
