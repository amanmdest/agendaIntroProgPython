import os


agenda = []


def verificar_alterações(ação):
    permissão = "S"

    if ação == "leitura" and agenda:
        resposta = input(
            "Sua agenda local não foi salva, aperte 'S' para gravar ou enter para ignorar aviso."
        ).upper()        

        if resposta == 'S':
            grava()
            permissão = input("Agenda gravada, deseja fazer a leitura? (S ou N) ").upper()
    
        return permissão
    
    if ação == "gravar" and not agenda:
        permissão = input(
            "Sua agenda local está vázia. aperte qualquer tecla para cancelar ou 'E' para ignorar aviso."
        ).upper()

        permissão = "N" if permissão != 'E' else 'S'

        return permissão
    
    return permissão


def lê_última_agenda():
    global agenda
    try:
        ultimas_agendas = open("ultimas-agendas.txt", "r", encoding="utf-8")
        linhas = ultimas_agendas.readlines()
        ultima_linha = linhas[-1].strip() if linhas else ""
        print("\n"+"-"*50+f"\nÚltima agenda: {ultima_linha}")
        ultimas_agendas.close()

        if ultima_linha != "":
            ultima_agenda = open(ultima_linha, "r", encoding="utf-8")
            for l in ultima_agenda.readlines():
                nome, telefone, email, data_aniversário = l.strip().split("#")
                # agenda.append([nome, telefone, email, data_aniversário])
                # print(f"Entrada: {len(agenda)} entradas")
                mostra_dados(nome, telefone, email, data_aniversário)
                print("-"*50)

            ultima_agenda.close()

    except FileNotFoundError:
        print(f"\nNão há registros de agendas salvas.\n"+"-"*50)


def pede_nome(u='(desconhecido)'):
    while True:
        n = input("Nome: ").strip()

        if pesquisa(n) == None:
            return n if n != "" else u
        else:
            print("Nome já existe na memória! tentar um nome ainda não registrado.")


def pede_telefone(u='(desconhecido)'):
    telefones = {}
    tipos_telefone = ["fixo", "celular", "trabalho", "residência"]
    while True:
        try:
            tt = int(input(f"\n\t  [1] Fixo\n\t  [2] Celular\n\t  [3] Trabalho \
                    \n\t  [4] Residência \n\nTipo de telefone: ").strip())
            if tt < 1 or tt > 4:
                tt = "Tipo Inválido"
        except ValueError:
            tt = "Tipo Inválido"

        if tt != "Tipo Inválido":
            tt = tipos_telefone[tt-1]
            t = input(f"Telefone {tt}: ").strip()
            t = t if t != "" else u
            telefones[tt] = t
            continuar = input(
                f"Digite 'E' caso queira encerrar.\nEnter com qualquer valor para adcionar novos números. "
                ).upper()

            if continuar == "E":
                break
        else:
            print("Tente novamente.")

    return telefones


def pede_email(u='(desconhecido)'):
    email = input("Email: ").strip()
    return email if email != "" else u


def pede_data_aniversário(u='(desconhecido)'):
    dn = input("Data de Aniversário: ").strip()
    return dn if dn != "" else u


def mostra_dados(nome, telefone, email, data_aniversário):
    print(
        f"Nome: {nome} Telefone(s): {telefone}\nEmail: {email} Data de Aniversário: {data_aniversário}"
        )


def pede_nome_arquivo():
    resposta = input("Nome do arquivo: ('E' para cancelar operação) ")
    resposta = resposta if resposta != "E" else "E"

    if resposta != "E":
        return resposta 


def pesquisa(nome):
    mnome = nome.lower()
    for p, e in enumerate(agenda):
        if e[0].lower() == mnome:
            return p    
        return None


def novo():
    nome = pede_nome()
    telefone = pede_telefone()
    email = pede_email()
    data_aniversário = pede_data_aniversário()
    agenda.append([nome, telefone, email, data_aniversário])


