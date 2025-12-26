# 🚦 CrowdShield AI  
## Real-Time Crowd Risk Detection & Intelligent Monitoring System

CrowdShield AI is a **full-stack, real-time AI system** that transforms ordinary video feeds into **actionable crowd-safety intelligence**.  
It uses **deep learning**, **real-time backend streaming**, and an **interactive frontend dashboard** to detect crowd density, assess risk levels, trigger alerts, and generate meaningful analytical reports.

This project is designed to simulate **real-world crowd safety monitoring systems** used in public spaces such as railway stations, stadiums, and large public events.

---

## 🌍 Why CrowdShield AI Exists (Problem Statement)

Large public gatherings often face serious safety risks due to:
- Overcrowding
- Panic situations
- Poor visibility for authorities
- Delayed response to dangerous conditions

### ❌ Traditional CCTV systems fail because:
- They are **passive** (humans must constantly monitor screens)
- Human monitoring is **slow and error-prone**
- Crowd conditions can escalate in **seconds**
- No real-time analytics or predictive insight is available

---

## ✅ What CrowdShield AI Solves

CrowdShield AI converts **raw video footage** into **real-time intelligence** by:

- Automatically detecting people using AI
- Measuring localized crowd density
- Classifying risk levels (SAFE / WARNING / CRITICAL)
- Streaming **synchronized video + analytics**
- Triggering real-time alerts
- Generating a final, easy-to-understand analytical report

In short:  
> **From video → to insight → to action**

---

## 🧠 High-Level System Architecture

┌──────────────┐ ┌────────────────┐ ┌────────────────────┐
│ ML Engine │ ───▶ │ FastAPI Backend │ ───▶ │ React Frontend UI │
└──────────────┘ └────────────────┘ └────────────────────┘


### 🔹 ML Engine (Brain)
- Processes video frame-by-frame
- Detects people using YOLOv8
- Computes crowd density & risk
- Sends metrics AND the same analyzed frames

### 🔹 Backend (Coordinator)
- Receives ML data via REST APIs
- Stores analytical metrics
- Streams live data using WebSockets
- Streams ML-synchronized video frames
- Manages session lifecycle and reports

### 🔹 Frontend (Visualization)
- Displays live video feed
- Shows real-time metrics and graphs
- Highlights alerts clearly
- Generates a final analytical report

---

## ⚙️ Tech Stack

### 🧠 Machine Learning
- Python
- YOLOv8 (Ultralytics)
- OpenCV
- NumPy

### ⚙️ Backend
- FastAPI
- WebSockets
- SQLAlchemy
- Uvicorn

### 🖥️ Frontend
- React (Vite)
- Chart.js
- WebSocket API
- CSS

---

## 🔍 How the System Works (Step-by-Step Workflow)

### 1️⃣ System Startup
1. Backend server starts
2. Frontend dashboard connects
3. ML pipeline begins video analysis

---

### 2️⃣ Video Processing (ML Pipeline)
- Video is read frame-by-frame
- Frames are processed at controlled FPS
- YOLO detects people in each frame
- Bounding boxes are drawn

---

### 3️⃣ Crowd Density Analysis
- Each frame is divided into a grid
- People are mapped to grid cells
- Metrics calculated:
  - Total crowd count
  - Average density
  - Maximum localized density

---

### 4️⃣ Risk Classification
Based on density thresholds:
- 🟢 SAFE – Normal conditions
- 🟡 WARNING – Moderate congestion
- 🔴 CRITICAL – High-risk situation

This hybrid **ML + rule-based logic** ensures:
- Accuracy
- Explainability
- Stability

---

### 5️⃣ Real-Time Data Streaming
- ML sends metrics to backend (`/ingest`)
- Backend broadcasts updates via WebSocket
- Frontend updates instantly without refresh

---

### 6️⃣ ML-Synchronized Video Streaming (Key Feature)
Unlike typical systems:
- The backend does NOT read the video independently
- The **same frame analyzed by ML** is streamed to frontend

✅ Video speed = ML speed  
✅ Visuals perfectly match analytics  
✅ No desynchronization

This is an **industry-grade design choice**.

---

### 7️⃣ Alerts System
- When CRITICAL risk is detected:
  - Alerts are triggered
  - Alert spam is prevented using debouncing
  - Alerts remain visible for review

---

### 8️⃣ Final Report Generation
Once video analysis completes:
- Live dashboard switches to report mode
- System summarizes:
  - Total frames analyzed
  - Max & average risk
  - Number of critical moments
  - Risk trend over time
- A clear **final verdict** is displayed

---

## 📊 Final Report – What It Tells You

The final report answers:
- ❓ Was the crowd safe overall?
- ❓ When was the highest risk moment?
- ❓ How severe was the situation?
- ❓ Was intervention required?

This transforms **raw ML output** into **decision-ready insight**.

---

## 🚀 Key Features

- 🎥 Real-time ML-synchronized video feed
- 📊 Dynamic risk trend visualization
- 🚨 Alert system for critical conditions
- ⚡ WebSocket-based real-time updates
- 🧠 Explainable AI logic
- 📝 Clean and informative final report

---

## ▶️ How to Run the Project

### 1️⃣ Backend
```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload

### 2️⃣ Frontend
```bash
cd frontend
npm install
npm run dev
### 3️⃣ ML pipeline
```bash

python realtime_detection.py

🔄 Demo Flow (Recommended Order)

Start Backend

Start Frontend

Run ML Pipeline

Observe live dashboard

View final report after completion

🎯 Use Cases

Crowd safety monitoring

Smart city surveillance

Event management systems

Public infrastructure safety

Academic & research projects

🎓 Academic & Professional Value

This project demonstrates:

Real-time AI system design

ML + Backend + Frontend integration

WebSocket-based live systems

Synchronization of analytics & video

Clean software engineering practices
