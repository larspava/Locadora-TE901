import sqlite3
import sys
from datetime import datetime

conexao = sqlite3.connect('locadora.db')

cursor = conexao.cursor()

def retiradaentrada():
    # login do usuario interno -----------------------------------------------------------------------
    print("Faça seu login de funcionário com e-mail e senha para efetuar a retirada do veículo:\n")
    func_email = input("E-mail: ")
    func_senha = input("Senha: ")

    login_query = """
    SELECT funcionario_nome, funcionario_id FROM funcionario 
    WHERE funcionario_email = ? AND funcionario_senha = ?;
    """
    try:
        cursor.execute(login_query, (func_email,func_senha,))
        func = cursor.fetchall()[0]
        print("Seja bem-vindo(a) " + func[0])
    except:
        print("Funcionário não cadastrado!")
        sys.exit()


    # Informe do ID da reserva e exibição do resultado
    print("Informe o ID da reserva para realizar a retirada: \n")
    id_informado = input("ID da Reserva: ")

    dados_reserva_query = """
    SELECT r.*, v.* 
    FROM reserva r
    INNER JOIN veiculo v
    ON r.veiculo_id == v.veiculo_id
    WHERE r.reserva_id == ?
    """

    cursor.execute(dados_reserva_query, (id_informado))
    result = cursor.fetchall()[0]

    print("Dados da Reserva:")
    print(f'        Veículo: {result[12]} {result[13]} \n\
            Placa: {result[11]} \n\
            Cor: {result[15]} \n\
            Ano: {result[14]} \n\
            Data de Retirada: {result[4]} \n\
            Data de Devolução: {result[5]} \n\
            Preço a pagar: R$ {result[6]}')

    # Confirmação da retirada do veículo
    confirma = input("Deseja efetuar a retirada do veículo? (S/N): ")
    if confirma == 'N':
        sys.exit()
    elif confirma == 'S':
        km = input("Informe a atual quilometragem do veículo: ")
        anomalia = input("Informe aqui alguma anomalia no veículo: ")
        dt_retirada = input("Informe a data efetiva desta retirada YYYY-MM-DD: ")

        if (dt_retirada >= result[4] and dt_retirada < result[5]):
            cursor.execute("SELECT MAX(retirada_id) FROM retirada")
            contador_retirada = cursor.fetchall()[0][0] + 1

            retirada_query = """
            INSERT INTO retirada (retirada_id, reserva_id, funcionario_id, agencia_id, retirada_data, retirada_quilometragem, retirada_anomalia)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """

            cursor.execute(retirada_query, (contador_retirada, result[0], func[1], result[3], dt_retirada, km, anomalia))
            conexao.commit()

            #Atualização na reserva --------------
            cursor.execute("UPDATE reserva SET retirada = ? WHERE reserva_id = ?", (dt_retirada, result[0]))
            conexao.commit()

            print("\n Retirada efetuada! \n")

