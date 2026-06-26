from dataclasses import dataclass

@dataclass
class CommitInfo:
    hash: str
    author: str
    message: str
    date: str

@dataclass
class RankedCommit(CommitInfo):
    score: int
    reasons: list[str]