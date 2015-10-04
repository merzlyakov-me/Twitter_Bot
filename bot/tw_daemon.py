# -*- coding: utf-8 -*-
#
# author:
#
""" This module recieve commands from client_tw and runs twitter_daemon with paramters """
from daemon import twitter_daemon
import logging
import pika # pip install pika is needed
import sys

class ReceiveCommand(object):
    """ Receive command message sended by the tw_client.py"""

    def __init__(self):
        """ Constructor """
        self.task_queue = "task_queue" # ==> may be define in config yaml 
        self.result_queue = "server_return_queue" # ==> .................
        self.result = ""

    def receive_task(self):
        """ connection initialization, receive message from brocker in Queue = daemon_id """
        self.connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.task_queue)
        print ' [*] Waiting for messages. To exit press CTRL+C'
        self.channel.basic_consume(self._callback, queue=self.task_queue, no_ack=True)
        try: 
            self.channel.start_consuming()
        except KeyboardInterrupt:
            print "\nExit"
            sys.exit(0)

    def _callback(self, ch, method, properties, body):
        """ receive task and execute daemon """
        print "Received task: {0}".format(body)
        self.logic = twitter_daemon.TwitterBot()
        if body:
            self.task_list = body.split(' ')
            if self.task_list[0]=="post_tweet":
                print "Run post_tweet {0}".format(self.task_list[1])
                self.result = self.logic.post_tweet(self.task_list[1])
            elif self.task_list[0]=="search":
                print "Run search {0}".format(self.task_list[1])
                self.logic.search(self.task_list[1]) #seach hasn't return value
                self.result = "search done"
        self._send_result()

    def _send_result(self):
        """ send message to the broker in Queue = result_queue """
        logging.info("send message(task)")
        # send result for tw_client queue="server_return_queue"
        self.channel.basic_publish(exchange='', routing_key=self.result_queue, body=self.result)

receiver = ReceiveCommand()
receiver.receive_task()