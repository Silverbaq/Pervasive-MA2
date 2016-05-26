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

base_data = []
base_gesture = []


def connect_and_run():
    connect_to_bluetooth()

    raw_input("Press Enter to continue...")
    try:
        while True:
            print "gesture # " + str(g_count)
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
                res = convert_and_calc_input(input)
                write_cvs(res)
                print "data has been written"
            else:
                #print "Failed gesture"
                p = "Failed gesture"

            g_count = g_count +1

    except KeyboardInterrupt:
        pass


    disconnect_from_bluetooth() # closes the bluetooth socket connection


# *** Bluetooth socket ***
def connect_to_bluetooth():
    bt_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    bt_sock.connect((bd_addr, bt_port))
    print 'Connected to braclet via Bluetooth %s' % bd_addr


def disconnect_from_bluetooth():
    bt_sock.close()


# *** Load data ***
def load_base_data():
    with open('model.vector', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            base_data.append(row[0])
            base_gesture(row[1])


# *** Save data ***
def write_cvs(data):
    b = open("vectors.csv", 'w')
    a = csv.writer(b)
    a.writerow(data)
    b.close()


def convert_and_calc_input(spamreader):
    for row in spamreader:
        vec_row = []
        count = 0

        row_split = row[0].split(',')
        row_split = row_split[:180]

        row_split2 = map(int, row_split)

        vec = [0,0,0,0,0,0]

        while count < 174: # Last set is only used once
            ax1 = row_split2[count]
            ay1 = row_split2[count + 1]
            az1 = row_split2[count + 2]
            gx1 = row_split2[count + 3]
            gy1 = row_split2[count + 4]
            gz1 = row_split2[count + 5]

            ax2 = row_split2[count + 6]
            ay2 = row_split2[count + 7]
            az2 = row_split2[count + 8]
            gx2 = row_split2[count + 9]
            gy2 = row_split2[count + 10]
            gz2 = row_split2[count + 11]

            a = [ax2 - ax1, ay2 - ay1, az2 - az1, gx2 - gx1, gy2 - gy1, gz2 - gz1]

            #add to line total vector
            vec[0]+= a[0]
            vec[1]+= a[1]
            vec[2]+= a[2]
            vec[3]+= a[3]
            vec[4]+= a[4]
            vec[5]+= a[5]

            count = count + 6  # Increase indexing

            vec_row.append(vec)
    return vec_row


if __name__ == '__main__':
    load_base_data()
    connect_and_run()