import requests
import url

a = b''
f = open("C:\\Users\\Pranjal\\Documents\\VS Code\\Python\\TS downloader\\11\\final.ts", "wb")

try :
    for i in range (0, 485):
        print("getting %d ..." %i)
        a+=requests.get(url.url+str('%04d' %i)+'.ts').content
        print("completed %d ..." %i)

except Exception as e:
    print(e)
    f.write(a)
    f.close()

else :
    f.write(a)
    f.close()