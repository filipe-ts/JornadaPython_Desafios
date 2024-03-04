from abc import ABC, abstractmethod, abstractproperty
import os


class Cliente (ABC):  # classe abstrata, pois nao faria sentido poder um cliente sem um id único como CPF ou CNPJ

    _lista_ids = []  # lista para armazenar ids dos clientes

    def __init__(self, identificador_unico):  # precisa apenas de um id único para ser criado
        self._id = identificador_unico  # algo como cpf ou cnpj
        self._endereco = ""  # endereço é criado vazio, para isolar passo de verificação de id
        self._contas = []  # aloca lista de contas do cliente

    @classmethod
    def atualiza_ids(cls, lista):  # método para adicionar ids de clientes carregados de uma variável lista
        for i in range(len(lista)):  # varre a lista
            cls._lista_ids.append(lista[i]._id)  # adiciona o id de cada um

    @staticmethod  # estático, pois retorna uma String, que não está salva como atributo ou propriedade
    @abstractmethod  # abstrato, pois cada tipo de conta pode ser baseado em um id diferente
    def id_name():  # método para obter a String do tipo de ID
        return "ID"  # retorna o tipo de ID em String (algo como "CPF" ou "CNPJ")

    @classmethod
    def verificar_cadastro(cls, identificador_unico, flag=False):  # método de classe para verificar se o cliente
        # já está cadastrado
        if identificador_unico in cls._lista_ids:  # verifica se o ID está dentro da variável de classe _lista_ids
            if not flag:  # serve para não exibir mensagem quando chamando em ".acha_por_id()"
                print("Erro! Cliente já cadastrado!\n")  # se sim, exibe mensagem de erro
            return False  # e retorna False
        else:  # caso o cliente não esteja cadastrado
            return True  # retorna True

    @classmethod
    def acha_por_id(cls, identificador_unico):  # retorna a posição no vetor _lista_ids de um id
        if identificador_unico and not cls.verificar_cadastro(identificador_unico, flag=True):  # verifica se o id
            # está preenchido e está na lista
            for i in range(len(cls._lista_ids)):  # varre a lista
                if cls._lista_ids[i] == identificador_unico:  # acha o índice do id fornecido
                    return i  # retorna o índice

    @staticmethod  # estático, pois é para verificar se um id (cpf/cnpj) é válido recebendo apenas uma String
    @abstractmethod  # abstrato, pois cada tipo de conta pode ter id diferentes
    def is_id_valid(identificador_unico):  # método para verificar se o id inserido é valido, deve ter retorno Boolean
        return True  # se válido retorna True (e se não válido deve retorna False)

    @classmethod  # método de classe para criar nova instância
    def cadastrar_cliente(cls, identificador_unico, **kwargs):  # recebe apenas o id como argumento
        valid_id = cls.is_id_valid(identificador_unico)  # salva se o id fornecido é válido ou não
        # utiliza o método estático ".is_id_valid()" para fazer a verificação
        if valid_id:  # se o id for válido
            cliente_cadastrado = cls.verificar_cadastro(identificador_unico)  # salva se o id já está cadastrado
            # utiliza o método de classe ".verificar_cadastro()" para fazer essa verificação
            if cliente_cadastrado:  # se o cliente não estiver cadastrado
                cls._lista_ids.append(identificador_unico)  # adiciona o id ao atributo de classe "._lista_ids"
                novo_cliente = cls(identificador_unico)  # instância um objeto da classe
                novo_cliente.completar_cadastro(**kwargs)  # chama o método ".completar_cadastro()" para preencher
                # outros atributos desejáveis para a conta (Nome, endereço, data de nascimento, estado civil etc)
                print("Cliente cadastrado com sucesso!\n")  # exibe mensagem de sucesso
                return novo_cliente  # retorna a nova instância criada
            else:  # se o cliente já estiver cadastrado
                return  # não retorna objeto tipo Cliente
        else:
            return  # não retorna objeto tipo Cliente

    @classmethod  # método para cadastra cliente via

    def cadastrar_endereco(self, novo_endereco=""):  # método para atualizar ou cadastrar o endereço do usuário
        if novo_endereco != "":  # verifica se alguma string foi fornecida
            self._endereco = novo_endereco  # caso positivo é alocada direto no endereço
        else:  # caso contrário exibe comando e recebe entrada do usuário
            novo_endereco = input("Insira o endereço do cliente no padrão:\n"
                                  "Logradouro, 123 - Bairro - Cidade/SIGLA DO ESTADO\n"
                                  "==> ")
            self._endereco = novo_endereco  # registra o endereço no atributo privado _endereco
            print("Endereço cadastrado/atualizado com sucesso!\n")  # exibe mensagem de sucesso

    @abstractmethod  # abstrato, pois cada tipo de conta pode ter atributos diferentes
    def completar_cadastro(self, **kwargs):  # atua sobre uma instância apenas
        # deve chamar métodos como ".cadastrar_endereco()" para completar todos os dados do cliente
        pass  # o corpo deve ser feito em cada classe filha

    def realizar_transacao(self, conta, transacao):  # método para solicitar transação
        if conta in self._contas:  # se a conta passada pertencer ao cliente o código prossegue
            transacao.registrar(conta)  # ativa o método para realizar e registrar a transação na conta do cliente
        else:  # caso contrário, exibe erro
            print("Este usuário não tem acesso a esta conta!\n")

    def adicionar_conta(self, nova_conta):  # método para adicionar nova conta ao atributo privado _contas[]
        self._contas.append(nova_conta)  # adiciona a conta recebida na lista

    def selecionar_conta(self):  # método para selecionar a conta que o cliente realizará as operações
        if len(self._contas) == 0:  # caso o cliente não possua contas cadastradas
            print("Cliente não possui contas cadastradas!\n")  # exibe mensagem de erro e retorna False
            return False
        elif len(self._contas) == 1:  # caso o cliente possua apenas uma conta cadastradas
            print(f"Conta: {self._contas[0]} selecionada.\n")  # é exibido que a conta foi selecionada
            return self._contas[0]  # conta única selecionada automaticamente
        elif len(self._contas) > 1:  # caso o cliente possua mais de uma conta cadastradas
            print("Selecione qual conta deseja acessar:\n")  # exibe comando para selecionar a conta desejada
            entradas_validas = []  # aloca lista para inputs válidos do usuário
            for i in range(len(self._contas)):  # laço para exibir as contas e a respectiva entrada do usuário
                print(f"[{i+1}] - Conta: {self._contas[i]}\n")  # exibi opção
                entradas_validas.append(str(i+1))  # adiciona valores de entrada de usuário válidas
            entrada_usuario = input("==>  ")  # indicativo para entrada do usuário
            while True:  # laço que se perpetua até receber uma entrada de usuário válida
                if entrada_usuario in entradas_validas:  # verifica se a entrada está dentro dos valores válidos
                    print(f"Conta: {self._contas[int(entrada_usuario)-1]} selecionada.\n")  # se sim exibe conta
                    return self._contas[int(entrada_usuario)-1]  # retorna a conta selecionada
                else:  # caso não haja entrada válida, exibe mensagem de erro e solicita nova entrada
                    print("Opção inválida, tente novamente!\n")  # exibe mensagem de erro
                    entrada_usuario = input("==>  ")  # indicativo de entrada de usuário


