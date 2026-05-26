from typing import List, Dict, Any
from repositories.interface import  IPaymentStrategy

class CartaoPayment(IPaymentStrategy):
    def process(self, amount: float) -> bool:
        print("Processando pagamento com cartao...\nCartao validado!")
        return True

class PixPayment(IPaymentStrategy):
    def process(self, amount: float) -> bool:
        print("Gerando QR Code PIX...\nPIX recebido!")
        return True

class BoletoPayment(IPaymentStrategy):
    def process(self, amount: float) -> bool:
        print("Gerando boleto...\nBoleto gerado!")
        return True