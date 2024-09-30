
import requests

from src.processor import host_fakes
from src.m3u8_parser import M3U8Parser
from src.server import Server
from src.ffmpeg_downloader import downloader
import urlfile
from src.utils import get_file_name_from_url


def main(url=None):
    if not url:
        url = urlfile.url

    download_file_name = get_file_name_from_url(url)
    headers = requests.head(url).headers
    m3u8_text = requests.get(url, headers={"Referer": "https://emturbovid.com"}).text

    fakes_map, updated_m3u8_data = M3U8Parser(url, m3u8_text).generate_all_urls_from_m3u8()
    parts_thread = host_fakes(fakes_map)

    server = Server(parts_thread, updated_m3u8_data)
    server.start()
    downloader(download_file_name)
    server.stop()

if __name__ == "__main__":
    main()