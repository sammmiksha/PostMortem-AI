from pathlib import Path
from git import Repo


class GitService:

    def __init__(self, repo_path: str):
        self.repo = Repo(Path(repo_path))

    def load_repo(self):
        return self.repo

    def find_file(self, filename: str) -> str:
        """Searches the repository for a file by base name and returns its relative path."""
        repo_root = Path(self.repo.working_tree_dir)
        # Recursively look for the filename in the repository
        for path in repo_root.rglob(filename):
            # Return the path relative to the Git repository root
            return str(path.relative_to(repo_root))
        return filename  # Fallback to original if not found

    def get_recent_commits(self, limit=10):
        commits = []
        for commit in self.repo.iter_commits(max_count=limit):
            commits.append({
                "hash": commit.hexsha,
                "author": commit.author.name,
                "message": commit.message.strip(),
                "date": str(commit.committed_datetime)
            })
        return commits

    def get_file_history(self, file_path: str, limit: int = 50):
        commits = []
        
        # Convert base filename (e.g., "main.py") to repo path (e.g., "backend/app/main.py")
        resolved_path = self.find_file(file_path)
        
        for commit in self.repo.iter_commits(paths=resolved_path, max_count=limit):
            commits.append({
                "hash": commit.hexsha,
                "author": commit.author.name,
                "message": commit.message.strip(),
                "date": str(commit.committed_datetime)
            })
        return commits

    def get_commit(self, commit_hash: str):
        commit = self.repo.commit(commit_hash)
        return {
            "hash": commit.hexsha,
            "author": commit.author.name,
            "message": commit.message.strip(),
            "date": str(commit.committed_datetime)
        }

    def get_diff(self, commit_hash: str):
        commit = self.repo.commit(commit_hash)
        if not commit.parents:
            return ""
        parent = commit.parents[0]
        return commit.diff(parent, create_patch=True)