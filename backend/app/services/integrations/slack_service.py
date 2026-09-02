from typing import Dict, Any

class SlackService:
    def create_block_payload(
        self,
        title: str,
        summary: str,
        root_cause: str,
        confidence_risk: int = 85,
        channel: str = "#incidents-postmortem"
    ) -> Dict[str, Any]:
        """Formats a Slack Block Kit payload for incident alert broadcast."""
        return {
            "channel": channel,
            "text": f"🚨 PostMortem-AI Alert: {title}",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"🚨 PostMortem-AI Analysis Ready: {title}",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Risk Confidence Score:*\n`{confidence_risk}% HIGH`"},
                        {"type": "mrkdwn", "text": "*Status:*\n`Postmortem Drafted`"}
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Executive Summary:*\n{summary}"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Root Cause:*\n```{root_cause}```"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "View Postmortem Dashboard"},
                            "style": "primary",
                            "url": "http://localhost:5173"
                        }
                    ]
                }
            ]
        }
