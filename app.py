from flask import Flask, render_template, request, jsonify
from datetime import datetime
import csv, os, re, json, urllib.request, urllib.error

app = Flask(__name__)
LEADS_FILE = "leads.csv"

BUSINESS = {
    "name": "PRODINNA",
    "services": [
        "Video Editing", "Graphic Design", "3D Animation",
        "CGI Ads Creation", "Commercial Ads", "UGC Ads",
        "Website Design & Development", "Digital Marketing",
        "AI Automation"
    ],
    "contact": "Please share your name and contact number, and our team will follow up."
}

def save_lead(name, contact, need):
    exists = os.path.exists(LEADS_FILE)
    with open(LEADS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["Date", "Name", "Contact", "Requirement"])
        writer.writerow([datetime.now().isoformat(timespec="seconds"), name, contact, need])

def local_reply(message):
    m = message.lower()
    if any(x in m for x in ["hello", "hi", "salam", "assalam", "hey"]):
        return "Assalam-o-Alaikum! Welcome to PRODINNA. I can help with our services, project inquiries, and quotations. What do you need?"
    if any(x in m for x in ["service", "offer", "kya kar", "what do you do"]):
        return "PRODINNA offers: " + ", ".join(BUSINESS["services"]) + ". Which service are you interested in?"
    if any(x in m for x in ["price", "pricing", "cost", "rate", "quotation", "quote"]):
        return "Pricing depends on your project requirements. Please tell me which service you need and a short description. Our team can then prepare a quotation."
    if any(x in m for x in ["human", "team", "person", "call", "contact"]):
        return "Sure. Please share your name, contact number, and what you need. Our team will follow up."
    if any(x in m for x in ["website", "web development"]):
        return "We provide website design and development. Are you looking for a business website, portfolio, or e-commerce website?"
    if any(x in m for x in ["video", "editing", "reel"]):
        return "We provide professional video editing for reels, social media, and commercial content. What type of video do you need?"
    if any(x in m for x in ["cgi", "3d", "animation", "ad"]):
        return "We create CGI ads, 3D animation, commercial ads, and UGC-style ads. Tell me about the product or idea you want to promote."
    return "Thanks for your message. I can help with PRODINNA services, project requirements, and quotations. Please tell me a little more about your business or project."

def ollama_reply(message, history):
    # Optional local AI. Works only if Ollama is installed and a model is downloaded.
    payload = {
        "model": os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b"),
        "stream": False,
        "messages": [
            {"role": "system", "content": (
                "You are PRODINNA's helpful business assistant. "
                "Reply in the same language as the customer. Be concise and professional. "
                "PRODINNA services: " + ", ".join(BUSINESS["services"]) + ". "
                "Never invent prices, guarantees, client results, or policies. "
                "If unsure, ask for details and say the team will confirm."
            )},
            *history[-8:],
            {"role": "user", "content": message}
        ]
    }
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=45) as response:
        data = json.loads(response.read().decode("utf-8"))
        return data["message"]["content"].strip()

@app.route("/")
def home():
    return render_template("index.html", business=BUSINESS)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    message = (data.get("message") or "").strip()
    history = data.get("history") or []
    if not message:
        return jsonify({"reply": "Please type a message."}), 400

    use_ai = os.getenv("USE_OLLAMA", "0") == "1"
    if use_ai:
        try:
            reply = ollama_reply(message, history)
            return jsonify({"reply": reply, "mode": "local-ai"})
        except Exception:
            pass
    return jsonify({"reply": local_reply(message), "mode": "starter"})

@app.route("/api/lead", methods=["POST"])
def lead():
    data = request.get_json(force=True)
    name = (data.get("name") or "").strip()
    contact = (data.get("contact") or "").strip()
    need = (data.get("need") or "").strip()
    if not name or not contact:
        return jsonify({"ok": False, "message": "Name and contact are required."}), 400
    save_lead(name, contact, need)
    return jsonify({"ok": True, "message": "Thank you! Your details have been saved. Our team will follow up."})

# WhatsApp Cloud API webhook scaffold. Add Meta credentials only when ready.
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN", "")
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token and token == verify_token:
        return challenge or "", 200
    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def receive_webhook():
    payload = request.get_json(silent=True) or {}
    # Next stage: parse incoming Meta WhatsApp messages and send replies
    print("WhatsApp webhook event received:", json.dumps(payload)[:2000])
    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
