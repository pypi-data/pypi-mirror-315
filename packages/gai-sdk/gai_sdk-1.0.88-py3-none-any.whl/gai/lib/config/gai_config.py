from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional, Dict, List

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
    
class ModuleConfig(BaseSettings):
    name: str
    class_: str = Field(alias="class")  # Use 'class' as an alias for 'class_'

    class Config:
        allow_population_by_name = True  # Allow access via both 'class' and 'class_'

class ServerLLMConfigBase(BaseSettings):
    type: str
    engine: str
    model: str
    name: str
    module: ModuleConfig
    