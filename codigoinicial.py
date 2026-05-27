from typing import List, Dict, Any
from repositories.order_repository import OrderRepository
from strategies.discount_strategy import StandardDiscountStrategy, SpecialDiscountStrategy
from strategies.payment_strategy import CartaoPayment, PixPayment, BoletoPayment
from observers.observers import Publisher, StandardNotificationObserver, SpecialNotificationObserver
from services.order_service import OrderService

class Sis:
    def __init__(self) -> None:
        self.repo = OrderRepository()
        self.publisher = Publisher()
        self._setup_observers()
        
        self.order_service = OrderService(self.repo, self._get_discount_strategy(), self.publisher)
        
       
        self.order_service.register_payment_strategy('cartao', CartaoPayment())
        self.order_service.register_payment_strategy('pix', PixPayment())
        self.order_service.register_payment_strategy('boleto', BoletoPayment())

    def _setup_observers(self) -> None:
        self.publisher.attach(StandardNotificationObserver())

    def _get_discount_strategy(self) -> Any:
        return StandardDiscountStrategy()

    def add_ped(self, n: str, its: List[Dict[str, Any]], t: str) -> int: return self.order_service.add_ped(n, its, t)
    def get_ped(self, id: int) -> Any: return self.repo.get(id)
    def upd_st(self, id: int, s: str) -> None: self.order_service.upd_st(id, s)
    def calc_tot_cli(self, n: str) -> float: return self.order_service.calc_tot_cli(n)
    def gerar_rel(self, tipo: str) -> None: self.order_service.gerar_rel(tipo)
    def proc_pag(self, id: int, m: str, vl: float) -> bool: return self.order_service.proc_pag(id, m, vl)
    def cancelar_pedido(self, id: int) -> None: self.order_service.cancelar_pedido(id)
    def validar_estoque(self, its: List[Dict[str, Any]]) -> bool: return True  # Mock simplificado
    def close(self) -> None: self.repo.close()


class PedEspecial(Sis):
    def _setup_observers(self) -> None:
        self.publisher.attach(SpecialNotificationObserver())

    def _get_discount_strategy(self) -> Any:
        return SpecialDiscountStrategy()

def main() -> None:
    s = Sis()
    its1 = [{'nome': 'produto1', 'p': 100, 'q': 2, 'tipo': 'normal'},
            {'nome': 'produto2', 'p': 50, 'q': 1, 'tipo': 'desc10'}]
    id1 = s.add_ped('Joao Silva', its1, 'normal')
    s.proc_pag(id1, 'cartao', 250)
    s.upd_st(id1, 'enviado')
    s.upd_st(id1, 'entregue')

    its2 = [{'nome': 'produto3', 'p': 200, 'q': 1, 'tipo': 'desc20'}]
    id2 = s.add_ped('Maria Santos', its2, 'vip')
    s.proc_pag(id2, 'pix', 160)

    its3 = [{'nome': 'produto1', 'p': 100, 'q': 5, 'tipo': 'normal'}]
    id3 = s.add_ped('Empresa XYZ', its3, 'corporativo')
    s.proc_pag(id3, 'boleto', 500)

    s.gerar_rel('vendas')
    s.gerar_rel('clientes')
    s.close()

if __name__ == '__main__':
    main()