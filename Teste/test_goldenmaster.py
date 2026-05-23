import pytest
import json
import os
from codigoinicial import Sis
from codigoinicial import Sis, PedEspecial

@pytest.fixture
def sis(tmp_path, monkeypatch):
    #Isola o banco em diretorio temporario por teste.
    monkeypatch.chdir(tmp_path)
    s = Sis()
    yield s
    s.close()

#TESTES DE CRIAÇÃO DE PEDIDO
def test_pedido_normal_calcula_total_corretamente(sis):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 2, 'tipo': 'normal'},
        {'nome': 'produto2', 'p': 50, 'q': 1, 'tipo': 'desc10'}
    ]
    id_ped = sis.add_ped('Joao Silva', itens, 'normal')
    pedido = sis.get_ped(id_ped)
    
    assert pedido['tot'] == pytest.approx(245.0)
    assert pedido['st'] == 'pendente'
    assert pedido['tp'] == 'normal'

def test_pedido_vip_aplica_desconto_de_5_por_cento(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Maria', itens, 'vip')
    pedido = sis.get_ped(id_ped)
    
    assert pedido['tot'] == pytest.approx(95.0)

def test_pedido_corporativo_aplica_desconto_de_10_por_cento(sis):
    itens = [{'nome': 'p1', 'p': 200, 'q': 2, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Empresa X', itens, 'corporativo')
    pedido = sis.get_ped(id_ped)
    
    assert pedido['tot'] == pytest.approx(360.0)

#TESTES DE PAGAMENTO
def test_pagamento_insuficiente_falha(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    
    assert sis.proc_pag(id_ped, 'cartao', 50) is False

def test_pix_aprova_pedido_automaticamente(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    
    assert sis.proc_pag(id_ped, 'pix', 100) is True
    assert sis.get_ped(id_ped)['st'] == 'aprovado'

def test_boleto_nao_aprova_automaticamente(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    
    assert sis.proc_pag(id_ped, 'boleto', 100) is True
    assert sis.get_ped(id_ped)['st'] == 'pendente'

#TESTES DE ATUALIZAÇÃO E CANCELAMENTO
def test_atualiza_status_pedido(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    
    sis.upd_st(id_ped, 'enviado')
    assert sis.get_ped(id_ped)['st'] == 'enviado'

def test_cancelamento_pedido(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    
    sis.cancelar_pedido(id_ped)
    assert sis.get_ped(id_ped)['st'] == 'cancelado'

#TESTES DE RELATÓRIOS
def test_geracao_relatorio_vendas(sis):
    sis.add_ped('Joao', [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}], 'normal')
    sis.gerar_rel('vendas')
    
    assert os.path.exists('rel_vendas.txt')
    with open('rel_vendas.txt', 'r') as f:
        conteudo = f.read()
        assert "Total de vendas: 100.0" in conteudo

def test_geracao_relatorio_clientes(sis):
    sis.add_ped('Joao', [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}], 'normal')
    sis.gerar_rel('clientes')
    
    assert os.path.exists('rel_clientes.txt')
    with open('rel_clientes.txt', 'r') as f:
        conteudo = f.read()
        assert "Joao, normal" in conteudo

def test_descontos_desc20_e_frete_gratis(sis):
    itens = [
        {'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'desc20'},
        {'nome': 'p2', 'p': 50, 'q': 1, 'tipo': 'frete_gratis'}
    ]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    pedido = sis.get_ped(id_ped)
    
    assert pedido['tot'] == pytest.approx(130.0)

def test_status_vip_aprovado_enviado(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Cliente VIP', itens, 'vip')
    
    sis.upd_st(id_ped, 'aprovado')
    assert sis.get_ped(id_ped)['st'] == 'aprovado'
    
    sis.upd_st(id_ped, 'enviado')
    assert sis.get_ped(id_ped)['st'] == 'enviado'

# TESTES DE ESTOQUE
def test_validar_estoque_com_sucesso(sis):
    itens = [{'nome': 'produto1', 'q': 10}]
    assert sis.validar_estoque(itens) is True

def test_validar_estoque_produto_inexistente(sis):
    itens = [{'nome': 'produto_fantasma', 'q': 1}]
    assert sis.validar_estoque(itens) is False

def test_validar_estoque_quantidade_insuficiente(sis):
    itens = [{'nome': 'produto1', 'q': 9999}] 
    assert sis.validar_estoque(itens) is False


#TESTES DA CLASSE PedEspecial
@pytest.fixture
def ped_especial(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    p = PedEspecial()
    yield p
    p.close()

def test_ped_especial_adiciona_e_pula_status(ped_especial):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = ped_especial.add_ped('Joao Especial', itens, 'vip')
    
    ped_especial.upd_st(id_ped, 'entregue')
    assert ped_especial.get_ped(id_ped)['st'] == 'entregue'

# --- TESTES DE TRANSIÇÕES DE STATUS E PONTUAÇÃO ---
def test_status_entregue_gera_pontos_vip(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Cliente VIP', itens, 'vip')
    
    sis.upd_st(id_ped, 'entregue')
    assert sis.get_ped(id_ped)['st'] == 'entregue'

def test_status_entregue_gera_pontos_corporativo(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Cliente Corp', itens, 'corporativo')
    
    
    sis.upd_st(id_ped, 'entregue')
    assert sis.get_ped(id_ped)['st'] == 'entregue'

def test_busca_pedido_inexistente(sis):
    assert sis.get_ped(9999) is None

def test_pagamento_metodo_invalido(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    
    assert sis.proc_pag(id_ped, 'cheque', 100) is False