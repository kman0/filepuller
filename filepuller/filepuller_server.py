"""
filepuller server
=================
"""
import datetime
import os
import sys
import zlib
import hashlib
from threading import Thread
import http.server, select, socket, socketserver, urllib.parse
import pickle
import binascii
from path import Path

__author__ = 'M'

port = 80
drv = 'd:'
bind_ip = '0.0.0.0'
DIR_SRC_BASE = 'src'


HEADER_200 = b'''HTTP/1.1 200 OK\n\n'''
HEADER_404 = b'''HTTP/1.1 404 File Not Found\n\n'''



class ProxyReadHandler (http.server.BaseHTTPRequestHandler):
    __base = http.server.BaseHTTPRequestHandler
    __base_handle = __base.handle


class ThreadingHTTPServer (socketserver.ThreadingMixIn,
                           http.server.HTTPServer):
    pass


def server_instance(bind_host, bind_port, Handler):
    print(('Proxy started on %s:%s' % (bind_host, bind_port)))
    server = ThreadingHTTPServer((bind_host, bind_port), Handler)
    server.serve_forever()


if __name__ == '__main__':
    proxyread = Thread(target=server_instance, args=[bind_ip, port, ProxyReadHandler])
    proxyread.start()
