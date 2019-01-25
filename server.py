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

    # This checks if the file can be reached.
    # If it can, serve the file. If not, send 404.
    def checkIfCanGet(self, request_array):
        # Need to get the path that the files to
        # display are in. 

        # We are not allowed to hardcode, so we need
        # to get the current directory that we're in.

        # https://www.techcoil.com/blog/how-to-get-the-directory-path-of-a-python-3-script-from-within-itself/
        serverDirectory = os.path.dirname(os.path.realpath(__file__))

        # Get path to file, checks if it exists, serve if yes, 404 if no
        filepath = serverDirectory + "/www" + request_array[1]

        # Code to test finding the filepaths

        # print(filepath)
        # if os.path.exists('/home/student/Assignments/Assignment1/CMPUT404-assignment-webserver/www/deep'):
            # print("Without slash success")
        # if os.path.exists('/home/student/Assignments/Assignment1/CMPUT404-assignment-webserver/www/deep/'):
        #   # print("With slash success")

        # Need to check if file exists.
        # If it doesn't exist, give a 404 response.
        # If it does exist, check if it's a folder.
        # If it is a folder, check if it has a slash at the end
        # If there isn't one, add it, so we can easily access the
        # HTML file. 

        # https://www.techcoil.com/blog/how-to-get-the-directory-path-of-a-python-3-script-from-within-itself/
        # https://dbader.org/blog/python-check-if-file-exists
        # https://stackoverflow.com/questions/3204782/how-to-check-if-a-file-is-a-directory-or-regular-file-in-python
        if os.path.exists(filepath):
            if os.path.isdir(filepath):
                if not filepath.endswith('/'):
                    filepath += "/"
                filepath += "index.html" # making sure we go to the index.html
                if not os.path.exists(filepath):
                    self.serve404()
                else:
                    self.serveFile(filepath)
            else:
                self.serveFile(filepath)
        else:
            self.serve404()

    # Since the filepath has already been verified to exist,
    # just send over the contents in a 200 OK response. 

    # I learned about formatting HTTP responses here:
    # https://www.tutorialspoint.com/http/http_responses.htm

    # and about mime-codes here:
    # https://www.sitepoint.com/mime-types-complete-list/
    def serveFile(self, filepath):
        # Get the mime-type
        if filepath.endswith("html"):
            mime_type = "text/html"
        elif filepath.endswith("css"):
            mime_type = "text/css"

        # Get the status code
        code = "200 OK"

        # Need to deal with confused folders, like /../../../../something_we_don't want
        try:
            # Read in the HTML/CSS
            with open(filepath, 'r') as read_file:
                text = read_file.read()
            
            self.sendResponse(code, mime_type, text)
        except Exception:
            self.serve404()

        # self.sendResponse(code, mime_type, text)

    # Get the 404 code and HTML message
    def serve404(self):
        code = "404 Not Found"
        mime_type = "text/html"

        # Note: the guide on making HTML messages
        # also comes from:
        # https://www.tutorialspoint.com/http/http_responses.htm
        text = "<html><head>\r\n<title>404 Not Found</title>" + \
        "\r\n</head><body>\r\n<h1>Not Found</h1>\r\n<p>The " + \
        "requested URL was not found.</p>\r\n</body></html>"

        self.sendResponse(code, mime_type, text) 
    
    # Get the 405 code and HTML message.
    def serve405(self):
        code = "405 Method Not Allowed"
        mime_type = "text/html"

        text = "<html><head>\r\n<title>405 Method Not Allowed</title>" + \
        "\r\n</head><body>\r\n<h1>Method Not Allowed</h1>\r\n<p>This " + \
        "method is not allowed in a request</p>\r\n</body></html>"

        self.sendResponse(code, mime_type, text) 

    # Finally sending the response over.
    # Python formatting found at:
    # https://realpython.com/python-string-formatting/
    def sendResponse(self, code, mime_type, text):
        httpResponse = "HTTP/1.1 {code}\r\n" + \
        "Content-Length: {length}\r\n" + \
        "Content-Type: {mime}\r\n" + \
        "Connection: Closed\r\n\r\n" + \
        "{text}\r\n"

        httpResponse = httpResponse.format(code=code,
                        length=str(len(text)), mime=mime_type,
                        text=text)

        # finally send the response to the client
        self.request.sendall(httpResponse.encode())

    
    # According to https://docs.python.org/2/library/socketserver.html,
    # This is to do all of the work required to service a request.
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data)


        # This code sees how the request data is represented
        # in Python
        # print(self.data)
        # print(type(self.data))


        # This code was used to identify the different parts
        # of the HTML request
        # element_table = self.data.split()
        # for element in element_table:
            # print(element, element_table.index(element))


        # This code was me looking at converting byte
        # literals to strings, inspired by this link
        # https://stackoverflow.com/questions/6269765/what-does-the-b-character-do-in-front-of-a-string-literal
        # print(type(element_table[0]))
        # print(type(element_table[0].decode('utf-8')))
        # print(element_table[0].decode('utf-8'))
        # for element in element_table:
            # element.decode('utf-8')
        # print(element_table)


        # Take request, split it into an array, and decode each element into strings.
        # Check if the method of the request has "GET" or not,
        # then we can serve the correct response.
        # Forgot about list comprehensions.
        # https://stackoverflow.com/questions/3371269/call-int-function-on-every-list-element

        request_array = [ element.decode('utf-8') for element in self.data.split() ]
        # print(request_array)
        method = request_array[0]
        # print(len(method))
        # print(type(method))
        if method != "GET":
            self.serve405()
            # print("405")
        else:
            self.checkIfCanGet(request_array)
            # print("Success!")


        # This code sends back just the word OK.
        # self.request.sendall(bytearray("OK",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080 # will run on http://127.0.0.1:8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
