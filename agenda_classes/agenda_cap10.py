import sys
import pickle
from functools import total_ordering


def nulo_ou_vazio(texto):
    return texto is None or not texto.strip()


def valida_faixa_inteiro(pergunta, inicio, fim, padrão=None):
    while True:
        try:
            entrada = input(pergunta)
            if nulo_ou_vazio(entrada) and padrão is not None:
                entrada = padrão
            valor = int(entrada)
            if inicio <= valor <= fim:
                return valor 
        except ValueError:
            print(f'Valor inválido, favor digitar entre {inicio} e {fim}')


def valida_faixa_inteiro_ou_branco(pergunta, inicio, fim):
    while True:
        try:
            entrada = input(pergunta)
            if nulo_ou_vazio(entrada):
                return None
            valor = int(entrada)
            if inicio <= valor <= fim:
                return valor 
        except ValueError:
            print(f'Valor inválido, favor digitar entre {inicio} e {fim}')


class ListaÚnica:
    def __init__(self, elem_class):
        self.lista = []
        self.elem_class = elem_class

    def __len__(self):
        return len(self.lista)
    
    def __iter__(self):
        return iter(self.lista)
    
    def __getitem__(self, p):
        return self.lista[p]
    
    def indiceValido(self, i):
        return i >= 0 and i < len(self.lista)
    
    def adciona(self, elem):
        if self.pesquisa(elem) == -1:
            self.lista.append(elem)

    def remove(self, elem):
        self.lista.remove(elem)

    def pesquisa(self, elem):
        self.verifica_tipo(elem)
        try:
            return self.lista.index(elem)
        except ValueError:
            return -1
        
    def verifica_tipo(self, elem):
        if not isinstance(elem, self.elem_class):
            raise TypeError('Tipo inválido')
        
    def ordena(self, chave=None):
        self.lista.sort(key=chave)

    
@total_ordering
class Nome:
    def __init__(self, nome):
        if nome is None or not nome.strip():
            raise ValueError('Nome não pode ser nulo nem em branco')
        self.nome = nome
        self.chave = nome.strip().lower()

    def __str__(self):
        return self.nome 
    
    def __repr__(self):
        return f'<Classe {type(self).__name__} em 0{id(self):x} Nome: {self.nome} Chave: {self.chave  }'
    
    def __eq__(self, outro):
        return self.nome == outro.nome
    
    def __lt__(self, outro):
        return self.nome < outro.nome


@total_ordering
class TipoTelefone:
    def __init__(self, tipo):
        self.tipo = tipo

    def __str__(self):
        return f'({self.tipo})'
    
    def __eq__(self, outro):
        if outro is None:
            return False
        return self.tipo == outro.tipo
    
    def __lt__(self, outro):
        return self.tipo < outro.tipo 


class Telefone:
    def __init__(self, número, tipo=None):
        self.número = número
        self.tipo = tipo
    
    def __str__(self):
        if self.tipo is not None:
            tipo = self.tipo
        else:
            tipo = ''
        return f'{self.número}{tipo}'
    
    def __eq__(self, outro):
        return self.número == outro.número and (
            (self.tipo == outro.tipo) or (
             self.tipo is None or outro.tipo is None))

    @property
    def número(self):
        return self.__número
    
    @número.setter
    def número(self, valor):
        if valor is None or not valor.strip():
            raise ValueError('Número não pode ser None ou em branco')
        self.__número = valor


class Telefones(ListaÚnica):
    def __init__(self):
        super().__init__(Telefone)


class DadoAgenda:
    def __init__(self, nome):
        self.nome = nome
        self.telefones = Telefones()
    
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, Nome):
            raise TypeError('nome deve ser uma instância da class Nome')
        self.__nome = valor

    def pesquisaTelefone(self, telefone):
        posição = self.telefones.pesquisa(Telefone(telefone))
        if posição == -1:
            return None
        else:
            return self.telefones[posição]


class TiposTelefone(ListaÚnica):
    def __init__(self):
        super().__init__(TipoTelefone)
    

