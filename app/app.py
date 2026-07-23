from flask import Flask, jsonify, Response, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import logging
import os
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

app = Flask(__name__)

# Environment Variables
APP_NAME = os.getenv("APP_NAME", "SSB DevOps Assignment")
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

# Prometheus Metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Latency",
    ["endpoint"]
)


@app.before_request
def start_timer():
    request.start_time = time.time()


@app.after_request
def log_request(response):
    latency = time.time() - request.start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path
    ).inc()

    REQUEST_LATENCY.labels(
        endpoint=request.path
    ).observe(latency)

    logger.info(
        "%s %s %s %.4fs",
        request.method,
        request.path,
        response.status_code,
        latency
    )

    return response


@app.route("/")
def home():
    return jsonify({
        "application": APP_NAME,
        "environment": ENVIRONMENT,
        "message": "Welcome to SSB Digital DevOps Assignment"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "UP"
    })


@app.route("/ready")
def ready():
    return jsonify({
        "status": "READY"
    })


@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )