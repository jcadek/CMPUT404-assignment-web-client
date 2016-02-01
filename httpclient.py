#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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
# you may use urllib to encode data appropriately
import urllib

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):
        split1 = re.split(":", url);
        if(len(split1) == 2):
            return int(split1[1]);
        else:
            return 80;
    def connect(self, host, port):
        
        import socket
        clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        clientSocket.connect((host, port))
        return clientSocket;

    def get_code(self, data):
        print data;
        return int(re.findall("HTTP/1.[01] ([0-5][0-9][0-9])", data)[0]);

    def get_headers(self,data):
        return re.split("\r\n\r\n",data,1)[0];

    def get_body(self, data):
        return re.split("\r\n\r\n",data,1)[1];

    def parseURL(self, url):
       
        proto = '';
        path = '';
        query = '';
        frag = '';
        split1 = re.split('://', url);
        if(len(split1) == 2):
            proto = split1[0];
        split2 = re.split('/', split1[-1],1);
        
        if(len(split2) == 1): 
            split3 = re.split('\?', split2[-1],1);
            if(len(split3) == 2):
                host = split3[0];
                split4 = re.split('#', split3[-1],1);
                query = split4[0];
                if(len(split4) == 2):
                    frag = split4[1];frag = split4[1];
            else:
                split4 = re.split('#', split3[-1],1);
                host = split4[0];
                if(len(split4) == 2):
                    frag = split4[1];frag = split4[1];
        else:
            host = split2[0];
            split3 = re.split('\?', split2[-1],1);
            if(len(split3) == 2):
                path = split3[0];
                split4 = re.split('#', split3[-1],1);
                query = split4[0];
                if(len(split4) == 2):
                    frag = split4[1];
            else:
                split4 = re.split('#', split3[-1],1);
                path = split4[0];
                if(len(split4) == 2):
                    frag = split4[1];frag = split4[1];

        proto = proto + "://";
        path = "/" + path;
        port = self.get_host_port(host);
        host = re.split(":",host)[0];
        return [proto, host, port, path, query, frag];
        
        
    def parseARGS(self, args):
       
        argout = ['']*len(args);
        counter = 0;
        for variable, index in args.iteritems():
            
            argout[counter] = variable + "=" + index;
            counter += 1;
        return argout;
       
        

    # read everything from the socket
    def recvall(self, sock):
        buff = bytearray()
        done = False
        while not done:
            
            part = sock.recv(1024)
            if (part):
                
                
                buff.extend(part)
            else:
                
                done = not part
        return str(buff)

    def GET(self, url, args=None):
        proto, host, port, path, query, frag = self.parseURL(url);
        print host;
        sock = self.connect(host, port);  
        body = "GET " +  path + " HTTP/1.1\r\n";
        body = body + "Host: " + host + "\r\n";
        body = body + "Connection: close\r\n";
        body = body + "\r\n";
        sock.sendall(body)
        buff = self.recvall(sock);
        code= self.get_code(buff);
        body = self.get_body(buff);
        print body
        return HTTPResponse(code, body)

    def POST(self, url, args=None):

        proto, host, port, path, query, frag = self.parseURL(url);
        
        argout = '';
        if(args != None):
            argsplit = self.parseARGS(args)
           
            for i in range(0,len(argsplit)):
                if((i != 0) or (query != "")):
                    argout = argout + "&";
                argout = argout + argsplit[i];
                
        
        
        sock = self.connect(host, port);  
        body = "POST " +  path + " HTTP/1.1\r\n";
        body = body + "Host: " + host + "\r\n";
        body = body + "Content-type: application/x-www-form-urlencoded\r\n";
        body = body + "Connection: close\r\n";
        body = body + "Content-length: " + str(len(query) + len(argout)) + "\r\n"
        body = body + "\r\n";
        body = body + query + argout + "\r\n";
        
        body = body + "\r\n";
        sock.sendall(body)
        buff = self.recvall(sock);
        code= self.get_code(buff);
        body = self.get_body(buff);
        
        print body
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        print url, command, args;
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1])
    elif (len(sys.argv) == 4):
        print client.command( sys.argv[2], sys.argv[1], sys.argv[3])
    else:
        print client.command( sys.argv[1] )
     
       
