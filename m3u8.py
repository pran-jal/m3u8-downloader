import requests as r
import url


f = open("1080.m3u8", 'wb')

f.write(r.get(url.url+"1080.m3u8").content)

f.close()