class PessoaFisica (Cliente):
    def __init__(self, identificador_unico):
        super().__init__(identificador_unico)
        self._nome = ""
        self._data_nascimento = ""

    @staticmethod  # estático, pois retorna uma String, que não está salva como atributo ou propriedade
    def id_name():  # método para obter a String do tipo de ID
        return "CPF"  # retorna o tipo de ID em String (no caso de pessoa física: "CPF")

    @staticmethod  # estático, pois é para verificar se um id (cpf/cnpj) é válido recebendo apenas uma String
    def is_id_valid(identificador_unico):  # método para verificar se o CPF inserido é valido, deve ter retorno Boolean
        if len(identificador_unico) == 11:  # verifica se o cpf tem 11 dígitos
            digitos = []  # cria lista para receber os 10 primeiros dígitos do cpf
            verificador = []  # cria lista para receber os dois dígitos verificadores

            for i in range(11):  # laço para registrar dígitos nos dois vetores anteriores
                digito = int(identificador_unico[i])  # converte o digito de String para Int
                if i < 9:  # até antes do décimo dígito
                    digitos.append(digito)  # são alocados em ordem em digitos[]
                elif i == 9:  # se for o décimo dígito
                    digitos.append(digito)  # alocado em digitos[]
                    verificador.append(digito)  # e também alocado em verficador[]
                elif i == 10:  # se for o último (11o) dígito
                    verificador.append(digito)  # aloca em verificador[]

            verificacao_primeiro_digito = 0  # aloca soma para verificar o primeiro dígito
            verificacao_segundo_digito = 0  # aloca soma para verificar o segundo dígito

            for i in range(10):  # laço para percorrer os 10 primeiros dígitos
                if i < 9:  # até o nono dígito
                    verificacao_primeiro_digito += digitos[i] * (i+1)  # sempre adiciona multiplicação ao verificador do
                    # primeiro dígito, o fator de multiplicação deve ser 1 para 1.º, 2 para 2.º, 3 para 3.º....
                verificacao_segundo_digito += digitos[i] * i  # sempre adiciona multiplicação ao verificador do segundo
                # dígito, o fator de multiplicação deve ser 0 para 1.º, 1 para 2.º, 2 para 3.º....

            verificacao_primeiro_digito = verificacao_primeiro_digito % 11  # pega o resto da divisão por onze
            verificacao_segundo_digito = verificacao_segundo_digito % 11  # pega o resto da divisão por onze

            if verificacao_primeiro_digito == 10:  # se o resto da divisão for dez, deve-se substituir por zero
                verificacao_primeiro_digito = 0  # substitui por zero

            if verificacao_segundo_digito == 10:  # se o resto da divisão for dez, deve-se substituir por zero
                verificacao_segundo_digito = 0  # substitui por zero

            if (verificacao_primeiro_digito == verificador[0]) and (verificacao_segundo_digito == verificador[1]):  # se
                # ambos os verificadores forem iguais aos dígitos de verificação o CPF é válido
                print("CPF validado com sucesso!\n")  # exibe mensagem de sucesso
                return True  # retorna True
            else:  # se pelo menos um for diferente
                print("Erro! O CPF fornecido não é válido!\n")  # exibe mensagem de erro
                return False  # retorna False
        else:  # caso a String fornecida não possui 11 caracteres
            print("Erro! O CPF deve possuir 11 dígitos. Escreva apenas números.\n")  # exibe mensagem de erro
            return False  # retorna False)

    def cadastrar_nome(self, novo_nome=""):  # método para cadastrar/alterar nome
        if novo_nome != "":  # verifica se alguma string foi fornecida
            self._nome = novo_nome  # caso positivo é alocada direto no endereço
        else:  # caso contrário exibe comando e recebe entrada do usuário
            novo_nome = input("Insira o nome do cliente\n"
                              "==> ")
            self._nome = novo_nome  # registra o nome no atributo privado _nome
            print("Nome cadastrado/atualizado com sucesso!\n")  # exibe mensagem de sucesso

    def cadastrar_data_nascimento(self, nova_data=""):  # método para cadastrar/alterar nome
        if nova_data != "":  # verifica se alguma string foi fornecida
            self._data_nascimento = nova_data  # caso positivo é alocada direto no endereço
        else:  # caso contrário exibe comando e recebe entrada do usuário
            nova_data = input("Insira a data de nascimento do cliente:\n"
                              "DD/MM/AAAA"
                              "==> ")
            self._data_nascimento = nova_data  # registra a data no atributo privado _data_nascimento
            print("Data de nascimento cadastrada/atualizada com sucesso!\n")  # exibe mensagem de sucesso

    def completar_cadastro(self, **kwargs):  # preenche os dados restantes do cliente, se forem fornecidos devem ser
        # nomeados, "Nome", "Data_de_nascimento", "Endereço". Caso algum não seja fornecido, será pedido que o usuário
        # os insira
        if kwargs:  # verifica se existe alguma chave fornecida
            for key in kwargs:  # varre as chaves do dicionário gerado por **kwargs
                if key == "Nome":  # se a chave for "Nome"
                    self.cadastrar_nome(kwargs["Nome"])  # chama o método ".cadastrar_nome()" e passa o valor como argu-
                    # mento
                elif key == "Data_de_nascimento":  # se a chave for "Data_de_nascimento"
                    self.cadastrar_data_nascimento(kwargs["Data_de_nascimento"])  # chama o método
                    # ".cadastrar_data_nascimento()" e passa o valor como argumento
                elif key == "Endereço":  # se a chave for "Endereço"
                    self.cadastrar_endereco(kwargs["Endereço"])  # chama o método ".cadastrar_endereco()" e passa o
                    # valor como argumento
            # o bloco a seguir serve para verificar se alguma chave não foi passada, caso isso aconteça, o respectivo
            # método é chamado
            if self._nome == "":  # se ._nome não foi preenchido
                self.cadastrar_nome()  # chama o método ".cadastrar_nome()" sem argumento, que irá pedir input
                # do usuário
            if self._data_nascimento == "":  # se ._data_nascimento não foi preenchido
                self.cadastrar_data_nascimento()  # chama o método ".cadastrar_data_nascimento()" sem argumento, que irá
                # pedir input do usuário
            if self._endereco == "":  # se ._endereco não foi preenchido
                self.cadastrar_endereco()  # chama o método ".cadastrar_endereco()" sem argumento, que irá pedir input
                # do usuário
        else:  # se nenhuma chave for fornecida, as funções são chamadas sem argumentos
            self.cadastrar_nome()  # chama o método ".cadastrar_nome()" sem argumento, que irá pedir input do usuário
            self.cadastrar_data_nascimento()  # chama o método ".cadastrar_data_nascimento()" sem argumento, que irá
            # pedir input do usuário
            self.cadastrar_endereco()  # chama o método ".cadastrar_endereco()" sem argumento, que irá pedir input
            # do usuário

    def __str__(self):  # cria versão String do tipo ContaCorrente
        return f"{self._nome} - CPF: {self._id} - DN: {self._data_nascimento} - Endereço: {self._endereco}"


