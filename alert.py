####################################################################################
#
# Program: alert
# Version: 1.2
# Date: 13/07/2018
#
# Description: Receives details of alert messages from the current server and sends
# this information to the RabbitMQ server (PiRMQ01)
#
####################################################################################
#!/usr/bin/python
import pika
import time
import datetime
import sys
import os

# Use plain credentials for authentication
mq_creds  = pika.PlainCredentials(
    username = "webmessage",
    password = "guest")

# Use localhost
mq_params = pika.ConnectionParameters(
    host         = "192.168.1.200",
    credentials  = mq_creds,
    virtual_host = "/")

# Set RabbitMQ Exchange and Queue Routing values
mq_exchange    = "amq.topic"
mq_routing_key = "PiCloud"
mq_routing_key2 = "BlueMix"
mq_routing_key3 = "PiWEB02"

# This a connection object
mq_conn = pika.BlockingConnection(mq_params)

# This is one channel inside the connection
mq_chan = mq_conn.channel()

# Get message text from argument passed in
messageType = sys.argv[1]
messageBody = sys.argv[2]

# Calculate timestamp
ts = time.time()
messageDatetime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

# Create message text for RabbitPi and NodeRed
messageText = messageDatetime + " [" + messageType + "] " + messageBody
messageText2 = "INSERT INTO rabbitpimessagelog (message_type, message_body, message_datetime) VALUES ('" + messageType + "','" + messageBody + "','" + messageDatetime + "');"

# Publish message to RabbitMQ Listener (RabbitMQ PiCloud queue)
mq_chan.basic_publish(
        exchange    = mq_exchange,
        routing_key = mq_routing_key,
        body        = messageText)

# Send any ALRT message to alert screen (RabbitMQ PiWEB02 queue)
if messageType == 'ALRT':
	mq_chan.basic_publish(
        	exchange    = mq_exchange,
        	routing_key = mq_routing_key3,
        	body        = messageText)

# Send message to messge log table (RabbitMQ BlueMix queue)
mq_chan.basic_publish(
        exchange    = mq_exchange,
        routing_key = mq_routing_key2,
        body        = messageText2)

# Send any ALRT message to the general slack channel
if messageType == 'ALRT':
	cmd = '$RabbitMQDIR/slackpost.sh "system_monitor" "' + messageText + '"'
	os.system(cmd)

