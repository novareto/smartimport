# -*- coding: utf-8 -*-
# Copyright (c) 2007-2015 NovaReto GmbH
# cklinger@novareto.de

import click

from kombu import Connection, Exchange, Queue

dale_exchange = Exchange('daleuv', 'topic', durable=True)
dale_queue = Queue('daleuv', exchange=dale_exchange, routing_key='daleuv.import')




@click.command()
@click.option('--dale_xml', help='bergeben Sie Ihr das DALE-XML-FILE.')
def main(dale_xml):
    with open(dale_xml, 'r') as dale_file:
        with Connection('amqp://guest:guest@localhost//') as conn:
            producer = conn.Producer(serializer='json')
            producer.publish({'file': dale_xml, 'content': dale_file.read()},
                        exchange=dale_exchange, routing_key='daleuv.import',
                        declare=[dale_queue])
