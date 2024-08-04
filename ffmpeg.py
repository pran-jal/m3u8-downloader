import subprocess
import url
import threading
import requests as r

url = url.url
c = 'cd 10'

def gets(i):
    print(f'getting {i} ....')
    s = 'ffmpeg -i "%s%04d.ts" -c copy %04d.ts -v 0' %(url, i, i)
    subprocess.run(["powershell", "-command", "%s; %s" %(c, s)] )
    print(f' done {i} ...')



# for j in range (1, 47):

#     threadss = []
#     for i in range((j-1)*10, j*10) :
#         t = threading.Thread(target=gets,args=(i,))
#         threadss.append(t)
#         t.start()

#     for i in threadss:
#         t.join()                # to keep program running till last thread is completed, seartg join()

#     for t in threadss:
#         while t.is_alive() :
#             continue


threadss = []
for i in range (474):
    t = threading.Thread(target=gets,args=(i,))
    threadss.append(t)
    t.start()

for i in threadss:
    t.join()                # to keep program running till last thread is completed, seartg join()

for t in threadss:
    while t.is_alive() :
        continue