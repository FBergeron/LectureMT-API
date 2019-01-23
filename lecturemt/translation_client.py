#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""translation_client.py: Client to communicate with a translation (OpenNMT) server."""
__author__ = "Frederic Bergeron"
__license__ = "undecided"
__version__ = "1.0"
__email__ = "bergeron@nlp.ist.i.kyoto-u.ac.jp"
__status__ = "Development"

import http.client
import json
import logging
import logging.config
import urllib.parse
import sys

class Client:

    def __init__(self, host='localhost', port=46001, logger=None):
        self.host = host
        self.port = port
        self.logger = logger

    def submit(self, text):
        json_data = None
        params = ('[{"src": "' + text + '", "id": 1}]').encode('utf-8')
        headers = {"Content-type": "application/json"}
        conn = http.client.HTTPConnection("{0}:{1}".format(self.host, self.port))
        conn.request("POST", "/translator/translate", params, headers)
        response = conn.getresponse()
        self.logger.debug("status={0} reason={1}".format(response.status, response.reason))
        if response.status == 200:
            data = response.read()
            self.logger.debug("data={0}".format(data))
            try:
                json_data = json.loads(data)
            except Exception as e:
                self.logger.error("Error when loading json e={0}".format(e))

        if json_data:
            if len(json_data) == 1 and len(json_data[0]) == 1 and 'tgt' in json_data[0][0]:
                translated_text = json_data[0][0]['tgt']
                return translated_text

        return ''

        # This works
        #
        # params = "[{\"src\": \"アルゴリズム と データ 構造 の 講義 です けれども きょう は 整列 に ついて\", \"id\": 1}]".encode('utf-8')
        # headers = {"Content-type": "application/json"}
        # conn = http.client.HTTPConnection("moss106:46101")
        # conn.request("POST", "/translator/translate", params, headers)
        # response = conn.getresponse()
        # print("status={0} reason={1}".format(response.status, response.reason))
        # data = response.read()
        # print("data={0}".format(data))
        
        # This works
        #
        # conn = http.client.HTTPConnection("moss106:46101")
        # conn.request("GET", "/translator/models")
        # response = conn.getresponse()
        # print("status={0} reason={1}".format(response.status, response.reason))
        # data = response.read()
        # print("data={0}".format(data))

def main():
    # logging.basicConfig()
    log = logging.getLogger("default")

    import argparse
    parser = argparse.ArgumentParser(description= "Send a translation request to the Translation Server", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--host", help = "Host of the server", default = 'localhost')
    parser.add_argument("--port", help = "Port of the server", default = 46001)
    args = parser.parse_args()

    client = Client(args.host, int(args.port), log)
    request = ''
    for line in sys.stdin:
        request += line

    response = client.submit(request)
    print(response)

if __name__ == '__main__':
    main()

