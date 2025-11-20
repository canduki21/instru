# Client Program
import socket
import threading
import os
import sys
import select
from time import sleep

class Transmit(threading.Thread):
    def run(self):
        global s  
        global threadRunning
        while(threadRunning):
            # Check keyboard input every 1 second
            i, o, e = select.select([sys.stdin], [], [], 1)
            if i:
                user_input = sys.stdin.readline().strip() + "\r\n"
                s.sendall(user_input.encode())
                print("Sent to LabVIEW:", user_input.strip())

class Receive(threading.Thread):
    def run(self):
        global s  
        global threadRunning
        while(threadRunning):
            ready = select.select([s], [], [], 1)
            if ready[0]:
                data = s.recv(1024).strip()
                if len(data) == 0:
                    threadRunning = False
                else:
                    msg = data.decode("utf-8")
                    print("LABVIEW SAYS:", msg)
            sleep(0.1)


HOST = '192.168.1.72'   # <--- YOUR WINDOWS IP
PORT = 5000             # <--- YOUR LABVIEW PORT

threadRunning = True
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

os.system('clear')
print("Connected to LabVIEW server")
print("---------------------------------------")
print("   TYPE ANY MESSAGE TO SEND TO LABVIEW")
print("   Press CTRL+C to close.")
print("---------------------------------------")

try:
    # Start receiving messages
    receive = Receive()
    receive.start()

    # Start allowing manual typing
    transmit = Transmit()
    transmit.start()

    while threadRunning:
        sleep(0.1)

except KeyboardInterrupt:
    threadRunning = False
    sleep(1)
    s.close()

finally:
    s.close()
