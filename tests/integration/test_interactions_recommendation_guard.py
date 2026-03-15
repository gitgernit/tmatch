from typing import cast

import pytest
from dishka import AsyncContainer

from app.application.auth_identity.interactors.sign_up import SignUpInteractor
from app.application.common.identity_provider import IdentityProvider
from app.application.interaction.errors import CandidateNotRecommendedError
from app.application.interaction.interactors.create_interaction import (
    CreateInteractionInteractor,
)
from app.application.user.data_gateway import UserDataGateway
from app.domain.interaction.value_objects import InteractionType
from tests.integration.di.identity_provider import MockIdentityProvider  # noqa: TC001


async def test_create_interaction_requires_recommendation(
    test_container: AsyncContainer,
    test_identity_provider: IdentityProvider,
    test_run_suffix: str,
) -> None:
    id_provider = cast("MockIdentityProvider", test_identity_provider)
    email1 = f"user1_{test_run_suffix}@test.local"
    email2 = f"user2_{test_run_suffix}@test.local"
    password = "test-password-123"  # noqa: S105

    sign_up = await test_container.get(SignUpInteractor)
    user_gateway = await test_container.get(UserDataGateway)

    response1 = await sign_up.sign_up_email(email1, password)
    response2 = await sign_up.sign_up_email(email2, password)

    user_a = await user_gateway.load_with_id(response1.user_id)
    user_b = await user_gateway.load_with_id(response2.user_id)
    assert user_a is not None
    assert user_b is not None

    id_provider.set_user(user_a)

    create_interaction = await test_container.get(CreateInteractionInteractor)
    with pytest.raises(CandidateNotRecommendedError):
        await create_interaction.execute(
            candidate_user_id=user_b.id,
            action=InteractionType.LIKE,
            ml_recommendation_id="missing-recommendation",
        )
