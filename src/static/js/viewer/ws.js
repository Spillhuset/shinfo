const wsUrl = new URL(window.location.href);
wsUrl.protocol = wsUrl.protocol.replace("http", "ws");
wsUrl.pathname = wsUrl.pathname.replace("viewer", "ws");


let ws = createWs();

function createWs() {
  let wsPulseInterval;
  const newWs = new WebSocket(wsUrl.href);
  newWs.onopen = () => {
    console.log("Screen WS connected");
    wsPulseInterval = setInterval(() => newWs.send(JSON.stringify({ type: "pulse" })), 30000);
  }

  newWs.onclose = () => {
    console.log("Screen WS disconnected");
    clearInterval(wsPulseInterval);
    ws = null;
    reloadWhenOkResponse();
  }

  newWs.onerror = (e) => {
    console.error(e);
    clearInterval(wsPulseInterval);
    ws = null;
    reloadWhenOkResponse();
  }

  newWs.onmessage = (e) => {
    const data = JSON.parse(e.data);
    onWsMessage(data);
    if (data.type === "reload_screen") window.location.reload();
  }

  return newWs;
}

async function reloadWhenOkResponse() {
  const testUrl = new URL(window.location.href);
  do {
    console.log("Waiting for server to be back up...");
    await sleep();
  } while (await fetch(testUrl.href).then(response => response.ok).catch(() => false) === false);
  await sleep();
  window.location.reload();
}

async function sleep(ms = 5_000) {
  await new Promise(r => setTimeout(r, ms));
}
