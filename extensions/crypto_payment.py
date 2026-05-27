from repositories.interface import IPaymentStrategy

class CryptoPayment(IPaymentStrategy):
    def process(self, amount: float) -> bool:
        total_com_taxa = amount * 1.02 
        print(f"Processando pagamento em Criptomoeda. Total com taxa (2%): R${total_com_taxa:.2f}")
        print("Criptomoeda validada!")
        return True