class Transacao(ABC):  # classe abstrata para transações
    def __init__(self, quantidade):  # recebe quantidade em dinheiro como atributo
        self._quantidade = quantidade

    def registrar(self, conta):  # utiliza método do objeto do tipo Conta para adicionar transação ao histórico da conta
        conta.atualiza_historico(self)

    @abstractmethod  # necessário redefinir aparência quando exibido em texto, o objetivo final
    def __str__(self):
        pass


class Deposito(Transacao):  # cria a transação do tipo Depósito

    def registrar(self, conta):  # sobrescreve método abstrato para adicionar operação de depósito na conta
        validacao_trasacao = conta.deposito(self._quantidade)  # verifica resultado, True se for bem-sucedido
        if validacao_trasacao:  # caso a transação seja bem-sucedida o método segue o padrão da classe pai
            super().registrar(conta)  # mantém comportamento do método pai (adicionar transação ao histórico da conta)

    def __str__(self):  # define o método obrigatório de converter para String
        exibicao = f"Depósito\t\t + R${self._quantidade:.2f}"  # String padrao: Depósito  + R$xx.xx
        return exibicao  # retorna String


class Saque(Transacao):  # cria a transação do tipo Saque

    def registrar(self, conta):  # sobrescreve método abstrato para adicionar operação de depósito na conta
        validacao_trasacao = conta.saque(self._quantidade)  # verifica resultado, True se for bem-sucedido
        if validacao_trasacao:  # caso a transação seja bem-sucedida o método segue o padrão da classe pai
            super().registrar(conta)  # mantém comportamento do método pai (adicionar transação ao histórico da conta)

    def __str__(self):  # define o método obrigatório de converter para String
        exibicao = f"{self.__class__.__name__}\t\t\t - R${self._quantidade:.2f}"  # String padrao: Saque  - R$xx.xx
        return exibicao  # retorna String


