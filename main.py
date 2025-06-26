# main.py

import cv2
import mediapipe as mp
from detector import SuspicionDetector
from utils import draw_score_overlay, print_final_report

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: Cannot access webcam.")
        return

    # Initialize MediaPipe FaceMesh
    mp_face_mesh = mp.solutions.face_mesh
    detector = SuspicionDetector()

    print("📹 Starting monitoring. Press 'q' to quit...")

    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:

        while True:
            ret, frame = cap.read()
            if not ret:
                print("⚠️ Failed to grab frame.")
                break

            # Flip for natural webcam view
            frame = cv2.flip(frame, 1)

            # Process frame for suspicion
            gaze_direction, suspicion_score = detector.process_frame(frame, face_mesh)

            # Determine suspicion level
            if suspicion_score < 8:
                level = "LOW"
            elif suspicion_score < 25:
                level = "MEDIUM"
            else:
                level = "HIGH"

            # Draw overlay
            frame = draw_score_overlay(frame, suspicion_score, level)

            # Display feed
            cv2.imshow("🎯 Interview Monitoring System", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print_final_report(detector)

if __name__ == "__main__":
    main()
