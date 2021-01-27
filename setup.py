from setuptools import setup
import os
import sys
import shutil

added_files = []
size_list = ['32', '48', '64', '72', '96', '128', '256', '512']
if 'linux' in sys.platform:
    # Generate directory for icons
    os.mkdir('icons')

    subdir = ""
    # Icons
    for size in size_list:
        subdir  = 'icons/' + size
        in_file = 'desktop/tor-util-' + size + '.png'
        os.mkdir(subdir)
        shutil.copy(in_file, subdir + '/tor-util.png')
        out_dir = 'share/icons/hicolor/' + size + "x" + size + "/apps/"
        entry   = (out_dir, [subdir + '/tor-util.png'] )
        added_files.append(entry)

    added_files.append(('share/tor-util/'    , ['tor-util.ui']))
    added_files.append(('share/applications/', ['desktop/tor_util.desktop']))

setup(name='tor_util',
      version='0.1.0',
      description='Utility for controling TOR via the API',
      author='GI Jack',
      author_email='GI_Jack@hackermail.com',
      url='https://github.com/GIJack/tor-util',
      packages=['tor_util'],
      license='GPLv3',
      scripts=['tor_util_cli.py', 'tor_util_gui.py'],
      data_files=added_files,
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
          'Topic :: System :: Networking',
      ],
      install_requires = ['PyQt5', 'stem']
     )

shutil.rmtree('icons')
