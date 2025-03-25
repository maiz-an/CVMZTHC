# Magice 
import cv2
import numpy as np
import pygame
import random
from utils.hand_tracking import HandTracker

# Initialize Hand Tracker
hand_tracker = HandTracker()

# Capture Video
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Initialize Pygame for Fire Effect
pygame.init()
screen = pygame.display.set_mode((1280, 720))

# Create a blank magic canvas
canvas = np.zeros((720, 1280, 3), np.uint8)

# Store previous points for smooth drawing
prev_x, prev_y = 0, 0

# Magic Fire Particles
particles = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip the frame horizontally
    results = hand_tracker.detect_hands(frame)
    landmark_list = hand_tracker.get_landmarks(results, frame)

    if landmark_list:
        index_finger = landmark_list[8]  # Index Finger Tip
        x, y = index_finger

        # Fire Effect Particles
        particles.append([x, y, random.randint(5, 15)])  # (x, y, size)

        # Drawing Mode: Draw glowing magic line
        if prev_x == 0 and prev_y == 0:
            prev_x, prev_y = x, y

        cv2.line(canvas, (prev_x, prev_y), (x, y), (255, 165, 0), 8)  # Glowing orange color
        prev_x, prev_y = x, y

        # Clear screen when touching thumb & index finger
        thumb_tip = landmark_list[4]
        if abs(index_finger[1] - thumb_tip[1]) < 30:
            canvas = np.zeros((720, 1280, 3), np.uint8)
            particles.clear()

    # Magic Particle Effect
    for p in particles:
        p[1] -= random.randint(2, 5)  # Move particles upward
        p[2] -= 0.2  # Reduce size
        if p[2] <= 0:
            particles.remove(p)  # Remove small particles

    for p in particles:
        cv2.circle(frame, (p[0], p[1]), int(p[2]), (255, 100, 0), -1)  # Glowing Fire

    # Merge Canvas with Webcam Feed
    frame = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

    cv2.imshow("Magic Wand Effect - Harry Potter Style", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()