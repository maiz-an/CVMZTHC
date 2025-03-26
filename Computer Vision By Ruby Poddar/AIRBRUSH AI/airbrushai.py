import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Define colors
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0),
          (255, 20, 147), (128, 0, 128), (0, 255, 255), (173, 216, 230), (255, 255, 255)]
current_color = colors[0]

# Define tools
BRUSH_SIZE = 5
PENCIL_SIZE = 2
HIGHLIGHTER_SIZE = 15
ERASER_SIZE = 20
current_tool = "Brush"

# Initialize drawing variables
canvas = None
prev_x, prev_y = None, None

# Webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    if canvas is None or canvas.shape[:2] != frame.shape[:2]:
        canvas = np.zeros_like(frame, dtype=np.uint8)
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            index_finger_tip = hand_landmarks.landmark[8]
            h, w, _ = frame.shape
            x, y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
            
            if prev_x is not None and prev_y is not None:
                if current_tool == "Brush":
                    cv2.line(canvas, (prev_x, prev_y), (x, y), current_color, BRUSH_SIZE)
                elif current_tool == "Pencil":
                    cv2.line(canvas, (prev_x, prev_y), (x, y), current_color, PENCIL_SIZE)
                elif current_tool == "Highlighter":
                    cv2.line(canvas, (prev_x, prev_y), (x, y), current_color, HIGHLIGHTER_SIZE)
                elif current_tool == "Eraser":
                    cv2.line(canvas, (prev_x, prev_y), (x, y), (0, 0, 0), ERASER_SIZE)
            
            prev_x, prev_y = x, y
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    else:
        prev_x, prev_y = None, None  # Reset if no hand detected
    
    # Overlay canvas onto frame
    frame = cv2.addWeighted(frame, 0.7, canvas, 0.3, 0)
    
    # Display current tool & color
    cv2.putText(frame, f"Tool: {current_tool}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, "Press C to Clear | S to Save | 1-9 Colors", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    cv2.imshow("Air Draw", frame)
    
    # Keyboard controls
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        canvas = np.zeros_like(frame, dtype=np.uint8)  # Clear canvas
    elif key == ord('s'):
        cv2.imwrite("airdraw_output.png", canvas)  # Save drawing
    elif key == ord('b'):
        current_tool = "Brush"
    elif key == ord('p'):
        current_tool = "Pencil"
    elif key == ord('h'):
        current_tool = "Highlighter"
    elif key == ord('e'):
        current_tool = "Eraser"
    elif key in [ord(str(i)) for i in range(1, 10)]:
        current_color = colors[int(chr(key))-1]  # Select color
    
cap.release()
cv2.destroyAllWindows()