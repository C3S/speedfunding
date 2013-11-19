import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'Babel',
    'deform',
    'lingua',
    'pyramid',
    'pyramid_beaker',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_localize',
    'pyramid_mailer',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'waitress',
    'zope.sqlalchemy',
]
test_requires = [
    'nose',
    'coverage',
    'webtest',
]
setup(name='speedfunding',
      version='0.0',
      description='speedfunding',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='speedfunding',
      install_requires=requires + test_requires,
      entry_points="""\
      [paste.app_factory]
      main = speedfunding:main
      [console_scripts]
      initialize_speedfunding_db = speedfunding.scripts.initializedb:main
      """,
      message_extractors={
          'speedfunding': [
              ('**.py', 'lingua_python', None),
              ('**.pt', 'lingua_xml', None),
          ]},
      )
