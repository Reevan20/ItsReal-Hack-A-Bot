from machine import Pin
from time import sleep

# Motor A (Left)
IN1 = Pin(2, Pin.OUT)
IN2 = Pin(3, Pin.OUT)

# Motor B (Right)
IN3 = Pin(4, Pin.OUT)
IN4 = Pin(5, Pin.OUT)

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


while True:
	init_test()    
