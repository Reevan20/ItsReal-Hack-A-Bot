import serial

class SerialHandler:
    def __init__(self, port='/dev/ttyACM0', baud=115200):
        self.ser = serial.Serial(port, baud, timeout=1)

    def send(self, msg: str):
        self.ser.write((msg + "\n").encode())

    def close(self):
        self.ser.close()
