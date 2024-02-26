menu = """

[cu] Criar Usuário
[cc] Criar Conta
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 1200
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

USUARIO_PADRAO = {"Nome": "Não cadastrado", "Data de nascimento": "DD/MM/AAAA", "CPF": "0123456789", "Endereço": "Rua dos Bobos, 0 - Imaginação - Rio de Janeiro/RJ"}
filipe = {"Nome": "Filipe", "Data de nascimento": "01/01/1995", "CPF": "08396247342", "Endereço": "Rua dos Bobos, 0 - Imaginação - Rio de Janeiro/RJ"}
usuarios = [filipe]
cpfs_cadastrados = [filipe["CPF"]]

CONTA_PADRAO = {"Agencia": "0001", "Conta": 0, "Proprietário": "0123456789"}
contas_cadastradas = []

def saque(*, saldo, numero_saques, LIMITE_SAQUES=LIMITE_SAQUES, limite, extrato):
    if numero_saques >= LIMITE_SAQUES:
        print("Operação falhou! Número máximo de saques excedido.")
    else:

        valor = float(input("Informe o valor do saque: "))

        if valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
        elif valor > limite:
            print("Operação falhou! O valor do saque excede o limite.")
        else:
            saldo = saldo - valor
            extrato = extrato + f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            print("Saque realizado!")

    return saldo, extrato, numero_saques


def deposito(saldo, extrato, /):
    valor = float(input("Informe o valor do depósito: "))

    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("Deposito realizado!")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato


def exibir_extrato(extrato, /, *, saldo,):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_usuario():
    novo_usuario = USUARIO_PADRAO.copy()

    novo_usuario["CPF"] = input("Digite o do novo usuário CPF (apenas números)\n==> ")
    if novo_usuario["CPF"] in cpfs_cadastrados:
        print("Operação cancelada, usuário já cadastrado")
        return
    elif len(novo_usuario["CPF"]) != 11:
        print("Operação cancelada, CPF inválido")
        return
    else:
        novo_usuario["Nome"] = input("\nDigite o nome do novo usuário\n==> ")
        novo_usuario["Data de nascimento"] = input("\nDigite a data de nascimento (DD/MM/AAA)\n==> ")
        novo_usuario["Endereco"] = input("\nDigite o endereço (Logradouro, Numero - Bairro - Cidade/Sigla estado)\n==> ")
        usuarios.append(novo_usuario.copy())
        cpfs_cadastrados.append(novo_usuario["CPF"])

        print("\nUsuário cadastrado com sucesso")

def criar_conta():
    cpf = input("Digite o CPF (apenas números) do proprietário\n==> ")
    if cpf not in cpfs_cadastrados:
        print("Operação cancelada, usuário não cadastrado")
        return
    elif len(cpf) != 11:
        print("Operação cancelada, CPF inválido")
        return
    else:
        if len(contas_cadastradas) == 0:
            numero_conta = 1
        else:
            numero_conta = contas_cadastradas[-1]["Conta"] + 1
        nova_conta = CONTA_PADRAO.copy()
        nova_conta["Conta"] = numero_conta
        nova_conta["Proprietário"] = cpf
        contas_cadastradas.append(nova_conta)

        print("\nConta 0001-{} com sucesso".format(numero_conta))

while True:

    opcao = input(menu)

    if opcao == "d":
        saldo, extrato = deposito(saldo, extrato)

    elif opcao == "s":
        saldo, extrato, numero_saques = saque(saldo=saldo, numero_saques=numero_saques, limite=limite, extrato=extrato)

    elif opcao == "e":
        exibir_extrato(extrato, saldo=saldo)

    elif opcao == "cu":
        criar_usuario()

    elif opcao == "cc":
        criar_conta()

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
