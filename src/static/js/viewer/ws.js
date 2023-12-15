const wsUrl = new URL(window.location.href);
wsUrl.protocol = wsUrl.protocol.replace("http", "ws");
wsUrl.pathname = wsUrl.pathname.replace("viewer", "ws");

let wsPulseInterval;

const ws = new WebSocket(wsUrl.href);
ws.onopen = () => {
  console.log("Screen WS connected");
  wsPulseInterval = setInterval(() => ws.send(JSON.stringify({ type: "pulse" })), 30000);
}

ws.onclose = () => {
  console.log("Screen WS disconnected");
  clearInterval(wsPulseInterval);
  setTimeout(window.location.reload.bind(window.location), 5000);
}

ws.onerror = (e) => {
  console.error(e);
  setTimeout(window.location.reload.bind(window.location), 5000);
}

ws.onmessage = (e) => {
  const data = JSON.parse(e.data);
  onWsMessage(data);
  if (data.type === "reload_screen") window.location.reload();
}
