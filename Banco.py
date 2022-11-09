from multiprocessing.sharedctypes import Value
from tinydb import TinyDB, Query
import pandas as pd
from datetime import date, datetime
import os

db = TinyDB('DB.json');
Cliente = Query();

class Clientes:
    def __init__(self):
        self.andaimes = 120;
        self.escoras = 607;

    @staticmethod
    def insereClientes():
        try:
            nomeClient = input(("Digite o nome do cliente: "));
            addresClient = input("Digite o endereço do cliente: ");
            addresObra = input("Digite o endereço da obra: ");
            cpf = input("Digite o cpf do cliente: ");
            cnpj = input("Digite o cnpj do cliente: ");
            valueEscora = int(input("Digite o valor da escora: "));
            sizeEscora = int(input("Digite o tamanho da escora: "));
            quantity = int(input("Digite a quantidade de escoras que serão alugadas: "));
            verificacaoA = Clientes.verificaçãoEstoque(Clientes().escoras, 'quantity', "escoras");
            if(verificacaoA == 0):
                return 0;
            else:
                pass;
            todayDate = date.today().strftime('%d/%m/%Y');
            paymentDate = input("Digite a data de vencimento do contrato (Formato -> (00/00/0000)): ");
            formPayment = input("Qual a forma de pagamento(INICIO/VENCIMENTO): ");
            quantityAndaimes = int(input("Digite a quantidade de andaimes que serão alugados: "));
            verificacaoAnda = Clientes.verificaçãoEstoque(Clientes().andaimes, 'quantityAndaimes', "andaimes");
            if(verificacaoAnda == 0):
                return 0;
            else:
                pass;

            valueAndaimes = int(input("Digite o preço do andaime: "));
            paymentAmount = (valueEscora * quantity) + (quantityAndaimes * valueAndaimes);
        except ValueError:
            print("Valores inválidos ou não permitidos, tente novamente!\n");
            return 0;
        print("\n" * os.get_terminal_size().lines)
        db.insert(
            {
                'nome': Clientes.verificaçãoNome(nomeClient),
                'addresClient': addresClient,
                'addresObra': addresObra,
                'cpf': Clientes.verificaçãoCPF(cpf),
                'cnpj': Clientes.verificaçãoCNPJ(cnpj),
                'valueEscora': valueEscora,
                'sizeEscora': sizeEscora,
                'quantity': quantity,
                'paymentAmount': paymentAmount,
                'todayDate': todayDate,
                'paymentDate': paymentDate,
                'formPayment': formPayment,
                'quantityAndaimes': quantityAndaimes,
                'valueAndaimes': valueAndaimes
            }
        );
        Clientes.escreveExcel();
        
    @staticmethod
    def alteraClientes():
        print("1 - Nome\n2 - Endereço do Cliente\n3 - Endereço da Obra\n4 - Valor da Escora\n5 - Tamanho da Escora\n6 - Quantidade da Escora\n7 - Forma de Pagamento\n8 - Quantidade de Andaimes\n9 - Valor do Andaime\n0 - Para sair\n");
        while True:
            try:
                awnser = int(input("Digite em qual campo você quer alterar: "));
                break;
            except ValueError:
                print("Valor inválido, digite novamente: ");
        if(awnser == 0):
            print("\n" * os.get_terminal_size().lines);
        else:
            alteracao = input("Digite o CPF do cliente para fazer a alteração: ");
            print("\n" * os.get_terminal_size().lines);
            alteracao = Clientes.verificaçãoCPF(alteracao);
            teste = Clientes.existeCliente(alteracao);
            if(teste == 0):
                return 0;
            else:
                if(awnser == 1):
                    Clientes.alteracaoC(alteracao, "nome", "nome");

                elif(awnser == 2):
                    Clientes.alteracaoC(alteracao, "addresClient", "Endereço do Cliente");
                
                elif(awnser == 3):
                    Clientes.alteracaoC(alteracao, "addresObra", "Endereço da Obra");
                
                elif(awnser == 4):
                    Clientes.alteracaoC(alteracao, "valueEscora", "Valor da Escora");

                elif(awnser == 5):
                    Clientes.alteracaoC(alteracao, "sizeEscora", "Tamanho da Escora");
                
                elif(awnser == 6):
                    Clientes.alteracaoC(alteracao, "quantity", "Quantidade de Escoras");
                
                elif(awnser == 7):
                    Clientes.alteracaoC(alteracao, "formPayment", "Forma de Pagamento");

                elif(awnser == 8):
                    Clientes.alteracaoC(alteracao, "quantityAndaimes", "Quantidade de Andaimes");
                
                elif(awnser == 9):
                    Clientes.alteracaoC(alteracao, "valueAndaimes", "Valor do Andaime");

        Clientes.escreveExcel();

    @staticmethod     
    def alteracaoC(cpf: str, tipoDado: str, campo: str):
        while True:
            try:
                if(tipoDado == 'valueEscora' or tipoDado == 'sizeEscora' or tipoDado == 'quantity' or tipoDado == 'quantityAndaimes' or tipoDado == 'valueAndaimes'):
                    newDice = int(input(f"Digite (a/o) {campo}: "));
                    db.update({tipoDado: newDice}, Cliente.cpf == cpf);
                    print("\n" * os.get_terminal_size().lines);
                    break;
                else:
                    newDice = input(f"Digite (a/o) {campo}: ");
                    db.update({tipoDado: newDice}, Cliente.cpf == cpf);
                    print("\n" * os.get_terminal_size().lines);
                    break;
            except ValueError:
                print("Valor inválido, digite novamente: ");

    @staticmethod
    def escreveExcel():
        listaNomes = [];
        listaAddresClient = []; 
        listaAddresObra = [];
        listaCpf = [];
        listaCnpj = [];
        listaValorEscora = [];
        listaTamEscora = [];
        listaQuantidade = [];
        listaPagamentoTotal = [];
        listaDataHoje = [];
        listaDataVencimento = [];
        listaFormaPagamento = [];
        listaQuantityAndaimes = [];
        listaValueAndaimes = [];

        el = db.all();
        for i in range(len(db)):
            dicionario = el[i];
            listaNomes.append(dicionario['nome']);
            listaAddresClient.append(dicionario['addresClient']);
            listaAddresObra.append(dicionario['addresObra']);
            listaCpf.append(dicionario['cpf']);
            listaCnpj.append(dicionario['cnpj']);
            listaValorEscora.append(dicionario['valueEscora']);
            listaTamEscora.append(dicionario['sizeEscora']);
            listaQuantidade.append(dicionario['quantity']);
            listaPagamentoTotal.append(dicionario['paymentAmount']);
            listaDataHoje.append(dicionario['todayDate']);
            listaDataVencimento.append(dicionario['paymentDate']);
            listaFormaPagamento.append(dicionario['formPayment']);
            listaQuantityAndaimes.append(dicionario['quantityAndaimes']);
            listaValueAndaimes.append(dicionario['valueAndaimes']);

        df = pd.DataFrame(zip(listaNomes, listaAddresClient,listaAddresObra, listaCpf, listaCnpj, listaValorEscora, listaTamEscora, listaQuantidade, listaPagamentoTotal, listaDataHoje, listaDataVencimento, listaFormaPagamento, listaQuantityAndaimes, listaValueAndaimes), columns = ["Nomes", "EndereçoCliente", "EndereçoObra", "CPF", "CNPJ", "ValorEscora", "TamanhoEscora", "QuantidadeEscora", "PagamentoTotal", "DataInicio", "DataVencimento", "FormaPagamento", "QuantidadeAndaimes", "ValorAndaimes"]);

        df.to_csv("/home/breno/Área de Trabalho/BancoDeDados.csv", index = False);
    
    @staticmethod
    def verificaçãoNome(nome: str):
        if(any(char.isdigit() for char in nome) == True):
            while(any(char.isdigit() for char in nome) == True):
                nome = input("Nome inválido, Digite novamente: ");
            return nome;
        else:
            return nome;

    @staticmethod
    def verificaçãoCPF(end: str):
            while(len(end) != 14 or end[3] != '.' or end[7] != '.' or end[11] != '-' or any(char.isalpha() for char in end) == True):
                end = input("CPF inválido!, digite novamente: ");
            return end;

    @staticmethod
    def verificaçãoCNPJ(end: str):
        while(len(end) != 12 or end[9] != '-' or any(char.isalpha() for char in end) == True):
                end = input("CNPJ inválido!, digite novamente: ");
        return end;

    @staticmethod
    def totalEscoras():
        listaEscoras = []
        somaEscoras = 0;
        el = db.all();
        for i in range(len(db)):
            escoras = el[i];
            listaEscoras.append(escoras['quantity']);
            somaEscoras += listaEscoras[i];
        
        conta = Clientes().escoras - somaEscoras;
        return print("A quantidade de escoras no estoque é de: {}".format(conta));

    def totalAndaimes():
        somaAndaimes = 0;
        el = db.all();
        for i in range(len(db)):
            andaimes = el[i];
            somaAndaimes += andaimes['quantityAndaimes'];
        conta = Clientes().andaimes - somaAndaimes;
        return print("A quantidade de andaimes no estoque é de: {}\n".format(conta));



    @staticmethod
    def lucroTotal():
        conta = 0;
        el = db.all();
        for i in range(len(db)):
            escoras = el[i];
            conta += escoras["paymentAmount"];

        return print("O lucro estimado para este mês é de: {}R$\n".format(conta));
    
    
    def verPrazoEntrega():
        diaAtual = date.today();
        el = db.all();
        for i in range(len(db)):
            datas = el[i];
            nomes = datas['nome'];
            data = datas['paymentDate'];
            conversorData = datetime.strptime(data, '%d/%m/%Y').date();
            dataAtual = date.fromordinal(diaAtual.toordinal());
            diferenca = conversorData - dataAtual;
            print(f"O contrato do Cliente {nomes} irá vencer em {diferenca.days} dias!\n");
    
    def devolução():
        print("1 - Devolução de Escoras\n2 - Devolução de Andaimes\n0 - Para sair\n");
        while True:
            try:
                awnser = int(input("Digite o campo no qual vai ser feita a devolução: "));
                break;
            except ValueError:
                print("Valor inválido, digite novamente: ");
        print("\n" * os.get_terminal_size().lines);
        if(awnser == 1):
            conta = 0;
            cpf = input("Digite o CPF do cliente para fazer a devolução: ");
            Clientes.verificaçãoCPF(cpf);
            teste = Clientes.existeCliente(cpf);
            if(teste == 0):
                return 0;
            else:
                while True:
                    try:
                        valorAlterado = int(input("Digite quantidade de escoras a serem devolvidas: "));
                        break;
                    except ValueError:
                        print("Valor inválido, digite novamente: ");
                cliente = db.get(Cliente.cpf == cpf);
                conta = cliente['quantity'] - valorAlterado;
                db.update({"quantity": conta}, Cliente.cpf == cpf);
                Clientes.escreveExcel();
                print("\n" * os.get_terminal_size().lines);
        elif(awnser == 2):
            conta = 0;
            cpf = input("Digite o CPF do cliente para fazer a devolução: ");
            Clientes.verificaçãoCPF(cpf);
            teste = Clientes.existeCliente(cpf);
            if(teste == 0):
                return 0;
            else:
                while True:
                    try:
                        valorAlterado = int(input("Digite quantidade de andaimes a serem devolvidos: "));
                        break;
                    except ValueError:
                        print("Valor inválido, digite novamente: ");
                cliente = db.get(Cliente.cpf == cpf);
                conta = cliente['quantityAndaimes'] - valorAlterado;
                db.update({"quantityAndaimes": conta}, Cliente.cpf == cpf);
                Clientes.escreveExcel();
                print("\n" * os.get_terminal_size().lines);
        else:
            awnser = 0;

    def existeCliente(cpf: str):
        el = db.all();
        existe = 0;
        for i in range(len(db)):
            cliente = el[i];
            if(cliente['cpf'] == cpf):
                existe = 1;
                break;
            else:
                existe = 0;
        if(existe == 1):
            return cpf;
        else:
            print("Cliente não encontrado, cadastre ele primeiro!\n");
            return 0;
    
    def verificaçãoEstoque(quant: int, tipo: str, frase: str):
        el = db.all();
        verificacao = 0;
        for i in range(len(db)):
            escoras = el[i];
            verificacao += escoras[tipo];
        if(verificacao - quant == 0):
            print(f"Sem {frase} disponíveis no estoque, tente quando liberar!\n"); 
            return 0;
        else:
            pass;
    
    def resetaBanco():
        while True:
            try:
                awnser = int(input("Você tem certeza que deseja resetar o banco de dados? (1 - sim/ 2 - não): "));
                break;
            except ValueError:
                print("Valor inválido, tente novamente!");
        if(awnser == 1):
            db.truncate();
        else:
            return 0;

