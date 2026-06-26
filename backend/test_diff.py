from app.services.git.git_service import GitService
from app.services.git.diff_processor import DiffProcessor

git = GitService(r"C:\projects\PostMortem-AI")

processor = DiffProcessor()

commit = "2bb022ebb815704d6f083dfdaf5b96f3232b230a"

diffs = git.get_diff(commit)

result = processor.format_diffs(diffs)

for d in result:
    print(d)