import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Initialize MediaPipe Hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8, max_num_hands=2)

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip image horizontally for better interaction
    frame = cv2.flip(frame, 1)
    
    # Convert BGR image to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    height, width, _ = frame.shape
    
    # Draw hand landmarks and detect gestures
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=3),
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
            )
            
            # Get landmark positions
            wrist_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * height
            finger_tips = {
                'Thumb': mp_hands.HandLandmark.THUMB_TIP,
                'Index Finger': mp_hands.HandLandmark.INDEX_FINGER_TIP,
                'Middle Finger': mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                'Ring Finger': mp_hands.HandLandmark.RING_FINGER_TIP,
                'Pinky': mp_hands.HandLandmark.PINKY_TIP
            }
            fingers = {name: hand_landmarks.landmark[tip].y * height < wrist_y for name, tip in finger_tips.items()}
            
            # Recognizing gestures
            if all(fingers.values()):
                cv2.putText(frame, 'Hands Up!', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif not any(fingers.values()):
                cv2.putText(frame, 'Hands Down!', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            elif fingers['Index Finger'] and fingers['Middle Finger'] and not fingers['Thumb'] and not fingers['Ring Finger'] and not fingers['Pinky']:
                cv2.putText(frame, 'Peace/V Sign!', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            elif fingers['Middle Finger'] and not any([fingers['Thumb'], fingers['Index Finger'], fingers['Ring Finger'], fingers['Pinky']]):
                cv2.putText(frame, 'Middle Finger (Fuck Off)', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            elif fingers['Thumb'] and fingers['Index Finger'] and not fingers['Middle Finger'] and not fingers['Ring Finger'] and not fingers['Pinky']:
                cv2.putText(frame, 'Clitch Hand!', (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
            elif fingers['Index Finger'] and not any([fingers['Thumb'], fingers['Middle Finger'], fingers['Ring Finger'], fingers['Pinky']]):
                cv2.putText(frame, 'Pointing Up!', (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 165, 0), 2)
            
            # Show each finger's status
            y_offset = 350
            for finger, status in fingers.items():
                color = (0, 255, 0) if status else (0, 0, 255)
                cv2.putText(frame, f'{finger}: {"Up" if status else "Down"}', (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                y_offset += 40
    
    # Display the result
    cv2.imshow('Advanced Hand Gesture Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
