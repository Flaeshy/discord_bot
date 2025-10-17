from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Discord webhook URL from environment variable
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

@app.route("/gitlab", methods=["POST"])
def gitlab_to_discord():
    data = request.json

    # Make sure this is an issue event
    object_kind = data.get("object_kind")
    if object_kind != "issue":
        return "Not an issue event", 200

    issue = data.get("object_attributes", {})
    title = issue.get("title", "No title")
    url = issue.get("url", "")
    state = issue.get("state", "").lower()
    labels = [label.get("title") for label in issue.get("labels", [])]

    # Only send message if status is "Ready for Review"
    if "Ready for Review" not in labels:
        return "Status not Ready for Review", 200

    # Construct Discord message
    msg = {
        "embeds": [{
            "title": f"📝 Issue Ready for Review: {title}",
            "description": f"[View Issue]({url})",
            "color": 0x00FF00,
            "fields": [
                {"name": "Status", "value": "Ready for Review", "inline": True}
            ]
        }]
    }

    # Send to Discord
    requests.post(DISCORD_WEBHOOK, json=msg)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

