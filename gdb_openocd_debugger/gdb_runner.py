# coding: UTF-8

import os
import subprocess as sp
import time
import io
import sys
import threading


gdbRunFlag = True
def gdbThread(gdbProc):
    
    while gdbRunFlag == True:
        out = gdbProc.stdout.read(1)
        if out == '' and gdbProc.poll() != None:
            break
        if out != '':
            sys.stdout.write(out.decode())
            sys.stdout.flush()

FW_WORKSPACE_ROOT = r'C:\Users\mm07860\workspace\gohei_system4\FW'
GDB_EXECUTABLE = os.environ['ARM_NONE_EABI_TOOLS_DIR'] + r'\arm-none-eabi-gdb'
os.chdir(FW_WORKSPACE_ROOT)

gdbProc = sp.Popen(GDB_EXECUTABLE + r' .\build\gohei_system4_FW.elf', stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.PIPE)

thread_gdb = threading.Thread(target = gdbThread, args=[gdbProc])

thread_gdb.start()

time.sleep(2)

gdbProc.stdin.write('target remote localhost:3333'.encode("utf8") + b"\n")
gdbProc.stdin.flush()
time.sleep(1)
gdbProc.stdin.write('interrupt'.encode("utf8") + b"\n")
gdbProc.stdin.flush()
time.sleep(1)
gdbProc.stdin.write('monitor reset halt'.encode("utf8") + b"\n")
gdbProc.stdin.flush()
time.sleep(1)
gdbProc.stdin.write('load'.encode("utf8") + b"\n")
gdbProc.stdin.flush()

time.sleep(5)


gdbRunFlag = False

gdbProc.kill()

