import sqlite3
import sys
from datetime import datetime
from devolucao import devolucaoentrada
from reserva import reservaentrada
from retirada import retiradaentrada

conexao = sqlite3.connect('locadora.db')

cursor = conexao.cursor()

def main():
    #MENU
    print("Seja bem vindo à 901 Locação de Veículos")
    print( 'Selecione a operação desejada:\n\
        1: Realizar Reserva\n\
        2: Realizar Retirada\n\
        3: Realizar Devolução\n\
        4: Sair\n')

    selecao = input("Operação:")

    if (selecao != '1' and selecao != '2' and selecao != '3' and selecao != '4'):
        print("Escolha a opção correta!")


    while(selecao != '4'):
        
        if(selecao) == '1':
            reservaentrada()
        elif (selecao) == '2':
            retiradaentrada()
        elif (selecao) == '3':
            devolucaoentrada()

        print("Seja bem vindo à 901 Locação de Veículos")
        print( 'Selecione a operação desejada:\n\
        1: Realizar Reserva\n\
        2: Realizar Retirada\n\
        3: Realizar Devolução\n\
        4: Sair\n')

        selecao = input("Operação:") 
        
    cursor.close()
    conexao.close()
    print("Muito obrigado por utilizar a 901 Locação de Veículos")

main()