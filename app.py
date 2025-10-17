from flask import Flask, request
import requests

app = Flask(__name__)

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/XXXXXX"  # replace this

@app.route("/gitlab", methods=["POST"])
def gitlab_to_discord():
    data = request.json
    user = data.get("user_name", "Unknown")
    project = data.get("project", {}).get("name", "Unknown project")
    commits = data.get("commits", [])

    for commit in commits:
        msg = {
            "embeds": [{
                "title": f"🧩 New commit in {project}",
                "description": commit["message"],
                "url": commit["url"],
                "color": 0x5865F2,
                "fields": [
                    {"name": "Author", "value": user, "inline": True},
                    {"name": "Branch", "value": data['ref'].split('/')[-1], "inline": True},
                ]
            }]
        }
        requests.post(DISCORD_WEBHOOK, json=msg)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
