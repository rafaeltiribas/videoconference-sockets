import socket
from vidstream import CameraClient
from vidstream import StreamingServer
import threading
import time
import random

#   Cadastro => "CADASTRO, nome"
#   Consulta => "CONSULTA, nome_consulta"

HEADER = 64
PORT = 5050 # Porta do servidor.
SERVER = socket.gethostbyname(socket.gethostname()) # Pega o IP da máquina automaticamente. \ ou SERVER = "192.168.0.177" <-- Ipv4
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)

#   cliente servidor 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

#   Varável para indicar se esta recebendo chamada.
recebendo_chamada = False

def envia(msg, client):
    mensagem = msg.encode(FORMAT)
    tamanho_msg = len(mensagem)
    envia_tamanho = str(tamanho_msg).encode(FORMAT)
    envia_tamanho += b' ' * (HEADER - len(envia_tamanho))
    client.send(envia_tamanho)
    client.send(mensagem)

def recebe(client):
    while True:
        mensagem = client.recv(2048).decode(FORMAT)
        if mensagem != '':
            print(mensagem) 
            if(mensagem == "[ESTAO TE LIGANDO]"):
                recebendo_chamada = True
                receber_ligacao(client)
        else:
            print("[MENSAGEM VAZIA]")

         
def receber_ligacao(client):
    #Isso funciona
    print("[LICAGAO RECEBIDA]")
    print("[ACEITAR] | [RECUSAR]")
    escolha = input()
    envia(f"{escolha}", client)

def iniciar_client(client):
    PORT_CLIENT = "None"
    conectado = True
    while conectado and not recebendo_chamada:
        print("[CADASTRO]   |   [CONSULTA]    |   [DESCONECTAR]    |   [LIGAR]")
        opcao = input()
        match opcao:
            case "CADASTRO":
                print("[DIGITE O NOME DE USUÁRIO]:")
                nome = input()
                print("[DIGITE A PORTA QUE SERÁ UTILIZADA]:")
                porta = input()
                envia(f"{opcao} {nome} {porta}", client)
                PORT_CLIENT = int(porta)
                #   Criar o receiver do cliente streaming de video
                receiver = StreamingServer(socket.gethostbyname(socket.gethostname()), PORT_CLIENT) # este codigo impede que de erro. mas por que?
            case "CONSULTA":
                print("[DIGITE O NOME DE USUÁRIO DO ENDEREÇO A SER CONSULTADO]:")
                nome = input()
                envia(f"{opcao} {nome}", client)
                
                # Se não tem este pedaço de código ele fica preso na thread de receber
                # Então estou usando para evitar esse erro, mesmo que eu não use essa variável para nada.
                # Foi a solução que encontrei enquanto não entendo a origem do problema.
                numero_aleatorio = random.randint(6000, 60000)
                bug_fix = StreamingServer(socket.gethostbyname(socket.gethostname()), numero_aleatorio)
                
                
            case "DESCONECTAR":
                print("[VOCÊ SERÁ DESCONECTADO E DESVINCULADO DO SERVIDOR DE REGISTRO].")
                envia("DESCONECTAR")
                conectado = False
                client.close()
            case "LIGAR":
                print("[DIGITE O ENDERECO IP/PORTA DA CONEXAO] [EXEMPLO] [25.1.98.186:12766] [IP:PORTA]") 
                end_conn = input()
                envia(f"{opcao} {end_conn}", client)
                
                # Se não tem este pedaço de código ele fica preso na thread de receber
                # Então estou usando para evitar esse erro, mesmo que eu não use essa variável para nada.
                # Foi a solução que encontrei enquanto não entendo a origem do problema.
                numero_aleatorio = random.randint(6000, 60000)
                bug_fix = StreamingServer(socket.gethostbyname(socket.gethostname()), numero_aleatorio)
                
                
        #print("[LOOP CONCLUIDO]")
            
if __name__ == "__main__":

    threading.Thread(target=recebe, args=(client,)).start()
    iniciar_client(client)





















'''
# Criar um if else para caso o cadastro seja feito com sucesso ele continue este codigo ou pare.

            #   Receber a porta do cliente que foi cadastrada no servidor.
            envia(f"CONSULTA {nome}")
            end_client = client.recv(2048).decode(FORMAT)
            end_client = end_client.split(',')
            client_port = end_client[1]
            client_port = client_port.split(')')
            client_port = int(client_port[0])
'''