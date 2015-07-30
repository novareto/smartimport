# -*- coding: utf-8 -*-
# Copyright (c) 2007-2015 NovaReto GmbH
# cklinger@novareto.de

from kombu import Connection
from .importer import dale_queue
from lxml import etree
from StringIO import StringIO
from kombu.mixins import ConsumerMixin
from kombu.log import get_logger

logger = get_logger(__name__)


class Worker(ConsumerMixin):

    def __init__(self, connection):
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=[dale_queue, ],
                         accept=['pickle', 'json'],
                         callbacks=[self.run_task])]

    def asDict(self, content):
        d = {}
        root = etree.parse(StringIO(content)).getroot()
        for leaf in root.iter():
            if leaf.text != "\n" and leaf.text is not None:
                d[leaf.tag] = leaf.text.strip()
        return d

    def run_task(self, body, message):
        try:
            data_dict = self.asDict(body['content'])
            message.ack()
        except StandardError, e:
            logger.error('task raised exception: %r', e)
            print e


def main():
    with Connection('amqp://guest:guest@localhost//') as conn:
        try:
            worker = Worker(conn)
            worker.run()
        except KeyboardInterrupt:
            print('bye bye')
