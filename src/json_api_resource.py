from typing import List, Set, Type, TypeVar
from .json_api_request import JsonApiRequest, QueryTypes
from .attribute import Attribute

H = TypeVar("H")


def auto_init(self, *args, **kwargs):
    for arg_val, arg_name in zip(args, self.__annotations__.keys()):
        setattr(self, arg_name, arg_val)

    self.__dict__.update(kwargs)


class MetaBase(type):
    def __new__(cls, name, bases, attrs):
        attrs['__init__'] = auto_init
        return super(MetaBase, cls).__new__(cls, name, bases, attrs)


class JsonApiResource(metaclass=MetaBase):

    @staticmethod
    def base_url() -> str:
        return "http://baseurl.com"

    @classmethod
    def find(cls: Type[H], object_id: int) -> H:
        return JsonApiRequest(cls).find(object_id=object_id)

    @classmethod
    def all(cls: Type[H]) -> List[H]:
        return JsonApiRequest(cls).all()

    @classmethod
    def with_params(cls: Type[H], **kwargs: QueryTypes) -> JsonApiRequest:
        return JsonApiRequest(cls).with_params(**kwargs)

    @classmethod
    def where(cls: Type[H], **kwargs: QueryTypes):
        return JsonApiRequest(cls).with_params(**kwargs)

    @classmethod
    def attributes(cls: Type[H]) -> Set[str]:
        return {
            key
            for key in cls.__annotations__.keys()
            if isinstance(getattr(cls, key), Attribute)
        }
