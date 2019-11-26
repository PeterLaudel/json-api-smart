from abc import abstractmethod, ABC
from typing import Type, TypeVar, List, Dict
from .json_api_request import QueryTypes, JsonApiRequest

H = TypeVar("H")


class JsonApiResourceBase(ABC):
    @staticmethod
    @abstractmethod
    def base_url() -> str:
        pass

    @classmethod
    @abstractmethod
    def find(cls: Type[H], resource_id: int) -> H:
        pass

    @classmethod
    @abstractmethod
    def all(cls: Type[H]) -> List[H]:
        pass

    @classmethod
    @abstractmethod
    def with_params(cls: Type[H], **kwargs: QueryTypes) -> JsonApiRequest:
        pass

    @classmethod
    @abstractmethod
    def where(cls: Type[H], **kwargs: QueryTypes) -> JsonApiRequest:
        pass

    @classmethod
    @abstractmethod
    def attributes(cls: Type[H]) -> List[str]:
        pass

    @classmethod
    @abstractmethod
    def relationships(cls: Type[H]) -> List[str]:
        pass

    @classmethod
    @abstractmethod
    def resource_name(cls: Type[H]) -> str:
        pass
