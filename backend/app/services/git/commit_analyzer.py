from app.services.git.git_service import GitService
from app.services.git.stacktrace_parser import StackTraceParser
from app.services.git.ranking_engine import RankingEngine
from app.services.git.diff_processor import DiffProcessor
from app.services.git.ai_commit_reviewer import AICommitReviewer


class CommitAnalyzer:

    def __init__(self, repo_path: str):
        self.git = GitService(repo_path)
        self.parser = StackTraceParser()
        self.ranker = RankingEngine()
        self.diff_processor = DiffProcessor()
        self.ai_reviewer = AICommitReviewer()

    def explain_commit(self, commit):
        explanation = []
        explanation.append(f"Score: {commit['score']}")
        for reason in commit.get("reasons", []):
            explanation.append(reason)
        return explanation

    def analyze(self, stack_trace: str, incident_summary: str = "", limit_output: int = 3, run_ai: bool = True):
        # 1. Parse the incoming crash stack trace
        parsed = self.parser.parse(stack_trace)

        # 2. Grab history for the file responsible (or recent repository history if file not parsed)
        if parsed.get("file"):
            history = self.git.get_file_history(parsed["file"])
        else:
            history = self.git.get_recent_commits(limit=30)

        # 3. Score and rank the commits
        ranked = self.ranker.rank_commits(history, stacktrace_info=parsed)

        top_candidates = ranked[:limit_output]

        # 4. Enrich top candidates with diffs, structural explanations, and AI analysis
        incident_context = {
            "summary": incident_summary or "Production incident / stack trace failure",
            "stacktrace": parsed
        }

        for commit in top_candidates:
            raw_diffs = self.git.get_diff(commit["hash"])
            commit["explanation"] = self.explain_commit(commit)
            commit["changes_diff"] = self.diff_processor.format_diffs(raw_diffs)

            if run_ai:
                try:
                    ai_res = self.ai_reviewer.review_commit(
                        incident=incident_context,
                        stacktrace=parsed,
                        commit=commit
                    )
                    commit["ai_confidence"] = ai_res.get("confidence", 50)
                    commit["ai_reason"] = ai_res.get("reason", "Analyzed commit diff and stack trace alignment.")
                    commit["ai_evidence"] = ai_res.get("evidence", [])
                    commit["ai_alternatives"] = ai_res.get("alternatives", [])
                except Exception as e:
                    print(f"AI review failed for commit {commit['hash']}: {e}")
                    commit["ai_confidence"] = commit["score"]
                    commit["ai_reason"] = "Heuristic score applied. AI review skipped or failed."

        return {
            "stacktrace": parsed,
            "candidate_commits": top_candidates
        }