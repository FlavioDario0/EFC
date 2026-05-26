import json
from datetime import datetime
from repositories.order_repository import OrderRepository
from services.notification_service import ConsoleNotificationService
from services.stock_service import MockStockService
from services.order_service import OrderService

class Sis:
    def __init__(self):
        # A montagem das camadas ocorre aqui. A injeção de dependência pura 
        # (DIP) vira exigência apenas no Sprint 2.
        self.repo = OrderRepository()
        self.notifier = ConsoleNotificationService()
        self.stock = MockStockService()
        self.order_service = OrderService(self.repo, self.notifier)

    def add_ped(self, n, its, t): return self.order_service.add_ped(n, its, t)
    def get_ped(self, id): return self.repo.get(id)
    def upd_st(self, id, s): self.order_service.upd_st(id, s)
    def calc_tot_cli(self, n): return self.order_service.calc_tot_cli(n)
    def gerar_rel(self, tipo): self.order_service.gerar_rel(tipo)
    def proc_pag(self, id, m, vl): return self.order_service.proc_pag(id, m, vl)
    def validar_estoque(self, its): return self.stock.validate(its)
    def cancelar_pedido(self, id): self.order_service.cancelar_pedido(id)
    def close(self): self.repo.close()

class PedEspecial(Sis):
    def add_ped(self, n, its, t):
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tot = sum(i['p'] * i['q'] for i in its if i['tipo'] == 'normal')
        tot += sum(i['p'] * i['q'] * 0.9 for i in its if i['tipo'] == 'desc10')
        tot += sum(i['p'] * i['q'] * 0.8 for i in its if i['tipo'] == 'desc20')
        
        tot = tot * 1.15
        id_ped = self.repo.add(n, json.dumps(its), tot, 'pendente', dt, t)
        print(f"Email especial enviado para {n}: Pedido especial recebido!")
        return id_ped

    def upd_st(self, id, s):
        p = self.repo.get(id)
        if p:
            self.repo.update_status(id, s)
            print(f"Pedido especial {id} -> {s}")

def main():
    s = Sis()
    its1 = [{'nome': 'produto1', 'p': 100, 'q': 2, 'tipo': 'normal'},
            {'nome': 'produto2', 'p': 50, 'q': 1, 'tipo': 'desc10'}]
    if s.validar_estoque(its1):
        id1 = s.add_ped('Joao Silva', its1, 'normal')
        print(f"Pedido {id1} criado!")
        s.proc_pag(id1, 'cartao', 250)
        s.upd_st(id1, 'enviado')
        s.upd_st(id1, 'entregue')

    its2 = [{'nome': 'produto3', 'p': 200, 'q': 1, 'tipo': 'desc20'}]
    if s.validar_estoque(its2):
        id2 = s.add_ped('Maria Santos', its2, 'vip')
        s.proc_pag(id2, 'pix', 160)

    its3 = [{'nome': 'produto1', 'p': 100, 'q': 5, 'tipo': 'normal'}]
    if s.validar_estoque(its3):
        id3 = s.add_ped('Empresa XYZ', its3, 'corporativo')
        s.proc_pag(id3, 'boleto', 500)

    s.gerar_rel('vendas')
    print()
    s.gerar_rel('clientes')
    s.close()

if __name__ == '__main__':
    main()