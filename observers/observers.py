from typing import List
from repositories.interface import IOrderObserver

class StandardNotificationObserver(IOrderObserver):
    def update(self, order_id: int, client: str, client_type: str, status: str, total: float) -> None:
        if status == 'pendente':
            print(f"Email enviado para {client}: Pedido recebido!")
            if client_type == 'vip': print(f"SMS enviado para {client}: Pedido VIP recebido!")
            elif client_type == 'corporativo': print(f"Notificacao enviada ao gerente de conta de {client}")
        elif status == 'aprovado':
            print(f"Email enviado para {client}: Pedido aprovado!")
            if client_type == 'vip': print(f"SMS enviado para {client}: Pedido aprovado!")
        elif status == 'enviado':
            print(f"Email enviado para {client}: Pedido enviado!")
        elif status == 'entregue':
            print(f"Email enviado para {client}: Pedido entregue!")
            
            
            pts: int = int(total * 2) if client_type == 'vip' else int(total * 1.5) if client_type == 'corporativo' else int(total)
            tipo_msg: str = "Cliente VIP" if client_type == 'vip' else "Cliente corporativo" if client_type == 'corporativo' else "Cliente"
            print(f"{tipo_msg} ganhou {pts} pontos!")

class SpecialNotificationObserver(IOrderObserver):
    def update(self, order_id: int, client: str, client_type: str, status: str, total: float) -> None:
        if status == 'pendente':
            print(f"Email especial enviado para {client}: Pedido especial recebido!")
        else:
            print(f"Pedido especial {order_id} -> {status}")

class Publisher:
    def __init__(self) -> None:
        self._observers: List[IOrderObserver] = []
        
    def attach(self, observer: IOrderObserver) -> None:
        self._observers.append(observer)
        
    def notify(self, order_id: int, client: str, client_type: str, status: str, total: float) -> None:
        for obs in self._observers:
            obs.update(order_id, client, client_type, status, total)