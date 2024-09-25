import requests



class M3U8Parser:

    def __init__(self, url, master_m3u8_text) -> None:
        self.url = url
        self.fake_segments_map = {}


        if master_m3u8_text == None:
            master_m3u8_text = requests.get(url).text

        self.master_m3u8_text = master_m3u8_text
        self.m3u8_tags = master_m3u8_text.split("\n")


    def url_prefix(self):
        return self.url.replace(self.url.split("/").pop(), "")


    def generate_all_urls_from_m3u8(self):
        index = 1
        for tag in self.m3u8_tags:
            if not tag.startswith("#") and tag:
                self.master_m3u8_text = self.master_m3u8_text.replace(tag, f"{index}.fake")
                if tag.startswith("http"):
                    self.fake_sagments_map[f"{index}.fake"] = tag
                else:
                    self.fake_sagments_map[f"{index}.fake"] = f"{self.url_prefix()}{tag}"
                index+=1
            elif tag.startswith("#EXT-X-KEY"):
                method, uri = tag.split(",")
                method = method.split("=").pop()
                self.fake_sagments_map["fake.key"] = uri.split("=").pop().strip('"')
                self.master_m3u8_text = self.master_m3u8_text.replace(tag, tag.replace(uri, 'URI="fake.key"'))
