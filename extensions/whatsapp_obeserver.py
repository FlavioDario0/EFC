from repositories.interface import IOrderObserver

class WhatsAppNotificationObserver(IOrderObserver):
    def update(self, order_id: int, client: str, client_type: str, status: str, total: float) -> None:
        print(f"WhatsApp enviado para {client}: Status do pedido {order_id} atualizado para '{status}'.")