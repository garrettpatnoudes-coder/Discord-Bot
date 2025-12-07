import os
from datetime import datetime, timezone

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

if not DISCORD_WEBHOOK:
    raise RuntimeError("Missing DISCORD_WEBHOOK env variable.")

COLOR_MAP = {
    "ENTRY": 0x3498db,
    "TARGET": 0x2ecc71,
    "STOP": 0xe74c3c,
    "SMT_BULL": 0x00ff9d,
    "SMT_BEAR": 0xf39c12,
    "DEFAULT": 0x95a5a6,
}


def get_color(alert_type: str) -> int:
    return COLOR_MAP.get((alert_type or "").upper().strip(), COLOR_MAP["DEFAULT"])


def send_discord_embed(title, desc, alert_type, raw=None):
    now_iso = datetime.now(timezone.utc).isoformat()

    lines = [desc or "No message."]
    if raw:
        extra = [
            f"**{k}:** {v}"
            for k, v in raw.items()
            if k not in ["alert_title", "alert_message", "alert_type"]
        ]
        if extra:
            lines.append("")
            lines.append("\n".join(extra))

    embed = {
        "title": title or "SMT Alert",
        "description": "\n".join(lines),
        "color": get_color(alert_type),
        "timestamp": now_iso,
        "footer": {"text": "SMT INTEL Engine v5.0"},
    }

    resp = requests.post(DISCORD_WEBHOOK, json={"embeds": [embed]}, timeout=10)
    resp.raise_for_status()
    return resp.status_code


@app.route("/alert", methods=["POST"])
def alert():
    data = request.get_json(force=True, silent=True)

    if not data:
        return jsonify({"error": "invalid JSON"}), 400

    try:
        status = send_discord_embed(
            data.get("alert_title", "SMT Alert"),
            data.get("alert_message", "No message."),
            data.get("alert_type", "DEFAULT"),
            data,
        )
        return jsonify({"status": "ok", "discord": status}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run("0.0.0.0", port)
