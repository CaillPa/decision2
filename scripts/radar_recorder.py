#!/usr/bin/python
import os
import sys
import rospy
from std_msgs.msg import String

TIMESTAMP = ""
OUT_FILE = None

def mount_usb():
    rospy.loginfo('manually mounting USB drive')
    os.system('echo cerema|sudo -S mount -a')

def time_callback(data):
    global TIMESTAMP
    TIMESTAMP = data.data

def radar_callback(data):
    global TIMESTAMP
    global OUT_FILE
    radar_str = data.data
    rospy.logdebug('received radar message: '+radar_str)
    OUT_FILE.write(TIMESTAMP+';'+radar_str+'\n')

def record():
    global OUT_FILE
    rospy.init_node('radar_recorder', anonymous=True)
    with open('/media/usb/radar.csv', 'a', buffering=1) as OUT_FILE:
        rospy.Subscriber('nmea_time', String, time_callback)
        rospy.Subscriber('radar', String, radar_callback)
        rospy.spin()


if __name__ == '__main__':
    if not os.path.exists('/dev/sda'):
        rospy.logfatal('Storage device not plugged!')
        rospy.logfatal('Exiting node ...')
        sys.exit(0)
    mount_usb()
    try:
        record()
    except rospy.ROSInterruptException:
        pass