class Historico:
    def __init__(self):
        self._log_original = "Nenhuma transação realizada\n"
        self._log = ""

    def adicionar_transacao(self, transacao):  # adiciona transações a _log
        self._log += str(transacao) + "\n"

    def __str__(self):
        # gera mensagem com o _log caso este não esteja vazio, caso contrário gera com _log_original
        exibicao = f"Histórico de transações:\n\n{self._log if self._log else self._log_original}"
        return exibicao  # retorna String


class Conta:  # classe Conta
    def __init__(self, cliente, numero_conta):
        self._saldo = 0.0  # toda conta nova é gerada sem saldo
        self._agencia = "0001"  # número da agencia padrão
        self._historico = Historico()  # cria-se um novo objeto histório em branco
        self._numero_conta = numero_conta  # Número da conta - Definido pelo Gerenciador/Menu
        self._cliente = cliente  # recebe um objeto cliente para representar o proprietário

    def exibe_saldo(self):  # nome auto-explicativo
        print(f"Saldo da conta:\t R${self._saldo:.2f}\n")  # exibe com precisão de duas casas após o ponto

    def saque(self, quantidade):  # nome auto-explicativo
        if quantidade <= 0:  # verifica se o valor fornecido é positivo
            print("O valor inserido é inválido!\n")  # exibe na tela o motivo do erro
            return False  # encerra o método e retorna número do erro
        elif quantidade > self._saldo:  # verifica se o saldo é suficiente
            print("Saldo insuficiente!\n")  # exibe na tela o motivo do erro
            return False  # encerra o método e retorna número do erro
        else:  # caso não haja inconsistências prossegue para a operação em si
            print("Saque realizado com sucesso!\n")  # exibe mensagem de sucesso na operação
            self._saldo -= quantidade  # atualiza o saldo subtraindo o valor desejado
            return True  # encerra o método e retorna sem erros

    def deposito(self, quantidade):  # nome auto-explicativo
        if quantidade <= 0:  # verifica se o valor fornecido é positivo
            print("O valor inserido é inválido!\n")  # exibe na tela o motivo do erro
            return False  # encerra o método e retorna número do erro
        else:  # caso não haja inconsistências prossegue para a operação em si
            self._saldo += quantidade  # atualiza o saldo somando o valor desejado
            print("Depósito realizado com sucesso!\n")  # exibe mensagem de sucesso na operação
            return True  # encerra o método e retorna sem erros

    def exibir_historico(self):  # método para exibição do histórico
        print(self._historico)  # exibe histórico de transações
        self.exibe_saldo()  # exibe saldo no final do histórico

    def atualiza_historico(self, trasacao):  # método para adicionar nova transação
        self._historico.adicionar_transacao(trasacao)  # utiliza o método ".adicionar_transacao" da classe Historico
        # para incorporar transação no historio local

    @property  # propriedade para obter o parâmetro privado _numero_conta
    def numero_conta(self):
        return self._numero_conta  # retorna o número da conta

    @classmethod  # método de classe para gerar um novo objeto do tipo Conta
    def nova_conta(cls, cliente, numero_conta):
        nova_conta = cls(cliente, numero_conta)  # utiliza o construtor
        return nova_conta  # retorna objeto Conta

    def __str__(self):  # refaz o método __str__
        return f"{self._agencia}-{self.numero_conta}"  # retorna numero da agência e número da conta


