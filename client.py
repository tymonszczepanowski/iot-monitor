import socket
import threading
import time
import random


class Client():
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._running = False

    def __str__(self):
        return 'Client object, host: {}, port: {}, running: {}'.format(self._host, self._port, self._running)
    
    def run(self):
        self._running = True
        self._socket.connect((self._host, self._port))
        print('Socket connected, host: {}, port: {}'.format(self._host, self._port))
        while self._running:
            time.sleep(5)
            value = random.randint(1, 100)
            self._socket.sendall(bytes(str(value), 'utf-8'))

    def disconnect(self):
        print('Disconnecting!')
        self._running = False
        self._socket.sendall(b'Client disconnecting!')
        self._socket.close()
        

def main():
    client = Client('localhost', 10000)
    print(client)
    thread = threading.Thread(target=client.run)
    thread.start()
    while True:
        print('Press x to stop')
        response = str(input())
        if response == 'x':
            client.disconnect()
            break
    thread.join()
    print('Exit')
    return 0

if __name__ == '__main__':
    main()
