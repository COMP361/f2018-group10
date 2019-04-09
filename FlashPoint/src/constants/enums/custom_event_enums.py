from enum import Enum,auto

class CustomEventEnum(Enum):
    ENABLE_KNOCKDOWN_PROMPT = auto()
    DISABLE_KNOCKDOWN_PROMPT = auto()
    ENABLE_VICTIM_LOST_PROMPT = auto()
    DISABLE_VICTIM_LOST_PROMPT = auto()
    ENABLE_VICTIM_SAVED_PROMPT = auto()
    DISABLE_VICTIM_SAVED_PROMPT = auto()