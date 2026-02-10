from dishka import STRICT_VALIDATION, AsyncContainer, make_async_container


def build_container() -> AsyncContainer:
    return make_async_container(
        validation_settings=STRICT_VALIDATION,
    )
