from dataclasses import dataclass, field


@dataclass(unsafe_hash=True)
class MatchSpan:
    start: int
    end: int
    text: str = field(default='', hash=False, compare=False)
