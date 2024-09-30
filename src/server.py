from functools import partial
from http.server import HTTPServer
import threading

from src.request_handler import CustomHTTPRequestHandler



class Server:
    
    def __init__(self, parts_data_to_serve, updated_m3u8_data) -> None:
        self.parts_data_to_serve = parts_data_to_serve
        self.updated_m3u8_data = updated_m3u8_data

    
    def start(self):
        server_address = ("", 8000)
        partial_handler = partial(CustomHTTPRequestHandler, self.parts_data_to_serve, self.updated_m3u8_data)
        self.server = HTTPServer(server_address, partial_handler)
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True, args=()).start()
        print(f"Now serving at: http://localhost:{self.server.server_address[1]}")

    
    
    def stop(self):
        if self.server_thread:
            self.server_thread.join()
            while self.server_thread.is_alive():
                continue
        
        self.server.shutdown()
        self.server.server_close()

    
    def __del__(self):
        if self.server_thread and self.server_thread.is_alive():
            self.stop()
