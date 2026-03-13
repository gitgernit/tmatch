from dishka import BaseScope, Provider, Scope, WithParents, provide_all

from app.application.profile.interactors.get_profile import GetProfileInteractor
from app.application.profile.interactors.upsert_profile import UpsertProfileInteractor


class ProfileInteractorProvider(Provider):
    scope: BaseScope | None = Scope.REQUEST

    provides = provide_all(
        WithParents[GetProfileInteractor],
        WithParents[UpsertProfileInteractor],
    )


providers = [
    ProfileInteractorProvider(),
]
