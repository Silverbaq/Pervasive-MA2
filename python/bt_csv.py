import bluetooth
import sys
import time
import csv

bd_addr = "20:16:01:20:28:49"  # device address
port = 1

input = []

def connect_and_record():
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port))
    print 'Connected'

    try:
        while True:
            data = sock.recv(50)
            print data

            # Checks if the data is ok
            tmp = data.split(',')
            if len(tmp) == 6:
                input.append(data)
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass

    sock.close()    # closes the socket connection
    write_cvs()     # Writes all records to cvs file.


def write_cvs():
    with open('records.csv', 'w') as csvfile:
        fieldnames = ['ax', 'ay', 'az', 'gx', 'gy', 'gz']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in input:
            d = i.split(',')
            ax = d[0]
            ay = d[1]
            az = d[2]
            gx = d[3]
            gy = d[4]
            gz = d[5]
            writer.writerow({'ax': ax, 'ay': ay, 'az': az, 'gx': gx, 'gy': gy, 'gz': gz})


if __name__ == '__main__':
    connect_and_record()