import pytest
import os
from agenda_db.agendaSqlite3 import AppAgenda, DBNome, DBTelefone, DBDadoAgenda


@pytest.fixture
def agenda_test():
    """Cria uma agenda em um banco SQLite temporário para cada teste."""
    nome_db = "test_temp.db"
    if os.path.exists(nome_db):
        os.remove(nome_db)
    
    app = AppAgenda(nome_db)
    
    yield app # O teste acontece aqui
    
    # Teardown: Fecha conexão e remove o arquivo após o teste
    app.agenda.conexão.close()
    if os.path.exists(nome_db):
        os.remove(nome_db)


def test_nome_vazio_lanca_erro():
    with pytest.raises(Exception) as excinfo:
        DBNome("")

    assert excinfo.value.args[0] == 'Nome não pode ser nulo nem em branco'
    assert excinfo.type is ValueError


def test_inserir_novo_contato(agenda_test):
    novo_nome = DBNome("João Silva")
    dados = DBDadoAgenda(novo_nome)
    tipo_celular = agenda_test.agenda.tiposTelefone[0]
    dados.telefones.adiciona(DBTelefone("11999999999", tipo_celular))
    
    agenda_test.agenda.novo(dados)
    registro = agenda_test.pesquisa("João Silva")
    telefone_gravado = registro.telefones[0]
    
    assert registro.nome.id == 1
    assert telefone_gravado.id == 1
    assert registro.nome.nome == "João Silva"
    assert telefone_gravado == DBTelefone("11999999999")


def test_pesquisa_nome_inexistente(agenda_test):
    resultado = agenda_test.pesquisa("Maria")

    assert resultado is None


def test_pesquisa_nome_raise_type_error(agenda_test):
    with pytest.raises(Exception) as excinfo:
        agenda_test.pesquisa(22)

    with pytest.raises(Exception) as excinfo2:
        agenda_test.agenda.pesquisaNome(22)

    assert excinfo.value.args[0] == "nome deve ser do tipo DBNome"
    assert excinfo2.value.args[0] == "nome deve ser do tipo DBNome"
    assert excinfo.type is TypeError
    assert excinfo2.type is TypeError


def test_apagar_contato(agenda_test):
    nome = DBNome("Remover")
    registro = DBDadoAgenda(nome)
    agenda_test.agenda.novo(registro)
    
    p = agenda_test.pesquisa("Remover")
    agenda_test.agenda.apaga(p)
    
    assert agenda_test.pesquisa("Remover") is None


def test_pede_nome(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "Carlos")
    
    assert AppAgenda.pede_nome() == "Carlos"


def test_novo_telefone_aceitando_padrao(agenda_test, monkeypatch):
    contato = DBDadoAgenda(DBNome("Maria"))
    
    respostas = iter(["1234-5678", ""]) 
    monkeypatch.setattr('builtins.input', lambda _: next(respostas))

    agenda_test.novo_telefone(contato)

    # assert excinfo 
    assert len(contato.telefones) == 1
    assert contato.telefones[0].número == "1234-5678"
    assert contato.telefones[0].tipo.tipo == "Celular"
