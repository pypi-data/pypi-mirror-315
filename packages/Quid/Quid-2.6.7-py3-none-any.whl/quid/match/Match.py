from dataclasses import dataclass
from quid.match.MatchSpan import MatchSpan


@dataclass(unsafe_hash=True)
class Match:
    source_span: MatchSpan
    target_span: MatchSpan
