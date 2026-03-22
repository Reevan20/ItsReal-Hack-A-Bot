import spidev
import time

class JoystickHandler:
    def __init__(self, channel_x=0, channel_y=1, deadzone=50):
        self.channel_x = channel_x
        self.channel_y = channel_y
        self.deadzone = deadzone

        # SPI setup
        self.spi = spidev.SpiDev()
        self.spi.open(0, 1)  # bus 0, device 0
        self.spi.max_speed_hz = 1350000

        # Default center (will calibrate)
        self.center_x = 512
        self.center_y = 512

    def read_adc(self, channel):
        # MCP3008 protocol
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        value = ((adc[1] & 3) << 8) + adc[2]
        return value  # 0–1023

    def calibrate(self, samples=50):
        total_x = 0
        total_y = 0

        for _ in range(samples):
            total_x += self.read_adc(self.channel_x)
            total_y += self.read_adc(self.channel_y)
            time.sleep(0.01)

        self.center_x = total_x // samples
        self.center_y = total_y // samples

    def read(self):
        x = self.read_adc(self.channel_x)
        y = self.read_adc(self.channel_y)

        # ---- STEERING ---- #
        if x > self.center_x + self.deadzone:
            steering = 1   # right
        elif x < self.center_x - self.deadzone:
            steering = -1  # left
        else:
            steering = 0

        # ---- THROTTLE ---- #
        if y > self.center_y + self.deadzone:
            throttle = 1   # forward
        else:
            throttle = 0

        return steering, throttle
