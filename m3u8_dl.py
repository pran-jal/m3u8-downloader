
import requests

from src.processor import StreamProcessor, host_fakes
from src.m3u8_parser import generate_all_urls_from_m3u8
from src.server import Server
from src.ffmpeg_downloader import downloader
import url


def main():
    download_file_name = "test_one1"
    headers = requests.head(url.url).headers
    m3u8_text = requests.get(url.url, headers={"Referer": "https://emturbovid.com"}).text

    fakes_map, updated_m3u8_data = generate_all_urls_from_m3u8(url.url, m3u8_text)
    parts_thread = host_fakes(fakes_map)

    server = Server(parts_thread, updated_m3u8_data)
    server.start()
    downloader(download_file_name)
    server.stop()

if __name__ == "__main__":
    main()