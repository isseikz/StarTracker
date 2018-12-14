#!/usr/bin/python
# -*- coding: utf-8 -*-
"""画像の２値化(binalize)とモーメント中心を見つけるモジュール."""

import numpy as np
import cv2
from matplotlib import pyplot as plt


def binalize(img):
    """画像の２値化を行う.

    1. 画像をグレースケールに変換
    2. しきい値[0, 255]を基準に２値化する

    # 入力：
     + img: cv2 モジュールで読み込んだ画像オブジェクト
    # 出力：
     + img_binalized: 2値化した画像オブジェクト

    参考
    https://www.blog.umentu.work/python-opencv3%E3%81%A7%E7%94%BB%E5%83%8F%E3%81%AE%E7%94%BB%E7%B4%A0%E5%80%A4%E3%82%92%E4%BA%8C%E5%80%A4%E5%8C%96%E3%81%97%E3%81%A6%E5%87%BA%E5%8A%9B/
    """
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = 60
    max_pixel = 255
    ret, img_binalized = cv2.threshold(
        img_gray,
        thresh,
        max_pixel,
        cv2.THRESH_BINARY
    )
    return img_binalized


def getCoG(img):
    """輪郭の重心を求める.輪郭が見つからなければ中心を出力.

    # 入力
     + img: cv2モジュールの画像オブジェクト
    # 出力
     + [x, y]: 輪郭から得られた重心位置
    参考
    http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html
    """
    img_size = np.array([img.shape[1], img.shape[0]])
    mu = cv2.moments(img, False)
    if mu["m00"] < 1.0e-2:
        # cv2.imshow("image",img)
        x = int(img_size[0]/2)
        y = int(img_size[1]/2)
    else:
        x, y = int(mu["m10"]/mu["m00"]), int(mu["m01"]/mu["m00"])
        pass

    return np.array([x, y])


def run(img):
    """色抽出を行わずに解析を行う.

    # 入力
     + img: cv2モジュールの画像オブジェクト
    # 出力
     + error: 重心位置の、画像中心からのずれ
     + center: 輪郭の重心位置
    """
    img_size = np.array([img.shape[1], img.shape[0]])

    img_binalized = binalize(img)
    center = getCoG(img_binalized)
    error = center - img_size/2

    print("Position: [%d, %d]" % (center[0], center[1]))
    print("Error: [%d, %d]" % (error[0], error[1]))
    print("Center: [%d, %d]" % (center[0], center[1]))

    cv2.circle(
        img,
        (center[0], center[1]),
        int(img.shape[1] * 0.01),
        (0, 0, 255),
        -1
    )

    return error, center


def runMovingObject(img, pastImg):
    """動体検出用.２つの画像から変化した部分の中心を出力.

    # 入力
    + img: cv2モジュールの画像オブジェクト
    + pastImg: cv2モジュールの画像オブジェクト
    # 出力
     + error: 重心位置の、画像中心からのずれ
     + center: 輪郭の重心位置

    例えば、img=現在の画像、pastImg=初期状態の画像とすれば、初期からの変位が取れるはず。
    """
    img_size = np.array([img.shape[1], img.shape[0]])

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    pastGray = cv2.cvtColor(pastImg, cv2.COLOR_RGB2GRAY)

    # cv2.accumulateWeighted(gray, pastGray, 0.5)
    delta = cv2.absdiff(gray, pastGray)

    ret, img_binalized = cv2.threshold(delta, 100, 255, cv2.THRESH_BINARY)
    center = getCoG(img_binalized)
    error = center - img_size/2

    print("Position: [%d, %d]" % (center[0], center[1]))
    print("Error: [%d, %d]" % (error[0], error[1]))
    print("Center: [%d, %d]" % (center[0], center[1]))

    cv2.circle(
        img,
        (center[0], center[1]),
        int(img.shape[1] * 0.01),
        (0, 0, 255),
        -1
    )

    return error, center


def runPink(img):
    """画像からピンク色を抽出し、解析を行う.

    # 入力
     + img: cv2モジュールの画像オブジェクト
    # 出力
     + error: 重心位置の画像中心からのずれ
     + center: 輪郭の重心位置

    lowerPink, upperPink を調整することで,他の色を抽出できる,
    配列は画像のHSVを表していて,[H, S, V]となる.
    範囲の決め方は以下を参考（英語）
    https://stackoverflow.com/questions/47483951/how-to-define-a-threshold-value-to-detect-only-green-colour-objects-in-an-image/47483966#47483966
    リンク先に載ってる図から欲しい色範囲を決めて,
    x範囲→H, y範囲→S に入れればよさげ.
    V は[20, 255]くらいで適当に.
    """
    img_size = np.array([img.shape[1], img.shape[0]])
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lowerPink = np.array([150, 150, 20])
    upperPink = np.array([170, 255, 255])

    # # オレンジはこれくらい？
    # lowerOrange = np.array([10, 150, 20])
    # upperOrange = np.array([25, 255, 255])
    #
    # # 赤はこれくらい？
    # lowerRed = np.array([165, 150, 20])
    # upperRed = np.array([180, 255, 255])

    imgMask = cv2.inRange(imgHSV, lowerPink, upperPink)
    imgMasked = cv2.bitwise_and(img, img, mask=imgMask)
    # plt.figure()
    # plt.imshow(cv2.cvtColor(imgMasked, cv2.COLOR_RGB2BGR))
    # plt.show()

    img_gray = cv2.cvtColor(imgMasked, cv2.COLOR_BGR2GRAY)
    # plt.figure()
    # plt.imshow(img_gray, cmap='gray')
    # plt.show()

    ret, img_binalized = cv2.threshold(img_gray, 60, 255, cv2.THRESH_BINARY)
    # plt.figure()
    # plt.imshow(img_binalized, cmap='gray')
    # plt.show()

    center = getCoG(img_binalized)
    error = center - img_size/2

    print("Position: [%d, %d]" % (center[0], center[1]))
    print("Error: [%d, %d]" % (error[0], error[1]))
    print("Center: [%d, %d]" % (center[0], center[1]))

    cv2.circle(
        img,
        (center[0], center[1]),
        int(img.shape[1] * 0.01),
        (0, 0, 255),
        -1
    )

    return error, center


if __name__ == '__main__':
    img = cv2.imread('./20180707test/out599.jpg', 1)
    error, center = runPink(img)

    cv2.circle(
        img,
        (center[0], center[1]),
        int(img.shape[1] * 0.01),
        (0, 0, 255),
        -1
    )
    plt.figure()
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    plt.show()

    # img = cv2.imread('./test/IMAGE_MOON.JPG',1)
    # error, center = run(img)
    #
    # cv2.circle(
    #     img,
    #     (center[0], center[1]),
    #     int(img.shape[1] * 0.01),
    #     (0, 0, 255),
    #     -1
    # )
    # plt.figure()
    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    # plt.show()
    #
    # img = cv2.imread('./test/IMAGE_MOON2.JPG',1)
    # error, center = run(img)
    #
    # cv2.circle(
    #     img,
    #     (center[0], center[1]),
    #     int(img.shape[1] * 0.01),
    #     (0, 0, 255),
    #     -1
    # )
    # plt.figure()
    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    # plt.show()
    #
    # img = cv2.imread('./test/IMAGE_MOON3.JPG',1)
    # error, center = run(img)
    #
    # cv2.circle(
    #     img,
    #     (center[0], center[1]),
    #     int(img.shape[1] * 0.01),
    #     (0, 0, 255),
    #     -1
    # )
    # plt.figure()
    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    # plt.show()
