import bluetooth
import time
import csv
from weka import *


# Bluetooth
bd_addr = "20:16:01:20:28:49"  # device address
bt_port = 1
bt_sock = None


def connect_and_run():
    #connect_to_bluetooth()
    bt_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    bt_sock.connect((bd_addr, bt_port))
    print 'Connected to braclet via Bluetooth %s' % bd_addr

    raw_input("Press Enter to continue...")
    try:
        while True:
            #print "new gesture"
            data = ''
            input = []
            i = 0
            while i < 40: # read data
                data += bt_sock.recv(50)
                i = i + 1
                time.sleep(0.06)


            tmp = data.split('\n')

            for r in tmp:
                tmp2 = r.split(',')
                if len(tmp2) >= 7 and tmp2[0] == 'h':
                    input.append(tmp2[1])
                    input.append(tmp2[2])
                    input.append(tmp2[3])
                    input.append(tmp2[4])
                    input.append(tmp2[5])
                    input.append(tmp2[6])

            input = input[0:180]

            if len(input) == 180:
                # TODO: Implement Weka
                print "SOMETHING"
            else:
                #print "Failed gesture"
                p = "Failed gesture"

            #g_count = g_count +1

    except KeyboardInterrupt:
        pass


    disconnect_from_bluetooth() # closes the bluetooth socket connection



def disconnect_from_bluetooth():
    bt_sock.close()

if __name__ == '__main__':
    connect_and_run()