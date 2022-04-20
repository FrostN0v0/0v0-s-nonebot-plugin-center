from pydantic import BaseSettings, Extra

class Config(BaseSettings):
    # Your Config Here
    plugin_setting: str = "default"

    anime_qq_friends: list[int]
    anime_qq_groups: list[int]
    class Config:
        extra = Extra.allow
        case_sensitive = False
        extra = "ignore"