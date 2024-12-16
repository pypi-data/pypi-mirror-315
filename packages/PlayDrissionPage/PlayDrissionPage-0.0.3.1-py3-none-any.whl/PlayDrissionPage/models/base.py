from pydantic import BaseModel


def to_camel_case(string: str) -> str:
    # 将字段名转换为驼峰命名
    components = string.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


class CDPBaseModel(BaseModel):

    class Config:
        alias_generator = to_camel_case
        populate_by_name = True

