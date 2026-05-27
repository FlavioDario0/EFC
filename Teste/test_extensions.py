from extensions.crypto_payment import CryptoPayment

def test_crypto_payment_processa_com_taxa():
    crypto = CryptoPayment()
    assert crypto.process(100.0) is True