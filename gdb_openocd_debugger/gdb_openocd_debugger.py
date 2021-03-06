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
        #out = openocdProc.stderr.read(1)
        #if out == '' and openocdProc.poll() != None:
        #    break
        #if out != '':
        #    sys.stdout.write(out.decode())
        #    sys.stdout.flush()

gccRunFlag = True
def gccThread(gccProc):
    
    while gccRunFlag == True:
        #sys.stdout.write(gccProc.stdout.readline().decode())
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

time.sleep(2)

thread_gcc = threading.Thread(target = gccThread, args=[gccProc])

thread_gcc.start()

time.sleep(2)

gccProc.stdin.write('target remote localhost:3333'.encode("utf8") + b"\n")
gccProc.stdin.flush()
time.sleep(1)
gccProc.stdin.write('interrupt'.encode("utf8") + b"\n")
gccProc.stdin.flush()
time.sleep(1)
gccProc.stdin.write('monitor reset halt'.encode("utf8") + b"\n")
gccProc.stdin.flush()
time.sleep(1)
gccProc.stdin.write('load'.encode("utf8") + b"\n")
gccProc.stdin.flush()

time.sleep(10)
sys.stdout.write("10sec elapsed")

gccRunFlag = False
openocdRunFlag = False

openocdProc.kill()
gccProc.kill()

