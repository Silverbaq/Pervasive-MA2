import bluetooth
import time
import csv

from weka.core.converters import Loader

import socket
import sys

# Bluetooth
bd_addr = "20:16:01:20:28:49"  # device address
bt_port = 1
bt_sock = None

# Socket Connection
sock = None
socket_ip = "localhost"
socket_port = 5000

# Weka fields
data_dir = "/my/datasets/"


def connect_and_run():
    connect_to_bluetooth()
    connect_to_socketserver()

    raw_input("Press Enter to continue...")
    try:
        data = ''

        while True:
            data += bt_sock.recv(50)  # Reads data from bluetooth socket

            # TODO: Use Weka
            



            time.sleep(0.05)

    except KeyboardInterrupt:
        pass


    disconnect_from_bluetooth() # closes the bluetooth socket connection
    disconnect_from_socketserver() # closes the TCP socket connection.


# *** Bluetooth socket ***
def connect_to_bluetooth():
    bt_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    bt_sock.connect((bd_addr, bt_port))
    print 'Connected to braclet via Bluetooth %s' % bd_addr


def disconnect_from_bluetooth():
    bt_sock.close()


# *** Socket Client ***
def connect_to_socketserver():
    #Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (socket_ip, socket_port)
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


# *** Weka ***
def load_dataset():
    loader = Loader(classname="weka.core.converters.ArffLoader")
    data = loader.load_file(data_dir + "iris.arff")
    data.class_is_last()
    print(data)





if __name__ == '__main__':
    connect_and_run()