class ClientesFinalizados(Clientes):

    @staticmethod
    def finalizaContrato():
        listaNome = [];
        listaEndC = [];
        listaEndO = [];
        listaCpf = [];
        listaCnpj = [];

        cpf = input("Digite o CPF no cliente para finalizar o contrato: ");
        Clientes.verificaçãoCPF(cpf);
        teste = Clientes.existeCliente(cpf);
        if(teste == 0):
            return 0;
        else:
            dadosCliente = db.get(Cliente.cpf == cpf);
            listaNome.append(dadosCliente['nome']);
            listaEndC.append(dadosCliente['addresClient']);
            listaEndO.append(dadosCliente['addresObra']);
            listaCpf.append(dadosCliente['cpf']);
            listaCnpj.append(dadosCliente['cnpj']);
            
            df = pd.DataFrame(zip(listaNome, listaEndC, listaEndO, listaCpf, listaCnpj), columns = ["NomeCliente", "EndereçoCliente", "EndereçoObra", "CPF", "CNPJ"]);
            if(os.path.exists("/home/breno/Área de Trabalho/ClientesFinalizados.csv") == False):
                df.to_csv("/home/breno/Área de Trabalho/ClientesFinalizados.csv", index = False);
            else:
                df2 = pd.read_csv("/home/breno/Área de Trabalho/ClientesFinalizados.csv");
                df_concat = pd.concat([df2, df]);
                df_concat.to_csv("/home/breno/Área de Trabalho/ClientesFinalizados.csv", index = False);
            
            db.remove(Cliente.cpf == cpf);
            Clientes.escreveExcel();
            print("\n" * os.get_terminal_size().lines)

