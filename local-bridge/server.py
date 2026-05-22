#!/usr/bin/env python3
"""
Severin local voice bridge, no external API.

Run on a laptop/mini-PC/cube on the same Wi-Fi as the TV box:

    python server.py

Then open on TV:

    http://<LOCAL_IP>:8787/

What it does now:
- receives microphone recordings from the browser;
- saves them to ./inbox/;
- serves the latest answer audio from ./outbox/answer.wav or ./outbox/answer.mp3;
- gives a simple local control page.

This is the skeleton for two-way voice without cloud API.
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import json
import time

ROOT = Path(__file__).resolve().parent
INBOX = ROOT / "inbox"
OUTBOX = ROOT / "outbox"
INBOX.mkdir(exist_ok=True)
OUTBOX.mkdir(exist_ok=True)

HOST = "0.0.0.0"
PORT = 8787

INDEX_HTML = r'''<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Северин · локальный мост</title>
  <style>
    body{margin:0;background:#071521;color:#eef7ff;font-family:Arial,sans-serif;padding:24px}
    main{max-width:900px;margin:auto;background:#10273a;border:1px solid #2f607e;border-radius:24px;padding:24px}
    h1{font-size:52px;margin:0 0 18px}p,li{font-size:24px;line-height:1.35}button{width:100%;font-size:34px;font-weight:800;border:0;border-radius:20px;background:#1cc7f5;color:#fff;margin:10px 0;padding:20px}audio{width:100%;margin:16px 0}pre{white-space:pre-wrap;background:#071521;color:#ffd36b;border:1px solid #2f607e;border-radius:16px;padding:16px;font-size:20px}
  </style>
</head>
<body>
<main>
  <h1>Северин · локальный мост</h1>
  <p>Без API. Эта страница пишет твой голос и отправляет запись на локальный сервер. Ответный голос берёт из <code>outbox/answer.wav</code> или <code>outbox/answer.mp3</code>.</p>
  <button id="rec">1 · Записать и отправить 5 секунд</button>
  <button id="play">2 · Проверить ответный файл</button>
  <button id="status">3 · Статус</button>
  <audio id="player" controls></audio>
  <pre id="log">Готово.</pre>
</main>
<script>
const logEl=document.getElementById('log'), player=document.getElementById('player');
function log(x){logEl.textContent='['+new Date().toLocaleTimeString('ru-RU')+'] '+x+'\n'+logEl.textContent}
async function status(){const r=await fetch('/status');log(await r.text())}
async function record(){
  try{
    if(!navigator.mediaDevices){log('mediaDevices нет: браузер не отдаёт микрофон');return}
    const stream=await navigator.mediaDevices.getUserMedia({audio:true});
    const chunks=[]; const rec=new MediaRecorder(stream);
    rec.ondataavailable=e=>{if(e.data&&e.data.size)chunks.push(e.data)};
    rec.onstop=async()=>{
      stream.getTracks().forEach(t=>t.stop());
      const blob=new Blob(chunks,{type:rec.mimeType||'audio/webm'});
      log('Запись готова, отправляю: '+blob.size+' bytes');
      const resp=await fetch('/upload',{method:'POST',headers:{'Content-Type':blob.type},body:blob});
      log(await resp.text());
    };
    rec.start(); log('Говори 5 секунд.'); setTimeout(()=>rec.stop(),5000);
  }catch(e){log('Ошибка микрофона: '+e.message)}
}
async function playAnswer(){
  const url='/answer?cache='+Date.now();
  player.src=url;
  try{await player.play();log('Пытаюсь проиграть ответный файл.')}catch(e){log('Не проигралось: '+e.message)}
}
document.getElementById('rec').onclick=record;
document.getElementById('play').onclick=playAnswer;
document.getElementById('status').onclick=status;
status().catch(e=>log('Статус ошибка: '+e.message));
</script>
</body>
</html>'''


def answer_file():
    wav = OUTBOX / "answer.wav"
    mp3 = OUTBOX / "answer.mp3"
    if wav.exists():
        return wav, "audio/wav"
    if mp3.exists():
        return mp3, "audio/mpeg"
    return None, None


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, data, content_type="text/plain; charset=utf-8"):
        if isinstance(data, str):
            data = data.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            return self._send(200, INDEX_HTML, "text/html; charset=utf-8")
        if path == "/status":
            af, _ = answer_file()
            info = {
                "ok": True,
                "inbox_count": len(list(INBOX.glob("*"))),
                "answer_file": af.name if af else None,
                "answer_exists": bool(af),
            }
            return self._send(200, json.dumps(info, ensure_ascii=False, indent=2), "application/json; charset=utf-8")
        if path == "/answer":
            af, ctype = answer_file()
            if not af:
                return self._send(404, "No answer.wav or answer.mp3 in outbox yet")
            return self._send(200, af.read_bytes(), ctype)
        return self._send(404, "Not found")

    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/upload":
            return self._send(404, "Not found")
        length = int(self.headers.get("Content-Length", "0"))
        data = self.rfile.read(length)
        stamp = time.strftime("%Y%m%d-%H%M%S")
        filename = INBOX / f"marina-{stamp}.webm"
        filename.write_bytes(data)
        return self._send(200, f"Saved {filename.name} ({len(data)} bytes)")

    def log_message(self, fmt, *args):
        print("[%s] %s" % (time.strftime("%H:%M:%S"), fmt % args))


if __name__ == "__main__":
    print(f"Severin local bridge: http://{HOST}:{PORT}/")
    print("Put answer audio into:", OUTBOX)
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
