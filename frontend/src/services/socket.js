let socket = null;

export function connectLiveSocket(onMessage, onClose) {
  socket = new WebSocket("ws://localhost:8000/ws/live");

  socket.onopen = () => {
    console.log("✅ WebSocket connected");
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onMessage(data);
  };

  socket.onclose = () => {
    console.log("❌ WebSocket disconnected");
    if (onClose) onClose();
  };

  socket.onerror = (err) => {
    console.error("WebSocket error", err);
  };
}

export function closeSocket() {
  if (socket) socket.close();
}
