import serial
from serial.tools import list_ports
import socket
import time

def get_serial():
    port = None
    if  len(list_ports.comports()) == 0:
        return None
    
    for p in list_ports.comports():
        if 'Arduino' in p.description:
            port = p.device
            
    if port == None:
        return None
    
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = port
    ser.timeout = .01
    return ser


def test(ser):
    buffer = ser.read(ser.inWaiting())
    data = str(buffer).split('\\r\\n')[-2]
    print(f'Test: {data}')
    ser.flushInput()
    return data

if __name__ == "__main__":
    ser = get_serial()   
    if ser is not None:
        with ser:
            host = 'localhost'
            port = 10000
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                while True:
                    time.sleep(5)
                    data = test(ser)
                    s.sendall(bytes(str(data), 'utf-8'))
    else:
        print("No Arduino board available")
