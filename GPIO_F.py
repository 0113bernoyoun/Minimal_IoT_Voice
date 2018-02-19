import RPi.GPIO as GPIO
import time

room1_led=3
room2_led=15

servo_pin=18  # PWM pin num 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin,GPIO.OUT)
GPIO.setup(room1_led,GPIO.OUT)
GPIO.setup(room2_led,GPIO.OUT)
p=GPIO.PWM(servo_pin,50)
p.start(0)
cnt=0
GPIO.output(room1_led,False)
GPIO.output(room2_led,False)
