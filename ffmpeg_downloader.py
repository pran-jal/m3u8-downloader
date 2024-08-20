import requests
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import threading

import ffmpeg

import url

from functools import partial



class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    
    def do_GET(self):
        print(self.path)
        if self.path == '/index.html':
            self.path = 'index.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        # elif self.path.endswith("m3u8") or self.path.endswith(".ts"):
        #     return self.m3u8()
        elif self.path.endswith(".fake"):
            return self.fake()
        
    def fake(self):
        f = self.fakes[os.path.basename(self.path)]
        self.send_response(200)
        self.end_headers()
        self.wfile.write(f)


class StreamProcessor:
    def __init__(self, parts_map) -> None:
        self.parts_map = parts_map
        self.active_threads_map = {}
        self.fake_parts_map = {}
        self.completed = False


    def _get_part_content(self, part_name, endpoint):
        c = requests.get(endpoint)
        if c.status_code != 200:
            print("failed to download.")
            #TODO handle retry
            # exit()
        self.fake_parts_map[part_name] = c.content


    def download_part(self, part, endpoint):
        thread = threading.Thread(target=self._get_part_content, name=part, args=(part, endpoint,))
        thread.start()
        self.active_threads_list[part] = thread


    def start_download_parts(self):
        for part, endpoint in self.parts_map.items():
            self.download_part(part, endpoint)


    def get_part_content(self, part_name):
        if not self.active_threads_map.get(part_name):
            self.download_part(part_name, self.parts_map[part_name])

        thread = self.active_threads_map.get(part_name)
        while thread.is_alive():
            continue

        return self.fake_parts_map[part_name]
    

    def download(self):
        self.start_download_parts()


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
        # master_m3u8_text = master_m3u8_text.replace(service_url, f"{index}.fake")

    return fakes_map



def start_server():
    server_address = ("", 8000)
    return HTTPServer(server_address, CustomHTTPRequestHandler)



def download_m3u8_with_ffmpeg(m3u8_url, download_file_name):
    fakes_map = generate_all_urls_from_m3u8(m3u8_url)
    thread_processor = StreamProcessor(fakes_map)
    thread_processor.download()

    server = start_server()
    server_thread = threading.Thread(target=server.serve_forever, args=()).start()

    while not thread_processor.completed:
        continue
    
    ffmpeg.input(f"http://localhost:8000/fake.part?key={key}").output(f"{download_file_name}.mp4", vcodec="copy", acodec="copy").overwrite_output().run()
    
    server.shutdown()
    server_thread.



if __name__ == "__main__":
    #tested with using server. file pathe method worked fine if file is saved but what if file in in momory. that requires the use of temp server.
    # download_m3u8_with_ffmpeg(url.url, "test5.mp4")
    # generate_all_urls_from_m3u8("http://192.168.1.3:8000/ts_sample/index.m3u8")
    # server = start_server()
    # try:
    #     print(f"Now serving at: http://{server.server_address[0]}:{server.server_address[1]}")
    #     server.serve_forever()
    # finally:
    #     server.shutdown()