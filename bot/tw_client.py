# -*- coding: utf-8 -*-
#
# author:
#
""" Run bot logic 
If --Run Task-- is selected, the task will be sent to tw_daemon.py. 
Then tw_deamon will run main twitter logic (twitter_daemon.py)
"""
import yaml # pip install pyyaml is needed
import logging
import pika # pip install pika is needed
import sys
SERVER_IP = "localhost" # if no config
#logging.basicConfig(level = logging.DEBUG)

class YamlConfig(object):
    """ get and ste config """
    def __init(self):
        """ Constructor """
        pass
    def get_config(self):
        """ get and set config from config.yaml """
        logging.info("Read config.yaml file.")
        with open('config.yaml', 'r') as config_file:
            config = yaml.load(config_file)
        logging.info("SERVER_IP init")
        SERVER_IP = config["parameters"]["server_ip"]
        """ get and set config form config.yaml """
        logging.info("Read config.yaml")
        with open('config.yaml', 'r') as config_file:
            config = yaml.load(config_file)
        SERVER_IP = config["parameters"]["server_ip"]
        logging.info("SERVER_IP init")
        return SERVER_IP

class SendCommand(object):
    """ Send command message to the queue for tw_server.py"""

    def __init__(self):
        """ Constructor """
        self.task_queue = "task_queue" # ===> config ?
        self.result_queue = "server_return_queue" # ===> config ?
        self.task = "test task" # to do variable
        # connection initialization"""
        logging.info("Connect to server ...")
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(SERVER_IP))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.result_queue)
        logging.info("connection established.")

    def __del__(self):
        """ Destructor """
        logging.info("Close connection.")
        self.connection.close()

    def _consume(self):   
        # wait for result from tw_server queue="result_queue"
        print " [x] Waiting for answer from server"
        print " [x] To EXIT press Ctrl+C"
        self.channel.basic_consume(self._on_response, queue=self.result_queue, no_ack=True)
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            print "\nExit"
            sys.exit(0)

    def _on_response(self, ch, method, properties, body):
        print "Daemon response: {0}".format(body)

    def send_task(self, task):
        self.task = task
        """ send message to the brocker in Queue = daemon_id"""
        logging.info("send message(task)")
        # send task for tw_server queue="task_queue"
        self.channel.basic_publish(exchange='', routing_key=self.task_queue, body=self.task)
        print " [x] Sent {0}".format(self.task)
        self._consume()

conf = YamlConfig()
conf.get_config()

sender = SendCommand()

select = True
while select:
    print("""
    1. Run Task.
    2. Print Help.
    0. Exit.
    """)
    select = raw_input("Select ")
    if select=="1":
        print ("\t\t--> post_tweet message\n\t\t--> search q")
        task = raw_input("Enter task: ")
        task_list = task.split(' ')
        if task_list[0] != "post_tweet" and task_list[0] != "search" or len(task_list) != 2: 
            print "Not valid command"
            break
        print "\n\tRun task:"
        sender.send_task(task)
    elif select=="2":
        print "\n\tPrint help: If --Run Task-- is selected, the task will be sent to tw_daemon.py." 
        print "\tThen tw_deamon will run main twitter logic (twitter_daemon.py)"
        print "\t\t commands for daemon:"
        print ("\t\t--> post_tweet message\n\t\t--> search q")
    elif select=="0":
        print "\n\tExit."
        break
    elif select!="":
        print ("\n\tNot Valid Choice")
