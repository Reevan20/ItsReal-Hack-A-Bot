from machine import Pin, SPI
from time import sleep, ticks_ms, ticks_diff
from nrf24l01 import NRF24L01

# Motor A (Left)
IN1 = Pin(2, Pin.OUT)
IN2 = Pin(3, Pin.OUT)

# Motor B (Right)
IN3 = Pin(4, Pin.OUT)
IN4 = Pin(5, Pin.OUT)

# RF transciever
spi = SPI(0, baudrate=4_000_000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(19), miso=Pin(16))
csn = Pin(10, Pin.OUT)
ce = Pin(9, Pin.OUT)

# LED
LED = Pin(6, Pin.OUT)

# ---- Motor Control Functions ---- #

def stop():
    IN1.low()
    IN2.low()
    IN3.low()
    IN4.low()

def forward():
    # Both motors forward
    IN1.high()
    IN2.low()
    
    IN3.high()
    IN4.low()

def backward():
    # Both motors backward
    IN1.low()
    IN2.high()
    
    IN3.low()
    IN4.high()

def left():
    # Left motor off, right motor forward
    IN1.low()
    IN2.low()
    
    IN3.high()
    IN4.low()

def right():
    # Right motor off, left motor forward
    IN1.high()
    IN2.low()
    
    IN3.low()
    IN4.low()

def init_test():
    forward()
    sleep(2)

    left()
    sleep(1)

    right()
    sleep(1)

    stop()
    sleep(2)

def get_blink_interval(distance):
    # Clamp distance range
    distance = max(5, min(distance, 100))
    
    # Map distance → interval (fast when close)
    # 5cm → 100ms, 100cm → 1000ms
    return int(100 + (distance - 5) * (900 / 95))

# --- Nain ---
# ---- NRF24L01 SETUP ---- #

nrf = NRF24L01(spi, csn, ce, payload_size=32)

# Pipe address (must match transmitter)
pipe = b"buggy"
nrf.open_rx_pipe(1, pipe)
nrf.start_listening()

# ---- LED TIMING ---- #
last_blink = ticks_ms()
blink_interval = 500  # default ms

while True:
    init_test()    

    if nrf.any():
        try:
            data = nrf.recv().decode().strip()
            print("Received:", data)

            # Expect format: "steering,throttle"
            steering, throttle, distance = map(int, data.split(","))

            blink_interval = get_blink_interval(distance)
        
            if throttle == 0:
                stop()
            else:
                if steering == 1:
                    left()
                elif steering == -1:
                    right()
                else:
                    forward()


        except Exception as e:
            print("Error:", e)
            stop()

    now = ticks_ms()
    if ticks_diff(now, last_blink) >= blink_interval:
        led.toggle()
        last_blink = now

    sleep(0.01)
