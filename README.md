# IOT monitor
Simple application to send data from IOT devices' sensors to host and provide user with Zabbixlike monitor. Tested with one Arduino UNO and one ESP32 boards and two H2SR04 ultrasonic sensors. Web application is written in Flask and we use three Docker containers to run it.
### Topology
#### IOT devices
**Arduino** <br/>
Connected to host through COM port using USB cable. Python client for arduino scans serial port and uses socket to send data to containerized  aggregator. <br/>
**ESP32** <br/>
Connected to the same wireless network as host. It uses socket with hosts' static ip to send data to containerized  aggregator.
#### Containerized applications
**Data Aggregator** <br/>
Containerized app with two listening sockets running in parallel. It initiates and sends received data into Containerized mysql database. Image based on python:3.8-slim-buster. <br/>
**MySQL Database** <br/>
For database, we use Docker Official Image for MySQL and run it in a container. <br/>
**Flask Web Monitor** <br/>
Containerized app made using Flask framework. It creates pyplot figures with data from the database. It automatically refreshes every 10 seconds. <br/>
### How to run it?
Firstly, you need to upload programs to Arduino and ESP32 boards. Then you need to run bash scripts from docker directory in the following order:
1. run_db.sh
1. run_aggregator.sh
1. run_monitor.sh

Next you need to run python client for Arduino and make sure your ESP32 works correctly. After that you are all set and the monitor should be available on the localhost, port 5000.
### Todo list:
- [ ] Run the app on the Raspberry Pi
- [ ] Create better connection string between containers (stop using host's network)
- [ ] Replace bash scripts with docker-compose
### Authors: Bartosz Kowalski, Tymon Szczepanowski
