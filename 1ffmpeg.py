import subprocess
import url
import threading

def gets(i):
    s = 'ffmpeg -i "%s" -c copy my_vids\%d.ts -y' %(url.url.format(i), i)
    subprocess.run(["powershell", "-command", "%s" %(s)] )

threadss = []
lol_str = "concat:"
for i in range (590, 654):
    lol_str+=f"my_vids\\{i}.ts|"
    t = threading.Thread(target=gets,args=(i,))
    t.start()
    threadss.append(t)

for i in threadss:
    t.join()                # to keep program running till last thread is completed, seartg join()

for t in threadss:
    while t.is_alive() :
        continue


# ffmpeg concat:file1.ts|file2.ts can be used toconcat mpeg-ts streams ie .ts extension files as these files already have the demuxing info available.
    
lol_str = lol_str.strip('|')
s = 'ffmpeg -i "%s" -c copy output.mp4' %(lol_str)
subprocess.run(["powershell", "-command", "%s" %(s)] )
print(f' done concatin ...')