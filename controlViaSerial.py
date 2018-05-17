import serial

class SerialCTRl(object):
    """docstring for SerialCTRl."""
    def __init__(self, port, baudrate=115200, to=10):
        self.s = serial.Serial(port,baudrate,timeout=to)
        self.isSending = false

    def write(data):
        self.s.write(data)
        s.close

    def read():
        res = self.s.readline()
        return res

    def controlMCU(data):
        if isSending == False:
            isSending = True
            write(data)
            s.close()

            while True:
                res = read()
                if res[4] == 0:
                    self.isSending = false
                    if res[6] == 0:
                        return True
        else:
            return False

if __name__ == '__main__':
    main()
