import bluetooth
import sys
import time
bd_addr = "20:16:01:20:28:49" #itade address

port = 1
sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))
print 'Connected'
#sock.settimeout(1.0)
#sock.send("x")
#print 'Sent data'

while True:

    data = sock.recv(50)
    print 'received [%s]'%data
    time.sleep(1)

sock.close()
