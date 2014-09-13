#   Remmember that this program uses the ps3 controller to communicate to a     #
#intigrated circuit(L293D) on a breadboard. The intigrated circuit is used to   #
#boost up the PWM (Pulse Width Modulation) to the input voltage and .6 amps.    #
#For my car I had to use a regular motor to control the front steering wheels,  #
#you may use a servo motor to control you steering. I would recommend that you  #
#go to adafruit.com to figure that out.                                         #
#Alek Lukanen :)                                                                #
#################################################################################
#import libraries
import pygame
import time
import os
import RPi.GPIO as io
from RPIO import PWM

#set up the io mode and io numbers
io.setwarnings(False)
io.setmode(io.BCM)
io.setup(17,io.OUT)
io.setup(4,io.OUT)
io.setup(24,io.OUT)
io.setup(25,io.OUT)
io.setup(23,io.OUT)

#set up the PWM
PWM.setup()
PWM.LOG_LEVEL_ERRORS
PWM.init_channel(0)
p=io.PWM(23,500)
p.start(0)
PWM.add_channel_pulse(0,22,0,0)

in1 = 17
in2 = 4
in3 = 25
in4 = 24

#Initial pygame
pygame.init()

#forwards for motor 1
def clockwise1():
   io.output(in3,True)
   io.output(in4,False)

#backwards for motor 1
def counter_clockwise1():
   io.output(in3,False)
   io.output(in4,True)

#stop motor 1
def stop1():
   io.output(in3,False)
   io.output(in4,False)

#forwards for motor 2
def clockwise():
   io.output(in1,True)
   io.output(in2,False)

#backwards for motor 2
def counter_clockwise():
   io.output(in1,False)
   io.output(in2,True)

#stop motor 2
def stop():
   io.output(in1,False)
   io.output(in2,False)

#wait for a ps3 control or other controller to connect to the system.
while pygame.joystick.get_count() == 0:
   print 'waiting for ps3 controller'
   print 'waiting for joystick count = %i' % pygame.joystick.get_count()
   time.sleep(10)
   pygame.joystick.quit()
   pygame.joystick.init()


j = pygame.joystick.Joystick(0)
j.init()

#print out the name of the joystick.
print 'initialized Joystick : %s' % j.get_name()
print 'now setting up key map'

#joystick threshold
threshold = 0.25
#Start button
PS3_BUTTON_START = 3

#Up button
PS3_BUTTON_UP = 4

#Select button
PS3_BUTTON_SELECT = 0

#Triangle button
PS3_BUTTON_TRI = 12

#X button
PS3_BUTTON_X = 14

#Square button
PS3_BUTTON_SQUARE = 15

#Left joystick: used for forwards and backwards.
PS3_AXIS_LEFT_VERTICAL = 1

#Right joystick: used for right and left steering.
PS3_AXIS_RIGHT_HORIZONTAL = 2

stop1()

def trying(event):
   if event.type == pygame.JOYBUTTONDOWN:
      if event.button == PS3_BUTTON_SELECT:
          #do something
         print
      elif event.button == PS3_BUTTON_START:
          #do something
         print
      elif event.button == PS3_BUTTON_TRI:
          #shut down the motors and and shut down the system (power off.)
         stop()
         p.stop()
         os.system('sudo poweroff')
      elif event.button == PS3_BUTTON_X:
          #run clockwise function
         counter_clockwise()
         print 'back'
      elif event.button == PS3_BUTTON_SQUARE:
          #stop motor 1
         print 'stop'
         stop()
      elif event.button == PS3_BUTTON_UP:
          #reboot the system
         os.system('sudo reboot')

   if event.type == pygame.JOYAXISMOTION:
      if event.axis == PS3_AXIS_LEFT_VERTICAL:
          #This is used to control the forwards and backwards movement.

         #if event.value>=.24:
           # print 'stop'
           # stop()
         if event.value>=threshold:
            clockwise()
            speed=int(event.value*100)
            p.ChangeDutyCycle(speed) 
         if event.value>=-.24:
            if event.value<0:
               stop()
         elif event.value<=-threshold:  
            counter_clockwise()
            speed=-1*(int(event.value*100))
            p.ChangeDutyCycle(speed)

      elif event.axis == PS3_AXIS_RIGHT_HORIZONTAL:
          #This is used to control the left and right movement.
         if event.value>=threshold:
            clockwise1()
            speed=int(event.value*500)
            if PWM.is_setup() == 1:
                #set up the pwm to be set out.
               PWM.add_channel_pulse(0,22,0,speed)
              
            else:
               PWM.setup()
               PWM.init_channel(0)
               PWM.add_channel_pulse(0,22,0,speed)
              
         if event.value>=-.24:
            if event.value<0:
               stop1()
         elif event.value<=-threshold:  
            counter_clockwise1()
            speed=-1*(int(event.value*500))
            if PWM.is_setup() == 1:
                #set up pwm
               PWM.add_channel_pulse(0,22,0,speed)
              
            else:
               PWM.setup()
               PWM.init_channel(0)
               PWM.add_channel_pulse(0,22,0,speed)

#YOU NEED TO HAVE THE CODE BELLOW!!!
try:
   while True:
      pygame.event.pump()
      time.sleep(.1)

      events = pygame.event.get()

      #for eventForAxis in events:
         #axisButtons(eventForAxis)

      for event in events:
         trying(event)
except KeyboardInterrupt:
   j.quit()
   PWM.cleanup()
print'done'
