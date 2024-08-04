import requests
import threading
import url

thread_data = [b'']*474
def gets(i):
    print(f'getting {i} ....')
    thread_data[i] = requests.get(url.url+str('%04d' %i)+'.ts').content
    print(f"done {i} ....")

threadss = []
for i in range (0, 474):
    t = threading.Thread(target=gets,args=(i,))
    threadss.append(t)
    t.start()

for i in threadss:
    t.join()                # to keep program running till last thread is completed, seartg join()

for t in threadss :
    while t.is_alive():
        continue


print("all process download complete")
f = open("C:\\Users\\Pranjal\\Documents\\VS Code\\Python\\TS downloader\\10_2\\hello.ts", "wb")
print("file open success")
for i in thread_data:
    f.write(i)
print("file data written")
f.close()