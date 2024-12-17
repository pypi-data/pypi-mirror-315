from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='wsgicas',
      version=version,
      description="WSGI CAS (Central Authentication Service) Utilities",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='cas wsgi',
      author='Matthew J Desmarais',
      author_email='matthew.desmarais@gmail.com',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'requests',
          'webob',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
