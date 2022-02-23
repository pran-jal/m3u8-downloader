import requests
import threading

def gets(i, url):
    print(f'getting {i} ....')
    f = open("C:\\Users\\Pranjal\\Documents\\VS Code\\Python\\Download\\9\\%04d.ts" %i, "wb")
    f.write(requests.get(url+str('%04d' %i)+'.ts').content)
    f.close()
    print(f' done {i} ...')

threadss = []
url = input("URL: ")
url = 'https://rnrlz.vidstream.pro/EqPVIPsNUV322yVezviuGdNz9wsVp_2yTlow5Od52MBlQ9QQS34k9aIzxgL+C_yI+tzdG4991OzT7fVrDiOikmeZRvMMHrxeQpiivXxFIkYzNJElHAAylNGaugrUoS2cZhCvTUQ97y6R+D0UtVNAz6N2wagmWALvnsKGV8Sh9+zKF5NgyE6Mk81ZPdqIEpxDacxb/br/hls/1080/1080.m3u8'


for i in range (0, 474):
    t = threading.Thread(target=gets,args=(i, url[:-9:]))
    threadss.append(t)
    t.start()

for i in threadss:
    t.join()                # to keep program running till last thread is completed, seartg join()
