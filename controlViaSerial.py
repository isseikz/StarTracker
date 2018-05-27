import serial

class SerialCTRl(object):
    """docstring for SerialCTRl."""
    # def __init__(self, p, br=115200, to=10):
    def __init__(self, serial):
        self.s = serial
        self.isSending = False

    def write(self,data):
        self.s.write(data)
        self.s.close

    def read(self):
        res = self.s.readline()
        return res

    def controlMCU(self,data):
        if self.isSending == False:
            self.isSending = True
            self.s.write(data)
            self.s.close()

            while True:
                res = self.read()
                if res[4] == 0:
                    self.isSending = false
                    if res[6] == 0:
                        return True
        else:
            return False

if __name__ == '__main__':
    startCode = [17,34,51,68]
    flag = 16
    dataSize = 2

    ser = serial.Serial("COM10", 115200)
    com = SerialCTRl(ser)

    sentData = bytearray(b'\x11\x22\x33\x44\x10\x02\x01\x0a\r\n')
    res = com.write(sentData)

    sentData = bytearray(b'\x11\x22\x33\x44\x10\x02\x00\x05\r\n')
    res = com.write(sentData)
