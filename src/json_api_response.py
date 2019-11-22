from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class JsonApiResponse:
    data: Dict
    included: Optional[Dict] = None
