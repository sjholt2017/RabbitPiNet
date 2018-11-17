####################################################################################
#
# Program: heartbeat
# Version: 1.2
# Date: 13/07/2018
#
# Description: Sends an 'heartbeat' message to the RabbitMQ server (PiRMQ01)
#
####################################################################################
#!/usr/bin/python
import pika
import time
import datetime
import sys
import os
import socket

# Use plain credentials for authentication
mq_creds  = pika.PlainCredentials(
    username = "webmessage",
    password = "guest")

# Use localhost
mq_params = pika.ConnectionParameters(
#    host         = "192.168.1.200",
    host         = "sjholt.webhop.me",
    credentials  = mq_creds,
    virtual_host = "/")

mq_exchange    = "amq.topic"
mq_routing_key = "PiCloud"
mq_routing_key2 = "BlueMix"

# This a connection object
mq_conn = pika.BlockingConnection(mq_params)

# This is one channel inside the connection
mq_chan = mq_conn.channel()

server_name = socket.gethostname()
if server_name == "sjholt.webhop.me":
	server_name = "PiRMQ01"

messageType = "INFO"
messageBody = "Heartbeat >> Server:" + server_name + " >> Status:OK"

ts = time.time()
messageDatetime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

# Create message for Online Queue Monitor
messageText = messageDatetime + " [" + messageType + "] " + messageBody

# Create messages for MySQL Database
messageText2 = "INSERT INTO rabbitpimessagelog (message_type, message_body, message_datetime) VALUES ('" + messageType + "','" + messageBody + "','" + messageDatetime + "');"
messageText3 = "UPDATE server_status set server_status = 1, last_updated = now() WHERE server_name = '" + server_name + "';"

# Send message to RabbitMQ listener
mq_chan.basic_publish(
        exchange    = mq_exchange,
        routing_key = mq_routing_key,
        body        = messageText)

# Send message to message log table
mq_chan.basic_publish(
        exchange    = mq_exchange,
        routing_key = mq_routing_key2,
        body        = messageText2)

# send message to server status table
mq_chan.basic_publish(
        exchange    = mq_exchange,
        routing_key = mq_routing_key2,
        body        = messageText3)
