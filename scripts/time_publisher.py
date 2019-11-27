#!/usr/bin/python
import rospy
import serial
import time
import pynmea2
import datetime
from dateutil import tz
from std_msgs.msg import String

DEVICE = '/dev/gps'
BAUDRATE = 4800
TIMEOUT = 1
#DATABITS = 8
#PARITY = None
#STOPBITS = 1

utc_zone = tz.gettz('UTC')
fr_zone = tz.gettz('Europe/Paris')
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

def talker():
    pub = rospy.Publisher('nmea_time', String, queue_size=10)
    rospy.init_node('nmea_publisher', anonymous=True)
    with serial.Serial(DEVICE, baudrate = BAUDRATE, timeout = TIMEOUT) as ser:
        while not rospy.is_shutdown():
            message = ser.readline()

            # parse the nmea message and handles parsing errors
            nmea_object = None
            try:
                nmea_object = pynmea2.parse(message)
            except:
                rospy.loginfo('Parsing error')
                continue

            # filters messages to only treat datetime messages
            if nmea_object.identifier() == 'GNZDA,':
                gps_datetime = datetime.datetime(nmea_object.year, nmea_object.month, nmea_object.day,\
                    nmea_object.timestamp.hour, nmea_object.timestamp.minute, nmea_object.timestamp.second,\
                    nmea_object.timestamp.microsecond, tzinfo=utc_zone)
                
                # publish the time as a string
                fr_time = gps_datetime.astimezone(fr_zone).strftime(DATETIME_FORMAT)
                rospy.loginfo(fr_time)
                pub.publish(fr_time)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass