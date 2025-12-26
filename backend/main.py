from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import time
import asyncio

from backend.database import SessionLocal, engine, Base
from backend.models import db_models
from backend.routes.video_stream import router as video_router

# ======================================================
# APP INIT
# ======================================================
app = FastAPI(title="CrowdShield AI Backend")

analysis_completed = False

# ======================================================
# CORS
# ======================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# DB INIT
# ======================================================
Base.metadata.create_all(bind=engine)

# ======================================================
# ROUTES
# ======================================================
app.include_router(video_router)

# ======================================================
# ROOT (🔥 REQUIRED – FIXES / 404)
# ======================================================
@app.get("/")
def root():
    return {"status": "CrowdShield AI Backend Running"}

# ======================================================
# WEBSOCKET MANAGER (PRODUCTION SAFE)
# ======================================================
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for ws in self.active_connections.copy():
            try:
                await ws.send_json(message)
            except:
                self.disconnect(ws)

manager = ConnectionManager()

# ======================================================
# HEALTH
# ======================================================
@app.get("/health")
def health():
    return {"status": "CrowdShield AI backend running"}

# ======================================================
# WEBSOCKET (🔥 STABLE & CORRECT)
# ======================================================
@app.websocket("/ws/live")
async def websocket_live(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # keeps connection alive + handles client pings
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# ======================================================
# INGEST (ML → BACKEND)
# ======================================================
@app.post("/ingest")
async def ingest_data(data: dict):
    global analysis_completed

    # --------------------------
    # RESET (NEW RUN)
    # --------------------------
    if data.get("reset") is True:
        analysis_completed = False
        db = SessionLocal()
        db.query(db_models.RiskMetric).delete()
        db.query(db_models.Alert).delete()
        db.commit()
        db.close()

        await manager.broadcast({"type": "RESET"})
        return {"message": "Backend reset successful"}

    # --------------------------
    # COMPLETION
    # --------------------------
    if data.get("completed") is True:
        analysis_completed = True
        await manager.broadcast({"type": "COMPLETED"})
        return {"message": "Video analysis completed"}

    # --------------------------
    # STORE ML DATA
    # --------------------------
    db = SessionLocal()

    metric = db_models.RiskMetric(
        crowd_count=data["crowd_count"],
        avg_density=data["avg_density"],
        max_density=data["max_density"],
        risk_score=data["risk_score"],
        status=data["status"]
    )
    db.add(metric)

    if data["status"] == "CRITICAL":
        db.add(
            db_models.Alert(
                risk_score=data["risk_score"],
                status=data["status"],
                message="Possible stampede detected"
            )
        )

    db.commit()
    db.close()

    # --------------------------
    # REAL-TIME PUSH
    # --------------------------
    await manager.broadcast({
        "type": "LIVE",
        "crowd_count": data["crowd_count"],
        "avg_density": data["avg_density"],
        "max_density": data["max_density"],
        "risk_score": data["risk_score"],
        "status": data["status"],
        "timestamp": time.time()
    })

    return {"ok": True}

# ======================================================
# REST FALLBACK
# ======================================================
@app.get("/risk/latest")
def get_latest_risk():
    db = SessionLocal()
    metric = db.query(db_models.RiskMetric)\
        .order_by(db_models.RiskMetric.timestamp.desc())\
        .first()
    db.close()
    return metric

@app.get("/risk/history")
def get_risk_history(limit: int = 100):
    db = SessionLocal()
    history = db.query(db_models.RiskMetric)\
        .order_by(db_models.RiskMetric.timestamp.desc())\
        .limit(limit)\
        .all()
    db.close()
    return history

@app.get("/alerts")
def get_alerts():
    db = SessionLocal()
    alerts = db.query(db_models.Alert)\
        .order_by(db_models.Alert.timestamp.desc())\
        .all()
    db.close()
    return alerts

# ======================================================
# FINAL REPORT
# ======================================================
@app.get("/report")
def final_report():
    if not analysis_completed:
        return {"status": "RUNNING"}

    db = SessionLocal()
    metrics = db.query(db_models.RiskMetric).all()
    alerts = db.query(db_models.Alert).all()
    db.close()

    return {
        "status": "COMPLETED",
        "total_frames": len(metrics),
        "max_risk": max((m.risk_score for m in metrics), default=0),
        "max_crowd": max((m.crowd_count for m in metrics), default=0),
        "total_alerts": len(alerts),
        "risk_timeline": [
            {"time": m.timestamp, "risk": m.risk_score}
            for m in metrics
        ]
    }
