import socket
import threading
import time
import mysql.connector
import matplotlib.pyplot as plt
from flask import Flask
from flask import render_template

class Database():
    def __init__(self, host, user):
        self._host = host
        self._user = user
        self._passwd = self._get_credentials()

    def select(self, name):
        db = mysql.connector.connect(
            host=self._host,
            user=self._user,
            password=self._passwd,
            database='iot'
        )
        cursor = db.cursor(buffered=True)
        expression = 'SELECT value, time FROM devices WHERE name="{}"'.format(name)
        cursor.execute(expression)
        values = []
        timestamps = []
        for value, time in cursor:
            values.append(value)
            timestamps.append(time)
        cursor.close()
        return values, timestamps

    def _get_credentials(self):
        credentials = open('credentials', 'r').read()
        return credentials.split('=')[1].replace('\n', '')


app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def monitor():
    database = Database('localhost', 'root')
    values_a, timestamps_a = database.select('distance_arduino')
    values_e, timestamps_e = database.select('distance_esp')
    fig, axs = plt.subplots(2)
    fig.suptitle('IOT Monitor', fontsize=16)
    fig.subplots_adjust(hspace=2)
    fig.set_size_inches(18.5, 10.5)

    axs[0].set_title('Distance - Arduino [cm]')
    axs[0].plot(timestamps_a, values_a, label='Distance ARDUINO')
    axs[0].set_xlabel('Timestamp')
    axs[0].set_ylabel('Distance [cm]')
    if len(timestamps_a) >= 10:
        ticks_a = list(range(1, len(timestamps_a), int(len(timestamps_a)/10)))
        labels_a = [timestamps_a[index] for index in ticks_a]
        axs[0].set_xticks(ticks_a)
        axs[0].set_xticklabels(labels_a, rotation=-45)

    axs[1].set_title('Distance - ESP32 [cm]')
    axs[1].plot(timestamps_e, values_e, label='Distance ESP')
    axs[1].set_xlabel('Timestamp')
    axs[1].set_ylabel('Distance [cm]')
    if len(timestamps_e) >= 10:
        ticks_e = list(range(1, len(timestamps_e), int(len(timestamps_e)/10)))
        labels_e = [timestamps_e[index] for index in ticks_e]
        axs[1].set_xticks(ticks_e)
        axs[1].set_xticklabels(labels_e, rotation=-45)
    
    plt.savefig('static/figure.png')
    return render_template('index.html', image='static/figure.png')
