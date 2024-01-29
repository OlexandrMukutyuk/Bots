from typing import Union, Optional

import texts.colors
from viberio.types.messages.keyboard_message import Keyboard, ButtonsObj, InternalBrowser


class KeyboardConstructor:
    @staticmethod
    def generate_kb(buttons: list[Union[dict, str]], options: Optional[dict] = None) -> Keyboard:
        button_list = []

        for btn in buttons:
            if isinstance(btn, str):
                btn = {"Text": btn}

                # @attr.s
                # class InternalBrowser(ViberBaseObject):
                #     ActionPredefinedURL: str = attr.ib(default=None)
                #     CustomTitle: str = attr.ib(default=None)
                #     ActionReplyData: str = attr.ib(default=None)
                #     ActionButton: str = attr.ib(default="forward")
                #     TitleType: str = attr.ib(default="default")
                #     Mode: str = attr.ib(default="fullscreen")
                #     FooterType: str = attr.ib(default="middle")

            internal_browser = None
            if btn.get("InternalBrowser"):
                internal_browser = InternalBrowser()

            button_list.append(
                ButtonsObj(
                    Columns=btn.get("Columns") or 6,
                    Rows=btn.get("Rows") or 1,
                    Text=f"<b>{btn.get('Text')}</b>",
                    ActionBody=btn.get("ActionBody") or btn.get("Text"),
                    ActionType=btn.get("ActionType") or "reply",
                    InternalBrowser=internal_browser,
                    TextSize="regular",
                    BgColor=btn.get("Color") or texts.GREY,
                )
            )

        return Keyboard(
            Type="keyboard",
            Buttons=button_list,
            InputFieldState=(options and options.get("InputFieldState")) or "regular",
            # ButtonsGroupColumns=(options and options.get("ButtonsGroupColumns")) or "6",
        )
