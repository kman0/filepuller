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


def get_files(root):
    """Returns selected list of directories"""
    ret_list = []
    root = Path(root)
    # append files from root dir
    ret_list.extend([Path(file.replace('\\', '/')) for file in root.files() if filter_file(file)])

    # append files from sub dirs
    for _dir in [_dir for _dir in root.dirs() if _dir.name not in IGNORE_ROOT_DIRS]:
        ret_list.extend([Path(file.replace('\\', '/')) for file in Path(_dir).walkfiles() if filter_file(file)])
    return ret_list


def gen_data(path):
    tim = datetime.datetime.now()
    files = get_files(path)
    tim2 = datetime.datetime.now()
    print('Time to walk(%s): %s' % (len(files), tim2 - tim))
    data = []
    for file in files:
        md5 = file.abspath().read_md5()
        if file.startswith('/%s/' % DIR_SRC_BASE) or file.startswith('/%s\\' % DIR_SRC_BASE):
            file = file[len(DIR_SRC_BASE) + 2:]
        data.append(file + ':' + binascii.b2a_hex(md5).decode())
    print('Time to hash(%s): %s' % (len(data), datetime.datetime.now() - tim2))
    return '\n'.join(data)


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
