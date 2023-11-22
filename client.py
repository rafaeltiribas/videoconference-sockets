import socket
from vidstream import CameraClient
from vidstream import StreamingServer
import threading
import time

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

#   Video Streaming
receiver = StreamingServer(socket.gethostbyname(socket.gethostname()), 9999)


def envia(msg):
    mensagem = msg.encode(FORMAT)
    tamanho_msg = len(mensagem)
    envia_tamanho = str(tamanho_msg).encode(FORMAT)
    envia_tamanho += b' ' * (HEADER - len(envia_tamanho))
    client.send(envia_tamanho)
    client.send(mensagem)
    
def receber():
    while True:
        try:
            mensagem_length = client.recv(HEADER).decode(FORMAT)
            if mensagem_length:
                mensagem_length = int(mensagem_length)
                mensagem = client.recv(mensagem_length).decode(FORMAT)
                print("[SERVIDOR]:", mensagem)
        except Exception as e:
            print(e)
            break

def iniciar_receber():
    thread_receber = threading.Thread(target=receber)
    thread_receber.start()

def iniciar_client():
    conectado = True
    while conectado:
        print("[CADASTRO]   |   [CONSULTA]    |   [DESCONECTAR]    |   [LIGAR]")
        opcao = input()
        match opcao:
            case "CADASTRO":
                print("[DIGITE O NOME DE USUÁRIO]:")
                nome = input()
                print("[DIGITE A PORTA QUE SERÁ UTILIZADA]:")
                porta = input()
                envia(f"{opcao} {nome} {porta}")
                PORT_CLIENT = int(porta)
                print(client.recv(2048).decode(FORMAT))
                #   Criar o receiver do cliente 
                receiver = StreamingServer(socket.gethostbyname(socket.gethostname()), PORT_CLIENT)
            case "CONSULTA":
                print("[DIGITE O NOME DE USUÁRIO DO ENDEREÇO A SER CONSULTADO]:")
                nome = input()
                envia(f"{opcao} {nome}")
                print(client.recv(2048).decode(FORMAT))
            case "DESCONECTAR":
                print("[VOCÊ SERÁ DESCONECTADO E DESVINCULADO DO SERVIDOR DE REGISTRO].")
                envia("DESCONECTAR")
                conectado = False
                print(client.recv(2048))    # O print recebido deve ser ajustado -> b'String'
            case "LIGAR":
                print("[DIGITE O ENDERECO IP/PORTA DA CONEXAO] [EXEMPLO] [25.1.98.186:12766] [IP:PORTA]") 
                end_conn = input()
                envia(f"{opcao} {end_conn}")
            
if __name__ == "__main__":
    iniciar_receber()
    iniciar_client()





















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