import time

from flask import Flask, render_template, request
from flask_sse import sse

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["REDIS_URL"] = "redis://localhost:6379"
app.register_blueprint(sse, url_prefix="/stream")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/room", methods=["POST"])
def room():
    data = request.form
    user = data["user"]
    return render_template("chat.html", user=user)

@app.route("/chat", methods=["POST"])
def chat():
    chat = request.json
    chat["time"] = time.strftime("%H:%M")
    sse.publish(chat, type="chat")
    return chat, 201

if __name__ == "__main__":
    app.run(debug=True)
