from typing import Dict, Optional
from .attribute import MISSING


class JsonApiCallContext:
    def __init__(self, data: Dict, included: Optional[Dict] = None):
        self.__data = data
        self.__included = included

    def get_id(self) -> str:
        return self.__data["id"]

    def get_attribute(self, key):
        return self.__data["attributes"].get(key, MISSING)

    def get_relationship(self, key) -> Dict:
        return self.__data["relationships"][key]

    def find_in_included(self, resource_type: str, resource_id: str) -> Optional[Dict]:
        for include in self.__included:
            if include["type"] == resource_type and include["id"] == resource_id:
                return include

        return None
