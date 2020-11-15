import RPi.GPIO as GPIO
#from gpio import GPIO
import time
import math
#import string
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(4, GPIO.IN)
GPIO.setup(17, GPIO.OUT)

D=[26,19,13,6,5,11,9,10]
def Let_it_light():
    for k in range (8):
        GPIO.output(D[k], 1) 

def Let_it_dark():
    for k in range (8):
        GPIO.output(D[k], 0)
     
def decToBinList(number):
    a = [0, 0, 0, 0, 0, 0, 0, 0]
    x = 0
    while number > 0:
        a[x] = number % 2
        number = number // 2
        x+=1
    a.reverse()
    return a


def lightNumber(List_of_number):
    Let_it_dark()
    for i in range (7,-1,-1): 
        if List_of_number[i]==1:
            GPIO.output(D[i], List_of_number[i]) 
GPIO.output(17,1)
print ("Enter value (-1 to exit)")
R=int(input())
while R!=-1:
    if R>-1 and R<256:
        m=decToBinList(R)
        lightNumber(m)
        Volage=int(((R*3.3)/256)*100)/100
        print (R, " = ", Volage, "V")
        print ("Enter value (-1 to exit)")
    else:
        print ("Enter right number")
        R=int(input())
        continue
    R=int(input())
    if R==-1:
        break