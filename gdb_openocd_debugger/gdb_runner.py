# coding: UTF-8

import os
import subprocess as sp
import time
import io
import sys
import threading


gccRunFlag = True
def gccThread(gccProc):
    
    while gccRunFlag == True:
        out = gccProc.stdout.read(1)
        if out == '' and gccProc.poll() != None:
            break
        if out != '':
            sys.stdout.write(out.decode())
            sys.stdout.flush()

FW_WORKSPACE_ROOT = r'C:\Users\mm07860\workspace\gohei_system4\FW'
GCC_EXECUTABLE = os.environ['ARM_NONE_EABI_TOOLS_DIR'] + r'\arm-none-eabi-gdb'
os.chdir(FW_WORKSPACE_ROOT)

gccProc = sp.Popen(GCC_EXECUTABLE + r' .\build\gohei_system4_FW.elf', stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.PIPE)

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

time.sleep(5)


gccRunFlag = False

gccProc.kill()

