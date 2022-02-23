import requests
import threading

thread_data = [b'']*485
def gets(i):
    print(f'getting {i} ....')
    thread_data[i] = requests.get('https://zdzye.vidstream.pro/EqPVJvsPWF322yVezviuGdNz9wsVp_2yTVow5Od52MBlQ9QQHn4g9fsywRf4FvyI+tzdG4991OzU4fFtBiOikmeZRvMMGbBaRJCivXxFIkYzNJElHAMylNGatA_UoimeZhCvTEQ97y6R+D0UtVNAz6N2wa0tWALvnsKGV8Sh9+zKF5NgwA_NwZ0BJoOCAZ1UYcQXvzA/br/hls/1080/'+str('%04d' %i)+'.ts').content
    print(f"done {i} ....")

threadss = []
for i in range (0, 485):
    t = threading.Thread(target=gets,args=(i,))
    threadss.append(t)
    t.start()

for i in threadss:
    t.join()                # to keep program running till last thread is completed, seartg join()

for t in threadss :
    while t.is_alive():
        continue


print("all process download complete")
f = open("C:\\Users\\Pranjal\\Documents\\VS Code\\Python\\Download\\10_2\\hello.ts", "wb")
print("file open success")
for i in thread_data:
    f.write(i)
print("file data written")
f.close()