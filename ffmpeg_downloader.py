from functools import partial
from socketserver import BaseServer
import requests
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import threading

import ffmpeg

import url

from functools import partial



class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):

    def __init__(self, data_to_serve, *args, **kwargs):
        assert data_to_serve!=None, "parts data is required"
        self.fakes = data_to_serve
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        print(self.path)
        if self.path == '/index.html':
            self.path = 'index.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        elif self.path.endswith("m3u8"):
            return self.m3u8()
        elif self.path.endswith(".fake"):
            return self.fake()
        
    def fake(self):
        f = self.fakes[os.path.basename(self.path)]
        self.send_response(200)
        self.end_headers()
        self.wfile.write(f)

    def m3u8(self):
        pass


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
        thread = threading.Thread(target=self._get_part_content, name=part, daemon=True, args=(part, endpoint,))
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


def generate_all_urls_from_m3u8(url, master_m3u8_text=None):
    if master_m3u8_text == None:
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


class Server:
    data_to_serve = None

    def start(self):
        server_address = ("", 8000)
        partial_handler = partial(CustomHTTPRequestHandler, self.data_to_serve)
        self.server = HTTPServer(server_address, partial_handler)
        self.server_thread = threading.Thread(target=server.serve_forever,daemon=True, args=()).start()
        print(f"Now serving at: http://{server.server_address[0]}:{server.server_address[1]}")

    
    def stop(self):
        self.server_thread.join()
        self.server.shutdown()
        while self.server_thread.is_alive():
            continue

    def __del__(self):
        if self.server_thread.is_alive():
            self.server_thread.join()
            while self.server_thread.is_alive():
                continue


def download_m3u8_with_ffmpeg(m3u8_url, download_file_name):
    fakes_map = generate_all_urls_from_m3u8(m3u8_url)
    thread_processor = StreamProcessor(fakes_map)
    thread_processor.download()
    return thread_processor





if __name__ == "__main__":
    download_file_name = "test_one"


    parts_thread = download_m3u8_with_ffmpeg(url.url)
    server = Server(parts_thread)
    server.start()
    ffmpeg.input(f"http://localhost:8000/fake.m3u8").output(f"{download_file_name}.mp4", vcodec="copy", acodec="copy").overwrite_output().run()
    server.stop()


