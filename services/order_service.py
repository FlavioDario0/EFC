import json
from datetime import datetime
from typing import List, Dict, Any
from repositories.interface import IOrderRepository, IDiscountStrategy, IPaymentStrategy
from observers.observers import Publisher

class OrderService:
    def __init__(self, repo: IOrderRepository, discount_strategy: IDiscountStrategy, publisher: Publisher) -> None:
        self.repo = repo
        self.discount_strategy = discount_strategy
        self.publisher = publisher
        self.payment_methods: Dict[str, Any] = {}

    def register_payment_strategy(self, name: str, strategy: IPaymentStrategy) -> None:
        self.payment_methods[name] = strategy

    def add_ped(self, n: str, its: List[Dict[str, Any]], t: str) -> int:
        dt: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tot: float = self.discount_strategy.calculate(its, t)
        
        id_ped: int = self.repo.add(n, json.dumps(its), tot, 'pendente', dt, t)
        self.publisher.notify(id_ped, n, t, 'pendente', tot)
        return id_ped

    def upd_st(self, id: int, s: str) -> None:
        p = self.repo.get(id)
        if p:
            self.repo.update_status(id, s)
            self.publisher.notify(id, str(p['cli']), str(p['tp']), s, float(p['tot']))

    def proc_pag(self, id: int, m: str, vl: float) -> bool:
        p = self.repo.get(id)
        if not p: return False
        if vl < float(p['tot']):
            print("Valor insuficiente!")
            return False
            
        strategy: IPaymentStrategy = self.payment_methods.get(m) 
        if not strategy:
            print("Metodo de pagamento invalido!")
            return False
            
        if strategy.process(vl) and m != 'boleto':
            self.upd_st(id, 'aprovado')
        return True

    def calc_tot_cli(self, n: str) -> float:
        return sum(float(r[3]) for r in self.repo.get_all_by_client(n))

    def gerar_rel(self, tipo: str) -> None:
        if tipo == 'vendas':
            rs = self.repo.get_all()
            print("=== RELATORIO DE VENDAS ===")
            tot_g: float = sum(float(r[3]) for r in rs)
            for r in rs:
                print(f"Pedido #{r[0]} - Cliente: {r[1]} - Total: R${r[3]:.2f} - Status: {r[4]}")
            print(f"Total Geral: R${tot_g:.2f}")
            with open('rel_vendas.txt', 'w') as f:
                f.write(f"Total de vendas: {tot_g}")
                
        elif tipo == 'clientes':
            rs_cli = self.repo.get_all_clients()
            print("=== RELATORIO DE CLIENTES ===")
            for rc in rs_cli:
                tot_c = self.calc_tot_cli(rc[0])
                print(f"Cliente: {rc[0]} ({rc[1]}) - Total gasto: R${tot_c:.2f}")
            with open('rel_clientes.txt', 'w') as f:
                for rc in rs_cli:
                    f.write(f"{rc[0]}, {rc[1]}\n")

    def cancelar_pedido(self, id: int) -> None:
        self.repo.update_status(id, 'cancelado')
        print(f"Pedido {id} cancelado")