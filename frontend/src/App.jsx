import { useEffect, useRef, useState } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
);

const WS_URL = "ws://127.0.0.1:8000/ws/live";
const VIDEO_URL = "http://127.0.0.1:8000/video";

export default function App() {
  const wsRef = useRef(null);
  const alertLock = useRef(false);

  const [live, setLive] = useState(null);
  const [history, setHistory] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [completed, setCompleted] = useState(false);
  const [connected, setConnected] = useState(false);

  // ===============================
  // WEBSOCKET CONNECTION
  // ===============================
  useEffect(() => {
    function connectWS() {
      const ws = new WebSocket(WS_URL);
      wsRef.current = ws;

      ws.onopen = () => {
        console.log("✅ WebSocket connected");
        setConnected(true);
      };

      ws.onmessage = (event) => {
        let data;
        try {
          data = JSON.parse(event.data); // 🔥 FIX: safe parse
        } catch {
          return;
        }

        // 🔄 RESET FROM BACKEND
        if (data.type === "RESET") {
          setLive(null);
          setHistory([]);
          setAlerts([]);
          setCompleted(false);
          return;
        }

        // 🏁 VIDEO COMPLETED
        if (data.type === "COMPLETED") {
          setCompleted(true);
          ws.close();
          return;
        }

        // 🔴 LIVE DATA
        if (data.type === "LIVE") {
          const payload = {
            ...data,
            timestamp: data.timestamp * 1000,
          };

          setLive(payload);
          setHistory((prev) => [...prev.slice(-59), payload]);

          // 🚨 ALERT (DEBOUNCED)
          if (payload.status === "CRITICAL" && !alertLock.current) {
            alertLock.current = true;
            setAlerts((prev) => [
              ...prev.slice(-9),
              {
                time: new Date().toLocaleTimeString(),
                message: "Possible stampede detected",
              },
            ]);

            setTimeout(() => {
              alertLock.current = false;
            }, 5000);
          }
        }
      };

      ws.onerror = (e) => {
        console.error("❌ WebSocket error", e);
      };

      ws.onclose = () => {
        console.warn("⚠ WebSocket disconnected");
        setConnected(false);
        if (!completed) {
          setTimeout(connectWS, 2000);
        }
      };
    }

    connectWS();
    return () => wsRef.current?.close();
  }, [completed]);

  // ===============================
  // FINAL REPORT
  // ===============================
  // ===============================
// FINAL REPORT (ENHANCED)
// ===============================
if (completed) {
  const maxRisk = Math.max(...history.map(h => h.risk_score));
  const avgRisk =
    history.reduce((a, b) => a + b.risk_score, 0) / history.length;

  const criticalMoments = history.filter(h => h.status === "CRITICAL").length;

  let verdict = "SAFE";
  let verdictColor = "#16a34a";
  let verdictText = "The crowd situation remained under control.";

  if (maxRisk > 70) {
    verdict = "CRITICAL";
    verdictColor = "#dc2626";
    verdictText =
      "High crowd density detected. Immediate intervention is recommended.";
  } else if (maxRisk > 40) {
    verdict = "WARNING";
    verdictColor = "#f59e0b";
    verdictText =
      "Moderate congestion observed. Monitoring is advised.";
  }

  return (
    <div className="app report">
      <h1>📊 CrowdShield AI – Analysis Report</h1>

      {/* SUMMARY CARDS */}
      <div className="summary-grid">
        <div className="card">
          <h4>Total Frames</h4>
          <p>{history.length}</p>
        </div>
        <div className="card">
          <h4>Max Risk</h4>
          <p>{maxRisk.toFixed(1)}%</p>
        </div>
        <div className="card">
          <h4>Average Risk</h4>
          <p>{avgRisk.toFixed(1)}%</p>
        </div>
        <div className="card">
          <h4>Critical Alerts</h4>
          <p>{criticalMoments}</p>
        </div>
      </div>

      {/* RISK GRAPH */}
      <div className="panel">
        <h3>📈 Risk Trend Over Time</h3>
        <Line
          data={{
            labels: history.map((_, i) => i + 1),
            datasets: [
              {
                label: "Risk Score (%)",
                data: history.map(h => h.risk_score),
                borderColor: "#ef4444",
                backgroundColor: "rgba(239,68,68,0.2)",
                fill: true,
                tension: 0.4,
              },
            ],
          }}
          options={{
            responsive: true,
            scales: {
              y: { min: 0, max: 100 },
            },
          }}
        />
      </div>

      {/* FINAL VERDICT */}
      <div className="verdict" style={{ borderColor: verdictColor }}>
        <h2 style={{ color: verdictColor }}>Final Verdict: {verdict}</h2>
        <p>{verdictText}</p>
      </div>

      <p className="done">✅ Video analysis completed successfully</p>
    </div>
  );
}

  // ===============================
  // LIVE DASHBOARD
  // ===============================
  return (
    <div className="app">
      <header className="topbar">
        <h1>CrowdShield AI</h1>
        <span className={`badge ${live?.status?.toLowerCase() || "safe"}`}>
          {connected ? live?.status || "LIVE" : "CONNECTING"}
        </span>
      </header>

      <div className="grid">
        {/* VIDEO */}
        <div className="panel">
          <h3>🎥 Live Feed</h3>
          <img src={VIDEO_URL} className="video" />
          {live && (
            <div className="overlay">
              👤 {live.crowd_count} &nbsp;|&nbsp;
              🔥 {live.max_density} &nbsp;|&nbsp;
              ⚠ {live.risk_score}
            </div>
          )}
        </div>

        {/* GRAPH */}
        <div className="panel">
          <h3>📈 Risk Trend</h3>
          <Line
            data={{
              labels: history.map((h) =>
                new Date(h.timestamp).toLocaleTimeString()
              ),
              datasets: [
                {
                  label: "Risk",
                  data: history.map((h) => h.risk_score),
                  borderColor: "#f43f5e",
                  tension: 0.4,
                },
              ],
            }}
            options={{
              responsive: true,
              animation: false,
              scales: {
                y: { min: 0, max: 100 }, // 🔥 FIX: correct ML scale
              },
            }}
          />
        </div>
      </div>

      {/* ALERTS */}
      <div className="alerts">
        <h3>🚨 Alerts</h3>
        {alerts.length === 0 ? (
          <p>No alerts</p>
        ) : (
          alerts.map((a, i) => (
            <div key={i} className="alert">
              {a.time} — {a.message}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
