from http.server import SimpleHTTPRequestHandler
import os



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
        elif self.path.endswith(".key"):
            return self.key()


    def key(self):
        content = self.fakes.get_part_content(os.path.basename(self.path))
        self.send_response(200)
        self.send_header("content-type", "application/octet-stream")
        self.send_header("Content-Length", len(content))
        self.end_headers()
        self.wfile.write(content)

        
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

