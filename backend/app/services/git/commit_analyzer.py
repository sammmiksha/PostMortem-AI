from app.services.git.git_service import GitService
from app.services.git.stacktrace_parser import StackTraceParser
from app.services.git.ranking_engine import RankingEngine
from app.services.git.diff_processor import DiffProcessor


class CommitAnalyzer:

    def __init__(self, repo_path: str):
        self.git = GitService(repo_path)
        self.parser = StackTraceParser()
        self.ranker = RankingEngine()
        self.diff_processor = DiffProcessor()
        
    def explain_commit(self, commit):
        explanation = []

        explanation.append(
            f"Score: {commit['score']}"
        )

        for reason in commit.get("reasons", []):
            explanation.append(reason)

        return explanation

    def analyze(self, stack_trace: str, limit_output: int = 3):
        # 1. Parse the incoming crash stack trace
        parsed = self.parser.parse(stack_trace)

        # 2. Grab history for the file responsible
        history = self.git.get_file_history(parsed["file"])

        # 3. Score and rank the history (fixed method name call to rank_commits)
        ranked = self.ranker.rank_commits(history)

        top_candidates = ranked[:limit_output]

        # 4. Enrich the top candidates with diffs and structural explanations
        for commit in top_candidates:
            raw_diffs = self.git.get_diff(commit["hash"])
            commit["explanation"] = self.explain_commit(commit)
            commit["changes_diff"] = self.diff_processor.format_diffs(raw_diffs)

        return {
            "stacktrace": parsed,
            "candidate_commits": top_candidates
        }