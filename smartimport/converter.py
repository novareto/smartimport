# -*- coding: utf-8 -*-
# Copyright (c) 2007-2015 NovaReto GmbH
# cklinger@novareto.de


from StringIO import StringIO
from lxml import etree

def as_dict(content):
    mapping = {}
    root = etree.parse(StringIO(content)).getroot()
    for leaf in root.iter():
        if leaf.text != "\n" and leaf.text is not None:
            mapping[leaf.tag] = leaf.text.strip()
    return mapping