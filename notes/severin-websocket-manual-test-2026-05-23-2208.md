# Severin WebSocket manual test note

Date: 2026-05-23

Source: pasted text from Marina / Severin chat.

This note records the manual WebSocket bridge test state and the next Termux command to verify protocol-level replies.

---

Марин, это хороший результат, но это ещё не кубик. Это наш ручной тест постучал в дверь и сказал: “тук-тук, я WebSocket” 🐟🔌

По логу:

```text
192.168.0.101 ... "GET /xiaozhi/ota/" 200
XIAOZHI WS CONNECTED
192.168.0.101 ... "GET /xiaozhi/ws" 200
```

Что значит:

1. `/xiaozhi/ota/` работает.

2. `/xiaozhi/ws` принимает подключение.

3. IP `192.168.0.101` — это сам телефон, не кубик.

4. Нет строки `XIAOZHI WS FIRST:` — значит наш ручной WebSocket подключился, но не отправил первое сообщение в протокол.

Я попытался сразу записать это в GitHub-память, но запись заблокировалась инструментом. Значит честно: в GitHub это пока не записано. Не драматизируем, просто держим здесь.

Следующий шаг

Теперь проверим не просто “дверь открылась”, а что WebSocket умеет получать и отвечать на сообщение.

Вставь в Termux вот это целиком:

```bash
python3 - <<'PY'
import socket, base64, os, json, struct, time

host = "192.168.0.101"
port = 8787
path = "/xiaozhi/ws"

def recv_exact(s, n):
    data = b""
    while len(data) < n:
        chunk = s.recv(n - len(data))
        if not chunk:
            raise EOFError("socket closed")
        data += chunk
    return data

def send_text(s, text):
    payload = text.encode("utf-8")
    mask = os.urandom(4)
    header = bytearray([0x81])

    n = len(payload)
    if n < 126:
        header.append(0x80 | n)
    elif n < 65536:
        header.append(0x80 | 126)
        header += struct.pack("!H", n)
    else:
        header.append(0x80 | 127)
        header += struct.pack("!Q", n)

    masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
    s.sendall(header + mask + masked)

def recv_frame(s):
    h = recv_exact(s, 2)
    opcode = h[0] & 0x0F
    masked = h[1] & 0x80
    length = h[1] & 0x7F

    if length == 126:
        length = struct.unpack("!H", recv_exact(s, 2))[0]
    elif length == 127:
        length = struct.unpack("!Q", recv_exact(s, 8))[0]

    mask = recv_exact(s, 4) if masked else b""
    payload = recv_exact(s, length) if length else b""

    if masked:
        payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))

    if opcode == 8:
        return "[close]"
    return payload.decode("utf-8", errors="replace")

key = base64.b64encode(os.urandom(16)).decode()

req = (
    f"GET {path} HTTP/1.1\r\n"
    f"Host: {host}:{port}\r\n"
    "Upgrade: websocket\r\n"
    "Connection: Upgrade\r\n"
    f"Sec-WebSocket-Key: {key}\r\n"
    "Sec-WebSocket-Version: 13\r\n"
    "\r\n"
)

s = socket.create_connection((host, port), timeout=5)
s.sendall(req.encode())
print(s.recv(4096).decode(errors="replace"))

send_text(s, json.dumps({"type":"hello","transport":"websocket"}, ensure_ascii=False))
print("SERVER 1:", recv_frame(s))

send_text(s, json.dumps({"type":"listen","state":"start"}, ensure_ascii=False))

for i in range(5):
    try:
        print("SERVER", i + 2, ":", recv_frame(s))
    except Exception as e:
        print("STOP:", e)
        break

s.close()
PY
```

Если всё хорошо, увидим ответы типа `hello`, `stt`, `llm`, `tts`.
Вот тогда наш мост не просто дверь, а уже разговорная будка с нервной системой 👾📞