class ContaCorrente(Conta):  # cria classe Conta Corrente da classe pai Conta
    def __init__(self, cliente, numero_conta):  # mantém o mesmo construtor
        super().__init__(cliente, numero_conta)  # mantém o mesmo construtor
        self._limite_por_saque = 500.00  # adiciona quantidade limite de saque
        self._limite_quantidade_saque = 3  # adiciona limite de saques por acesso (simulando limite de saques diário)
        self._contador_saque = 0  # adiciona contador de saques

    def saque(self, quantidade):  # sobrescreve método .sacar() para se adequar a novos limites
        if self._contador_saque >= self._limite_quantidade_saque:  # verifica se há saques disponíveis
            print("Limites de saques atingido!\n")
            print(f"Quantidade de saques realizados: [{self._contador_saque}]/[{self._limite_quantidade_saque}]\n")
            return False  # em caso negativo exibe quantidade de saques, mensagem de erro e retorna False
        elif quantidade > self._limite_por_saque:  # verifica se o valor está dentro do limite por saque
            print(f"Operação não autorizada! Limite por saque: R${self._limite_por_saque:.2f}\n")  # exbibe erro
            return False  # retorna False
        else:  # caso contrario executa método da classe pai
            if super().saque(quantidade):  # se o método da classe pai retorna True ele prossegue
                self._contador_saque += 1  # adiciona um saque ao contador de saques
                print(  # exibe quantidade de saques realizados
                    f"Quantidade de saques realizados: [{self._contador_saque}]/[{self._limite_quantidade_saque}]\n")
                return True
            else:  # caso o método pai retorne falso
                return False  # o método do filho também retorna False


