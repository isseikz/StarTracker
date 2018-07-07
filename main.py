#!/usr/bin/python
# -*- coding: utf-8 -*-

import http

import time
import io
import cv2

from PIL import Image
from matplotlib import pyplot as plt
import numpy as np

import json
import urllib.parse
from time import sleep

import PD
import PID

import serial

import binmom
import controlViaSerial as cvs
import gainAdjuster as ga
import msearch

def sendData(steps, com):
    # TODO: implementation
    """convert the steps into packet data and send it"""
    if steps[0] < 0:
        dir = b'\x00'
    else:
        dir = b'\x01'


    if abs(steps[0]) > 250:
        phase = int(250)
    else:
        phase = int(round(abs(steps[0])))

    data = bytearray()
    phaseBytes = phase.to_bytes(1,'big')
    data =b'\x11\x22\x33\x44\x10\x02' + dir + phaseBytes + b'\r\n'

    com.write(data)
    pass

def controlMotor1(error, com, threshold):
    if error[0] > threshold:
        yaw = b'\x01'
    elif error[0] < -threshold:
        yaw = b'\x00'
    else:
        yaw = b'\x10'
        pass

    if error[1] > threshold*2:
        pitch = b'\x01'
    elif error[1] < -threshold*2:
        pitch = b'\x00'
    else:
        pitch = b'\x10'
        pass

    sentData = b'\x11\x22\x33\x44\x10\x02'+yaw+pitch +b'\r\n'
    com.write(sentData)
    return True

def controlMotorPD(controller, error, com):
    """send data to ESP32 with desired steps calculated by PD control."""
    controller.updateData(error)
    ctrl = controller.getControlParam()
    sendData(ctrl,com)


def controlMotorPID(controller, error, com):
    """send data to ESP32 with desired steps calculated by PID control."""
    controller.updateData(error)
    ctrl = controller.getControlParam()
    sendData(ctrl,com)


def run():
    thresholdCTRL = 10 #threshold for driving motor or not[pixel]

    uri, host, url, cameraHost, cameraUrl =  msearch.urlLiveview()
    print(f'connect to http://{host}/{url}')

    print(cameraHost)
    print(cameraUrl)
    control = http.client.HTTPConnection(cameraHost)
    jsonDict = {"method":"startLiveview","params":[],"id":1,"version":"1.0"}
    jsonData = json.dumps(jsonDict)
    print(jsonData)
    control.request("POST", cameraUrl, body=jsonData)
    # control.request("POST", cameraUrl)
    conres = control.getresponse()
    control.close()
    jsonRes = json.load(conres)
    print(jsonRes)
    print(urllib.parse.unquote(jsonRes['result'][0]))

    control = http.client.HTTPConnection(cameraHost)
    jsonDict = {"method":"setShootMode","params":["movie"],"id":1,"version":"1.0"}
    jsonData = json.dumps(jsonDict)
    print(jsonData)
    control.request("POST", cameraUrl, body=jsonData)
    # control.request("POST", cameraUrl)
    conres = control.getresponse()
    control.close()
    jsonRes = json.load(conres)
    print(jsonRes)
    #
    control = http.client.HTTPConnection(cameraHost)
    jsonDict = {"method":"startMovieRec","params":[],"id":1,"version":"1.0"}
    jsonData = json.dumps(jsonDict)
    print(jsonData)
    control.request("POST", cameraUrl, body=jsonData)
    # control.request("POST", cameraUrl)
    conres = control.getresponse()
    control.close()
    jsonRes = json.load(conres)
    print(jsonRes)

    time.sleep(1)

    conn = http.client.HTTPConnection(host)
    conn.request("GET", '/'+url)
    res = conn.getresponse()


    ser = serial.Serial("COM10", 115200)
    com = cvs.SerialCTRl(ser)
    sentData = bytearray(b'\x11\x22\x33\x44\x11')
    com.write(sentData)


    # PD = PD.PDControl(0.5, 0.3)
    PIDctrl = PID.PIDControl(0.5, 0.3, 0.3)

    payloadData = None
    pastData = None

    cnt = 0
    while True:
        cnt += 1

        commonHeaderLength = 1 + 1 + 2 + 4
        commonHeader = res.read(commonHeaderLength)
        payloadType = commonHeader[1]
        sequenceNumber = commonHeader[2:4]
        # print("Payload type: %d" % payloadType)

        payloadHeader = res.read(128)
        startCode = payloadHeader[0:4]

        payloadDataSize = payloadHeader[4:7]
        paddingSize = payloadHeader[7]
        # print("%d, %d, %d" % (payloadDataSize[0],payloadDataSize[1],payloadDataSize[2]))
        dataSize = int.from_bytes(payloadDataSize,'big')
        # print("Data size    [Bytes]: %d" % dataSize)
        # print("Padding size [Bytes]: %d" % paddingSize)

        if payloadData != None:
            pastData = payloadData
            pass
        payloadData = res.read(dataSize)
        if paddingSize != 0:
            paddingData = res.read(paddingSize)

        if payloadType == 1:
            # print("Show:")

            # redefineThresholdCTRL(thresholdCTRL, error)
            if cnt % 5 == 0:
                img_np = cv2.imdecode(np.fromstring(payloadData, np.uint8), cv2.IMREAD_COLOR)
                if pastData != None:
                    imgPast_np = cv2.imdecode(np.fromstring(pastData, np.uint8), cv2.IMREAD_COLOR)
                    error, center = binmom.runPink(img_np)
                # error, center = binmom.run(img_np)
                # print(error)
                # controlMotorPID(PIDctrl, error, com)
                controlMotor1(error, com, thresholdCTRL)

            if cnt % 5 == 0:
                cv2.namedWindow('StarTracker', cv2.WINDOW_NORMAL)
                cv2.imshow("StarTracker",img_np)
                cv2.waitKey(1)

            if cnt % 100 == 0:
                img = Image.open(io.BytesIO(payloadData))

                filename = 'out%d.jpg' % int.from_bytes(sequenceNumber,'big')
                img.save(filename)

                # pass


        # controlMotorPD(PD, error, com)



if __name__ == '__main__':
    run()
