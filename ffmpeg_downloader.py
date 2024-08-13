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
import requests
import socket
import ffmpeg
import threading
import time


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        print(self.path)
        if self.path == '/index.html':
            self.path = 'index.html'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        # elif self.path.endswith("m3u8") or self.path.endswith(".ts"):
        #     return self.m3u8()
        elif self.path.endswithswith(".fake"):
            return self.fake()
        
    def fake(self):
        f = self.fakes[os.path.basename(self.path)]
        self.send_response(200)
        self.end_headers()
        self.wfile.write(f)

    
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
    def m3u8(self):
        file_name = os.path.basename(self.path)
        try:
            # If request media segment, return it
            if self.path.endswith(".m3u8"):
                # audio/mpegurl
                # application/x-mpegURL
                content_type = "audio/mpegurl"
            if file_name.endswith(".ts"):
                # "application/x-mpegURL"
                # application/vnd.apple.mpegurl
                # application/vnd.apple.mpegURL
                # application/octet-stream
                content_type = "application/octet-stream"
            if not content_type:
                raise Exception("Illegal url")
    #         # Now create the header
            f = open("ts_sample/"+file_name, 'rb')
            content_length = str(os.fstat(f.fileno())[6])
            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.send_header("Content-Length", content_length)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(f.read())
        except IOError as e:
            # 404 File Not found
            print(e)
            self.send_error(404, e)
        except Exception as e:
            # 500 internal server error
            self.send_error(500, e)
        return f


# need to check if works with no internet connection ie by using localhost
# def get_ip_address():
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.connect(('8.8.8.8', 0))  # connecting to a UDP address doesn't send packets
#     add_name = s.getsockname()[0]
#     print(add_name)
#     if s.connect_ex((add_name, 8000)):
#         print("Default Port Not Available. Please provide an alternative port.")
#     return add_name


def generate_all_urls_from_m3u8(url):
    master_m3u8_text = requests.get(url).text
    a = []
    b = master_m3u8_text.split("\n")
    for i in b:
        if not i.startswith("#") and i:
            a.append(i)
    new_service_url_prefix = url.replace(url.split("/").pop(), "")
    
    fakes_map = {}
    for index,service_url in enumerate(a):
        fakes_map[f"{index}.fake"] = new_service_url_prefix + service_url
        master_m3u8_text = master_m3u8_text.replace(service_url, f"{index}.fake")

    return fakes_map, master_m3u8_text


    def gets(part):
        print(f'getting {part} ....')
        c = requests.get(part)
        if c.status_code != 200:
            print("failed to download.")
            exit()
        
        fakes[part] = c.content
        threadss.pop(part)

    def download_parts(parts):
        threadss = []
        for part in parts:
            t = threading.Thread(target=gets,args=(part,))
            threadss.append(t)
            t.start()

        for i in threadss:
            t.join()                # to keep program running till last thread is completed, seartg join()
    
        for t in threadss:
            while t.is_alive() :
                continue


def download_m3u8_with_ffmpeg(m3u8_url, download_file_name):
    threading.Thread(target=start_server, args=()).start()
    fakes_map, m3u8_file = generate_all_urls_from_m3u8(m3u8_url)
    print(m3u8_file)
    # key = "index0.ts"
    # ffmpeg.input(f"http://localhost:8000/fake.part?key={key}").output(f"{download_file_name}.mp4", vcodec="copy", acodec="copy").overwrite_output().run()


def start_server():
    Handler = CustomHTTPRequestHandler
    httpd = socketserver.TCPServer(("", 8000), Handler)
    httpd.serve_forever()

if __name__ == "__main__":
    #tested with using server. file pathe method worked fine if file is saved but what if file in in momory. that requires the use of temp server.
    download_m3u8_with_ffmpeg("https://test-streams.mux.dev/x36xhzz/url_8/193039199_mp4_h264_aac_fhd_7.m3u8", "test5.mp4")
    # generate_all_urls_from_m3u8("http://192.168.1.3:8000/ts_sample/index.m3u8")