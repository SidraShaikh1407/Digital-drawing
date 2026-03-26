# ✋ Digital Drawing with Hand Gestures

A real-time hand gesture–controlled digital drawing application built with Python, OpenCV, and MediaPipe. Draw lines, rectangles, and circles or erase just by holding up fingers in front of your webcam!

---

## 🎥 Demo

> Open your webcam, show your hand, and start drawing in the air!

---

## ✨ Features

- 👆 **1 Finger** — Draw a freehand line
- ✌️ **2 Fingers** — Draw a rectangle
- 🤟 **3 Fingers** — Draw a circle
- 🖐️ **4 / 5 Fingers** — Erase
- Real-time hand skeleton overlay on webcam feed
- Separate drawing canvas window
- Live finger count and gesture name display

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10 | Core language |
| OpenCV | Camera feed & drawing |
| MediaPipe 0.10.33 | Hand landmark detection |
| NumPy | Canvas array management |

---

## 📦 Installation

**1. Clone the repository**
```bash
git clone https://github.com/SidraShaikh1407/Digital-drawing.git
cd Digital-drawing
```

**2. Install dependencies**
```bash
pip install opencv-python mediapipe numpy
```

**3. Run the app**
```bash
python "digital drawing.py"
```

> ⚠️ On first run, the app will automatically download the MediaPipe hand landmark model (~10MB). Make sure you have an internet connection.

---

## 🖐️ Gesture Guide

| Fingers Up | Gesture | Action |
|-----------|---------|--------|
| 1 | ☝️ Index only | Draw Line |
| 2 | ✌️ Index + Middle | Draw Rectangle |
| 3 | 🤟 Three fingers | Draw Circle |
| 4 | 🖖 Four fingers | Erase |
| 5 | 🖐️ Open palm | Erase |

---

## 📁 Project Structure

```
Digital-drawing/
│
├── digital drawing.py       # Main application
├── hand_landmarker.task     # MediaPipe model (auto-downloaded)
└── README.md
```

---

## ⌨️ Controls

| Key | Action |
|-----|--------|
| `Q` | Quit the application |

---

## ⚙️ Requirements

- Python 3.10+
- Webcam
- Internet connection (first run only, for model download)

---

## 🙋‍♀️ Author

**Sidra Shaikh**  
GitHub: [@SidraShaikh1407](https://github.com/SidraShaikh1407)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