class Menu(ABC):  # classa abstrata para servir de base aos menus

    def __init__(self):
        self._input_voltar = "v"  # valor padrão para voltar ao menu anterior
        self._opcao_voltar = "Voltar ao menu anterior"  # Descrição da opção voltar
        self._input_sair = "x"  # valor padrão para fechar programa
        self._opcao_sair = "Sair do programa"  # Descrição da opção voltar
        self._inputs_validos = [self._input_voltar, self._input_sair]  # vetor de opções que o usuário pode digitar
        # para gerar uma ação
        self._string_opcoes = [self._opcao_voltar, self._opcao_sair]  # vetor de descrições das opções do usuário
        self._vetor_acao = [self.voltar, self.sair]  # aloca os métodos para cada opção, exceto "voltar"
        self._voltar_menu = False  # controle de retorno para o menu anterior

    @staticmethod
    def sair(obj):  # apelido para fechar programa
        exit()

    def voltar(self, obj):  # troca a indicação para permitir volta ao menu anterior
        self._voltar_menu = True  # padrão é False, na criação do objeto e no método ".iniciar()"

    def remover_opcoes(self, *args):  # remove opções do menu - Necessário que todas as que forem removidas
        # de fato estejam entre as opções
        for i in range(len(args)):  # percorre as opções que se deseja remover
            remover_index = self._inputs_validos.index(args[i])  # acha o índice que a opção se encontra
            self._string_opcoes.pop(remover_index)  # remove-se o índice das descrições
            self._inputs_validos.pop(remover_index)  # remove-se o índice das entradas válidas do usuário
            self._vetor_acao.pop(remover_index)  # remove-se a ação associada do vetor de ações

    def adicionar_opcoes(self, *args):  # adiciona opções ao menu, as entradas devem vir antes de sua
        # respectiva descrição
        novas_entradas = []  # aloca vetor para novas entradas
        novas_strings = []  # aloca vetor para novas descrições
        for i in range(0, len(args), 2):  # percorre as opções fornecidas pulando as descrições
            novas_entradas.append(args[i])  # adiciona nova entrada
            novas_strings.append(args[i+1])  # adiciona nova descrição
        novas_strings.extend(self._string_opcoes)  # adiciona entradas já existentes
        novas_entradas.extend(self._inputs_validos)  # adiciona descrições já existentes
        self._string_opcoes = novas_strings.copy()  # sobrescreve as opções de entrada com o novo conjunto
        self._inputs_validos = novas_entradas.copy()  # sobrescreve as descrições de entrada com o novo conjunto

    def adicionar_acoes(self, *args):  # adiciona acoes ao menu, fornecer métodos sem os "()"
        novas_acoes = []  # aloca vetor para novas acoes
        for i in range(0, len(args)):  # percorre as acoes fornecidas
            novas_acoes.append(args[i])  # adiciona nova acao
        novas_acoes.extend(self._vetor_acao)  # adiciona acoes já existentes
        self._vetor_acao = novas_acoes.copy()  # sobrescreve as opções de entrada com o novo conjunto

    @property  # propriedade devolve a quantidade de opções no menu
    def len_opcoes(self):
        return len(self._inputs_validos)

    def mostrar_opcoes(self):  # método para mostrar as opções disponíveis no menu
        for i in range(self.len_opcoes):  # para cada opção no menu
            print(f"[{self._inputs_validos[i]}] - {self._string_opcoes[i]}")
            # exibi algo como "[A] - Ação"

    def iniciar(self, obj=None):  # método para executar menu
        self._voltar_menu = False  # define que não quer voltar ao menu anterior
        while not self._voltar_menu:  # verdadeiro enquanto .voltar() não for chamado
            self.mostrar_opcoes()  # mostra opções
            entrada_usuario = input("==> ")  # indicativo de entrada do usuário
            for i in range(self.len_opcoes):  # varre todas as opções
                if entrada_usuario == self._inputs_validos[i]: # verifica qual entrada o usuário escolheu
                    self._vetor_acao[i](obj)  # chama a propriedade correspondente a opção


