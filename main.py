import pysony
import six
import http

import time
import io
import cv2

from PIL import Image
from matplotlib import pyplot as plt
import numpy as np

import binmom

search = pysony.ControlPoint()
cameras = search.discover(5)
if len(cameras) == 0:
    print("Your camera is not found...")
    exit()
    pass

print(cameras)
for x in cameras:
    print("Camera: %s" % x)

if len(cameras) > 1:
    print("Which?[0]")
    for cam in cameras:
        print(cam)

# TODO: 複数のデバイスが見つかった時に選択させる
x = cameras[0]
camera = pysony.SonyAPI(QX_ADDR=x)

mode = camera.getAvailableApiList()
print(mode)
print("")

res = camera.startLiveview()
print(res)

conn = http.client.HTTPConnection("10.0.0.1:60152")
conn.request("GET", "/liveview.JPG?!1234!http-get%3a*%3aimage%2fjpeg%3a*!!!!!")
res = conn.getresponse()

cnt = 0
while True:
    cnt += 1

    commonHeaderLength = 1 + 1 + 2 + 4
    commonHeader = res.read(commonHeaderLength)
    payloadType = commonHeader[1]
    sequenceNumber = commonHeader[2:4]
    print("Payload type: %d" % payloadType)

    payloadHeader = res.read(128)
    startCode = payloadHeader[0:4]

    payloadDataSize = payloadHeader[4:7]
    paddingSize = payloadHeader[7]
    print("%d, %d, %d" % (payloadDataSize[0],payloadDataSize[1],payloadDataSize[2]))
    dataSize = int.from_bytes(payloadDataSize,'big')
    print("Data size    [Bytes]: %d" % dataSize)
    print("Padding size [Bytes]: %d" % paddingSize)

    payloadData = res.read(dataSize)
    if paddingSize != 0:
        paddingData = res.read(paddingSize)

    if payloadType == 1:
        print("Show:")
        img = Image.open(io.BytesIO(payloadData))

        filename = 'out%d.jpg' % int.from_bytes(sequenceNumber,'big')
        img.save(filename)
        img_saved = cv2.imread(filename)
        # cv2.imshow('Liveview',img_saved)

        error, center = binmom.run(img_saved)

        if cnt % 10 == 0:
            cv2.circle(img_saved, (center[0],center[1]), 10, (0,0,255), -1)
            plt.imshow(cv2.cvtColor(img_saved, cv2.COLOR_BGR2RGB))
            plt.pause(.01)
            pass


# TODO: モータの制御
def controlMotor(error):
    error = np.array(error)
    gain  = np.matrix([
    [1,0],
    [0,1]
    ])
    input = gain * error
    btSend(input)
