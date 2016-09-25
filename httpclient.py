#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust, Justin Wong
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
import urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code = 200, body = ""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port_ID(self, url):
        host = url.hostname
        #host = (url.netloc).split(":")[0]
        if url.port <> None:
            port = url.port
        else:
            port = 80
        ID = url.path
        if (url.params).split(' ')[0] <> '':
            ID += ';' + url.params
        if (url.query).split(' ')[0] <> '':
            ID += '?' + url.query
        if (url.fragment).split(' ')[0] <> '':
            ID += '#' + url.fragment
        return host, port, ID
    
    def connect_to(self, host, port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        return client_socket

    def get_code(self, data):
        return int(data.split()[1])

    def get_headers(self, data):
        return data.split("\r\n\r\n")[0]

    def get_body(self, data):
        return data.split("\r\n\r\n")[1]

    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args = None):
        host, port, ID = self.get_host_port_ID(urlparse(url))
        connection = self.connect_to(host, port)
        connection.sendall("GET " + ID + " HTTP/1.1\r\nHost: " + host + "\r\n\r\n")
        return_msg = self.recvall(connection)
        code = self.get_code(return_msg)
        body = self.get_body(return_msg)
        return HTTPResponse(code, body)

    def POST(self, url, args = None):
        host, port, ID = self.get_host_port_ID(urlparse(url))
        if args <> None:
            data = urllib.urlencode(args)
        else:
            data = ""
        connection = self.connect_to(host, port)
        connection.sendall("POST " + ID + " HTTP/1.1\r\nHost: " + host + "\r\nContent-Type: application/x-www-form-urlencoded; charset=utf-8\r\nContent-Length: " + str(len(data)) + "\r\n\r\n" + data)
        return_msg = self.recvall(connection)
        code = self.get_code(return_msg)
        body = self.get_body(return_msg)
        return HTTPResponse(code, body)

    def command(self, url, command = "GET", args = None):
        if (command == "POST"):
            return self.POST(url, args)
        else:
            return self.GET(url, args)

if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command(sys.argv[2], sys.argv[1]) + "\n"
    else:
        print client.command(sys.argv[1]) + "\n"