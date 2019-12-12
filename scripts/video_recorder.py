#!/usr/bin/python
import os
import cv2
import sys
import rospy
from std_msgs.msg import String

DEFAULT_CAMERA_ADDRESS = 'rtsp://root:toor@192.168.1.120:554/mpeg4/media.amp'
VIDEO_FPS = 30
VIDEO_RES = (640,480)
REC_DURATION = 1
TIMESTAMP = ""
OUTPUT_DIR = "/media/usb/videos/"

CAMERA_ADDRESS = rospy.get_param("/camera_address", DEFAULT_CAMERA_ADDRESS)

def callback(data):
    global TIMESTAMP
    TIMESTAMP = data.data

def reset_usb():
    rospy.loginfo('mounting USB drive')
    os.system('echo cerema|sudo -S mount -a')

def draw_text(img, text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.6
    color = (255, 255, 255)
    org = (10,20)
    lineType = 2
    res = cv2.putText(img, text, org, font, scale, color, lineType=lineType)
    return res

def recorder():
    global TIMESTAMP
    sub = rospy.Subscriber('nmea_time', String, callback)
    rospy.init_node('video_recorder', anonymous=True)
    rospy.loginfo("Opening camera : " + CAMERA_ADDRESS)
    cap = cv2.VideoCapture(CAMERA_ADDRESS)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    frame_cpt = 0
    writer = None
    while not rospy.is_shutdown():
        # begin record
        if frame_cpt == 0:
            filename = OUTPUT_DIR+TIMESTAMP+'.avi'
            writer = cv2.VideoWriter(filename, fourcc, VIDEO_FPS, VIDEO_RES)
            rospy.loginfo('creating new video file '+filename)
        # close record
        if frame_cpt > (REC_DURATION*60*VIDEO_FPS):
            frame_cpt = 0
            writer.release()
            rospy.loginfo('closing video file')
            continue

        #rospy.loginfo(TIMESTAMP)
        ret, frame = cap.read()
        if ret:
            img = draw_text(frame, TIMESTAMP)
            writer.write(img)
            frame_cpt += 1
            """
            cv2.imshow('test', img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            """
    writer.release()
    pass

if __name__ == '__main__':
    if not os.path.exists('/dev/sda'):
        rospy.logfatal('Storage device not plugged!')
        rospy.logfatal('Exiting node ...')
        sys.exit(0)
    reset_usb()
    try:
        rospy.logingo('creating output dir:'+OUTPUT_DIR)
        os.mkdir(OUTPUT_DIR)
    except:
        pass
    try:
        recorder()
    except rospy.ROSInterruptException:
        pass
