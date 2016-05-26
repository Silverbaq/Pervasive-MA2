import bluetooth
import sys
import time
import csv
import curses
import weka

bd_addr = "20:16:01:20:28:49"  # device address
port = 1


g = 'OUT'


def connect_and_record():
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port))

    g_count = 0

    run = False

    res = ""

    print 'Connected'
    # input.append(['ax','ay','az','gx','gy','gz','timestamp','gesture'])
    try:


        print 'Start!!!'

        i = 0

        while True:
            print "gesture # " + str(g_count)
            data = ''
            input = []
            i = 0
            while i < 40: # read data
                data += sock.recv(50)
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
            input.append(g)
            if len(input) == 181:
                write_cvs(input)
            else:
                print "Failed gesture"

            g_count = g_count +1

    except KeyboardInterrupt:
        pass



    sock.close()    # closes the socket connection



def write_cvs(data):
    b = open("record123.csv", 'a')
    a = csv.writer(b)
    a.writerow(data)
    b.close()


if __name__ == '__main__':
    connect_and_record()