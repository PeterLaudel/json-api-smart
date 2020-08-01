from abc import abstractmethod, ABC
from typing import Type, List


class JsonApiResourceBase(ABC):
    @staticmethod
    @abstractmethod
    def base_url() -> str:
        """ base url of the resource """

    @classmethod
    @abstractmethod
    def attributes(cls: Type["JsonApiResourceBase"]) -> List[str]:
        """ All attributes of this resource """

    @classmethod
    @abstractmethod
    def relationships(cls: Type["JsonApiResourceBase"]) -> List[str]:
        """ All relationships of this resource """

    @classmethod
    @abstractmethod
    def resource_id(cls: Type["JsonApiResourceBase"]) -> str:
        """ Return the name of the resource id """

    @classmethod
    @abstractmethod
    def resource_name(cls: Type["JsonApiResourceBase"]) -> str:
        """ The resource name which is used for url creation"""
