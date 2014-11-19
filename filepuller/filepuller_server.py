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


