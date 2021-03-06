#!/usr/bin/python
import os
import cv2
import sys
import rospy
from std_msgs.msg import String

#DEFAULT_CAMERA_ADDRESS = 'rtsp://root:toor@192.168.1.120:554/mpeg4/media.amp'
DEFAULT_CAMERA_ADDRESS = 'rtsp://admin:cerema76@192.168.1.64:554/mpeg4/media.amp'
DEFAULT_OUTPUT_DIR = "/home/paul/Videos/"
DEFAULT_VIDEO_FPS = 30

VIDEO_RES = (640,480)
REC_DURATION = 60 # duration in minutes
TIMESTAMP = "video"
DEFAULT_OUTPUT_DIR = "/home/paul/Videos/"

CAMERA_ADDRESS = rospy.get_param("/camera_address", DEFAULT_CAMERA_ADDRESS)
OUTPUT_DIR = rospy.get_param("/video_directory", DEFAULT_OUTPUT_DIR)
VIDEO_FPS = rospy.get_param("/video_fps", DEFAULT_VIDEO_FPS)

def callback(data):
    global TIMESTAMP
    TIMESTAMP = data.data

def reset_usb():
    rospy.loginfo('mounting USB drive')
    #pas bien !pi
    cere
    os.system('echo paul|sudo -S mount -a')

def draw_text(img, text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.6
    color = (255, 255, 255)
    org = (10,20)
    lineType = 2
    res = cv2.putText(img, text, org, font, scale, color, lineType=lineType)
    return res

def recorder():
    global TIMESTAMP, VIDEO_RES
    sub = rospy.Subscriber('nmea_time', String, callback)
    rospy.init_node('video_recorder', anonymous=True)
    rospy.loginfo("Opening camera : " + CAMERA_ADDRESS)
    cap = cv2.VideoCapture(CAMERA_ADDRESS)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    frame_cpt = 0
    writer = None
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        # begin record
        if frame_cpt == 0:
            VIDEO_RES = frame.shape[0:2][::-1]
            rospy.loginfo(VIDEO_RES)
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
            
            cv2.imshow('test', img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            
    writer.release()
    rospy.loginfo('closing video file')
    cap.release()


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
