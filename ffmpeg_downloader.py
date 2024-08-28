from functools import partial
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import threading

import ffmpeg
import requests

import url



class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):

    def __init__(self, parts_data_to_serve, updated_m3u8_data, *args, **kwargs):
        assert parts_data_to_serve!=None, "parts data is required"
        self.fakes = parts_data_to_serve
        self.m3u8_data = updated_m3u8_data
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        print(self.path)
        if self.path.endswith("m3u8"):
            return self.m3u8()
        elif self.path.endswith(".fake"):
            return self.fake()
        
    def fake(self):
        content = self.fakes.get_part_content(os.path.basename(self.path))
        self.send_response(200)
        self.send_header("content-type", "video/mp2t")
        self.send_header("Content-Length", len(content))
        self.end_headers()
        print(os.path.basename(self.path))
        self.wfile.write(content)


    def m3u8(self):
        content_type = "application/vnd.apple.mpegurl"
        content_length = str(len(self.m3u8_data.encode()))
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.send_header("Content-Length", content_length)
        # self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(self.m3u8_data.encode())
        return self.m3u8


def generate_all_urls_from_m3u8(url, master_m3u8_text=None):
    if master_m3u8_text == None:
        master_m3u8_text = requests.get(url).text
    
    new_service_url_prefix = url.replace(url.split("/").pop(), "")
    
    index = 1
    fakes_map = {}
    b = master_m3u8_text.split("\n")
    for i in b:
        if not i.startswith("#") and i:
            master_m3u8_text = master_m3u8_text.replace(i, f"{index}.fake")
            if i.startswith("http"):
                fakes_map[f"{index}.fake"] = i
            else:
                fakes_map[f"{index}.fake"] = f"{new_service_url_prefix}/{i}"
            index+=1
        elif i.startswith("#EXT-X-KEY"):
            method, uri = i.split(",")
            method = method.split("=").pop()
            uri = uri.split("=").pop().strip('"')
            key = requests.get(uri).content
            # print(key.decode())
            fakes_map["key.fake"] = uri
            master_m3u8_text = master_m3u8_text.replace(i, i.replace(uri, f"key.fake"))
    return fakes_map, master_m3u8_text


class Server:
    def __init__(self, parts_data_to_serve, updated_m3u8_data) -> None:
        self.parts_data_to_serve = parts_data_to_serve
        self.updated_m3u8_data = updated_m3u8_data

    def start(self):
        server_address = ("", 8000)
        partial_handler = partial(CustomHTTPRequestHandler, self.parts_data_to_serve, self.updated_m3u8_data)
        self.server = HTTPServer(server_address, partial_handler)
        self.server_thread = threading.Thread(target=self.server.serve_forever,daemon=True, args=()).start()
        print(f"Now serving at: http://localhost:{self.server.server_address[1]}")

    
    def stop(self):
        self.server_thread.join()
        self.server.shutdown()
        while self.server_thread.is_alive():
            continue

    def __del__(self):
        if self.server_thread.is_alive():
            self.stop()


class StreamProcessor:
    def __init__(self, parts_map) -> None:
        self.parts_map = parts_map
        self.active_threads_map = {}
        self.fake_parts_map = {}
        self.remaining = len(parts_map)
        self.max_thread_count = 50

    def _get_part_content(self, part_name, endpoint):
        tries = 5
        host = endpoint.split("://").pop().split("/")[0]
        while tries:
            try:
                c = requests.get(endpoint, headers={"Host": host, "Referer": "https://kwik.si/"})
                if c.status_code != 200:
                    print(f"{part_name}: failed to download. Error: {c.status_code}, {c.reason}")
                    #TODO handle retry
                self.fake_parts_map[part_name] = c.content
                self.remaining-=1
                print(f"{part_name} complete. {self.remaining} remaining", end="\r")
                break
            except:
                tries-=1
        else:
            with open("report.txt", "a") as f:
                f.write(f"failed to download: {part_name}\n")


    def download_part(self, part, endpoint):
        while threading.active_count() > self.max_thread_count:
            continue

        thread = threading.Thread(target=self._get_part_content, name=part, daemon=True, args=(part, endpoint,))
        self.active_threads_map[part] = thread
        thread.start()


    def start_download_parts(self):
        for part, endpoint in self.parts_map.items():
            self.download_part(part, endpoint)


    def get_part_content(self, part_name):
        if not self.active_threads_map.get(part_name):
            self.download_part(part_name, self.parts_map[part_name])

        thread = self.active_threads_map.get(part_name)
        while thread.is_alive():
            continue
        
        # print(self.fake_parts_map)
        return self.fake_parts_map[part_name]
    

    def download(self):
        self.start_download_parts()


def download_m3u8_with_ffmpeg(fakes_map):
    thread_processor = StreamProcessor(fakes_map)
    thread_processor.download()
    return thread_processor


if __name__ == "__main__":
    download_file_name = "test_one"
    m3u8_text = requests.get(url.url).text
    headers = requests.head(url.url).headers
    # with open("start-094.m3u8", 'r') as f:
    #     m3u8_text = f.read()
# 
    fakes_map, updated_m3u8_data = generate_all_urls_from_m3u8(url.url, m3u8_text)
    # print(updated_m3u8_data)
    # exit()
    parts_thread = download_m3u8_with_ffmpeg(fakes_map)

    server = Server(parts_thread, updated_m3u8_data)
    server.start()
    ffmpeg.input(f"http://localhost:8000/fake.m3u8").output(f"{download_file_name}.mp4", vcodec="copy", acodec="copy").overwrite_output().run()
    server.stop()
        

    # server = Server([], m3u8_text)
    # try:
    #     server.start()
    #     while True:
    #         continue
    # except KeyboardInterrupt:
    #     server.stop()


