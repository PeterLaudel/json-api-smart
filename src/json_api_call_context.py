from typing import Dict, Optional, List


class MISSING:
    pass


class JsonApiCallContext:
    def __init__(self, data: Dict, included: Optional[List[Dict]] = None):
        self.__data = data
        self.__included = included

    def get_id(self) -> str:
        return self.__data["id"]

    def get_attribute(self, key):
        return self.__data["attributes"].get(key, MISSING)

    def get_relationship(self, key) -> Optional[Dict]:
        return self.__data["relationships"].get(key, None)

    def find_in_included(self, resource_type: str, resource_id: str) -> Optional[Dict]:
        if self.__included is None:
            return None

        for include in self.__included:
            if include["type"] == resource_type and include["id"] == resource_id:
                return include

        return None
