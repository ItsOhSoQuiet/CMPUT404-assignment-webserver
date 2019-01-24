#  coding: utf-8 
import socketserver
import os # to handle finding files and directories

# Copyright 2013, 2018 Abram Hindle, Eddie Antonio Santos, Matthew Kluk
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    # This serves the file at a certain filepath.
    def serveFile(self, filePath):
        pass

    def serve404(self):
        pass
    
    def serve405(self):
        pass

    
    # According to https://docs.python.org/2/library/socketserver.html,
    # This is to do all of the work required to service a request
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data)

        '''
            This code sees how the request data is represented
            in Python
        '''
        print(self.data)
        print(type(self.data))
        '''
            This code was used to identify the different parts
            of the HTML request
        '''
        element_table = self.data.split()
        for element in element_table:
            print(element, element_table.index(element))

        '''
            This code was me looking at converting byte
            literals to strings, inspired by this link
            https://stackoverflow.com/questions/6269765/what-does-the-b-character-do-in-front-of-a-string-literal
        '''
        print(type(element_table[0]))
        print(type(element_table[0].decode('utf-8')))
        print(element_table[0].decode('utf-8'))

        # This code sends back just the word OK.
        self.request.sendall(bytearray("OK",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080 # will run on http://127.0.0.1:8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
