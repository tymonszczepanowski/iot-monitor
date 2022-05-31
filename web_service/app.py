import socket
import threading
import time
import base64
import mysql.connector
import matplotlib.pyplot as plt
from flask import Flask
from flask import render_template
from io import BytesIO

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
    values_d, timestamps_d = database.select('distance')
    values_i, timestamps_i = database.select('interruption')
    fig, axs = plt.subplots(2)
    fig.suptitle('IOT Monitor', fontsize=16)
    fig.subplots_adjust(hspace=2)
    fig.set_size_inches(18.5, 10.5)

    axs[0].set_title('Distance - ESP32 [cm]')
    axs[0].plot(timestamps_d, values_d, label='Distance')
    axs[0].set_xlabel('Timestamp')
    axs[0].set_ylabel('Distance [cm]')
    if len(timestamps_d) >= 10:
        ticks_d = list(range(1, len(timestamps_d), int(len(timestamps_d)/10)))
        labels_d = [timestamps_d[index] for index in ticks_d]
        axs[0].set_xticks(ticks_d)
        axs[0].set_xticklabels(labels_d, rotation=-45)

    axs[1].set_title('Interruption - Arduino')
    axs[1].plot(timestamps_i, values_i, label='Interruption')
    axs[1].set_xlabel('Timestamp')
    axs[1].set_ylabel('Interruption')
    if len(timestamps_i) >= 10:
        ticks_i = list(range(1, len(timestamps_i), int(len(timestamps_i)/10)))
        labels_i = [timestamps_i[index] for index in ticks_i]
        axs[1].set_xticks(ticks_i)
        axs[1].set_xticklabels(labels_i, rotation=-45)
    
    plt.savefig('static/figure.png')
    return render_template('index.html', image='static/figure.png')
