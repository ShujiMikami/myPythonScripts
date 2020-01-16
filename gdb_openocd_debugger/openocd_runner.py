# coding: UTF-8

import os
import subprocess as sp
import time
import io
import sys
import threading


openocdRunFlag = True
def openocdThread(openocdProc):
   
    while openocdRunFlag == True:
        sys.stdout.write(openocdProc.stderr.readline().decode())

OPENOCD_EXECUTABLE = os.environ['ECLIPSE_OPENOCD_BIN_DIR'] + r'\openocd'
 
FW_WORKSPACE_ROOT = r'C:\Users\mm07860\workspace\gohei_system4\FW'
os.chdir(FW_WORKSPACE_ROOT)

openocdProc = sp.Popen(OPENOCD_EXECUTABLE + r' -f .\stlink.cfg -f .\stm32f4x.cfg', stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.PIPE)

thread_openocd = threading.Thread(target = openocdThread, args=[openocdProc])

thread_openocd.start();
try:
    openocdProc.wait()

    openocdRunFlag = False

    openocdProc.kill()
except KeyboardInterrupt:
    openocdRunFlag = False

    openocdProc.kill()

    sys.exit()


