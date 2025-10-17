from flask import Flask, request
import requests

app = Flask(__name__)

# Provide your Discord webhook URL here manually
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1428805748410028114/sWRn_MDpqOIHNnaJN2xzQ_E46x_nQr1KN97gvyd395XdbXsBXeWGJIKAroGoJDh4ttkY"

@app.route("/gitlab", methods=["POST"])
def gitlab_to_discord():
    data = request.json

    # Sicherstellen, dass es ein Issue Event ist
    if data.get("object_kind") != "issue":
        return "Not an issue event", 200

    issue = data.get("object_attributes", {})
    title = issue.get("title", "No title")
    url = issue.get("url", "")

    # Prüfen, ob der Status sich auf "Ready for Review" geändert hat
    changes = data.get("changes", {})
    status_change = changes.get("status", {})  # GitLab liefert alte/neue Werte in changes.status

    if not status_change:
        return "No status change", 200
    else:
        new_status = status_change.get("current").get("name")  # neuer Status
        old_status = status_change.get("previous").get("name")  # alter Status

        if new_status != "Ready for Review":
            return f"Status changed to {new_status}, not Ready for Review", 200

        # Nachricht an Discord erstellen
        msg = {
            "embeds": [{
                "title": f"📝 @everyone Issue Ready for Review: {title}",
                "description": f"[View Issue]({url})",
                "color": 0x00FF00,
                "fields": [
                    {"name": "Status", "value": "Ready for Review", "inline": True}
                ]
            }]
        }
 
    # Nachricht senden
    requests.post(DISCORD_WEBHOOK, json=msg)
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
