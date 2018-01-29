from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='smartimport',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Christian Klinger',
      author_email='ck@novareto.de',
      url='http://www.novareto.de',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'logbook',
          'click',
          'kombu',
          'amqp',
          'lxml',
          'sqlalchemy',
          'psycopg2',
          'pdbpp',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
