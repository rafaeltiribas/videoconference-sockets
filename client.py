import socket
from vidstream import CameraClient
from vidstream import StreamingServer
from vidstream import AudioSender
from vidstream import AudioReceiver
import threading
import time
import random

HEADER = 64
PORT = 5050 # Porta do servidor.
SERVER = '192.168.1.15' # IP do servidor
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)
ADDR_SEND = ''

#   cliente servidor 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def envia(msg, client):
    mensagem = msg.encode(FORMAT)
    tamanho_msg = len(mensagem)
    envia_tamanho = str(tamanho_msg).encode(FORMAT)
    envia_tamanho += b' ' * (HEADER - len(envia_tamanho))
    client.send(envia_tamanho)
    client.send(mensagem)

def recebe(client):
    global ADDR_SEND
    while True:
        mensagem = client.recv(2048).decode(FORMAT)
        if mensagem != '':
            msg = mensagem.split()
            if(msg[0] == "[ESTAOTELIGANDO]"):
                print("[Ligação Recebida]")
                ADDR_SEND = msg[1]
                print(ADDR_SEND)
                print(f"[ENDERECO]: {ADDR_SEND}")
                print("[ACEITAR] | [RECUSAR]")
            else:
                print(mensagem)
        else:
            print("[MENSAGEM VAZIA]")

def iniciar_client(client):
    global ADDR_SEND
    PORT_CLIENT = "None"
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
                envia(f"{opcao} {nome} {porta}", client)
                PORT_CLIENT = int(porta)
                #   Criar o receiver do cliente streaming de video
                receiver = StreamingServer(SERVER, PORT_CLIENT) 
                receiver_audio = AudioReceiver(SERVER, PORT_CLIENT-1)
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
                end_separado = end_conn.split(":")
                sending = CameraClient(SERVER, int((end_separado[1])))              #Video
                sender = AudioSender(SERVER, int((end_separado[1]))-1)              #Audio
                t1 = threading.Thread(target=receiver.start_server)
                t1.start()
                
                time.sleep(10)
                
                t2 = threading.Thread(target=sending.start_stream)
                t2.start()
                
                receiver_thread = threading.Thread(target=receiver_audio.start_server)
                receiver_thread.start()

                time.sleep(5)

                sender_thread = threading.Thread(target=sender.start_stream)
                sender_thread.start()
                
                while input("") != "PARAR":
                    continue
                
                receiver_audio.stop_server()
                sender.stop_stream()
                receiver.stop_server()
                sending.stop_stream()
                ADDR_SEND = ''
            
            case "ACEITAR":
                print("[LIGACAO ACEITA]")
                print(ADDR_SEND)
                end_aceite = ADDR_SEND
                end_separado = end_aceite.split(":")
                sending = CameraClient(end_separado[0], int((end_separado[1])))     #Video
                sender = AudioSender(SERVER, int((end_separado[1]))-1)              #Audio
                t1 = threading.Thread(target=receiver.start_server)
                t1.start()
                
                time.sleep(1)
                
                t2 = threading.Thread(target=sending.start_stream)
                t2.start()
                
                receiver_thread = threading.Thread(target=receiver_audio.start_server)
                receiver_thread.start()

                time.sleep(5)

                sender_thread = threading.Thread(target=sender.start_stream)
                sender_thread.start()
                
                while input("") != "PARAR":
                    continue
                
                receiver_audio.stop_server()
                sender.stop_stream()
                receiver.stop_server()
                sending.stop_stream()
                ADDR_SEND = ''
                
                # Se não tem este pedaço de código ele fica preso na thread de receber
                # Então estou usando para evitar esse erro, mesmo que eu não use essa variável para nada.
                # Foi a solução que encontrei enquanto não entendo a origem do problema.
                numero_aleatorio = random.randint(6000, 60000)
                bug_fix = StreamingServer(socket.gethostbyname(socket.gethostname()), numero_aleatorio)
                
                
        #print("[LOOP CONCLUIDO]")
            
if __name__ == "__main__":

    threading.Thread(target=recebe, args=(client,)).start()
    iniciar_client(client)