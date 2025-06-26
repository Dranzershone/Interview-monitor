# detector.py

import time
import os
import cv2
import numpy as np
from collections import deque
from utils import calculate_eye_gaze_direction, is_horizontal_scanning

import mediapipe as mp
mp_face_mesh = mp.solutions.face_mesh

import platform
import threading

# Cross-platform beep function
def play_beep():
    if platform.system() == 'Windows':
        import winsound
        winsound.Beep(1000, 250)  
    else:
        # For macOS/Linux with 'beep' installed
        os.system('echo -e "\a"')  # fallback bell sound

class SuspicionDetector:
    def __init__(self):
        self.gaze_history = deque(maxlen=30)
        self.away_frame_count = 0
        self.look_away_events = 0
        self.reading_pattern_count = 0
        self.response_delay_events = 0
        self.suspicion_score = 0
        self.total_frames = 0

        self.last_response_time = time.time()
        self.max_away_frames = 50  # adjusted threshold for stability
        self.max_screenshots = 5
        self.screenshots_taken = 0

        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

    def process_frame(self, frame, face_mesh):
        self.total_frames += 1
        suspicious = False
        gaze_direction = "forward"

        # MediaPipe face landmarks
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0]
            gaze_direction = calculate_eye_gaze_direction(frame, landmarks)
            self.gaze_history.append(gaze_direction)

            if gaze_direction in ['left', 'right', 'down']:
                self.away_frame_count += 1
                if self.away_frame_count > self.max_away_frames:
                    self.look_away_events += 1
                    suspicious = True
                    self.away_frame_count = 0
            else:
                self.away_frame_count = 0

            # Detect reading pattern
            if is_horizontal_scanning(self.gaze_history, window=20):
                self.reading_pattern_count += 1
                suspicious = True
                self.gaze_history.clear()

        else:
            # No face detected — reset suspicion logic
            self.away_frame_count = 0
            self.gaze_history.append('forward')

        # Simulated delayed response logic
        if time.time() - self.last_response_time > 10:  # No input/change for 10 sec
            self.response_delay_events += 1
            suspicious = True
            self.last_response_time = time.time()
            self.suspicion_cooldown = 3
        # Increase suspicion score if suspicious activity detected
        if suspicious:
            self.suspicion_score += 1

        # Save screenshot if suspicion is high and limit not reached
        if self.suspicion_score >= 30 and self.screenshots_taken < self.max_screenshots:
            filename = f"screenshots/suspicion_{time.strftime('%Y%m%d-%H%M%S')}.png"
            cv2.imwrite(filename, frame)
            self.screenshots_taken += 1
            threading.Thread(target=play_beep).start()

        return gaze_direction, self.suspicion_score
