from setuptools import setup
import os

setup(name='tor_util',
      version='0.1.0',
      description='Utility for controling TOR via the API',
      author='GI Jack',
      author_email='GI_Jack@hackermail.com',
      url='https://github.com/GIJack/tor-util',
      packages=['tor_util'],
      license='GPLv3',
      scripts=['tor_util_cli.py', 'tor_util_gui.py'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: X11 Applications :: Qt',
          'Intended Audience :: End Users/Desktop',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX :: Linux',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Utilities',
      ],
      install_requires = ['PyQt5', 'stem']
     )
