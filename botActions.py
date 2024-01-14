import Jetson.GPIO as GPIO
import time
import threading

class botActions:
    
    def __init__(self, motor_pin=20):
        self.motor_pin = motor_pin
        #Initiates output nodes
        GPIO.setmode(GPIO.BOARD)
        # or
        #GPIO.setmode(GPIO.BCM)
        # or
        #GPIO.setmode(GPIO.CVM)
        # or
        #GPIO.setmode(GPIO.TEGRA_SOC)
        
        
        GPIO.setup(motor_pin, GPIO.out)
        
        pwm_frequency = 50  # Frequency for servo control (50Hz is common)
        self.pwm = GPIO.PWM(motor_pin, pwm_frequency)
        self.pwm.start(0)
        
    def set_servo_angle(self, angle):
        duty_cycle = self.angle_to_duty_cycle(angle)
        self.pwm.ChangeDutyCycle(duty_cycle)

    def angle_to_duty_cycle(self, angle):
        # Converts angle (0-180 degrees) to duty cycle (usually 2-12%)
        # Adjust this formula based on your specific servo
        return 2 + (angle / 18)

    def pull_trigger(self):
        #GPIO.output(self.motor_pin, GPIO.HIGH)
        self.set_servo_angle(90)
        
    def release_trigger(self):
        #GPIO.output(self.motor_pin, GPIO.LOW)
        self.set_servo_angle(0)
        
    def shoot_racoon(self, duration=2):
        self.is_shooting = True
        self.pull_trigger()
        
        #Sleep won't work since it will pause all functionality from other file
        time.sleep(duration)
        
        self.release_trigger()
        self.is_shooting = False
    
    def threaded_shoot_racoon(self, duration=2):
        motor_thread = threading.Thread(target=self.shoot_racoon, args=(duration,))
        motor_thread.start()
    
    def clean(self):
        #Closes all pins and sets them to default
        self.pwm.stop()
        GPIO.cleanup()