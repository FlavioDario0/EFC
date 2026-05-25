from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Order:
    id: int
    client: str
    items: List[Dict]
    total: float
    status: str
    date: str
    client_type: str