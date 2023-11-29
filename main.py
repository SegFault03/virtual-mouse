import cv2
import mediapipe as mp
import pyautogui
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
hand_detector = mp.solutions.hands.Hands(max_num_hands=1)
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0
while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x*frame_width)
                y = int(landmark.y*frame_height)
                if id == 8:  # index finger
                    # cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    index_x = screen_width/frame_width*x
                    index_y = screen_height/frame_height*y

                if id == 4:  # thumb finger
                    # cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width/frame_width*x
                    thumb_y = screen_height/frame_height*y
                    # print('outside', abs(index_y - thumb_y))
                if id == 12:  # middle finger
                    middle_x = screen_width/frame_width*x
                    middle_y = screen_height/frame_height*y
            if abs(index_y - thumb_y) < 50 and abs(middle_y - thumb_y) < 50:
                pyautogui.moveTo(index_x, index_y)
            elif abs(index_y - thumb_y) < 50:
                pyautogui.click()
                pyautogui.sleep(1)
            elif abs(middle_y - thumb_y) < 50:
                pyautogui.rightClick()
                pyautogui.sleep(1)
            elif abs(index_y - thumb_y) > 100:
                pyautogui.moveTo(index_x, index_y)
    cv2.imshow('Virtual Mouse', frame)
    # observe the keypress by the user
    keypress = cv2.waitKey(1) & 0xFF

    # if the user pressed "q", then stop looping
    if keypress == ord("q"):
    # free up memory
       cap.release()
       cv2.destroyAllWindows()
       break