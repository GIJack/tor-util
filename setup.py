from setuptools import setup
import os
import sys
import tempfile
import shutil

added_files = []
size_list = ['32', '48', '64', '72', '96', '128', '256', '512']
if 'linux' in sys.platform or 'freebsd' in sys.platform or 'openbsd' in sys.platform:
    # Generate directory for icons
    temp_dir_obj = tempfile.TemporaryDirectory("tor-util-icons")
    temp_dir     = temp_dir_obj.name + "/"

    subdir = ""
    # Icons
    for size in size_list:
        subdir  = temp_dir + size
        in_file = 'desktop/tor-util-' + size + '.png'
        os.mkdir(subdir)
        shutil.copy(in_file, subdir + '/tor-util.png')
        out_dir = 'share/icons/hicolor/' + size + "x" + size + "/apps/"
        entry   = (out_dir, [subdir + '/tor-util.png'] )
        added_files.append(entry)

    added_files.append(('share/tor-util/'    , ['tor-util.ui']))
    added_files.append(('share/applications/', ['desktop/tor_util.desktop']))
elif 'win' in sys.platform:
    raise TypeError("Windows support not written yet")
elif 'darwin' in sys.platform:
    raise TypeError("Apple support not written yet")
else:
    raise TypeError("OS " + sys.platform + " not supported!")

#read from requirements.txt
f = open('requirements.txt','r')
dep_list = []
for item in f.readlines():
    item = item.rstrip('\n')
    dep_list.append(item)
f.close()

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
      install_requires = dep_list
     )
# Clean Up temp files
if 'linux' in sys.platform or 'freebsd' in sys.platform or 'openbsd' in sys.platform:
    #shutil.rmtree('icons')
    temp_dir_obj.cleanup()
elif 'win' in sys.platform:
    raise TypeError("Windows support not written yet")
elif 'darwin' in sys.platform:
    raise TypeError("Apple support not written yet")
else:
    raise TypeError("OS " + sys.platform + " not supported!")
