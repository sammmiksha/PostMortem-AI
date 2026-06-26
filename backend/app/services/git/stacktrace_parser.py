import re
from pathlib import Path

class StackTraceParser:

    def parse(self, trace: str):

        result = {
            "file": None,
            "line": None,
            "function": None,
            "error": None
        }

        file_match = re.search(
            r'File "(.*?)", line (\d+), in (\w+)',
            trace
        )

        if file_match:
            result["file"] = Path(file_match.group(1)).name
            result["line"] = int(file_match.group(2))
            result["function"] = file_match.group(3)

        error_match = re.findall(r'(\w+Error)', trace)

        if error_match:
            result["error"] = error_match[-1]

        return result