#!/usr/bin/env python2

import json
import urllib2
from lxml import etree

mappings = json.loads(urllib2.urlopen(
    'https://gist.githubusercontent.com/wilgert/7305244/raw/'
    'a4f0d38aaf7fecef94939644093c65609c4d1aaf/dutch_banks.json'
).read())
xml = etree.Element('openerp')
data_node = etree.SubElement(xml, 'data')
for bank_code, data in mappings.iteritems():
    node = etree.SubElement(
        data_node, 'record', model='res.bank.iban.bic.mapping',
        id='bic_mapping_nl_%s' % bank_code)
    etree.SubElement(node, 'field', name='match_type').text = 'regex'
    etree.SubElement(node, 'field', name='country_id', ref='base.nl')
    etree.SubElement(
        node, 'field', name='data', eval="'^%s'" % bank_code)
    etree.SubElement(node, 'field', name='bic').text = "%s" % data['BIC']
print etree.tostring(
    xml, pretty_print=True, xml_declaration=True, encoding='UTF-8'
)
