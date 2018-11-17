####################################################################################
#
# Program: topProc
# Version: 1.2
# Date: 13/07/2018
#
# Description: Checks the top running process and sends the details to the RabbiMQ 
# server (PiRMQ01)
#
####################################################################################
#!/usr/bin/python
import pika
import time
import datetime
import sys
import os
import socket
import commands

topProc = commands.getoutput("top -bn1 | sed -n '8,8'p | awk -v N=12 '{print $N}'")
#print topProc

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

# Get user ID for message
server_name = socket.gethostname()
if server_name == "sjholt.webhop.me":
    server_name = "PiRMQ01"

# Create timestamp
ts = time.time()
messageDatetime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

# Create message text
messageType = "INFO"
messageBody = "Top Process >> Server: " + server_name + " >> Process:" + topProc
messageText = messageDatetime + " [" + messageType + "] " + messageBody
messageText2 = "INSERT INTO rabbitpimessagelog (message_type, message_body, message_datetime) VALUES ('" + messageType + "','" + messageBody + "','" +  messageDatetime + "');"

#print messageText

# Publish message to RabbitPi queue
mq_chan.basic_publish(
      	exchange    = mq_exchange,
      	routing_key = mq_routing_key,
      	body        = messageText)

# Publush message to NodeRed queue
mq_chan.basic_publish(
      	exchange    = mq_exchange,
      	routing_key = mq_routing_key2, 
      	body        = messageText2)

# Send message to general slack channel
#cmd = '$RabbitMQDIR/slackpost.sh "system_monitor" "' + messageText + '"'
#os.system(cmd)

