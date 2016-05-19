import bluetooth
import sys
import time
import csv
import curses
import weka

import socket
import sys

# Bluetooth
bd_addr = "20:16:01:20:28:49"  # device address
port = 1

#Socket Connection
sock = None
socket_ip = "localhost"


def connect_and_run():
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port))
    print 'Connected to braclet via Bluetooth %s' % bd_addr

    connect_to_socketserver()

    raw_input("Press Enter to continue...")
    try:
        data = ''

        while True:
            data += sock.recv(50)  # Reads data from bluetooth socket

            # TODO: Use Weka

            time.sleep(0.05)

    except KeyboardInterrupt:
        pass


    sock.close()    # closes the bluetooth socket connection
    disconnect_from_socketserver() # closes the TCP socket connection.


def connect_to_socketserver():
    #Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (socket_ip, 5000)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)


def disconnect_from_socketserver():
    print >>sys.stderr, 'closing socket'
    sock.close()


def send_message(message):
    try:
        # Send data
        print >>sys.stderr, 'sending "%s"' % message
        sock.sendall(message)
    except Exception as ex:
        print ex.message






if __name__ == '__main__':
    connect_and_run()