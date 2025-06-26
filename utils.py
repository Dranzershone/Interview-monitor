import cv2
import numpy as np

# Indices of eye landmarks from MediaPipe
LEFT_EYE = [33, 133]
RIGHT_EYE = [362, 263]

def calculate_eye_gaze_direction(image, landmarks):
    h, w, _ = image.shape

    left_eye = [(int(landmarks.landmark[i].x * w), int(landmarks.landmark[i].y * h)) for i in LEFT_EYE]
    right_eye = [(int(landmarks.landmark[i].x * w), int(landmarks.landmark[i].y * h)) for i in RIGHT_EYE]

    eye_center_x = (left_eye[0][0] + right_eye[1][0]) // 2
    face_center_x = w // 2

    deviation = eye_center_x - face_center_x

    if deviation > 60:
        return 'right'
    elif deviation < -60:
        return 'left'
    else:
        return 'forward'
def is_horizontal_scanning(gaze_history, window):
    recent = list(gaze_history)[-window:]  # ✅ Convert to list before slicing
    if recent.count('left') > window * 0.3 and recent.count('right') > window * 0.3:
        return True
    return False
def draw_score_overlay(frame, score, level):
    color = (0, 255, 0) if level == 'LOW' else (0, 255, 255) if level == 'MEDIUM' else (0, 0, 255)
    text = f"Suspicion Score: {score} ({level})"
    cv2.putText(frame, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    return frame

def print_final_report(detector):
    print("\n--- Final Report ---")
    print(f"Total Frames: {detector.total_frames}")
    print(f"Look Away Events: {detector.look_away_events}")
    print(f"Reading Patterns Detected: {detector.reading_pattern_count}")
    print(f"Response Delay Events: {detector.response_delay_events}")
    print(f"Final Suspicion Score: {detector.suspicion_score}")

    total_suspicious = (
        detector.look_away_events +
        detector.reading_pattern_count +
        detector.response_delay_events
    )
    percent_suspicious = (total_suspicious / (detector.total_frames / 30)) * 100  # Assuming ~30 FPS
    print(f"% Time Suspicious: {percent_suspicious:.2f}%")
