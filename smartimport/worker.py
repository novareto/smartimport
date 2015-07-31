# -*- coding: utf-8 -*-
# Copyright (c) 2007-2015 NovaReto GmbH
# cklinger@novareto.de

from kombu import Connection
from .importer import dale_queue
from lxml import etree
from StringIO import StringIO
from kombu.mixins import ConsumerMixin
from kombu.log import get_logger
from sqlalchemy import create_engine, MetaData, Table


engine = create_engine('postgresql+psycopg2://asd:asd@localhost/dale')
metadata = MetaData(bind=engine)
edokumente = Table('edokimp', metadata, autoload=True, autoload_with=engine)



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

    def inDB(self, data):
        data['edokimpid'] = 1
        columns = [x.name for x in edokumente._columns]
        for key in data.keys():
            if key not in columns:
                data.pop(key)
        import pdb; pdb.set_trace()
        conn = engine.connect()
        ins = edokumente.insert(values=data)
        dd = conn.execute(ins)
        print "ROWCOUNT-->", dd.rowcount

    def run_task(self, body, message):
        try:
            import pdb; pdb.set_trace()
            data_dict = self.asDict(body['content'])
            self.inDB(data_dict)
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
