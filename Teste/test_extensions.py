from extensions.crypto_payment import CryptoPayment
from strategies import StandardDiscountStrategy
from extensions.whatsapp_obeserver import WhatsAppNotificationObserver
from extensions.volume_discount import VolumeDiscountDecorator

#teste do pagamento por criptomoeda
def test_crypto_payment_processa_com_taxa():
    crypto = CryptoPayment()
    assert crypto.process(100.0) is True

#teste de notificacao via whats
def test_whatsapp_observer_notifica_todos_os_clientes(capsys):
    observer = WhatsAppNotificationObserver()
    observer.update(1, "Joao", "normal", "aprovado", 100.0)
    
    captured = capsys.readouterr()
    assert "WhatsApp enviado para Joao" in captured.out

#teste do desconto por volume
def test_volume_discount_aplica_15_por_cento_acima_de_3_itens():
    base = StandardDiscountStrategy()
    decorator = VolumeDiscountDecorator(base)
    
    itens = [{'nome': 'p1', 'p': 100, 'q': 3, 'tipo': 'normal'}]
    
    total = decorator.calculate(itens, 'normal')
    assert total == 255.0