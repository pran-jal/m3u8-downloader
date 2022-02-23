import requests
import threading

a = b''
f = open("C:\\Users\\Pranjal\\Documents\\VS Code\\Python\\Download\\11\\final.mp4", "wb")

try :
    for i in range (0, 485):
        print("getting %d ..." %i)
        a+=requests.get('https://zdzye.vidstream.pro/EqPVJvsPWF322yVezviuGdNz9wsVp_2yTVow5Od52MBlQ9QQHn4g9fsywRf4FvyI+tzdG4991OzU4fFtBiOikmeZRvMMGbBaRJCivXxFIkYzNJElHAMylNGatA_UoimeZhCvTEQ97y6R+D0UtVNAz6N2wa0tWALvnsKGV8Sh9+zKF5NgwA_NwZ0BJoOCAZ1UYcQXvzA/br/hls/1080/'+str('%04d' %i)+'.ts').content
        print("completed %d ..." %i)

except :
    f.write(a)
    f.close()

f.write(a)
f.close()