from pydantic import BaseModel, field_validator

class ScopedConfig(BaseModel):
    model: str = 'qwen2.5:0.5b'
    url: str = 'http://127.0.0.1:11434/'
    priority: int = 5

    @field_validator('priority')
    @classmethod
    def check_priority(cls, v: int):
        if v >= 1:
            return v
        raise ValueError('ollama command priority must be greater than 1')
    
    @field_validator('url')
    @classmethod
    def check_url(cls, v: str):
        if v.startswith('http://') and v.endswith('/'):
            return v
        raise ValueError('ollama url must start with http:// and end with /')
    
class Config(BaseModel):
    ollama: ScopedConfig = ScopedConfig()