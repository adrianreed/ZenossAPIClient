from setuptools import find_packages, setup

name = 'ZenossAPIClient'
version = '0.1'
release = '0.1.1'

setup(name=name,
      version=release,
      description='Zenoss API client module',
      long_description="""
Python module for interacting with the Zenoss API an an object-oriented way.
The philosophy here is to use objects to work with everything in the Zenoss 
API, and to try to normalize the various calls to the different routers.
Thus `get` methods will always return an object, `list` methods will return 
data. All methods to add or create start with `add`, all remove or delete 
start with `delete`. As much as possible the methods try to hide the 
idiosyncrasies of the JSON API, and to do the work for you, for example 
by letting you use a device name instead of having to provide the full 
device UID for every call.
""",
      url='https://github.com/Zuora-TechOps/ZenossAPIClient',
      author='Mark Troyer',
      author_email='disco@zuora.com',
      license='Apache',
      classifiers=[
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Natural Language :: English',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Topic :: System :: Monitoring',
      ],
      keywords='Zenoss monitoring api',
      packages=find_packages(where='src'),
      package_dir={'': 'src'},
      zip_safe=False,
      tests_require=[
          'pytest>=3.2.3',
          'pytest-responses>=0.3.0',
      ],
      install_requires=[
          'python-dateutil>=2.6.1',
          'requests>=2.18.1',
      ]
      )
