from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, Dict

class ClientLLMConfig(BaseSettings):
    type: str
    engine: str
    model: str
    url: Optional[str] = None
    env: Optional[Dict] = None
    extra: Optional[Dict] = None

class ClientSpecConfig(BaseSettings):
    default: str=None
    configs: Optional[Dict[str,ClientLLMConfig]]={}
        
class ClientConfig(BaseSettings):
    ttt: ClientSpecConfig = None
    rag: ClientSpecConfig = None
    tti: ClientSpecConfig = None
    tts: ClientSpecConfig = None
    stt: ClientSpecConfig = None
    itt: ClientSpecConfig = None
    ttc: ClientSpecConfig = None
    
    @classmethod
    def from_config(cls, config: dict):
        # Preprocess the config and initialize the object
        return cls(
            ttt=ClientSpecConfig(**config["clients"]["ttt"]),
            rag=ClientSpecConfig(**config["clients"]["rag"]),
            tti=ClientSpecConfig(**config["clients"]["tti"]),
            tts=ClientSpecConfig(**config["clients"]["tts"]),
            stt=ClientSpecConfig(**config["clients"]["stt"]),
            itt=ClientSpecConfig(**config["clients"]["itt"]),
            ttc=ClientSpecConfig(**config["clients"]["ttc"]),
        )
    