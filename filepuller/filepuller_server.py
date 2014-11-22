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


IGNORE_PREFIX = ['/src/exec',
                 '/src/res',
                 '/src/others',
                 '/src/.git',
                 '/src/.idea']

IGNORE_EXTENSIONS = ['.pyc', '.project', '.gitignore', '.git', '.svn', '.jar', '__pycache__']

IGNORE_ROOT_DIRS = ['.git', '.idea', 'res', 'exec']


def filter_file(cur_path):
    if [cur_path for ip in IGNORE_PREFIX if cur_path.startswith(ip)]:
        return None
    if cur_path.isfile() and cur_path.ext in IGNORE_EXTENSIONS:
        return None
    return cur_path


def md5_file(file, block_size=2**20):  #2**20=1mb
    if os.path.exists(file):
        handle=open(file,'rb')
        md5 = hashlib.md5()
        while True:
            block_data = handle.read(block_size)
            if not block_data:
                break
            md5.update(block_data)
        return md5.hexdigest()
    else:
        return False


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
