import cv2
#import pyautogui
import mediapipe as mp
import math
#from screen_brightness_control import set_brightness
import keyboard as keyboard
#from picamera2 import Picamera2
import subprocess
import time

cam= cv2.VideoCapture(1)
#cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
#cam = Picamera2()

# Set the resolution of the camera preview
#cam.preview_configuration.main.size = (640, 360)
#cam.preview_configuration.main.format = "RGB888"
#cam.preview_configuration.controls.FrameRate=30

#cam.configure("preview")
#cam.start()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
brightness_changed = False

def calculate_distance_two_points(point1, point2):
    # Calculate Euclidean distance between two points (landmarks)
    return math.sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)
    
def calculate_distance_three_points(point1, point2, point3):
    # Calculate Euclidean distance between two points (landmarks)
    return math.sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)



prev_value=int()

v=int()
#time.sleep(5)
while True:
    ret, frame = cam.read()
    #frame=cam.capture_array()
    #if not ret:
      #  break

    image_rgb = cv2.cvtColor (frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks (frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_finger_y = hand_landmarks.landmark[mp_hands .HandLandmark.INDEX_FINGER_TIP].y
            thumb_y = hand_landmarks.landmark [mp_hands.HandLandmark.THUMB_TIP].y
            index_finger_x = hand_landmarks.landmark[mp_hands .HandLandmark.INDEX_FINGER_TIP].x
            middle_finger_x = hand_landmarks.landmark[mp_hands .HandLandmark.MIDDLE_FINGER_PIP].x
            #middle_finger_y = hand_landmarks.landmark[mp_hands .HandLandmark.MIDDLE_FINGER_TIP].y
            #middle_finger_z = hand_landmarks.landmark[mp_hands .HandLandmark.MIDDLE_FINGER_TIP].z
            index_finger_z = hand_landmarks.landmark[mp_hands .HandLandmark.INDEX_FINGER_TIP].z
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            distance = calculate_distance_two_points(index_finger_tip, thumb_tip)

            #prev_value=current_value
            #prev_value=int()        
			#if hand_gesture == "not touched":
            if (index_finger_x < 0.7) & (index_finger_x > 0.3) & (index_finger_y < 0.3):
                hand_gesture_vol = "pointing up"
            elif (index_finger_x < 0.7) & (index_finger_x > 0.3) & (index_finger_y > 0.7):
                hand_gesture_vol = "pointing down"
            elif index_finger_z > 0:
                hand_gesture_vol = "other"
            elif index_finger_z < 0:
                hand_gesture_vol = "other"


            current_value=100-int(index_finger_y*100)
            #print(prev_value)
            #print(current_value)
            if current_value>prev_value:
                sign="+"
            elif current_value<prev_value:
                sign="-"
            
            
            prev_value=current_value
            
            
            
            if hand_gesture_vol == "pointing up":
                v+=1
                subprocess.run(["amixer", "-D", "pulse", "sset", "Master", f"{v}%+"])
			#time.sleep(0.5)
			#volume_gap+=1
            if hand_gesture_vol == "pointing down":
                v-=1
                subprocess.run(["amixer", "-D", "pulse", "sset", "Master", f"{v}%-"])
			#time.sleep(0.5)
			#volume_gap-=1
            




            if (index_finger_y<0.7) & (index_finger_y>0.3) & (index_finger_x<0.3):
                hand_gesture_track="previous"
            elif (index_finger_y<0.7) & (index_finger_y>0.3) & (index_finger_x>0.7):
                hand_gesture_track="next"
            elif index_finger_z > 0:
                hand_gesture_track="other"
            elif index_finger_z < 0:
                hand_gesture_track="other"
            elif (index_finger_y<0.7) & (index_finger_y>0.3) & (index_finger_x>0.3) & (index_finger_x<0.7):
                hand_gesture_track="other"


            if hand_gesture_track=="previous":
            #print("Previous Track")
                subprocess.run(["vlc-ctrl", "prev"])
            #time.sleep(2)
            elif hand_gesture_track=="next":
            #print("Next Track")
               subprocess.run(["vlc-ctrl", "next"])
               
            
           
            #time.sleep(2)




			#print("ind & thm are touched")
			#set_brightness(100-index_finger_y*100)
			#adjust_brigthness(100-int(index_finger_y*100))




            
    cv2.imshow("Hand Gesture", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
