from datetime import timedelta
from uuid import uuid4

import pytest

from app.domain.access_token.entity import AccessToken
from app.domain.access_token.errors import AccessTokenExpiredError
from app.domain.chat.entity import Chat, Message
from app.domain.user.entity import UserId


def test_chat_factory_normalizes_user_pair_order() -> None:
    id_a = uuid4()
    id_b = uuid4()
    user_id_1 = UserId(id_a)
    user_id_2 = UserId(id_b)
    chat = Chat.factory(user_id_1=user_id_1, user_id_2=user_id_2)
    assert chat.user_a_id <= chat.user_b_id
    assert {chat.user_a_id, chat.user_b_id} == {user_id_1, user_id_2}


def test_message_factory_creates_with_given_fields() -> None:
    chat = Chat.factory(user_id_1=UserId(uuid4()), user_id_2=UserId(uuid4()))
    text = "hello"
    msg = Message.factory(chat_id=chat.id, sender_user_id=chat.user_a_id, text=text)
    assert msg.chat_id == chat.id
    assert msg.sender_user_id == chat.user_a_id
    assert msg.text == text


def test_access_token_ensure_not_expired_raises_when_expired() -> None:
    token = AccessToken.factory(user_id=UserId(uuid4()), expires_in=timedelta(seconds=-1))
    with pytest.raises(AccessTokenExpiredError):
        token.ensure_not_expired()
