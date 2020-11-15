import RPi.GPIO as GPIO
import time
import math
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import string
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(4, GPIO.IN)


D=[26,19,13,6,5,11,9,10]

def Let_it_light(pins):
    for k in range (8):
        GPIO.output(pins[k], 1) 

def Let_it_dark(pins):
    for k in range (8):
        GPIO.output(pins[k], 0)
     
def num2leds(value):
    if value < 0 or value > 255:
        a = "введите натуральное число в интервале (0; 255)"
    else:
        a = [0, 0, 0, 0, 0, 0, 0, 0]
        x = 0
        while value > 0:
            a[x] = value % 2
            value = value // 2
            x+=1
        a.reverse()
    return a

def num2dac(pins,value):
    Let_it_dark(pins)
    for i in range (7,-1,-1):
        if value[i]==1:
            GPIO.output(pins[i], value[i])

def num2pins(pins,value): #8
    s=num2leds(j)
    num2dac(pins,s)

def adc():
    c=0
    b=255
    j=int((c+b)/2)
    while True:
        num2dac(D,j)
        time.sleep(0.01)
        if b-c==2 or j == 0:
            Voltage=int(((j*3.3)/256)*100)/100
            print("Digital value: ", j , ", Analog Value: ", Voltage, "V")
            return j
            break
        elif GPIO.input(4)==1:
            c=j
            j=int((c+b)/2)
        elif GPIO.input(4)==0:
            b=j
            j=int((c+b)/2)

try:
    while adc() > 0:
        GPIO.output (17, 0)
        print ("zero voltage")
        time.sleep (1)
    t_st = time.time()
    listV = [] 
    listT = []
    measure = []
    GPIO.output(17,1)
    while adc() < 252:
        listT.append(time.time()-t_st)
        k = adc()
        measure.append(k)
        listV.append(int((k*3.3)/256*100)/100)
        time.sleep(0.01)
        if k >= 252:
            break 
    GPIO.output(17,0)
    while adc() > 0:
        listT.append(time.time()-t_st)
        measure.append (adc())
        listV.append(int((adc()*3.3)/256*100)/100)
        time.sleep(0.01)
    np.savetxt('data.txt', listV, fmt='%d') #7

    dT=0
    for i in range (len(listT) - 1):
        dT=dT+abs(listT[i+1]-listT[i])
    dT=dT/(len(listT)-1)
    dV = 0
    for i in range (len(listV) - 1):
        dV = dV + abs(listV[i+1] - listV[i])
    dV = dV / (len(listV[i+1]) - 1)
    X =  [dT, dV]
    np.savetxt('settings.txt', X, fmt='%f') 

    plt.plot(listT,listV, 'r-')#10
    plt.title('График зависимости напряжения на конденсаторе от времени')
    plt.xlabel('Время, с')
    plt.ylabel('Напряжение, В')
    plt.show()

finally:
        for i in range (7,-1,-1):
            GPIO.output(D[i], 0)