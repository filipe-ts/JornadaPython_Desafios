import Desafio_03 as Des3
import pickle

with open('var_lista_clientes.pkl', 'rb') as vlc:
    lista_clientes = pickle.load(vlc)

Des3.PessoaFisica.atualiza_ids(lista_clientes)

menu = Des3.MenuCliente()
menu.iniciar(lista_clientes)
