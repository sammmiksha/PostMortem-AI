from typing import Dict, Any

class JiraService:
    def create_issue_payload(
        self,
        summary: str,
        description: str,
        issue_type: str = "Task",
        priority: str = "High",
        project_key: str = "PM"
    ) -> Dict[str, Any]:
        """Formats a standard REST payload for Jira Cloud API."""
        ticket_id = f"{project_key}-1024"
        return {
            "ticket_id": ticket_id,
            "jira_url": f"https://jira.company.com/browse/{ticket_id}",
            "status": "Created",
            "fields": {
                "project": {"key": project_key},
                "summary": f"[PostMortem-AI Action] {summary}",
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "text": description}
                            ]
                        }
                    ]
                },
                "issuetype": {"name": issue_type},
                "priority": {"name": priority},
                "labels": ["postmortem-ai", "automated-prevention"]
            }
        }
