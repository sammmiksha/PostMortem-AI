import re
from typing import List, Dict, Any

class RankingEngine:
    def __init__(self):
        self.suspicious_keywords = ["fix", "bug", "break", "db", "timeout", "error", "init"]

    def rank_commits(self, history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Scores and ranks commits based on suspicious keywords,
        capping the keyword contribution to a maximum of 20 points.
        """
        ranked_history = []
        
        for commit in history:
            message = commit.get("message", "").lower()
            matches = 0
            
            # Count unique keyword matches
            for keyword in self.suspicious_keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', message):
                    matches += 1
            
            # Apply the capped score logic: 10 points per match, max 20
            score = min(matches * 10, 20)
            
            # Attach the score to the commit data
            ranked_commit = commit.copy()
            ranked_commit["score"] = score
            ranked_history.append(ranked_commit)
            
        # Sort commits in descending order by score (highest risk first)
        return sorted(ranked_history, key=lambda x: x["score"], reverse=True)