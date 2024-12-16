from setuptools import setup, find_packages
import codecs
import os

VERSION = '420.666.1333'
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
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://youtube.com/@dclxviclan',
    packages=find_packages(),
    install_requires=['colorama'],
    keywords=['python', 'game', 'terminalgame', 'consolegame', 'snake', 'dclxviclan', 'shell', 'terminal', 'cmd'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
