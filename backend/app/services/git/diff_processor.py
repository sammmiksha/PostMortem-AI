import re

class DiffProcessor:
    CATEGORY_KEYWORDS = {
        "Database": ["sql", "database", "db", "postgres", "mysql", "query"],
        "Authentication": ["auth", "jwt", "token", "login", "password"],
        "Networking": ["timeout", "socket", "http", "request", "connection", "retry"],
        "Configuration": ["config", "env", "setting", "yaml", "json"],
        "Caching": ["cache", "redis"],
        "API": ["endpoint", "route", "api"]
    }

    def should_process_file(self, file_path: str) -> bool:
        """Filters out non-source clutter and compiled binary cache noise."""
        if not file_path:
            return False
        
        ignored_patterns = ["__pycache__/", "node_modules/", ".git/", ".env"]
        if any(pattern in file_path for pattern in ignored_patterns):
            return False
            
        # Ignore common binary compiled formats
        if file_path.endswith(('.pyc', '.png', '.jpg', '.ico', '.exe')):
            return False
            
        return True

    def detect_category(self, file_path: str, patch_body: str) -> str:
        """Detects category using both file context and actual patch content."""
        combined_text = f"{file_path} {patch_body}".lower()

        for category, words in self.CATEGORY_KEYWORDS.items():
            # Using regex word boundaries avoids matching '__pycache__' for 'cache'
            for word in words:
                if re.search(r'\b' + re.escape(word) + r'\b', combined_text):
                    return category

        return "General"

    def detect_change_type(self, patch: str, diff_obj) -> str:
        """Determines change type reliably using git object metadata and lines."""
        if diff_obj.new_file:
            return "Added"
        if diff_obj.deleted_file:
            return "Removed"
        if diff_obj.renamed:
            return "Renamed"

        # Count actual structural changes inside diff body lines
        added = len(re.findall(r'^\+[^+]', patch, re.MULTILINE))
        removed = len(re.findall(r'^\-[^-]', patch, re.MULTILINE))

        if added and removed:
            return "Modified"
        if added:
            return "Added"
        if removed:
            return "Removed"

        return "Unknown"

    def format_diffs(self, diffs):
        results = []

        for diff in diffs:
            file_path = diff.b_path or diff.a_path
            
            # Skip noise files immediately
            if not self.should_process_file(file_path):
                continue

            patch = ""
            if diff.diff:
                patch = diff.diff.decode("utf-8", errors="ignore")

            # Strip off git top headers to only analyze actual text changes
            patch_body = re.sub(r'^diff --git.*?(?=\n@@)', '', patch, flags=re.DOTALL) if patch else ""

            results.append({
                "file": file_path,
                "category": self.detect_category(file_path, patch_body),
                "change_type": self.detect_change_type(patch, diff),
                "summary": patch_body[:500] if patch_body else patch[:500]
            })

        return results