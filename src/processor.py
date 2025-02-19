import concurrent
import requests
import threading

class StreamProcessor:
    def __init__(self, parts_map) -> None:
        self.parts_map = parts_map
        self.active_threads_map = {}
        self.fake_parts_map = {}
        self.remaining = len(parts_map)
        self.max_thread_count = 100
        self.download_complete = False


    def _get_part_content(self, part_name, endpoint):
        tries = 5
        host = endpoint.split("://").pop().split("/")[0]
        while tries:
            try:
                c = requests.get(endpoint, headers={"Host": host}, timeout=200)
                if c.status_code != 200:
                    print(f"{part_name}: failed to download. Error: {c.status_code}, {c.reason}, {self.remaining} remaining", end="\r")
                    continue
                    #TODO handle retry
                self.fake_parts_map[part_name] = c.content
                self.remaining-=1
                print(end="\r")
                print(f"{part_name} complete. {self.remaining} remaining", end="\r")
                break
            except:
                tries-=1
        else:
            self.active_threads_map.pop(part_name)
            with open("report.txt", "a") as f:
                f.write(f"failed to download: {part_name}\n")


    def download_part(self, part, endpoint):
        while threading.active_count() > self.max_thread_count:
            continue

        thread = threading.Thread(target=self._get_part_content, name=part, daemon=True, args=(part, endpoint,))
        self.active_threads_map[part] = thread
        thread.start()

        if self.remaining == 0:
            self.download_complete = True


    # def download_part_with_workers(self):
    #     with concurrent.futures.ThreadPoolExecutor(self.max_thread_count) as executor:
    #         for part, endpoint in self.parts_map.items():
    #             executor.submit(self._get_part_content, part, endpoint)


    # def get_download_parts(self):
    #     self.download_part_with_workers()


    def start_download_parts(self):
        for part, endpoint in self.parts_map.items():
            self.download_part(part, endpoint)


    def get_part_content(self, part_name):
        if not self.active_threads_map.get(part_name):
            self.download_part(part_name, self.parts_map[part_name])

        thread = self.active_threads_map.get(part_name)
        while thread.is_alive():
            continue
        
        return self.fake_parts_map.pop(part_name)
    

    def download(self):
        if not hasattr(self, "downloader_thread"):
            self.downloader_thread = threading.Thread(target=self.start_download_parts, name="downloader_thread", daemon=True, args=())
            self.downloader_thread.start()
        
        elif self.downloader_thread.is_alive():
                print("Already downloading...")

        elif self.download_complete:
            ans = input("Dowloading already completed. Do you wish to restart (Y/N) ?")
            if ans in "Yy":
                self.download_complete = False
                self.remaining = len(self.parts_map)
                if hasattr(self, "downloader_thread"):
                    del self.downloader_thread
                self.download()

        



def host_fakes(fakes_map):
    thread_processor = StreamProcessor(fakes_map)
    thread_processor.download()
    return thread_processor