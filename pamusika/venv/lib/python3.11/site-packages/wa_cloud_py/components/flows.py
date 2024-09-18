from enum import Enum


class FlowCategory(str, Enum):
    SIGN_UP = "SIGN_UP"
    SIGN_IN = "SIGN_IN"
    APPOINTMENT_BOOKING = "APPOINTMENT_BOOKING"
    LEAD_GENERATION = "LEAD_GENERATION"
    CONTACT_US = "CONTACT_US"
    CUSTOMER_SUPPORT = "CUSTOMER_SUPPORT"
    SURVEY = "SURVEY"
    OTHER = "OTHER"


class FlowFontWeight(str, Enum):
    BOLD = "bold"
    ITALIC = "italic"
    BOLD_ITALIC = "bold_italic"
    NORMAL = "normal"


class FlowLayoutType(str, Enum):
    SINGLE_COLUMN = "SingleColumnLayout"


class FlowLayout:
    def __init__(self, type: FlowLayoutType, children):
        pass


class FlowScreen:
    def __init__(
        self,
        id: str,
        title: str,
        data,
        layout: FlowLayout,
        terminal: bool = False,
        refresh_on_back: bool = False,
    ):
        pass


class FlowLayoutChild:
    pass


class FlowHeading:
    def __init__(self, text: str, visible: bool = True):
        self.heading_type = "TextHeading"
        self.text = text
        self.visible = visible

    def to_dict(self):
        return {
            "type": self.heading_type,
            "text": self.text,
            "visible": self.visible,
        }


class FlowSubheading:
    def __init__(self, text: str, visible: bool = True):
        self.sub_heading_type = "TextSubheading"
        self.text = text
        self.visible = visible

    def to_dict(self):
        return {
            "type": self.sub_heading_type,
            "text": self.text,
            "visible": self.visible,
        }


class FlowBody:
    def __init__(
        self,
        text: str,
        font_weight: FlowFontWeight = FlowFontWeight.NORMAL,
        strikethrough: bool = False,
        visible: bool = True,
    ):
        self.body_type = "TextBody"
        self.text = text
        self.font_weight = font_weight
        self.strikethrough = strikethrough
        self.visible = visible

    def to_dict(self):
        return {
            "type": self.body_type,
            "text": self.text,
            "font-weight": self.font_weight,
            "strikethrough": self.strikethrough,
            "visible": self.visible,
        }


class FlowCaption:
    def __init__(
        self,
        text: str,
        font_weight: FlowFontWeight = FlowFontWeight.NORMAL,
        strikethrough: bool = False,
        visible: bool = True,
    ):
        self.caption_type = "TextCaption"
        self.text = text
        self.font_weight = font_weight
        self.strikethrough = strikethrough
        self.visible = visible

    def to_dict(self):
        return {
            "type": self.caption_type,
            "text": self.text,
            "font-weight": self.font_weight,
            "strikethrough": self.strikethrough,
            "visible": self.visible,
        }


class FlowInputType(str, Enum):
    TEXT = "text"
    NUMBER = "number"
    EMAIL = "email"
    PASSWORD = "password"
    PASSCODE = "passcode"
    PHONE = "phone"


class FlowTextInput:
    def __init__(
        self,
        name: str,
        label: str,
        input_type: FlowInputType,
        required: bool = True,
        min_chars: int = 0,
        max_chars: int = 80,
        helper_text: str = None,
        visible: bool = True,
    ):
        self.input_type = "TextInput"
        self.name = name
        self.label = label
        self.input_type = input_type
        self.required = required
        self.min_chars = min_chars
        self.max_chars = max_chars
        self.helper_text = helper_text
        self.visible = visible

    def to_dict(self):
        return {
            "type": self.input_type,
            "name": self.name,
            "label": self.label,
            "input_type": self.input_type,
            "required": self.required,
            "min-chars": self.min_chars,
            "max-chars": self.max_chars,
            "helper-text": self.helper_text,
            "visible": self.visible,
        }


class FlowTextArea:
    def __init__(
        self,
        name: str,
        label: str,
        required: bool = True,
        max_length: int = 600,
        helper_text: str = None,
        visible: bool = True,
        enabled: bool = True,
    ):
        self.input_type = "TextArea"
        self.name = name
        self.label = label
        self.required = required
        self.helper_text = helper_text
        self.visible = visible
        self.max_length = max_length
        self.enabled = enabled

    def to_dict(self):
        return {
            "type": self.input_type,
            "name": self.name,
            "label": self.label,
            "required": self.required,
            "max-length": self.max_length,
            "helper_text": self.helper_text,
            "visible": self.visible,
            "enabled": self.enabled,
        }


class FlowCheckBox:
    def __init__(
        self, id: str, title: str, description: str, enabled: bool, metadata: str = ""
    ):
        self.input_type = "CheckBox"
        self.id = id
        self.title = title
        self.description = description
        self.enabled = enabled
        self.metadata = metadata

    def to_dict(self):
        return {
            "type": self.input_type,
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "enabled": self.enabled,
            "metadata": self.metadata,
        }


class FlowCheckBoxGroup:
    def __init__(
        self,
        name: str,
        checkboxes: list[FlowCheckBox],
        min_selected: int,
        max_selected: int,
        enabled: bool,
        label: str,
        required: bool,
        visible: bool,
    ):
        self.input_type = "CheckBoxGroup"
        self.name = name
        self.checkboxes = checkboxes
        self.min_selected = min_selected
        self.max_selected = max_selected
        self.enabled = enabled
        self.label = label
        self.required = required
        self.visible = visible
        #  add on select action

    def to_dict(self):
        return {
            "type": self.input_type,
            "name": self.name,
            "checkboxes": [checkbox.to_dict() for checkbox in self.checkboxes],
            "min_selected": self.min_selected,
            "max_selected": self.max_selected,
            "enabled": self.enabled,
            "label": self.label,
            "required": self.required,
            "visible": self.visible,
        }