class MenuCliente(Menu):

    def __init__(self):
        super().__init__()  # inicia os mesmos atributos da classe superior
        self._input_selecionar = "1"  # opção de entrada para selecionar cliente
        self._string_selecionar = "Selecionar cliente"  # descrição da opção para selecionar cliente
        self._input_cadastrar = "2"  # opção de entrada para cadastrar novo cliente
        self._string_cadastrar = "Cadastrar novo cliente"  # descrição da opção para cadastrar novo cliente
        super().remover_opcoes("v")  # por ser o menu inicial, removemos a opção de voltar ao menu anterior
        super().adicionar_opcoes(self._input_selecionar, self._string_selecionar,  # adiciona as novas opções
                                 self._input_cadastrar, self._string_cadastrar)          # ao menu
        super().adicionar_acoes(self.selecionar_cadastro, self.adicionar_cadastro)  # adiciona acoes do método ao
        # ._vetor_acao

    @staticmethod
    def selecionar_cadastro(lista_clientes):  # exibi lista de clientes para a escolha
        if lista_clientes:  # caso haja clientes na lista
            for cliente in lista_clientes:  # varre toda a lista
                print(f"{cliente}")  # exibe cada cliente da lista
            print()  # exibe linha em branco
            entrada_usuario = input("Digite o CPF do cliente que deseja acessar ou [v] para voltar.\n==> ")
            # indicativo de entrada de usuário
            if entrada_usuario == "v":  # hard code para voltar
                return
            index = PessoaFisica.acha_por_id(entrada_usuario)  # retorna o index do cliente na lista
            if index is not None:  # caso o cliente esteja na lista
                print(f"Cliente selecionado:\n{lista_clientes[index].__str__()}\n")  # exibe qual o
                # cliente foi selecionado
                menu_conta = MenuConta()  # instância um menu de contas
                menu_conta.iniciar(lista_clientes[index])  # inicia o menu passando o cliente desejado
                # como argumento
            else:  # caso o cliente não esteja na lista ou ceja digito um cpf errado
                print("CPF inválido! Tente novamente.\n")  # exibe erro
        else:  # caso não haja cliente na lista
            print("Não há clientes cadastrados!\n")  # exibe erro

    @staticmethod
    def adicionar_cadastro(lista_clientes):
        entrada_usuario = input("Favor forneça o CPF do cliente (apenas números):\n==> ")
        lista_clientes.append(PessoaFisica.cadastrar_cliente(entrada_usuario))

    # @property
    # def vetor_acao(self):
    #     return self.vetor_acao
    #
    # @vetor_acao.setter  # setter do .vetor_acao
    # def vetor_acao(self, *args):  # recebe outras propriedades/ lambdas
    #     for i in range(len(args)):  # para cada propriedade fornecida
    #         self.vetor_acao.append(args[i])  # aloca no .vetor_acao


class MenuConta(Menu):

    _numero_das_contas = [1, 2, 3, 4, 5, 6, 7]  # lista para armazenar números de contas utilizados.
    # tem o hard code na inicialização para as contas criadas para o teste

    def __init__(self):
        super().__init__() # inicia os mesmos atributos da classe superior
        self._input_selecionar = "1"  # opção de entrada para selecionar conta
        self._string_selecionar = "Selecionar conta"  # descrição da opção para selecionar conta
        self._input_cadastrar = "2"  # opção de entrada para cadastrar nova conta
        self._string_cadastrar = "Criar nova conta"  # descrição da opção para cadastrar nova conta
        super().adicionar_opcoes(self._input_selecionar, self._string_selecionar,  # adiciona as novas opções
                                 self._input_cadastrar, self._string_cadastrar)  # ao menu
        super().adicionar_acoes(self.selecionar_conta, self.chama_adicionar_conta)  # adiciona acoes do método ao
        # vetor_acao

    @classmethod
    def _proximo_novo_numero(cls):  # método para gerar próximo número de conta
        if not cls._numero_das_contas:  # caso não haja nada na lista de números utilizados
            return 1  # retorna 1
        else:  # caso haja algum número na lista
            novo_numero = 1  # instancia o novo numero a ser adicionado
            while True:  # sempre verdadeiro, roda até retornar
                if novo_numero in cls._numero_das_contas:  # se o novo número estiver na lista
                    novo_numero += 1  # muda o número para o próximo inteiro
                else:  # caso não esteja na lista
                    cls._numero_das_contas.append(novo_numero)  # adiciona novo número na lista de utilizados
                    return novo_numero  # retorna o novo número

    @staticmethod
    def chama_adicionar_conta(cliente):  # método para opção de criar nova conta
        novo_numero = MenuConta._proximo_novo_numero()  # gera novo número de conta
        nova_conta = ContaCorrente(cliente, novo_numero)  # cria objeto do tipo conta corrente
        cliente.adicionar_conta(nova_conta)  # adiciona a nova conta corrente ao objeto cliente
        print(f"Conta {nova_conta} criada!\n")  # exibe confirmação na tela e número da nova conta

    @staticmethod
    def selecionar_conta(cliente):  # menu para selecionar entre as contas de um cliente
        conta_selecionada = cliente.selecionar_conta()  # amazena a conta selecionada
        entrada_usuario = input(f"Deseja prosseguir com a conta {conta_selecionada}?\n"
                                "[c] - Continuar\n"
                                "[v] - Voltar ao menu anterior\n"
                                f"==> ")
        # exibe mensagem com conta selecionada e indicativo de entrada para voltar ou continuar
        if entrada_usuario == "v":  # hard code para voltar
            return  # encerra método
        elif entrada_usuario == "c":  # hard code para continuar
            cliente_conta = [cliente, conta_selecionada]  # armazena o cliente e a conta selecionada numa lista
            menu_operacao_conta = MenuOperacaoConta()  # instancia menu de operação de conta
            menu_operacao_conta.iniciar(cliente_conta)  # passa lista cliente_conta como argumento
        else:  # entrada diferente das sugeridas
            print("Opção inválida! Retornando ao menu anterior.\n")  # exibe mensagem erro
            return  # encerra método


