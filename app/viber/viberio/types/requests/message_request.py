import attr

from viberio.types.messages.message import TypedMessage
from viberio.types.messages.message_type import parse_message
from viberio.types.user_profile import UserProfile
from viberio.utils.safe import ensure_cls, ensure_factory
from .base import ViberRequestObject


@attr.s
class ViberMessageRequest(ViberRequestObject):
    message: TypedMessage = attr.ib(converter=ensure_factory(parse_message))
    sender: UserProfile = attr.ib(converter=ensure_cls(UserProfile))
    file_name: str
    chat_id: str = attr.ib(default=None)
    reply_type: str = attr.ib(default=None)
    silent: str = attr.ib(default=None)
