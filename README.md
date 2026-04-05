# 🎯 AI Interview Monitoring System

An intelligent AI-based interview system that evaluates candidate answers while monitoring behavior using computer vision.

---

## 🚀 Features

- 🎥 Real-time webcam monitoring
- 👤 Face detection using OpenCV DNN
- 🔴 "Looking Away" detection (basic gaze approximation)
- ⌨️ Answer typing directly inside camera window
- ⏱️ Timer for each question
- ⏭️ Skip question (ESC key)
- ❌ Exit interview anytime (Q key)
- 🧠 Keyword-based answer evaluation
- 📊 Final performance report with scores

---

## 🛠️ Technologies Used

- Python
- OpenCV (Computer Vision)
- NumPy
- DNN Face Detection Model (Caffe)

---

## 📁 Project Structure

AI-Interview-Monitoring-System/
│
├── app.py
├── requirements.txt
│
models/
│
├── deploy.prototxt
├── res10_300x300_ssd_iter_140000.caffemodel
│
└── yolo/
    ├── yolov3-tiny.cfg
    ├── yolov3-tiny.weights
    └── coco.names
└── README.md


---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/AI-Interview-Monitoring-System.git
cd AI-Interview-Monitoring-System

2️⃣ Install Dependencies
pip install -r requirements.txt

If requirements.txt is not available:

pip install opencv-python numpy

3️⃣ Download Face Detection Model

Place these files inside the models/ folder:

deploy.prototxt
res10_300x300_ssd_iter_140000.caffemodel

👉 You can download from:
https://github.com/opencv/opencv/tree/master/samples/dnn/face_detector

▶️ How to Run
python app.py

