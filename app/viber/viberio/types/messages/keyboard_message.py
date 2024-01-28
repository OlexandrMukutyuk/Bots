import attr

from viberio.types.base import ViberBaseObject
from .picture_message import PictureMessage
from .text_message import TextMessage


@attr.s
class InternalBrowser(ViberBaseObject):
    ActionPredefinedURL: str = attr.ib(default=None)
    CustomTitle: str = attr.ib(default=None)
    ActionReplyData: str = attr.ib(default=None)
    ActionButton: str = attr.ib(default="forward")
    TitleType: str = attr.ib(default="default")
    Mode: str = attr.ib(default="fullscreen")
    FooterType: str = attr.ib(default="default")


@attr.s
class Map(ViberBaseObject):
    Latitude: str = attr.ib(default=None)
    Longitude: str = attr.ib(default=None)


@attr.s
class Frame(ViberBaseObject):
    BorderWidth: str = attr.ib(default=None)
    CornerRadius: str = attr.ib(default=None)
    BorderColor: str = attr.ib(default="#000000")


@attr.s
class MediaPlayer(ViberBaseObject):
    Title: str = attr.ib(default=None)
    Subtitle: str = attr.ib(default=None)
    ThumbnailURL: str = attr.ib(default=None)
    Loop: bool = attr.ib(default=False)


@attr.s
class ButtonsObj(ViberBaseObject):
    BgColor: str = attr.ib(default=None)
    BgMediaScaleType: str = attr.ib(default=None)
    BgMedia: str = attr.ib(default=None)
    ImageScaleType: str = attr.ib(default=None)
    ActionBody: str = attr.ib(default=None)
    Text: str = attr.ib(default=None)
    InternalBrowser: InternalBrowser = attr.ib(default=None)
    Map: Map = attr.ib(default=None)
    Frame: Frame = attr.ib(default=None)
    TextBgGradientColor: str = attr.ib(default=None)
    MediaPlayer: MediaPlayer = attr.ib(default=None)
    Image: str = attr.ib(default=None)
    BgMediaType: str = attr.ib(default=None)
    Columns: int = attr.ib(default=6)
    Rows: int = attr.ib(default=1)
    Silent: bool = attr.ib(default=False)
    BgLoop: bool = attr.ib(default=True)
    ActionType: str = attr.ib(default="reply")
    TextVAlign: str = attr.ib(default="middle")
    TextHAlign: str = attr.ib(default="center")
    # TextPaddings: list = attr.ib(default=[12, 12, 12, 12])
    TextOpacity: int = attr.ib(default=100)
    TextSize: str = attr.ib(default="regular")
    OpenURLType: str = attr.ib(default="internal")
    OpenURLMediaType: str = attr.ib(default="not-media")
    # OpenURLMediaType: str = attr.ib(default="middle")
    # TextShouldFit: bool = attr.ib(default=False)

    def to_dict(self):
        return attr.asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


@attr.s
class Keyboard(ViberBaseObject):
    Type: str = attr.ib(default=None)
    BgColor: str = attr.ib(default=None)
    ButtonsGroupRows: int = attr.ib(default=None)
    FavoritesMetadata: int = attr.ib(default=None)
    CustomDefaultHeight: int = attr.ib(default=None)
    DefaultHeight: bool = attr.ib(default=False)
    Buttons: [ButtonsObj] = attr.ib(default=None)
    # HeightScale: int = attr.ib(default=100)
    # ButtonsGroupColumns: int = attr.ib(default=6)
    InputFieldState: str = attr.ib(default="regular")

    def to_dict(self):
        return attr.asdict(self, recurse=True)

    @classmethod
    def from_dict(cls, data):
        data["Buttons"] = [
            ButtonsObj.from_dict(button_data) for button_data in data.get("Buttons", [])
        ]
        return cls(**data)


@attr.s
class KeyboardMessage(TextMessage, PictureMessage):
    keyboard: Keyboard = attr.ib(default=None)
