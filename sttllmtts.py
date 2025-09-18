# app.py
from flask import Flask, request, jsonify, send_from_directory
from faster_whisper import WhisperModel
import tempfile, subprocess, os

app = Flask(__name__, static_url_path="", static_folder=".")
model = WhisperModel("small", device="cpu", compute_type="int8")  # try "tiny" if slow

@app.get("/")
def root():
    # serve your HTML file - change if your filename differs
    return send_from_directory(".", "recorder.html")

@app.post("/stt")
def stt():
    f = request.files["audio"]
    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as inp:
        f.save(inp.name)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as wav:
        subprocess.run(
            ["ffmpeg", "-y", "-i", inp.name, "-ac", "1", "-ar", "16000", wav.name],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
        )
    segments, _ = model.transcribe(wav.name, vad_filter=True, language="en")
    text = "".join(s.text for s in segments).strip()
    os.remove(inp.name); os.remove(wav.name)
    return jsonify({"text": text})

# optional placeholders so the "server" providers work everywhere
@app.post("/llm")
def llm():
    t = (request.get_json() or {}).get("text", "")
    return jsonify({"reply": f"dummy response: {t}"})

@app.post("/tts")
def tts():
    # reuse is handled in the front end - return an empty 200
    return ("", 204)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
