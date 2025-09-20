from flask import Flask, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "ICEGODS Backend is running 🚀"

@app.route("/api/test")
def test():
    return jsonify({"status": "ok", "message": "API working!"})

@app.route("/api/fetch-users")
def fetch_users():
    """
    Run fetch_all_bots_users.py and return its output.
    Adjust according to how your script works.
    """
    try:
        # Run the script and capture output
        result = subprocess.run(
            ["python3", "fetch_all_bots_users.py"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()

        return jsonify({"status": "success", "data": output})
    except subprocess.CalledProcessError as e:
        return jsonify({
            "status": "error",
            "message": e.stderr.strip() if e.stderr else str(e)
        }), 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
