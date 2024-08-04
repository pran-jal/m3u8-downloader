from email.header import Header
from email.mime import base
import requests as r
import base64
url = ['https://mmxpl.vidstream.pro/EqPVJvsPWF322yVezviuGdNz9wsVp_2yQlow5Od52MBlQ9QQHH4h9fsymRbkFPyI+tzdG4991OzR6vBoACOikmeZRvMMHLtbQZaivXxFIkYzNJElHAAzltGZvw7UoiyGeRinX1o4myn55zkboURBwqd_wa04TwHgws2BU8ys+ujdBJg_yF2Rkc1ZPdqIEpxDacxb/br/hls/720/0001.ts',
'https://mmxpl.vidstream.pro/EqPVJvsPWF322yVezviuGdNz9wsVp_2yQlow5Od52MBlQ9QQHH4h9fsymRbkFPyI+tzdG4991OzR6vBoACOikmeZRvMMHLtbQZaivXxFIkYzNJElHAAzltGZvw7UoiyGeRinX1o4myn55zkboURBwqd_wa04TwHgws2BU8ys+ujdBJg_yF2Rkc1ZPdqIEpxDacxb/br/hls/720/0002.ts',
'https://mmxpl.vidstream.pro/EqPVJvsPWF322yVezviuGdNz9wsVp_2yQlow5Od52MBlQ9QQHH4h9fsymRbkFPyI+tzdG4991OzR6vBoACOikmeZRvMMHLtbQZaivXxFIkYzNJElHAAzltGZvw7UoiyGeRinX1o4myn55zkboURBwqd_wa04TwHgws2BU8ys+ujdBJg_yF2Rkc1ZPdqIEpxDacxb/br/hls/720/0003.ts',
'https://mmxpl.vidstream.pro/EqPVJvsPWF322yVezviuGdNz9wsVp_2yQlow5Od52MBlQ9QQHH4h9fsymRbkFPyI+tzdG4991OzR6vBoACOikmeZRvMMHLtbQZaivXxFIkYzNJElHAAzltGZvw7UoiyGeRinX1o4myn55zkboURBwqd_wa04TwHgws2BU8ys+ujdBJg_yF2Rkc1ZPdqIEpxDacxb/br/hls/720/0004.ts',
'https://mmxpl.vidstream.pro/EqPVJvsPWF322yVezviuGdNz9wsVp_2yQlow5Od52MBlQ9QQHH4h9fsymRbkFPyI+tzdG4991OzR6vBoACOikmeZRvMMHLtbQZaivXxFIkYzNJElHAAzltGZvw7UoiyGeRinX1o4myn55zkboURBwqd_wa04TwHgws2BU8ys+ujdBJg_yF2Rkc1ZPdqIEpxDacxb/br/hls/720/0005.ts',
'https://mmxpl.vidstream.pro/EqPVJvsPWF322yVezviuGdNz9wsVp_2yQlow5Od52MBlQ9QQHH4h9fsymRbkFPyI+tzdG4991OzR6vBoACOikmeZRvMMHLtbQZaivXxFIkYzNJElHAAzltGZvw7UoiyGeRinX1o4myn55zkboURBwqd_wa04TwHgws2BU8ys+ujdBJg_yF2Rkc1ZPdqIEpxDacxb/br/hls/720/0006.ts',
'https://mmxpl.vidstream.pro/EqPVJvsPWF322yVezviuGdNz9wsVp_2yQlow5Od52MBlQ9QQHH4h9fsymRbkFPyI+tzdG4991OzR6vBoACOikmeZRvMMHLtbQZaivXxFIkYzNJElHAAzltGZvw7UoiyGeRinX1o4myn55zkboURBwqd_wa04TwHgws2BU8ys+ujdBJg_yF2Rkc1ZPdqIEpxDacxb/br/hls/720/0007.ts',
'https://mmxpl.vidstream.pro/EqPVJvsPWF322yVezviuGdNz9wsVp_2yQlow5Od52MBlQ9QQHH4h9fsymRbkFPyI+tzdG4991OzR6vBoACOikmeZRvMMHLtbQZaivXxFIkYzNJElHAAzltGZvw7UoiyGeRinX1o4myn55zkboURBwqd_wa04TwHgws2BU8ys+ujdBJg_yF2Rkc1ZPdqIEpxDacxb/br/hls/720/0008.ts',
'https://mmxpl.vidstream.pro/EqPVJvsPWF322yVezviuGdNz9wsVp_2yQlow5Od52MBlQ9QQHH4h9fsymRbkFPyI+tzdG4991OzR6vBoACOikmeZRvMMHLtbQZaivXxFIkYzNJElHAAzltGZvw7UoiyGeRinX1o4myn55zkboURBwqd_wa04TwHgws2BU8ys+ujdBJg_yF2Rkc1ZPdqIEpxDacxb/br/hls/720/0009.ts',
'https://mmxpl.vidstream.pro/EqPVJvsPWF322yVezviuGdNz9wsVp_2yQlow5Od52MBlQ9QQHH4h9fsymRbkFPyI+tzdG4991OzR6vBoACOikmeZRvMMHLtbQZaivXxFIkYzNJElHAAzltGZvw7UoiyGeRinX1o4myn55zkboURBwqd_wa04TwHgws2BU8ys+ujdBJg_yF2Rkc1ZPdqIEpxDacxb/br/hls/720/0010.ts',
'https://mmxpl.vidstream.pro/EqPVJvsPWF322yVezviuGdNz9wsVp_2yQlow5Od52MBlQ9QQHH4h9fsymRbkFPyI+tzdG4991OzR6vBoACOikmeZRvMMHLtbQZaivXxFIkYzNJElHAAzltGZvw7UoiyGeRinX1o4myn55zkboURBwqd_wa04TwHgws2BU8ys+ujdBJg_yF2Rkc1ZPdqIEpxDacxb/br/hls/720/0011.ts',
'https://mmxpl.vidstream.pro/EqPVJvsPWF322yVezviuGdNz9wsVp_2yQlow5Od52MBlQ9QQHH4h9fsymRbkFPyI+tzdG4991OzR6vBoACOikmeZRvMMHLtbQZaivXxFIkYzNJElHAAzltGZvw7UoiyGeRinX1o4myn55zkboURBwqd_wa04TwHgws2BU8ys+ujdBJg_yF2Rkc1ZPdqIEpxDacxb/br/hls/720/0012.ts',
]

a=b''

HEX = []
# for i in url:
#     HEX.append(r.get(i).content)
#     a+=r.get(i).content

# for i in HEX:
#     a+=i[564::]

HEX.append(r.get(url[0]).content)
print(HEX)
# for i in range(len(HEX)):
#     HEX[i] = base64.b64encode(HEX[i])

# print(len(base64.b64decode( HEX[0][:752:])))
# open('my_vids/x.mp4', 'wb').write(a)