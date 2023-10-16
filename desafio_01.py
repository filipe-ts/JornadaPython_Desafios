#Mensagem do menu principal
menu = """Olá, seja muito bem-vindo! Para prosseguir com seu atendimento selecione uma das operações abaixo:

[1] - Sacar

[2] - Depositar

[3] - Extrato

[4] - Encerrar atendimento

:"""

#Variaveis relacionadas a operação de saque
LIMITE_POR_SAQUE = 500
LIMITE_QUANTIDADE_SAQUES = 3
numero_saques_hoje = 0
valor_minimo = 100

#Variaveis relacionadas a operação de saldo
saldo = 1300

#Variaveis relacionadas a operação de extrato
extrato = ""

#Mensagens relacionadas a operacao de saque
mensagem_saque_insuficiente = """O seu saldo é insuficiente para prosseguir com esta operação.
Este caixa possui apenas cédula de R$ {0}.

Retornando ao menu principal.
""" #0 = valor_minimo

mensagem_saque_invalido ="""
Este valor não é adequado para prosseguir com esta operação.
Este caixa possui apenas cédula de R$ {0}.

Retornando ao menu principal.
""" #0 = valor_minimo

mensagem_saque_valido = """Favor digite o valor desejado para sacar.
Limite de R$ {1} por saque.
{2}/{3} de saques por dia realizados.
Este caixa possui apenas cédula de R$ {0}.

:"""#0 = valor_minimo; 1 = LIMITE_POR_SAQUE; 2 = numero_saques_hoje; 3 = LIMITE_QUANTIDADE_SAQUES

mensagem_saque_limites_numero_saques_execidos = """Limites de saque ultrapassados:

{0}/{1} de saques por dia realizados.

Retornando ao menu principal.
"""#0 = numero_saques_hoje; 1 = LIMITE_QUANTIDADE_SAQUES

mensagem_saque_limites_valor_saque_execidos = """Limites de saque ultrapassados:

Limite de R$ {0} por saque.

Retornando ao menu principal.
"""#0 = LIMITE_POR_SAQUE

mensagem_saque_aprovado = """Saque realizado com secusso.

Retornando ao menu principal.
"""

#Mensagens da operaçao deposito
mensagem_deposito = """
Favor digite o valor que será depositado no caixa:""" 

mensagem_deposito_negativo = """Operação Invalida.

Retornado ao menu principal.""" 

mensagem_deposito_aprovado = """Deposito realizado com secusso.

Retornando ao menu principal.
"""

#Mensagens Extrato
mensagem_extrato = """Seu extrato diário será exibido a seguir:

{}
Saldo final: R$ {:.2f}
"""

mensagem_extrato_sem_movimento = """Seu extrato diário será exibido a seguir:

Não ocorreram movimentações financeiras em sua conta hoje.

Saldo final: R$ {:.2f}
"""

#Mensagens de Operação encerramento
mensagem_encerramento = """Obrigado pela sua confiança.

Estaremos sempre a sua disposição."""

#Mensagens de Erros Menu
mensagem_opcao_invalida = "EA001: Opção inválida, fover tecle a operação desejada\n"



while (True):
    
    opcao_menu = input(menu)
    #escolhe a opçao de sacar
    if opcao_menu == "1":
        
        #Verifica se a saldo minimo
        if saldo < valor_minimo:
            print(mensagem_saque_insuficiente.format(valor_minimo)) #mensagem de erro
            continue #retorna ao menu principal
        #verifica se limite de quantidade de saquer foi atingido
        elif numero_saques_hoje >= LIMITE_QUANTIDADE_SAQUES:
            print(mensagem_saque_limites_numero_saques_execidos.format(numero_saques_hoje, LIMITE_QUANTIDADE_SAQUES))
            continue    
        else: #cliente está habilitado a sacar
            saque = input(mensagem_saque_valido.format(valor_minimo, LIMITE_POR_SAQUE, numero_saques_hoje, LIMITE_QUANTIDADE_SAQUES)) #pede o valor do saque
            saque = float(saque) #convete para número flutuante
            
            if saque > LIMITE_POR_SAQUE: #verifica o limite de valor por saque
                print(mensagem_saque_limites_valor_saque_execidos.format(LIMITE_POR_SAQUE)) #mensagem de erro
                continue #retorna ao menu principal
            elif saque%valor_minimo != 0 or saque < valor_minimo: #verifica se o valor é positivo e pode ser sacado com as cédulas disponíveis, 
                #supondo todas as cedulas de um mesmo valor
                print(mensagem_saque_invalido.format(valor_minimo)) #mensagem de erro 
                continue #retorna ao menu principal
            elif saque > saldo: #verifica se o saque é superior ao saque
                print(mensagem_saque_insuficiente.format(valor_minimo)) #mensagem de erro
                continue #retorna ao menu principal

            saldo = saldo - saque #retira o saque do saldo
            numero_saques_hoje += 1 #atualiza o numero de saques diarios
            extrato = extrato + f"Saque: - R$ {saque: .2f}\n"

            print(mensagem_saque_aprovado) #confirmaçao do saque

    elif opcao_menu == "2": #escolhe a opção de deposito
        deposito = input(mensagem_deposito) #determina valor a ser depositado
        deposito = float(deposito)
        if deposito < 0: # verificando se o deposito é positivo
            print(mensagem_deposito_negativo)
            continue

        saldo = saldo + deposito # Atualizando saldo    
        extrato = extrato + f"Deposito: + R$ {deposito: .2f}\n"

        print(mensagem_deposito_aprovado) #Confirmação de deposito

    elif opcao_menu == "3":

        if extrato != "": #verifica se ocorreram movimentações no extrato
            print(mensagem_extrato.format(extrato, saldo)) #exibe o extrato atualizado
        else:
            print(mensagem_extrato_sem_movimento.format(saldo))#exibe o extrato atualizado

    elif opcao_menu == "4":

        print(mensagem_encerramento) #mensagem de encerramento
        break

    else:
        print(mensagem_opcao_invalida) #mensagem de erro caso uma opcao nao valida seja digitada


