from dataclasses import dataclass
from typing import override


@dataclass(frozen=True, slots=True)
class RecommendationProviderUnavailableError(Exception):
    @override
    def __str__(self) -> str:
        return "Recommendation provider unavailable"

