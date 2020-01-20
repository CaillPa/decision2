#!/usr/bin/python
import os
import time
import rospy
import serial
from std_msgs.msg import String

DEVICE = '/dev/radar'
BAUDRATE = 2400
TIMEOUT = 1

ser = None

def run_test(publisher):
    global ser
    rospy.logdebug("writing 'P'")
    ser.write('P')
    rospy.logdebug("wrote 'P'")
    ser.readline()
    while ser.is_open and not rospy.is_shutdown():
        rospy.logdebug("writing 'L'")
        ser.write('L')
        msg = str(ser.readline()).strip()
        rospy.logdebug('received: '+msg)
        publisher.publish(msg)
        time.sleep(1)
    
def run(publisher):
    # MUST BE TESTED !
    global ser
    rospy.logdebug("writing 'G'")
    ser.write('G')
    rospy.logdebug("wrote 'G'")
    ser.readline()
    while ser.is_open and not rospy.is_shutdown():
        msg = str(ser.readline()).strip()
        if msg:
            rospy.logdebug('received: '+msg)
            publisher.publish(msg)

def resetUSB():
    rospy.logwarn('resetting radar USB')
    os.system('echo paul|sudo -S /home/pi/catkin_ws/src/decision2/misc/reset_usb.py search PL2303')
    time.sleep(5)
    rospy.logwarn('done resetting radar USB')
    pass

def talker():
    global ser
    pub = rospy.Publisher('radar', String, queue_size=10)
    rospy.init_node('radar_publisher', anonymous=True)
    while not rospy.is_shutdown():
        try:
            rospy.loginfo("Opening serial connection")
            ser = serial.Serial(DEVICE, baudrate = BAUDRATE, timeout = TIMEOUT)
            rospy.loginfo("Serial connection successful")
            #run_test(pub)
            run(pub)
        except IOError:
            rospy.logerr("IOError, resetting USB")
            resetUSB()
        finally:
            if ser:
                rospy.loginfo("Closing serial connection")
                ser.close()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
