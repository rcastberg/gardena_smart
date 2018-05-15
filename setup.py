from setuptools import setup

setup(name='gardena_smart',
      version='0.11b2',
      description='Library to access the gardena smart platform',
      long_description="""This is an attempt at creating a library for the
      gardena smart system in python. At the moment it is a work in progress and not
      all components are supported. At the moment we only have read only access
      to the mower component. Please see github page for more information""",
      url='http://github.com/rcastberg/gardena_smart',
      author='Rene Castberg',
      author_email='rene@castberg.org',
      license='GPL',
      packages=['gardena_smart'],
      zip_safe=False)
