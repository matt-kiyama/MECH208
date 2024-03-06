import serial
import time

port = "/dev/ttyACM0"
baud = 115200
ser = serial.Serial(port, baud)

while True:
    input_string = "10 10\n" #both fans at 10% duty cycle
    print(input_string)
    ser.write(input_string.encode('utf-8'))
    time.sleep(3)
    input_string = "50 10\n" #one fan at 50% duty cycle, one at 10% duty cycle
    print(input_string)
    ser.write(input_string.encode('utf-8'))
    time.sleep(5)
    input_string = "10 50\n" #one fan at 50% duty cycle, one at 10% duty cycle, fans switch speed
    print(input_string)
    ser.write(input_string.encode('utf-8'))
    time.sleep(5)
