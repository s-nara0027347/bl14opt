#!/opt/local/bin/python3

import sys
import struct
import socket
from time import time,sleep

host = '192.168.67.39'
port = 6510
waittime = 0.04
BUFSIZ = 1024

header_format = "Ii4I2i3I2i80s"
len_ = 0
name = b""

if (len(sys.argv) < 2):
    print("Usage:  "+sys.argv[0]+" command")
    print("Example: "+sys.argv[0]+" ct")
    print("Example: "+sys.argv[0]+" abort (send Cntl+C)")
    sys.exit()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))

    sec = time()
    usec = 1000000*(sec-int(sec))

    cmd = 14 # SV_HELLO
    spec_head = struct.pack(header_format,0xFEEDFACE,4,132,1,\
                        int(sec),int(usec),cmd,0,0,0,len_,0,0,name)
    sock.send(spec_head)
    sleep(waittime)
    print("Connected to "+sock.recv(BUFSIZ)[132:].decode()+".")

    if (sys.argv[1] == "abort"):
        print("Send cntl+C to server.")
        cmd = 2 #SV_ABORT
        len_ = 0
        spec_head = struct.pack(header_format,0xFEEDFACE,4,132,1,\
                            int(sec),int(usec),cmd,0,0,0,len_,0,0,name)
        sock.send(spec_head)
    else:
        print("Execute \""+sys.argv[1]+"\" on server.")
        cmd = 3 # SV_CMD
        com = sys.argv[1].encode()+b"\0"
        len_ = len(com)
        spec_head = struct.pack(header_format,0xFEEDFACE,4,132,1,\
                            int(sec),int(usec),cmd,0,0,0,len_,0,0,name)
        sock.send(spec_head)
        sock.send(com)
