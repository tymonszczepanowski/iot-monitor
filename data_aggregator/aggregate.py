import socket
import threading
import time
import mysql.connector

class Database():
    def __init__(self, host, user):
        self._host = host
        self._user = user
        self._passwd = self._get_credentials()
        self._db_init()
    
    def _db_init(self):
        db = mysql.connector.connect(
            host=self._host,
            user=self._user,
            password=self._passwd
        )
        cursor = db.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS iot')
        cursor.close()

        db = mysql.connector.connect(
            host=self._host,
            user=self._user,
            password=self._passwd,
            database='iot'
        )
        cursor = db.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS devices (name VARCHAR(255), value INT)')
        cursor.close()
        print('Db init done!')

    def insert(self, name, value):
        db = mysql.connector.connect(
            host=self._host,
            user=self._user,
            password=self._passwd,
            database='iot'
        )
        cursor = db.cursor()
        expression = 'INSERT INTO devices VALUES ("{}", "{}")'.format(name, value)
        print(expression)
        cursor.execute(expression)
        db.commit()
        cursor.close()

    def _get_credentials(self):
        credentials = open('credentials', 'r').read()
        return credentials.split('=')[1].replace('"','')
        

class Server():
    def __init__(self, host, port, database):
        self._host = host
        self._port = port
        self._db = database
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._running = False
        self._device_name = self._get_name()
    
    def __str__(self):
        return 'Server object, host: {}, port: {}, device: {}'.format(self._host, self._port, self._device_name)

    def run(self):
        self._running = True
        self._socket.bind((self._host, self._port))
        self._socket.listen()
        print('Socket binded on {} to {} and is listening'.format(self._host, self._port))
        while self._running:
            connection, address = self._socket.accept()
            with connection:
                print('Connected by {}'.format(address))
                while True:
                    data = connection.recv(1024)
                    if data:
                        print('Received data: {}'.format(data.decode()))
                        print('### Should insert: {}'.format(int(data.decode())))
                        self._db.insert(self._device_name, int(data.decode()))

    def _get_name(self):
        if self._port == 10000:
            return 'distance'
        if self._port == 20000:
            return 'interruption'
        
    def disconnect(self):
        print('Disconnecting!')
        self._running = False
        self._socket.close()


def main():
    database = Database('localhost', 'root')
    server = Server('localhost', 10000, database)
    print(server)
    server.run()


if __name__ == '__main__':
    main()
