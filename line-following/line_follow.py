from pyimagesearch.linetracker import LineTracker
from imutils.video import VideoStream
from multiprocessing import Process
from multiprocessing import Manager
import easygopigo3
import imutils
import signal
import time
import sys
import cv2
# set the wheel speed constant which should be tuned based on your
# driving surface and available voltage
WHEEL_SPEED_CONSTANT = 33
def signal_handler(sig, frame):
    # print a status message and reset
    print("[INFO] You pressed `ctrl + c`! Resetting your "
          "GoPiGo3...")
    gpg = easygopigo3.EasyGoPiGo3()
    gpg.reset_all()
    sys.exit()

def video_feed(lMotor, rMotor):
    # signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)

    # initialize the video stream and allow the camera to warm up
    print("[INFO] starting video stream...")
    vs = VideoStream(usePiCamera=True).start()
    # vs = VideoStream(src=0).start()
    time.sleep(2.0)

    # initialize the line tracker
    lt = LineTracker()

    # loop over the frames from the video stream indefinitely
    while True:
        # grab the frame from the threaded video stream
        frame = vs.read()

        # grab updated fuzzy logic wheel multipliers from the line
        # tracker
        (lMultiplier, rMultiplier) = lt.update(frame)

        # set the desired motor speeds
        lMotor.value = int(WHEEL_SPEED_CONSTANT * lMultiplier)
        rMotor.value = int(WHEEL_SPEED_CONSTANT * rMultiplier)

def drive(lMotor, rMotor):

    # signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)

    # create the GoPiGo3 object
    gpg = easygopigo3.EasyGoPiGo3()

    # indefinitelly set the motor speeds according to the
    # process safe values
    while True:
        # set motor directions
        gpg.set_motor_power(gpg.MOTOR_LEFT, int(lMotor.value))
        gpg.set_motor_power(gpg.MOTOR_RIGHT, int(rMotor.value))
        time.sleep(0.01)

# check if we're on the main thread of execution
if __name__ == '__main__':
    # start a manager for managing process-safe variables
    with Manager() as manager:
        # initialize motor values
        lMotor = manager.Value('i', 0)
        rMotor = manager.Value('i', 0)
        # define the process which will handle our video feed and
        # update the wheel speeds
        videoProcess = Process(target=video_feed, args=(lMotor,
                                                        rMotor, ))

        # define the drive thread which takes a desired motor value
        # and sets each motor speed with the GoPiGo controller
        driveProcess = Process(target=drive, args=(lMotor, rMotor, ))

        # start all the processes
        videoProcess.start()
        driveProcess.start()
        # if a process ends, we'll join (stop) all processes
        videoProcess.join()
        driveProcess.join()
        # reset the GPG prior to stopping the script
        gpg = easygopigo3.EasyGoPiGo3()
        gpg.reset_all()
