import bluetooth
import sys
import time
import csv

bd_addr = "20:16:01:20:28:49"  # device address
port = 1

input = []


g = 'OUT'
def connect_and_record():
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port))
    print 'Connected'
    input.append(['ax','ay','az','gx','gy','gz','timestamp','gesture'])
    try:
        while True:
            data = sock.recv(50)


            # Checks if the data is ok
            tmp = data.split(',')

            if len(tmp) == 6:
                t = time.time()
                tmp.append(str(t))
                tmp.append(g)
                tt = str(t)
                tmp[5] = tmp[5][0:-2]
                print tmp
                input.append(tmp)
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass

    sock.close()    # closes the socket connection
    write_cvs(tt,input)     # Writes all records to cvs file.


def write_cvs(tt,data):
    b = open("record"+tt+g+".csv", 'w')
    a = csv.writer(b)
    a.writerows(data)
    b.close()


if __name__ == '__main__':
    connect_and_record()