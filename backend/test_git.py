from app.services.git.git_service import GitService

git = GitService(r"C:\projects\PostMortem-AI")

history = git.get_file_history("backend/app/main.py")
diff = git.get_diff("400983ebe6b37f0492022f9d654f46919bc57c76")

for file_diff in diff:
    print(file_diff)
for commit in history:
    print(commit)