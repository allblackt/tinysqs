# -*- coding: utf-8 -*-

from distutils.core import setup

install_requires = ['requests >= 1.2.0']

tests_require = ['pytest', 'pytest-cov', 'pytest-raisesregexp']

setup(name='tinysqs',
      version='0.0.1',
      description=("A small library for interacting with SQS queues: getting "
                   "messages, sending messages."),

      author='Tudor Tabacel',
      author_email='tudorsmt@gmail.com',
      url='https://github.com/allblackt/tinysqs',
      packages=['tinysqs'],
      license='MIT',
      classifiers=[
          # make sure to use :: Python *and* :: Python :: 3 so
          # that pypi can list the package on the python 3 page
          'Programming Language :: Python',
          'Programming Language :: Python :: 3'
      ],

      platforms='Any',
      keywords=('amazon', 'aws', 'sqs'),

      package_dir={'': '.'},
      install_requires=install_requires,
      tests_require=tests_require,
      test_suite='tinysqs.tests')
