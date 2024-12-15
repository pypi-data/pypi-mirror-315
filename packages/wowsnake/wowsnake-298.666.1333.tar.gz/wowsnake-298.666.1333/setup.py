from setuptools import setup, find_packages
import codecs
import os

VERSION = '298.666.1333'
DESCRIPTION = 'Stupid gamedeveloper games example'

def readme():
  with open('README.md', 'r') as f:
    return f.read()

# Setting up
setup(
    name="wowsnake",
    version=VERSION,
    author="dclxviclan (dclxviclan)",
    author_email="<dclxviclan@gmail.com>",
    description="👁👄👁💬 import💢🚸🧞‍♀️/x  and play 🎃👻🍬",
    packages=find_packages(),
    install_requires=['colorama'],
    keywords=['python', 'game', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
