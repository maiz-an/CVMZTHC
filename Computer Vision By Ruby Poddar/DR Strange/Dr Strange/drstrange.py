import cv2
import mediapipe as mp
import numpy as np
import pygame
from PIL import Image

# Initialize pygame for sound effects
pygame.mixer.init()
magic_sound = pygame.mixer.Sound(r"C:\Users\abhis\OneDrive\Desktop\Code By Ruby Poddar\DR Strange\Images\magic_sound.mp3")

# Load images (convert GIFs to PNG)
def load_image(path):
    try:
        if path.lower().endswith(".gif"):
            img = Image.open(path)
            img = img.convert("RGBA")
            path = path.replace(".gif", ".png")  # Convert filename
            img.save(path)  # Save as PNG for OpenCV compatibility
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if img is None:
            print(f"Warning: Failed to load image at {path}")
        return img
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return None

image_paths = {
    "index_up": r"C:\Users\abhis\OneDrive\Desktop\Code By Ruby Poddar\DR Strange\Images\e7cdb166ca55730afcbb946e22d214e1.gif",
    "open_hand": r"C:\Users\abhis\OneDrive\Desktop\Code By Ruby Poddar\DR Strange\Images\blueshieldgif.gif",
    "fist": r"C:\Users\abhis\OneDrive\Desktop\Code By Ruby Poddar\DR Strange\Images\blackshieldgif.gif",
    "open_again": r"C:\Users\abhis\OneDrive\Desktop\Code By Ruby Poddar\DR Strange\Images\1686776446_en-idei-club-p-doctor-strange-circle-dizain-instagram-1.png",
}

overlay_images = {key: load_image(path) for key, path in image_paths.items()}

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Webcam
cap = cv2.VideoCapture(0)

# Image size (increased)
image_size = 200

# Gesture detection functions
def is_index_up(landmarks):
    return landmarks[8].y < landmarks[6].y and all(landmarks[i].y > landmarks[i-2].y for i in [12, 16, 20])

def is_all_fingers_open(landmarks):
    return all(landmarks[i].y < landmarks[i-2].y for i in [8, 12, 16, 20])

def is_fist(landmarks):
    return all(landmarks[i].y > landmarks[i-2].y for i in [8, 12, 16, 20])

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = hand_landmarks.landmark

            if is_index_up(landmarks):
                gesture_detected = "index_up"
            elif is_all_fingers_open(landmarks):
                gesture_detected = "open_hand"
            elif is_fist(landmarks):
                gesture_detected = "fist"
            else:
                gesture_detected = "open_again"

            # Get position for overlay
            h, w, _ = frame.shape
            hand_x, hand_y = int(landmarks[9].x * w), int(landmarks[9].y * h)

            # Draw hand landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Display overlay image
            if gesture_detected and overlay_images[gesture_detected] is not None:
                overlay = overlay_images[gesture_detected]
                overlay = cv2.resize(overlay, (image_size, image_size))

                # Ensure overlay stays within bounds
                x_offset = max(0, min(hand_x - image_size // 2, frame.shape[1] - overlay.shape[1]))
                y_offset = max(0, min(hand_y - image_size // 2, frame.shape[0] - overlay.shape[0]))

                # Handle alpha blending (GIF transparency)
                if overlay.shape[-1] == 4:  
                    alpha_s = overlay[:, :, 3] / 255.0
                    alpha_l = 1.0 - alpha_s

                    for c in range(3):
                        frame[y_offset:y_offset+overlay.shape[0], x_offset:x_offset+overlay.shape[1], c] = (
                            alpha_s * overlay[:, :, c] + alpha_l * frame[y_offset:y_offset+overlay.shape[0], x_offset:x_offset+overlay.shape[1], c]
                        )

                # Play sound effect (only once per gesture)
                magic_sound.play()

    cv2.imshow("Hand Gesture Recognition", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
