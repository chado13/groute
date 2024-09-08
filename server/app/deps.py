from app.config import config
from app.assistant import GrouteAssistant
from functools import lru_cache

@lru_cache()
def get_assistant() -> GrouteAssistant:
    return GrouteAssistant(config.api_key)