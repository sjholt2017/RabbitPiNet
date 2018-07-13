####################################################################################
#
# Program: logonMessage
# Version: 1.2
# Date: 13/07/2018
#
# Description: Sends the details of the logon id to the RabbitMQ server (PiRMQ01)
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
    host         = "192.168.1.200",
    credentials  = mq_creds,
    virtual_host = "/")

mq_exchange    = "amq.topic"
mq_routing_key = "PiCloud"
mq_routing_key2 = "BlueMix"

# This a connection object
mq_conn = pika.BlockingConnection(mq_params)

# This is one channel inside the connection
mq_chan = mq_conn.channel()

# Get user ID for message
user_id = os.environ['USER'] 
server_name = socket.gethostname()
if server_name == "sjholt.webhop.me":
    server_name = "PiRMQ01"

# Create timestamp
ts = time.time()
messageDatetime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

# Create message text
messageType = "WARN"
messageBody = "Logon >> Server: " + server_name + " >> ID:" + user_id
messageText = messageDatetime + " [" + messageType + "] " + messageBody
messageText2 = "INSERT INTO rabbitpimessagelog (message_type, message_body, message_datetime) VALUES ('" + messageType + "','" + messageBody + "','" +  messageDatetime + "');"

# Publish message to RabbitMQ listener (RabbitMQ PiCloud queue)
mq_chan.basic_publish(
      	exchange    = mq_exchange,
      	routing_key = mq_routing_key,
      	body        = messageText)

# Publush message to message log table (RabbitMQ Bluemix queue)
mq_chan.basic_publish(
      	exchange    = mq_exchange,
      	routing_key = mq_routing_key2, 
      	body        = messageText2)
