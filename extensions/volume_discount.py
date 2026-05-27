from typing import List, Dict, Any
from repositories.interface import IDiscountStrategy

class VolumeDiscountDecorator(IDiscountStrategy):
    def __init__(self, base_strategy: IDiscountStrategy) -> None:
        self.base_strategy = base_strategy

    def calculate(self, items: List[Dict[str, Any]], client_type: str) -> float:
        total = self.base_strategy.calculate(items, client_type)
        
        desconto_extra = 0.0
        for i in items:
            if i['q'] >= 3:
                desconto_extra += (i['p'] * i['q']) * 0.15
                
        return total - desconto_extra