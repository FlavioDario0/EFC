from repositories.interface import INotificationService

class ConsoleNotificationService(INotificationService):
    def notify_received(self, client, client_type):
        if client_type == 'normal': print(f"Email enviado para {client}: Pedido recebido!")
        elif client_type == 'vip':
            print(f"Email enviado para {client}: Pedido recebido!")
            print(f"SMS enviado para {client}: Pedido VIP recebido!")
        elif client_type == 'corporativo':
            print(f"Email enviado para {client}: Pedido recebido!")
            print(f"Notificacao enviada ao gerente de conta de {client}")

    def notify_approved(self, client, client_type):
        print(f"Email enviado para {client}: Pedido aprovado!")
        if client_type == 'vip': print(f"SMS enviado para {client}: Pedido aprovado!")

    def notify_shipped(self, client):
        print(f"Email enviado para {client}: Pedido enviado!")

    def notify_delivered(self, client, client_type, total):
        print(f"Email enviado para {client}: Pedido entregue!")
        if client_type == 'vip':
            print(f"Cliente VIP ganhou {int(total * 2)} pontos!")
        elif client_type == 'corporativo':
            print(f"Cliente corporativo ganhou {int(total * 1.5)} pontos!")
        else:
            print(f"Cliente ganhou {int(total)} pontos!")