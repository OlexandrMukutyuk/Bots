import attr

from viberio.types.user_profile import UserProfile
from viberio.utils.safe import ensure_cls
from .base import ViberRequestObject


@attr.s
class ViberSubscribedRequest(ViberRequestObject):
    user: UserProfile = attr.ib(converter=ensure_cls(UserProfile))
    api_version: str = attr.ib()
