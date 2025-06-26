
# 📷 Online Interview Cheating Detection System

A lightweight, real-time Python project that detects **potential cheating behavior** during online interviews using **rule-based computer vision techniques**.

---

## 🚀 Features

- ✅ Real-time face and eye tracking using **MediaPipe**
- ✅ Detects:
  - Eye gaze **looking away** (left, right, down)
  - **Reading behavior** (horizontal eye scanning)
  - **Response delay** (no activity for 10+ seconds)
- ✅ Suspicion scoring system with:
  - 🔵 Green = Low
  - 🟡 Yellow = Medium
  - 🔴 Red = High
- ✅ **Audio beep alerts** at high suspicion
- ✅ Saves **screenshots** of suspicious activity (max 5)
- ✅ Final report summary in the console

## 📁 Project Structure

```
interview-monitor/
├── main.py            # Main webcam UI and control logic
├── detector.py        # Core detection and scoring system
├── utils.py           # Helper functions for gaze & overlays
├── requirements.txt   # Python dependencies
└── screenshots/       # Saved suspicious screenshots (auto-created)
```

---

## 🔧 Requirements

- Python 3.7+
- OpenCV
- MediaPipe
- NumPy

Install with:

bash
pip install -r requirements.txt

## ▶️ How to Run

```bash
python main.py
```

- Press **`q`** to quit
- Screenshots saved in `screenshots/` folder when score ≥ 30
- Audio alert sounds once per high suspicion event

---

## ⚙️ Adjustable Thresholds

In `main.py`:

```python
if suspicion_score < 6:
    level = "LOW"
elif suspicion_score < 30:
    level = "MEDIUM"
else:
    level = "HIGH"
```

In `detector.py`:

```python
self.max_away_frames = 50          # How long user must look away to count
self.suspicion_cooldown = 3       # Seconds between score increments
```

---

## 📊 Final Report Example

```
--- Final Report ---
Total Frames: 1923
Look Away Events: 3
Reading Patterns Detected: 2
Response Delay Events: 1
Final Suspicion Score: 6
% Time Suspicious: 10.42%
```

---

## 🔒 Disclaimer

This project is intended for **educational and personal use only**. It is not a certified proctoring tool and should not be used for surveillance or invasive monitoring.

---

## 📌 TODOs (Optional Enhancements)

- [ ] Decaying suspicion score over time
- [ ] Export report as PDF or CSV
- [ ] GUI mode with start/stop buttons
- [ ] Mic-based voice delay detection

---

## 🧑‍💻 Author

Built by Shone Kuncheria 
Feel free to fork or contribute 🤖
