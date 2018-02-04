#!/usr/bin/env python
# encoding:utf-8

import unittest

from WHOISpy import domain_extract
from WHOISpy import whois_server


class TestDomain(unittest.TestCase):

    def setUp(self):
        with open('test_data/extract_domain.dat') as f:
            self.test_domain_list = [l.strip() for l in f.readlines() if not l.startswith('//')]
        with open('test_data/WHOIS_server_list.dat') as f:
            self.test_WHOIS_data_list = [l.strip() for l in f.readlines() if not l.startswith('//')]

    def test_get_relay_WHOIS_server(self):
        self.assertIsInstance(whois_server.WHOIS_server().get_random_relay_WHOIS_server(), str)

    def test_WHOIS_server(self):
        for i in self.test_WHOIS_data_list:
            if i.find(':') != -1:
                t, s = i.split(':')
                t = t.strip()
                s = s.strip()
                self.assertEqual(whois_server.WHOIS_server().get_WHOIS_server(t), s)
            elif i.strip():
                t = i.strip()
                if not whois_server.WHOIS_server().get_WHOIS_server(t):
                    self.assertEqual(whois_server.WHOIS_server().get_WHOIS_server(t), 'whois.nic.' + t)

    def test_get_WHOIS_server(self):
        count = 0
        for domain in self.test_domain_list:
            t = domain_extract.Domain(domain).tld_punycode
            s = domain_extract.Domain(domain).suffix_punycode
            if not whois_server.WHOIS_server().get_WHOIS_server(s):
                if not whois_server.WHOIS_server().get_WHOIS_server(t):
                    print t + "\t don't have record about WHOIS server"
                    count += 1
        if count:
            print "==================================================================="
            print "total " + str(count) + " tld or suffix can't get their WHOIS server"
            print "maybe update the WHOISpy/data/WHOIS_server_list.dat can fix a few"
