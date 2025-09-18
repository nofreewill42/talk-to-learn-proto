# talk-to-learn-proto

Minimal turn-based voice UI. One table row is one turn: Record -> STT -> Ask LLM -> TTS.

* Frontend is `recorder.html`
* Optional backend for real STT is `sttllmtts.py` using Flask + faster-whisper

---

## Requirements

* Python 3.10+
* A modern browser with microphone permission
* For local STT only: ffmpeg on PATH

Install ffmpeg

* Windows: `winget install Gyan.FFmpeg` then restart the terminal
* macOS: `brew install ffmpeg`
* Linux: `sudo apt-get install ffmpeg`

---

## Option A - dummy only (no backend)

Runs entirely in the browser with hardcoded results.

```bash
python -m http.server 8000
# then open http://localhost:8000/recorder.html
```

In the top selectors leave:

* STT: dummy
* LLM: dummy
* TTS: reuse recorded audio

Use flow

1. Click Record, then Stop - the audio appears in the row.
2. Click Transcribe - fills Transcript with "dummy transcription".
3. Click Ask LLM - fills LLM Reply with "dummy response: <transcript>".
4. Click TTS - plays back the same recorded audio in the TTS Audio cell.
5. Click + Row to add the next turn.

---

## Option B - local STT on your laptop (same origin, recommended)

Serve the page and the `/stt` endpoint from one Flask app.

Install once

```bash
pip install flask faster-whisper
```

Run

```bash
python sttllmtts.py
# open http://127.0.0.1:5000
```

In the page selectors set:

* STT: server
* LLM: dummy
* TTS: dummy

Now Transcribe calls faster-whisper and returns real text.

Speed tips

```python
# in sttllmtts.py
# faster on CPU but less accurate:
model = WhisperModel("tiny", device="cpu", compute_type="int8")
# on NVIDIA GPU:
# model = WhisperModel("small", device="cuda", compute_type="float16")
```

---

## Provider selectors and server contracts

At the top of the page you can choose providers:

* STT: dummy or server
* LLM: dummy or server
* TTS: dummy or server

When set to server, the UI expects:

* POST `/stt` - multipart form-data with field `audio` -> returns JSON `{ "text":"..." }`
* POST `/llm` - JSON `{ "text":"..." }` -> returns JSON `{ "reply":"..." }`
* POST `/tts` - JSON `{ "text":"..." }` -> audio bytes

`sttllmtts.py` implements `/stt` and includes placeholders for `/llm` and `/tts`.

---

## Troubleshooting

* Transcribe does nothing

  * If you opened `http://localhost:8000`, set STT to dummy.
  * For real STT, open `http://127.0.0.1:5000` from the Flask app and set STT to server.
* 501 on `/stt`

  * You posted to the simple server on port 8000. Use the Flask URL on port 5000 or change the fetch URL and enable CORS.
* ffmpeg not found

  * Install ffmpeg and restart the terminal. Verify with `ffmpeg -version`.
* Slow transcription

  * Switch the model to `"tiny"` as shown above.
* Mic does not start

  * Use `http://localhost` or `http://127.0.0.1` and allow microphone permission in the browser.
