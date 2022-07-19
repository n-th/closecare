import os

from flask import Flask

app = Flask(__name__)


@app.route("/healthcheck")
def health_check():
    return "Api is up and running :)", 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
