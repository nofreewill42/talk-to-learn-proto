# talk-to-learn-proto

Minimal web prototype for a turn-based voice UI. Each table row is one turn:
Record -> STT -> Ask LLM -> TTS.

Works out of the box with dummy providers. You can switch to real backends without changing the UI.

## Run

You must serve from HTTPS or localhost for the mic to work.

```bash
python -m http.server 8000
# open with http://localhost:8000/recorder.html
