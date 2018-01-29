# -*- coding: utf-8 -*-
# Copyright (c) 2007-2015 NovaReto GmbH
# cklinger@novareto.de

from kombu import Connection
from .importer import dale_queue
from .utils import log
from .converter import as_dict

from kombu.mixins import ConsumerMixin
from kombu.log import get_logger
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql import select


engine = create_engine('postgresql+psycopg2://dale:dale@localhost/dale')
metadata = MetaData(bind=engine)
edokumente = Table('edokimp', metadata, autoload=True, autoload_with=engine)



logger = get_logger(__name__)



class Worker(ConsumerMixin):

    def __init__(self, connection):
        self.connection = connection
        self.db_conn = engine.connect()

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=[dale_queue, ],
                         accept=['pickle', 'json'],
                         callbacks=[self.run_task])]

    def getNextNumber(self):
        return len(self.db_conn.execute(select([edokumente])).fetchall()) + 2

    def inDB(self, data):
        data['edokimp_id'] = self.getNextNumber()
        columns = [x.name for x in edokumente._columns]
        for key in data.keys():
            if key not in columns:
                data.pop(key)
        ins = edokumente.insert(values=data)
        dd = self.db_conn.execute(ins)
        print "ROWCOUNT-->", dd.rowcount

    def run_task(self, body, message):
        try:
            log.info('Receiving NEW MESSAGE')
            data_dict = as_dict(body['content'])
            log.info('TO DICT WORKS')
            import pdb; pdb.set_trace()
            self.inDB(data_dict)
            log.info('TO DB WORKS')
            message.ack()
        except Exception, e:
            logger.error('task raised exception: %r', e)


def main():
    with Connection('amqp://guest:guest@localhost//') as conn:
        try:
            worker = Worker(conn)
            worker.run()
        except KeyboardInterrupt:
            print('bye bye')
