from dishka import BaseScope, Provider, Scope, provide

from app.application.common.messaging.in_memory import InMemoryMessagingService


class MessagingProvider(Provider):
    scope: BaseScope | None = Scope.APP

    messaging_service = provide(InMemoryMessagingService, scope=Scope.APP)


providers = [
    MessagingProvider(),
]