class Agenda(ListaÚnica):
    def __init__(self):
        super().__init__(DadoAgenda)
        self.tiposTelefone = TiposTelefone()

    def adicionaTipo(self, tipo):
        self.tiposTelefone.adiciona(TipoTelefone(tipo))

    def pesquisaNome(self, nome):
        if isinstance(nome, str):
            nome = Nome(nome)

        for dados in self.lista:
            if dados.nome == nome:
                return dados
            else:
                return None
            
    def ordena(self):
        super().ordena(lambda dado: str(dado.nome))


class Menu:
    def __init__(self):
        self.opções = [['Sair', None]]

    def adicionaopção(self, nome, função):
        self.opções.append([nome, função])

    def exibe(self):
        print('====')
        print('Menu')
        print('====\n')
        for i, opção in enumerate(self.opções):
            print(f'[{i}] - {opção[0]}')
        print()
    
    def execute(self):
        while True:
            self.exibe()
            escolha = valida_faixa_inteiro('Escolhe uma opção: ',
                                           0, len(self.opções)-1)
            if escolha == 0:
                break
            self.opções[escolha][1]()


class AppAgenda:
    @staticmethod
    def pede_nome():
        return input('Nome: ')
    
    @staticmethod
    def pede_telefone():
        return input('Telefone: ')
    
    def mostra_dados(dados):
        print(f'Nome: {dados.nome}')
        for telefone in dados.telefones:
            print(f'Telefone: {telefone}')
        print()

    @staticmethod
    def mostra_dados_telefone(dados):
        print(f'Nome: {dados.nome}')
        for i, telefone in enumerate(dados.telefones):
            print(f'{i} - Telefone: {telefone}')
        print()

    @staticmethod
    def pede_nome_arquivo():
        return input('Nome do arquivo: ')
    
    def __init__(self):
        self.agenda = Agenda()
        self.agenda.adicionaTipo('Celular')
        self.agenda.adicionaTipo('Residência')
        self.agenda.adicionaTipo('Trabalho')
        self.agenda.adicionaTipo('Fax')
        self.menu = Menu()
        self.menu.adicionaopção('Novo', self.novo)
        self.menu.adicionaopção('Altera', self.altera)
        self.menu.adicionaopção('Apaga', self.apaga)
        self.menu.adicionaopção('Lista', self.lista)
        self.menu.adicionaopção('Grava', self.grava)
        self.menu.adicionaopção('Lê', self.lê)
        self.menu.adicionaopção('Ordena', self.ordena)
        self.ultimo_arquivo = None

    def pede_tipo_telefone(self, padrão=None):
        for i, tipo in enumerate(self.agenda.tiposTelefone):
            print(f' {i} - {tipo} ', end=None)
        t = valida_faixa_inteiro(
            "Tipo: ", 0, len(self.agenda.tiposTelefone) - 1, padrão
        )

        return self.agenda.tiposTelefone[t]
    
    def pesquisa(self, nome):
        dado = self.agenda.pesquisaNome(Nome)
        return dado
    
    def novo(self):
        novo = AppAgenda.pede_nome()
        if nulo_ou_vazio(novo):
            return
        nome = Nome(novo)
        if self.pesquisa(nome) is not None:
            print('Nome já existe')
            return
        registro = DadoAgenda(nome)
        self.menu_telefones(registro)
        self.agenda.adiciona(registro)

    def apaga(self):
        if len(self.agenda) == 0:
            print('Agenda vazia, nada a apagar')
        nome = AppAgenda.pede_nome()
        if nulo_ou_vazio(nome):
            return
        p = self.pesquisa(nome)
        if p is not None:
            self.agenda.remove(p)
            print(f'Apagado. A agenda agora possui apenas: {len(self.agenda)} registros')
        else:
            print('Nome não encontrado!')
            
    def altera(self):
        if len(self.agenda) == 0:
            print('Agenda vazia, nada a alterar')
        nome = AppAgenda.pede_nome()
        if nulo_ou_vazio(nome):
            return
        p = self.pesquisa(nome)
        if p is not None:
            print('\nEncontrado:\n')
            AppAgenda.mostra_dados(p)
            print(f'Digite enter caso não queira alterar o nome')
            novo = AppAgenda.pede_nome()
            if not nulo_ou_vazio(novo):
                p.nome = Nome(novo)
            self.menu_telefones(p)
        else:
            print('Nome não encontrado!')
            
    def menu_telefones(self, dados):
        while True:
            print('\nEditando telefones:\n')
            AppAgenda.mostra_dados_telefone(dados)
            if len(dados.telefones) > 0:
                print('\n[A] - alterar\n[D] - apagar\n', end='')
            print('\n[N] - novo\n[S] - sair\n', end='')
            operação = input('Escolha uma operação: ')
            operação = operação.lower()
            if operação not in ['a', 'd', 'n', 's']:
                print('Operação inválida. Digite A, D, N ou S')
                continue
            if operação == 'a' and len(dados.telefones) > 0:
                self.altera_telefones(dados)
            elif operação == 'd' and len(dados.telefones) > 0:
                self.apaga_telefone(dados)
            elif operação == 'n':
                self.novo_telefone(dados)
            elif operação == 's':
                break

    def novo_telefone(self, dados):
        telefone = AppAgenda.pede_telefone()
        if nulo_ou_vazio(telefone):
            return
        if dados.pesquisaTelefone(telefone) is not None:
            print('Telefone já existe!')
        tipo = self.pede_tipo_telefone()
        dados.telefones.adiciona(Telefone(telefone, tipo))

    def apaga_telefone(self, dados):
        t = valida_faixa_inteiro_ou_branco(
            'Digite a posição do número a apagar, enter para sair: ',
            0, len(dados.telefones) - 1)
        if t is None:
            return
        dados.telefones.remove(dados.telefones[t])

    def altera_telefones(self, dados):
        t = valida_faixa_inteiro_ou_branco(
            'Digite a posição do número a alterar, enter para sair: ',
            0, len(dados.telefones) - 1)
        if t is None:
            return
        telefone = dados.telefones[t]
        print(f'Telefone: {telefone}')
        print(f'Digite enter caso não queira alterar o número')
        novotelefone = AppAgenda.pede_telefone()
        if not nulo_ou_vazio(novotelefone):
            telefone.número = novotelefone
        print('Digite enter caso não queria alterar o tipo')
        telefone.tipo = self.pede_tipo_telefone(
            self.agenda.tiposTelefone.pesquisa(telefone.tipo))
        
    def lista(self):
        print('\nAgenda')
        print('-' * 60)
        for e in self.agenda:
            AppAgenda.mostra_dados(e)
        print('-' * 60)

    def lê(self, nome_arquivo=None):
        if nome_arquivo is None:
            nome_arquivo = AppAgenda.pede_nome_arquivo()
        if nulo_ou_vazio(nome_arquivo):
            return
        with open(nome_arquivo, 'rb') as arquivo:
            self.agenda = pickle.load(arquivo)
        self.ultimo_arquivo = nome_arquivo

    def ordena(self):
        self.agenda.ordena()
        print('\nAgenda ordenada\n')

    def grava(self, nome_arquivo=None):
        if self.ultimo_arquivo is not None:
            print(f'Último arquivo utilizado foi: {self.ultimo_arquivo}')
            print('Digite enter caso queira utilizar o mesmo nome')
        nome_arquivo = AppAgenda.pede_nome_arquivo()
        if nulo_ou_vazio(nome_arquivo):
            if self.ultimo_arquivo is not None:
                nome_arquivo = self.ultimo_arquivo
            else:
                return
        with open(nome_arquivo, 'wb') as arquivo:
            pickle.dump(self.agenda, arquivo)

    def execute(self):
        self.menu.execute()


if __name__ == "__main__":
    app = AppAgenda()
    if len(sys.argv) > 1:
        app.lê(sys.argv[1])
    app.execute()