def apaga():
    nome = pede_nome()
    p = pesquisa(nome)
    if p is not None:
        confirmação = input('Tem certeza?(S ou N) ').upper()
        if confirmação == 'S':
            del agenda[p]
            print('Dados apagados')
        elif confirmação == 'N':
            print('Operação cancelada')
    else:
        print("Nome não encontrado")


def altera():
    n = input("Nome: ").strip()
    p = pesquisa(n)
    if p is not None:
        nome = agenda[p][0]
        telefone = agenda[p][1]
        email = agenda[p][2]
        data_aniversário = agenda[p][3]
        print('Encontrado: ')
        mostra_dados(nome, telefone, email, data_aniversário)
        print("Atualizar: ")
        nome = pede_nome()
        telefone = pede_telefone()
        email = pede_email()
        data_aniversário = pede_data_aniversário()
        confirmação = input('Tem certeza?(S ou N) ').upper()
        if confirmação == 'S':
            agenda[p] = [nome, telefone, email, data_aniversário] 
            print("Alterado para: ")
            mostra_dados(nome, telefone, email, data_aniversário)
        elif confirmação == 'N':
            print('Operação cancelada')
    else:
        print('Nome não encontrado.')


def lista():
    print("\nAgenda\n\n-----")

    for p, e in enumerate(agenda):
        print(f'Entrada {p+1}')
        mostra_dados(e[0], e[1], e[2], e[3])

    print("-----\n")


def ordena_lista():
    agenda.sort()
    print("\nAgenda\n\n-----")

    for p, e in enumerate(agenda):
        print(f'Entrada {p+1}')
        mostra_dados(e[0], e[1], e[2], e[3])

    print("-----\n")


def lê():
    global agenda
    permissão = verificar_alterações("leitura")

    if permissão == "S":
        print("Leitura:\n")
        print("-----\n")
        nome_arquivo = pede_nome_arquivo()

        if nome_arquivo:
            with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
                for l in arquivo.readlines():
                    nome, telefone, email, data_aniversário = l.strip().split("#")
                    agenda.append([nome, telefone, email, data_aniversário])
                    mostra_dados(nome, telefone, email, data_aniversário)

            grava_ultima_agenda(nome_arquivo)
            agenda = []


def grava_ultima_agenda(nome_arquivo): 
    with open("ultimas-agendas.txt", "a+", encoding="utf-8") as arquivo:
        conteúdo = arquivo.readline()
        print(conteúdo)
        if conteúdo.strip() == "":
            arquivo.write(f"{nome_arquivo}")
        else:
            arquivo.write(f"\n{nome_arquivo}")



def grava():
    global agenda
    permissão = verificar_alterações("gravar")

    if permissão == "S":
        nome_arquivo = pede_nome_arquivo()

        if nome_arquivo:
            with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
                for e in agenda:
                    arquivo.write(f"{e[0]}#{e[1]}#{e[2]}#{e[3]}\n")

            grava_ultima_agenda(nome_arquivo)
            agenda = []


def valida_faixa_inteiro(pergunta, inicio, fim):
    while True:
        try:
            valor = int(input(pergunta))
            if inicio <= valor <= fim:
                return valor
        except ValueError:
            print(f"Valor inválido, favor digitar entre {inicio} e {fim}")


def menu():
    print(f'Agenda local: {len(agenda)} entradas\n'+'-'*50)
    print("""
          [1] Novo
          [2] Altera
          [3] Apaga
          [4] Lista
          [5] Pôr em Ordem Alfabética
          [6] Grava .txt 
          [7] Lê .txt 

          [0] Sai
    """)
    print('-'*50)
    return valida_faixa_inteiro('Escolha uma opção: ', 0, 7)
    
lê_última_agenda()

while True:
    opção = menu()
    if opção == 0:
        break
    elif opção == 1:
        novo()
    elif opção == 2:
        altera()
    elif opção == 3:
        apaga()
    elif opção == 4:
        lista()
    elif opção == 5:
        ordena_lista()
    elif opção == 6:
        grava()
    elif opção == 7:
        lê()
    