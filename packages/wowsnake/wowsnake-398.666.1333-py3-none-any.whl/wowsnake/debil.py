#!/usr/bin/env python3
from subprocess import Popen
import sys

print('готовимся запустить процесс')
Popen([sys.executable, '-c', 'import time; import wowsnakes; time.sleep(3); print("дит vodka I debilё")'])
print('выходим')
