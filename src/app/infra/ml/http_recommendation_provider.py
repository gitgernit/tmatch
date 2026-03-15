from collections.abc import Mapping
from typing import Any, override

import httpx

from app.application.recommendation.dto import RecommendationItem
from app.application.recommendation.errors import RecommendationProviderUnavailableError
from app.application.recommendation.protocol import RecommendationProvider
from app.domain.recommendation.value_objects import RecommendationFeatureName
from app.domain.user.entity import UserId


class HttpRecommendationProvider(RecommendationProvider):
    def __init__(self, *, base_url: str) -> None:
        self._base_url = base_url.rstrip("/")

    @override
    async def get_recommendations(self, *, user_id: UserId) -> list[RecommendationItem]:
        if not self._base_url:
            raise RecommendationProviderUnavailableError
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    url=f"{self._base_url}/recommendation",
                    json={"user_id": str(user_id)},
                )
        except httpx.HTTPError as error:
            raise RecommendationProviderUnavailableError from error

        if response.status_code >= 400:
            raise RecommendationProviderUnavailableError

        payload = self._parse_payload(response)
        items: list[RecommendationItem] = []
        for raw_item in payload:
            item = self._build_item(raw_item=raw_item, user_id=user_id)
            if item is not None:
                items.append(item)
        return items

    def _parse_payload(self, response: httpx.Response) -> list[dict[str, Any]]:
        try:
            raw_payload = response.json()
        except ValueError as error:
            raise RecommendationProviderUnavailableError from error

        if isinstance(raw_payload, dict) and "items" in raw_payload:
            raw_payload = raw_payload["items"]
        if not isinstance(raw_payload, list):
            raise RecommendationProviderUnavailableError
        return [item for item in raw_payload if isinstance(item, dict)]

    def _build_item(self, *, raw_item: dict[str, Any], user_id: UserId) -> RecommendationItem | None:
        ml_recommendation_id = raw_item.get("ml_recommendation_id")
        candidate_user_id = raw_item.get("candidate_user_id")
        if not isinstance(ml_recommendation_id, str) or not isinstance(candidate_user_id, str):
            return None

        reasons = self._normalize_reasons(raw_item.get("reasons"))
        return RecommendationItem(
            ml_recommendation_id=ml_recommendation_id,
            user_id=str(user_id),
            candidate_user_id=candidate_user_id,
            reasons=reasons,
        )

    def _normalize_reasons(self, raw_reasons: object) -> dict[RecommendationFeatureName, float]:
        if not isinstance(raw_reasons, Mapping):
            return {RecommendationFeatureName.LIFESTYLE: 0.0}

        normalized: dict[RecommendationFeatureName, float] = {}
        for raw_name, raw_score in raw_reasons.items():
            feature = self._resolve_feature_name(raw_name)
            if feature is None:
                continue
            try:
                normalized[feature] = float(raw_score)
            except (TypeError, ValueError):
                normalized[feature] = 0.0
        return normalized or {RecommendationFeatureName.LIFESTYLE: 0.0}

    def _resolve_feature_name(self, raw_name: object) -> RecommendationFeatureName | None:
        if isinstance(raw_name, RecommendationFeatureName):
            return raw_name
        if not isinstance(raw_name, str):
            return None
        normalized_name = raw_name.strip().lower()
        if normalized_name == RecommendationFeatureName.LIFESTYLE.value:
            return RecommendationFeatureName.LIFESTYLE
        return None
