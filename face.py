
import httplib, urllib, base64
import json

########### Call Face - detect API #############
headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'f3cda7c8e0cd4a24a5a9746976e29c0c',
}

params = urllib.urlencode({
    # Request parameters
    'returnFaceId': 'false',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'emotion',
})

url_face = 'http://pngimg.com/uploads/man/man_PNG6534.png'
url_face2 = 'https://snapshot2.blob.core.windows.net/test/myblockblob'
orange = 'http://battaco.com/wp-content/uploads/2014/06/Orange.jpg'

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/detect?%s" % params, "{\"url\":\""+ url_face +"\"}", headers)
    response = conn.getresponse()
    data = response.read()
    #print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
#######################################

#print(data)
########### Parse JSON #############
for char in data:
    if char in "[]":
        data = data.replace(char,'')


#j = json.loads(data)
#print(j)
####################################


#### Detect face, return bool ######
x = 'faceAttributes'
boo = x in data
print boo
####################################

##### Detect roll###################
emotion_comfort = 'Cheer up! This is not the worst day! <3'
if boo:
	j = json.loads(data)
	anger = j['faceAttributes']['emotion']['anger']
	sadness = j['faceAttributes']['emotion']['sadness']
	if anger > 0.2:
		print emotion_comfort
	elif sadness > 0.2:
		print emotion_comfort

####################################


#print(j)
#j = json.loads('{"faceId":"866b979b-04c9-4cc9-b930-47a5e9874a4d","faceRectangle":{"top":435,"left":667,"width":551,"height":551},"faceAttributes":{"smile":0.296}}')
#j = json.loads(+ data + )
#print j['faceRectangle']

#[{"faceRectangle":{"top":435,"left":667,"width":551,"height":551},"faceAttributes":{"headPose":{"pitch":0.0,"roll":-0.2,"yaw":1.0}}}]



# import cognitive_face as CF

# KEY = '3810f64a2e524c8c81037ca4d4069a0f'  # Replace with a valid subscription key (keeping the quotes in place).
# CF.Key.set(KEY)

# # You can use this example JPG or replace the URL below with your own URL to a JPEG image.
# img_url = 'http://www.pk.all.biz/img/pk/catalog/middle/3474.jpeg'
# result = CF.face.detect(img_url)
# print result

# import time
# time1 = time.time()
# print time1
# product = 1

# #for i in range(1, 100000):
# #	product = product * i

# time2 = time.time()
# print time2

# import datetime
# dt = datetime.datetime.now()
# print dt.hour, dt.minute, dt.second