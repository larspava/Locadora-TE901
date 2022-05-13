import sqlite3
import sys
from datetime import datetime

conexao = sqlite3.connect('locadora.db')

cursor = conexao.cursor()

def devolucaoentrada():
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
    print("Informe o ID da reserva para realizar a devolução: \n")
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


    # Confirmação da devolução do veículo
    confirma = input("Deseja efetuar a devolucao do veículo? (S/N): ")
    if confirma != 'S':
        sys.exit()

    km = input("Informe a atual quilometragem do veículo: ")
    avaria_in = input("O veículo possui alguma avaria? (S/N): ")
    avaria_selecionada = 7
    avaria_preco = 0

    if avaria_in == "S":
        avaria_query="""
        SELECT *
        FROM avaria
        """
        cursor.execute(avaria_query)
        avaria = cursor.fetchall()
        print("Lista de avaria: ")
        for i in range(len(avaria)):
            print(f'ID:{avaria[i][0]} - {avaria[i][1]}')
        avaria_selecionada = input("Seleciona o ID da avaria: ")
        for j in range (len(avaria)):
            if int(avaria_selecionada) == avaria[j][0]:
                avaria_preco = avaria[j][2]
                print("Valor da avaria: " + str(avaria_preco))

    dt_devolucao = input("Informe a data efetiva desta devolução YYYY-MM-DD: ")
    atraso_preco = 0
    if (dt_devolucao > result[5]):
        atraso_dias = datetime.strptime(dt_devolucao, "%Y-%m-%d") - datetime.strptime(result[5], "%Y-%m-%d")
        atraso_dias = atraso_dias.days
        
        atraso_query = """
        SELECT b.categoria_preco
        FROM veiculo a
        INNER JOIN categoria b
        ON a.categoria_id = b.categoria_id
        WHERE a.veiculo_id == ?;
        """
        id_veiculo = str(result[1])
        cursor.execute(atraso_query, (id_veiculo))
        atraso_categoria_preco = cursor.fetchall()[0][0]
        
        atraso_preco = atraso_dias * atraso_categoria_preco
        print("Valor do atraso na devolução: "+ str(atraso_preco))
        

    valor_final = result[6] + avaria_preco + atraso_preco
    print("Valor da reserva atualizado (diarias + avarias)= R$ " + str(valor_final))

    # Query para inserir devolução na base -----------------------------------
    cursor.execute("SELECT MAX(devolucao_id) FROM devolucao")
    contador_devolucao = cursor.fetchall()[0][0] + 1

    devolucao_query = """
    INSERT INTO devolucao (devolucao_id, reserva_id, funcionario_id, agencia_id, devolucao_data, devolucao_quilometragem, avaria_id)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    cursor.execute(devolucao_query, (contador_devolucao, result[0], func[1], result[3], dt_devolucao, km, avaria_selecionada))
    conexao.commit()

    #Atualização na reserva --------------
    cursor.execute("UPDATE reserva SET devolucao = ?, reserva_preco = ? WHERE reserva_id = ?", (dt_devolucao, valor_final, result[0]))
    conexao.commit()

    print("\n Devolução efetuada! \n")

