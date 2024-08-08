# import ffmpeg
# import requests
# from http.server import BaseHTTPRequestHandler, HTTPServer
# import time

# hostName = "192.168.1.3"
# serverPort = 8080

# class MyServer(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         self.send_header("Content-type", "text/html")
#         self.end_headers()
#         self.wfile.write(bytes("<html><head><title>lol</title></head>", "utf-8"))
#         self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
#         self.wfile.write(bytes("<body>", "utf-8"))
#         self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
#         self.wfile.write(bytes("</body></html>", "utf-8"))



# ffmpeg -i "Season 01/Family Guy - S01E01 - Death Has A Shadow.mkv" -c:a copy -c:v copy -sn -hls_time 100 -hls_list_size 0 -hls_base_url http://127.0.0.1:8080/ -f hls "index.m3u8"
# >>
# m3u8_url = "https://cdn138.vibanes.com/data/4/99/687NAKZ958JHB5hKGTM2qnuAInSyKCaAFll/687NAKZ958JHB5hKGTM2qnuAInSyKCaAFll1080.m3u8"
# referer="https://emturbovid.com/"

# r=requests.get(m3u8_url, headers={"Referer":referer})
# print(r.text.split())




# ffmpeg.input(m3u8_url, referer = referer).output("demo1.mp4", vcodec="copy", acodec="copy").overwrite_output().run()
#!/usr/bin/env python3

import http.server
import socketserver
import os
import socket
import time
import re
import argparse

global master_playlist
global start_time
global is_vod

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        print(self.path)
        if self.path == '/index.html':
            self.path = 'index.html'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        elif self.path.endswith("m3u8") or self.path.endswith(".ts"):
            return self.m3u8()
    
    def m3u8(self):
        file_name = os.path.basename(self.path)

        f = open("ts_sample/"+file_name, 'rb') #TODO 
        """ handle here the code which gets all the .ts parts of any m3u8 file.
         with path as map key return the right part in order to create the completed file
        """
        return f
    

        # might be required to handle the m3u8s with headers, keys, signatures, etc
        # def mp4(self):
        #     f = open("ts_sample/lol.mp4", "rb")
        #     self.send_response(200)
        #     self.send_header("Content-type", "video/mp4")
        #     self.send_header("Content-Length",  str(os.fstat(f.fileno())[6]))
        #     self.send_header("accept-ranges", "bytes")
        #     self.send_header("Access-Control-Allow-Origin", "*")
        #     self.end_headers()
        #     self.wfile.write(f.read())
        #     # return f
    

    #how to handle multiple url requests from same endpoint
    # def test_m3u8(self):
    #     file_name = os.path.basename(self.path)
    #     try:
    #         # If request media segment, return it
    #         if file_name.endswith(".ts"):
    #             content_type = "video/mp2t"
    #         # If request master playlist, return it (it's already prepared
    #         if self.path.endswith(".m3u8"):
    #             content_type = "application/vnd.apple.mpegurl"
    #         if not content_type:
    #             raise Exception("Illegal url")
    # #         # Now create the header
    #         f = open("ts_sample/"+file_name, 'rb')
    #         content_length = str(os.fstat(f.fileno())[6])
    #         self.send_response(200)
    #         self.send_header("Content-type", content_type)
    #         self.send_header("Content-Length", content_length)
    #         self.send_header("Access-Control-Allow-Origin", "*")
    #         self.end_headers()
    #         self.wfile.write(f.read())
    #     except IOError as e:
    #         # 404 File Not found
    #         print(e)
    #         self.send_error(404, e)
    #     except Exception as e:
    #         # 500 internal server error
    #         self.send_error(500, e)
    #     return f


# need to check if works with no internet connection ie by using localhost
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
    return s.getsockname()[0]


def main():
    Handler = CustomHTTPRequestHandler
    httpd = socketserver.TCPServer(("", 8000), Handler)
    print("Watch stream at: http://{}:{}/index.html".format(get_ip_address(), 8000))
    httpd.serve_forever()

if __name__ == "__main__":
    main()