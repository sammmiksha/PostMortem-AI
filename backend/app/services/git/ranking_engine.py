from datetime import datetime, timezone
import re
from typing import List, Dict, Any, Optional

class RankingEngine:
    def __init__(self):
        self.suspicious_keywords = [
            "fix", "bug", "break", "db", "timeout", "error", "init", "pool",
            "leak", "auth", "config", "retry", "connection", "refactor", "update"
        ]

    def rank_commits(
        self,
        history: List[Dict[str, Any]],
        stacktrace_info: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Scores and ranks commits based on:
        - File Match: +40 points if commit touched affected file
        - Function Match: +30 points if function mentioned in commit/stacktrace
        - Recentness: +20 points for recent commits
        - Keyword Match: up to +20 points for suspicious keywords
        """
        ranked_history = []
        target_file = stacktrace_info.get("file", "").lower() if stacktrace_info else ""
        target_func = stacktrace_info.get("function", "").lower() if stacktrace_info else ""

        for idx, commit in enumerate(history):
            score = 0
            reasons = []

            # Factor 1: Touched target file (+40)
            score += 40
            reasons.append("Touched affected file (+40 pts)")

            # Factor 2: Function match (+30)
            message = commit.get("message", "").lower()
            if target_func and target_func in message:
                score += 30
                reasons.append(f"Function '{target_func}' match in commit message (+30 pts)")

            # Factor 3: Recentness (+20 for top 5 most recent commits)
            if idx < 5:
                score += 20
                reasons.append("Recent commit (+20 pts)")
            elif idx < 15:
                score += 10
                reasons.append("Relatively recent commit (+10 pts)")

            # Factor 4: Suspicious Keywords (max 20)
            matches = 0
            matched_words = []
            for keyword in self.suspicious_keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', message):
                    matches += 1
                    matched_words.append(keyword)

            keyword_score = min(matches * 10, 20)
            if keyword_score > 0:
                score += keyword_score
                reasons.append(f"Matched keywords ({', '.join(matched_words[:3])}) (+{keyword_score} pts)")

            ranked_commit = commit.copy()
            ranked_commit["score"] = score
            ranked_commit["reasons"] = reasons
            ranked_history.append(ranked_commit)

        return sorted(ranked_history, key=lambda x: x["score"], reverse=True)