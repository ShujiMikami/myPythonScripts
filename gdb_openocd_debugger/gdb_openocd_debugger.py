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
        out = openocdProc.stderr.read(1)
        if out == '' and openocdProc.poll() != None:
            break
        if out != '':
            sys.stdout.write(out.decode())
            sys.stdout.flush()

gccRunFlag = True
def gccThread(gccProc):
    
    while gccRunFlag == True:
        out = gccProc.stdout.read(1)
        if out == '' and gccProc.poll() != None:
            break
        if out != '':
            sys.stdout.write(out.decode())
            sys.stdout.flush()

OPENOCD_EXECUTABLE = os.environ['ECLIPSE_OPENOCD_BIN_DIR'] + r'\openocd'
 
FW_WORKSPACE_ROOT = r'C:\Users\mm07860\workspace\gohei_system4\FW'
GCC_EXECUTABLE = os.environ['ARM_NONE_EABI_TOOLS_DIR'] + r'\arm-none-eabi-gdb'
os.chdir(FW_WORKSPACE_ROOT)

openocdProc = sp.Popen(OPENOCD_EXECUTABLE + r' -f .\stlink.cfg -f .\stm32f4x.cfg', stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.PIPE)

gccProc = sp.Popen(GCC_EXECUTABLE + r' .\build\gohei_system4_FW.elf', stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.PIPE)

thread_openocd = threading.Thread(target = openocdThread, args=[openocdProc])


thread_openocd.start();

time.sleep(5)

thread_gcc = threading.Thread(target = gccThread, args=[gccProc])

thread_gcc.start()

time.sleep(5)

#gccProc.communicate(input=b"target remote localhost:3333")
gccProc.stdin.write(b"target remote localhost:3333")

time.sleep(30)
sys.stdout.write("30sec elapsed")

gccRunFlag = False
openocdRunFlag = False

openocdProc.kill()
gccProc.kill()


#
#time.sleep(3)
#
#time.sleep(3)
##gccProc.communicate(input=b"interrupt")
##time.sleep(1)
##gccProc.communicate(input=b"monitor reset halt")
##time.sleep(1)
##gccProc.communicate(input=b"load")
##time.sleep(4)
##time.sleep(1)
##gccProc.stdin.write(b"interrupt")
##time.sleep(1)
##gccProc.stdin.write(b"monitor reset halt")
##time.sleep(1)
##gccProc.stdin.write(b"load")
##time.sleep(4)
#
#
#

#res=openocdProc.communicate()
#
#for response in res:
#    print(response.decode())
#
#res = gccProc.communicate()
#
#for response in res:
#    print(response.decode())
#
