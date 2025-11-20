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
            i, o, e = select.select([sys.stdin], [], [], 1)
            if(i):
                string = sys.stdin.readline().strip() + '\r\n'
                byteArray = bytearray(string, "utf-8")
                s.sendall(byteArray)
        return

class Receive(threading.Thread):
    def run(self):
        global s
        global threadRunning
        while(threadRunning):
            ready = select.select([s], [], [], 1)
            if(ready[0]):
                data = s.recv(1024).strip()
                if(len(data) == 0):
                    threadRunning = False
                else:
                    print('Received:', data.decode("utf-8"))
            sleep(0.1)
        return

HOST = '192.168.1.72'   # <--- CHANGE TO WINDOWS IP
PORT = 5000             # <--- CHANGE TO YOUR LABVIEW PORT

threadRunning = False
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

os.system('clear')
print('Connection with server established')

try:
    print(34 * '-')
    print("        M A I N - M E N U")
    print(' Press CTRL+C to close connection')
    print(34 * '-')

    threadRunning = True

    # Start receiving (keep this)
    receive = Receive()
    receive.start()

    # OPTIONAL: start transmit thread if you want keyboard send
    # transmit = Transmit()
    # transmit.start()

    while(threadRunning):
        sleep(0.1)

except KeyboardInterrupt:
    threadRunning = False
    sleep(1)
    s.close()

finally:
    s.close()
