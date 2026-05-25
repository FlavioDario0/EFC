import json
from datetime import datetime
from repositories.interface import IOrderRepository, INotificationService

class OrderService:
    def __init__(self, repo: IOrderRepository, notifier: INotificationService):
        self.repo = repo
        self.notifier = notifier

    def add_ped(self, n, its, t):
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tot = 0
        for i in its:
            if i['tipo'] == 'normal': tot += i['p'] * i['q']
            elif i['tipo'] == 'desc10': tot += i['p'] * i['q'] * 0.9
            elif i['tipo'] == 'desc20': tot += i['p'] * i['q'] * 0.8
            elif i['tipo'] == 'frete_gratis': tot += i['p']

        if t == 'vip': tot = tot * 0.95
        elif t == 'corporativo': tot = tot * 0.90

        its_str = json.dumps(its)
        id_ped = self.repo.add(n, its_str, tot, 'pendente', dt, t)
        self.notifier.notify_received(n, t)
        return id_ped

    def upd_st(self, id, s):
        p = self.repo.get(id)
        if p:
            self.repo.update_status(id, s)
            if s == 'aprovado': self.notifier.notify_approved(p['cli'], p['tp'])
            elif s == 'enviado': self.notifier.notify_shipped(p['cli'])
            elif s == 'entregue': self.notifier.notify_delivered(p['cli'], p['tp'], p['tot'])

    def proc_pag(self, id, m, vl):
        p = self.repo.get(id)
        if not p: return False
        if vl < p['tot']:
            print("Valor insuficiente!")
            return False
        
        if m == 'cartao':
            print("Processando pagamento com cartao...\nCartao validado!")
            self.upd_st(id, 'aprovado')
            return True
        elif m == 'pix':
            print("Gerando QR Code PIX...\nPIX recebido!")
            self.upd_st(id, 'aprovado')
            return True
        elif m == 'boleto':
            print("Gerando boleto...\nBoleto gerado!")
            return True
        else:
            print("Metodo de pagamento invalido!")
            return False

    def cancelar_pedido(self, id):
        self.repo.update_status(id, 'cancelado')
        print(f"Pedido {id} cancelado")

    def calc_tot_cli(self, n):
        return sum(r[3] for r in self.repo.get_all_by_client(n))

    def gerar_rel(self, tipo):
        if tipo == 'vendas':
            rs = self.repo.get_all()
            print("=== RELATORIO DE VENDAS ===")
            tot_g = sum(r[3] for r in rs)
            for r in rs:
                print(f"Pedido #{r[0]} - Cliente: {r[1]} - Total: R${r[3]:.2f} - Status: {r[4]}")
            print(f"Total Geral: R${tot_g:.2f}")
            with open('rel_vendas.txt', 'w') as f:
                f.write(f"Total de vendas: {tot_g}")
                
        elif tipo == 'clientes':
            rs = self.repo.get_all_clients()
            print("=== RELATORIO DE CLIENTES ===")
            for r in rs:
                tot = self.calc_tot_cli(r[0])
                print(f"Cliente: {r[0]} ({r[1]}) - Total gasto: R${tot:.2f}")
            with open('rel_clientes.txt', 'w') as f:
                for r in rs:
                    f.write(f"{r[0]}, {r[1]}\n")