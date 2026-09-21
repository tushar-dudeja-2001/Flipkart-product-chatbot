from flask import Flask, Response, jsonify, render_template, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

from flipkart.rag_agent import RAGAgent
from utils.logger import get_logger

logger = get_logger(__name__)

app = Flask(
    __name__,
    template_folder="frontend/template",
    static_folder="frontend/static",
)

agent = RAGAgent()

REQUEST_COUNT = Counter("http_requests_total", "Total chat requests")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get", methods=["POST"])
def get_response():
    REQUEST_COUNT.inc()
    user_input = request.form["msg"]
    try:
        return agent.ask(user_input)
    except Exception as e:
        logger.error(f"Error in /get: {e}")
        return "Sorry, something went wrong while answering. Please try again."


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
