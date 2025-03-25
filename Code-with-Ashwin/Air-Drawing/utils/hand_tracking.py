# Magice 
import cv2
import mediapipe as mp

# Initialize Hand Tracking
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

class HandTracker:
    def __init__(self, min_detection_confidence=0.7, min_tracking_confidence=0.7):
        self.hands = mp_hands.Hands(min_detection_confidence=min_detection_confidence,
                                    min_tracking_confidence=min_tracking_confidence)

    def detect_hands(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        return results

    def get_landmarks(self, results, frame):
        landmark_list = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                for lm in hand_landmarks.landmark:
                    x, y = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])
                    landmark_list.append((x, y))
        return landmark_list