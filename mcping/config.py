from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    # account = "202001051321"
    password = "sun106829"
    url = "http://jwgl.sdust.edu.cn/app.do"
    class Config:
        extra = "ignore"
