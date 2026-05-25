from repositories.interface import IStockService

class MockStockService(IStockService):
    def __init__(self):
        self.est = {'produto1': 100, 'produto2': 50, 'produto3': 75}

    def validate(self, items):
        for i in items:
            if i['nome'] not in self.est:
                print(f"Produto {i['nome']} nao encontrado!")
                return False
            if self.est[i['nome']] < i['q']:
                print(f"Estoque insuficiente para {i['nome']}!")
                return False
        return True