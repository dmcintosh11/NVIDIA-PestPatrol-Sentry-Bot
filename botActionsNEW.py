import Jetson.GPIO as GPIO
import time
import threading

class botActions:

    
    def __init__(self, motor_pin=32):
        self.motor_pin = motor_pin
        #self.is_shooting = False
        self.thread_lock = threading.Lock()
        #Initiates output nodes
        GPIO.setmode(GPIO.BOARD)
        # or
        #GPIO.setmode(GPIO.BCM)
        # or
        #GPIO.setmode(GPIO.CVM)
        # or
        #GPIO.setmode(GPIO.TEGRA_SOC)

        self.released_angle = 0
        self.pulled_angle = 45


        GPIO.setup(motor_pin, GPIO.OUT)

        self.pwm_frequency = 50  # Frequency for servo control (50Hz is common)
        self.pwm = GPIO.PWM(self.motor_pin, self.pwm_frequency)
        self.pwm.start(0)
        self.set_servo_angle(self.released_angle)
    
    def set_servo_angle(self, angle):
        duty_cycle = self.angle_to_duty_cycle(angle)
        self.pwm.ChangeDutyCycle(duty_cycle)

    def angle_to_duty_cycle(self, angle):
        # Converts angle (0-180 degrees) to duty cycle (usually 2-12%)
        # Adjust this formula based on your specific servo
        return 2 + (angle / 18)

    def pull_trigger(self):
        #GPIO.output(self.motor_pin, GPIO.HIGH)
        self.set_servo_angle(self.pulled_angle)

    def release_trigger(self):
        #GPIO.output(self.motor_pin, GPIO.LOW)
        self.set_servo_angle(self.released_angle)

    def shoot_racoon(self, duration=2):
        with self.thread_lock:
            print("Thread starting")
            #self.is_shooting = True
            self.pull_trigger()

            #Sleep won't work since it will pause all functionality from other file
            time.sleep(duration)

            self.release_trigger()
            time.sleep(duration)
            #self.is_shooting = False
            print('Thread ending')

    def threaded_shoot_racoon(self, duration=2):
        if not self.thread_lock.locked():

            motor_thread = threading.Thread(target=self.shoot_racoon, args=(duration,))
            motor_thread.start()

    def is_shooting(self):
        return self.thread_lock.locked()

    def clean(self):
        #Closes all pins and sets them to default
        self.set_servo_angle(0)
        self.pwm.stop()
        GPIO.cleanup()
        time.sleep(2)