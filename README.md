# talk-to-learn-proto

Minimal web prototype to try a turn-based voice UI.
Each table row is one turn:
record -> STT -> Ask LLM -> TTS.

No backend required. Uses the browser MediaRecorder API and dummy handlers.

## Run

You must serve the file from HTTPS or localhost for mic permissions. Install python if it is not installed already.

```bash
# from the repo root
python -m http.server 8000
# then open:
# http://localhost:8000/recorder.html
