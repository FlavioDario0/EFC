from typing import List, Dict, Any
from repositories.interface import IDiscountStrategy

class StandardDiscountStrategy(IDiscountStrategy):
    def calculate(self, items: List[Dict[str, Any]], client_type: str) -> float:
        tot: float = 0.0
        for i in items:
            t: str = i['tipo']
            if t == 'normal': tot += i['p'] * i['q']
            elif t == 'desc10': tot += i['p'] * i['q'] * 0.9
            elif t == 'desc20': tot += i['p'] * i['q'] * 0.8
            elif t == 'frete_gratis': tot += i['p']
            
        if client_type == 'vip': tot *= 0.95
        elif client_type == 'corporativo': tot *= 0.90
        return tot

class SpecialDiscountStrategy(IDiscountStrategy):
    def calculate(self, items: List[Dict[str, Any]], client_type: str) -> float:
        tot: float = 0.0
        for i in items:
            t: str = i['tipo']
            if t == 'normal': tot += i['p'] * i['q']
            elif t == 'desc10': tot += i['p'] * i['q'] * 0.9
            elif t == 'desc20': tot += i['p'] * i['q'] * 0.8
        return tot * 1.15