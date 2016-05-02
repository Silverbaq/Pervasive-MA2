import bluetooth
import sys
import time
bd_addr = "20:16:01:20:28:49" #itade address

port = 1
sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))
print 'Connected'

while True:
    data = sock.recv(50)
    print data
    time.sleep(0.5)


sock.close()
