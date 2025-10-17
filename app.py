from flask import Flask, request
import requests

app = Flask(__name__)

# Provide your Discord webhook URL here manually
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1428805748410028114/sWRn_MDpqOIHNnaJN2xzQ_E46x_nQr1KN97gvyd395XdbXsBXeWGJIKAroGoJDh4ttkY"

@app.route("/gitlab", methods=["POST"])
def gitlab_to_discord():
    data = request.json

    # Make sure this is an issue event
    if data.get("object_kind") != "issue":
        return "Not an issue event", 200

    issue = data.get("object_attributes", {})
    title = issue.get("title", "No title")
    url = issue.get("url", "")
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
