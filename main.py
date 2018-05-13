import pysony
import six
import binmom

search = pysony.ControlPoint()
cameras = search.discover(5)

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

# TODO: 写真を撮る/ Liveviewを始める
# TODO: 画面上に撮影画像(n秒ごと) or Liveviewを表示
# TODO: 誤差の解析
# TODO: モータの制御
