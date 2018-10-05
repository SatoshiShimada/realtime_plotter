import serial
import socket
import threading
from multiprocessing import Value

sensor_x = Value('d')
sensor_y = Value('d')
sensor_z = Value('d')

def readSensor():
    baudrate = 256000
    with serial.Serial('/dev/ttyAMA0', baudrate, timeout=1.0) as SerialData:
        msg = ''
        count = 0
        while True:
            c = SerialData.read()
            if c != ' ' and c != ',':
                msg += c
            if c == ',':
                if count == 0:
                    with sensor_x.get_lock():
                        try:
                            sensor_x.value = float(msg)
                        except ValueError:
                            print("error")
                elif count == 1:
                    with sensor_y.get_lock():
                        try:
                            sensor_y.value = float(msg)
                        except ValueError:
                            print("error")
                msg = ' '
                count += 1
                if count > 2:
                    count = 0
            elif c == ' ':
                try:
                    value = float(msg)
                    with sensor_z.get_lock():
                        sensor_z.value = value
                except ValueError:
                    print("error")
                msg = ''
                count = 0

def sendValue():
    host = '127.0.0.1'
    port = 10003
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        v = [0.0, 0.0, 0.0]
        with sensor_x.get_lock():
            v[0] = sensor_x.value
        with sensor_y.get_lock():
            v[1] = sensor_y.value
        with sensor_z.get_lock():
            v[2] = sensor_z.value
        m = str(v[0]) + ',' + str(v[1]) + ',' + str(v[2])
        m = str(m).encode('ascii')
        conn.sendall(m)
        conn.close()

if __name__ == '__main__':
    th1 = threading.Thread(target=readSensor)
    th2 = threading.Thread(target=sendValue)
    th1.start()
    th2.start()
    th1.join()
    th2.join()