class MenuOperacaoConta(Menu):
    def __init__(self):
        super().__init__()
        self._input_extrato = "1"  # opção de entrada ver extrato
        self._string_extrato = "Extrato"  # descrição da opção de ver extrato
        self._input_deposito = "2"  # opção de entrada para depositar
        self._string_deposito = "Depósito"  # descrição da opção de depositar
        self._input_saque = "3"  # opção de entrada para sacar
        self._string_saque = "Saque"  # descrição da opção de sacar
        super().adicionar_opcoes(self._input_extrato, self._string_extrato,  # adiciona as novas opções
                                 self._input_deposito, self._string_deposito,
                                 self._input_saque, self._string_saque)  # ao menu
        super().adicionar_acoes(self.chamar_historico, self.chamar_deposito, self.chamar_saque)  # adiciona acoes do método ao

    @staticmethod
    def chamar_historico(cliente_conta):  # método para exibir o histórico da conta (extrato)
        cliente = cliente_conta[0]  # armazena apenas o cliente
        conta = cliente_conta[1]  # armazena apenas a conta
        conta.exibir_historico()  # chama o método .exibir_historico() para exibir extrato na tela

    @staticmethod
    def chamar_deposito(cliente_conta):  # método para chamar operação de depósito
        cliente = cliente_conta[0]  # armazena apenas o cliente
        conta = cliente_conta[1]  # armazena apenas a conta
        entrada_usuario = input("Quanto deseja deposita?\n"
                                "==> R$ ")
        deposito = Deposito(float(entrada_usuario))  # cria objeto de depósito
        cliente.realizar_transacao(conta, deposito)  # tenta realizar depósito

    @staticmethod
    def chamar_saque(cliente_conta):  # método para chamar operação de depósito
        cliente = cliente_conta[0]  # armazena apenas o cliente
        conta = cliente_conta[1]  # armazena apenas a conta
        entrada_usuario = input("Quanto deseja sacar?\n"
                                "==> R$ ")
        deposito = Saque(float(entrada_usuario))  # cria objeto de depósito
        cliente.realizar_transacao(conta, deposito)  # tenta realizar depósito




# lista_clientes = []
#
# maria = PessoaFisica.cadastrar_cliente("16305086087", Nome="Maria", Data_de_nascimento="02/02/1991", Endereço="Marginal Tiete")
# conta1 = ContaCorrente.nova_conta(maria, 1)
# conta2 = ContaCorrente.nova_conta(maria, 2)
# maria.adicionar_conta(conta1)
# maria.adicionar_conta(conta2)
# maria._contas[0]._saldo = 1000.0
# maria._contas[1]._saldo = 2350.0
#
# joao = PessoaFisica.cadastrar_cliente("55785048094", Nome="João", Data_de_nascimento="01/01/1990", Endereço="Avina Paulista")
# conta3 = ContaCorrente.nova_conta(joao, 3)
# conta4 = ContaCorrente.nova_conta(joao, 4)
# conta5 = ContaCorrente.nova_conta(joao, 5)
# joao.adicionar_conta(conta3)
# joao.adicionar_conta(conta4)
# joao.adicionar_conta(conta5)
# joao._contas[0]._saldo = 10000.0
# joao._contas[1]._saldo = 7500.0
# joao._contas[2]._saldo = 5000.0
#
#
# marcos = PessoaFisica.cadastrar_cliente("24695708086", Nome="Marcos", Data_de_nascimento="03/03/1993", Endereço="Av. Bandeirantes")
# conta6 = ContaCorrente.nova_conta(marcos, 6)
# marcos.adicionar_conta(conta6)
# marcos._contas[0]._saldo = 680.0
#
# amanda = PessoaFisica.cadastrar_cliente("61220410098", Nome="Amanda", Data_de_nascimento="04/04/1994", Endereço="Av. Inter Lagos")
# conta7 = ContaCorrente.nova_conta(marcos, 7)
# amanda.adicionar_conta(conta7)
# amanda._contas[0]._saldo = 450.0
#
#
# lista_clientes.extend([maria, joao, marcos, amanda])

# menu_cliente = MenuCliente()
# menu_cliente.iniciar(lista_clientes)




