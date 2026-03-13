from datetime import date

from app.domain.common.value_object import value_object


@value_object
class Profile:
    first_name: str
    last_name: str | None
    birth_date: date
    region: str | None
    avatar_url: str | None
