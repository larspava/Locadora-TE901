import sqlite3
import sys
from datetime import datetime

conexao = sqlite3.connect('locadora.db')

cursor = conexao.cursor()

def reservaentrada():
    # login do cliente externo -----------------------------------------------------------------------
    print("Faça seu login com e-mail para efetuar a reserva:\n")
    cliente_email = input("E-mail: ")
    cliente_senha = input("Senha: ")

    login_query = """
    SELECT cliente_nome, cliente_id FROM cliente 
    WHERE cliente_email = ? AND cliente_senha = ?;
    """
    try:
        cursor.execute(login_query, (cliente_email,cliente_senha,))
        cliente_info = cursor.fetchall()[0]
        print("Seja bem-vindo(a) " + cliente_info[0])
        cliente_id = cliente_info[1]
    except:
        print("Usuario nao cadastrado!")
        sys.exit()

    # Cliente seleciona data de retirada e devolucao e categoria desejada ---------------------------
    retirada_data = input("Insira a data de retirada (formato AAAA-MM-DD): ")
    devolucao_data = input("Insira a data de devolucao (formato AAAA-MM-DD): ")
    reserva_categoria = input("Insira a categoria desejada (E1, E2, E3, S1): ")

    consulta_query = """
    SELECT veiculo.veiculo_id, veiculo.veiculo_marca, veiculo.veiculo_modelo, veiculo.veiculo_cor, 
    veiculo.veiculo_ano, veiculo.veiculo_placa, veiculo.agencia_id, reserva.retirada, reserva.devolucao
    FROM veiculo 
    LEFT JOIN reserva 
    ON veiculo.veiculo_id = reserva.veiculo_id
    WHERE veiculo.categoria_id = ? AND
    (reserva.retirada IS NULL OR
    (
    (? != reserva.retirada AND ? != reserva.devolucao) AND
    (? != reserva.retirada AND ? != reserva.devolucao)
    ) AND
    (
    (? NOT BETWEEN reserva.retirada AND reserva.devolucao) AND
    (? NOT BETWEEN reserva.retirada AND reserva.devolucao)
    ) AND
    (
    (reserva.retirada NOT BETWEEN ? AND ?) AND
    (reserva.devolucao NOT BETWEEN ? AND ?)
    ))
    """
    # Exibição dos veículos disponiveis 
    cursor.execute(consulta_query, (reserva_categoria, retirada_data, devolucao_data, retirada_data, devolucao_data, retirada_data, devolucao_data, retirada_data, devolucao_data, retirada_data, devolucao_data))
    veiculos = cursor.fetchall()

    print("Veículos disponíveis: ")
    for i in range (len(veiculos)):
        print("ID: %s - Veículo %s %s, Cor: %s, Ano: %s, Placa: %s" %(veiculos[i][0],veiculos[i][1],veiculos[i][2],veiculos[i][3],veiculos[i][4],veiculos[i][5]))

    #Cliente seleciona o carro que deseja reservar pelo ID ---------------------------------------------
    cliente_escolha_id = input("Escolha pelo ID qual carro deseja reservar: ")
    for j in range (len(veiculos)):
        if int(cliente_escolha_id) == veiculos[j][0]:
            veiculo_escolhido = veiculos[j]

    #Calculo de variaveis para reserva ---------------------------------------------------------
    cursor.execute("SELECT MAX(reserva_id) FROM reserva")
    contador_reserva_id = cursor.fetchall()[0][0] + 1

    cursor.execute("SELECT categoria_preco FROM categoria WHERE categoria_id == ?", (reserva_categoria,))
    preco_categoria = cursor.fetchall()[0][0]

    d0 = datetime.strptime(retirada_data, "%Y-%m-%d")
    d1 = datetime.strptime(devolucao_data, "%Y-%m-%d")
    delta = d1.date() - d0.date()
    dias = delta.days + 1 

    preco_final = dias * preco_categoria

    #Registro na base -----------------------------------------------------------------------------
    reserva_query = """
    INSERT INTO reserva (reserva_id, veiculo_id, cliente_id, agencia_id, retirada, devolucao, reserva_preco)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """

    cursor.execute(reserva_query, (contador_reserva_id, veiculo_escolhido[0], cliente_id, veiculo_escolhido[6], retirada_data, devolucao_data, preco_final))
    conexao.commit()

    print("\n Reserva efetuada! \n")

    #cursor.close()
    #conexao.close()