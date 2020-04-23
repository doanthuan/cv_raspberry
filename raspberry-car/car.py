import RPi.GPIO as GPIO
import sys
from time import sleep
 
GPIO.setmode(GPIO.BCM)
 
# khai bao cac chan
Motor1A = 15
Motor1B = 18
Motor2A = 23
Motor2B = 24
 
# thiet lap cac cong ra
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)

def toi():
    print("toi")
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)

def lui():
    print("lui")
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)

count = 1
while count < 10:
 
    try:  
        
        toi()

        sleep(1)

        lui()
        
        sleep(1)
        
        count += 1
      
    except KeyboardInterrupt:  
        # here you put any code you want to run before the program   
        # exits when you press CTRL+C  
        print("Exit!")
        GPIO.cleanup() # this ensures a clean exit  
    except:  
        # this catches ALL other exceptions including errors.  
        # You won't get any error messages for debugging  
        # so only use it once your code is working  
        print("Unexpected error:", sys.exc_info()[0])
        raise
      


