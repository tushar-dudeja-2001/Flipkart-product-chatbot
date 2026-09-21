from flask import Flask, jsonify, render_template, request

from flipkart.rag_agent import RAGAgent
from utils.logger import get_logger

logger = get_logger(__name__)

app = Flask(
    __name__,
    template_folder="frontend/template",
    static_folder="frontend/static",
)

agent = RAGAgent()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get", methods=["POST"])
def get_response():
    user_input = request.form["msg"]
    try:
        return agent.ask(user_input)
    except Exception as e:
        logger.error(f"Error in /get: {e}")
        return "Sorry, something went wrong while answering. Please try again."


@app.route("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