def main():
    awnser = None;
    mensagem = ("1 - Inserir clientes no banco de dados\n2 - Alterar valores dos clientes\n3 - Total de Escoras/Andaimes no estoque\n4 - Visualizar lucro total no mês\n5 - Finalizar o contrato de um cliente\n6 - Visualizar tempo restante de contrato dos clientes\n7 - Devolução de escoras ao estoque\n8 - Apaga os dados de todos os clientes\n0 - Para fechar o programa\n");
    while(awnser != 0):
        print(mensagem);
        while True:
            try:
                awnser = int(input("Digite o número correspondente para executar a ação: "));
                break;
            except ValueError:
                print("Valor invalido, tente novamente: ");

        print("\n" * os.get_terminal_size().lines);
        if(awnser == 1):
            Clientes.insereClientes();
            wait = input("Aperte qualquer botão ou ENTER para voltar!\n");
            print("\n" * os.get_terminal_size().lines);

        elif(awnser == 2):
            Clientes.alteraClientes();
            wait = input("Aperte qualquer botão ou ENTER para voltar!\n");
            print("\n" * os.get_terminal_size().lines);
        elif(awnser == 3):
            Clientes.totalEscoras();
            Clientes.totalAndaimes();
            wait = input("Aperte qualquer botão ou ENTER para voltar!\n");
            print("\n" * os.get_terminal_size().lines);

        elif(awnser == 4):
            Clientes.lucroTotal();
            wait = input("Aperte qualquer botão ou ENTER para voltar!\n");
            print("\n" * os.get_terminal_size().lines);

        elif(awnser == 5):
            ClientesFinalizados.finalizaContrato();
            wait = input("Aperte qualquer botão ou ENTER para voltar!\n");
            print("\n" * os.get_terminal_size().lines);

        elif(awnser == 6):
            Clientes.verPrazoEntrega();
            wait = input("Aperte qualquer botão ou ENTER para voltar!\n");
            print("\n" * os.get_terminal_size().lines);

        elif(awnser == 7):
            Clientes.devolução();
            wait = input("Aperte qualquer botão ou ENTER para voltar!\n");
            print("\n" * os.get_terminal_size().lines);
        elif(awnser == 8):
            Clientes.resetaBanco();
            print("\n" * os.get_terminal_size().lines);

main();
