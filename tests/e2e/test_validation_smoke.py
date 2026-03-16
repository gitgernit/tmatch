"""E2E negative smoke tests: hit HTTP endpoints with invalid data, assert validation (400/422/401)."""

from litestar import Litestar
from litestar.testing import TestClient

# Litestar may return 400 or 422 for validation errors; both indicate rejected invalid input.
VALIDATION_ERROR_CODES = (400, 422)


def test_auth_registration_email_missing_body_returns_validation_error(
    client: TestClient[Litestar],
) -> None:
    response = client.post("/auth/registration/email", content=b"", headers={"Content-Type": "application/json"})
    assert response.status_code in VALIDATION_ERROR_CODES


def test_auth_registration_email_invalid_body_returns_validation_error(
    client: TestClient[Litestar],
) -> None:
    response = client.post(
        "/auth/registration/email",
        json={},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code in VALIDATION_ERROR_CODES


def test_auth_registration_email_short_password_returns_validation_error(
    client: TestClient[Litestar],
) -> None:
    response = client.post(
        "/auth/registration/email",
        json={"email": "user@example.com", "password": "short"},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code in VALIDATION_ERROR_CODES


def test_auth_registration_email_invalid_email_returns_validation_error(
    client: TestClient[Litestar],
) -> None:
    response = client.post(
        "/auth/registration/email",
        json={"email": "not-an-email", "password": "validpass123"},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code in VALIDATION_ERROR_CODES


def test_recommendations_without_auth_returns_401(client: TestClient[Litestar]) -> None:
    response = client.get("/recommendations")
    assert response.status_code == 401


def test_health_returns_200(client: TestClient[Litestar]) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_targeting_put_invalid_gender_returns_validation_error(
    client: TestClient[Litestar],
) -> None:
    response = client.put(
        "/targeting/me",
        json={"gender_target": "invalid", "age_from": 18, "age_to": 30},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code in VALIDATION_ERROR_CODES


def test_targeting_put_negative_age_returns_validation_error(
    client: TestClient[Litestar],
) -> None:
    response = client.put(
        "/targeting/me",
        json={"gender_target": "both", "age_from": -1, "age_to": 30},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code in VALIDATION_ERROR_CODES


def test_interactions_post_invalid_action_returns_validation_error(
    client: TestClient[Litestar],
) -> None:
    response = client.post(
        "/interactions",
        json={
            "candidate_user_id": "86a5bb27-d9b2-59cf-8958-fbe6849a84ef",
            "action": "invalid_action",
        },
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code in VALIDATION_ERROR_CODES


def test_interactions_post_invalid_uuid_returns_validation_error(
    client: TestClient[Litestar],
) -> None:
    response = client.post(
        "/interactions",
        json={"candidate_user_id": "not-a-uuid", "action": "like"},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code in VALIDATION_ERROR_CODES


def test_interactions_without_auth_returns_401(client: TestClient[Litestar]) -> None:
    response = client.post(
        "/interactions",
        json={
            "candidate_user_id": "86a5bb27-d9b2-59cf-8958-fbe6849a84ef",
            "action": "like",
        },
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 401
