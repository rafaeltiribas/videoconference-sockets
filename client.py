import socket

#   Cadastro => "CADASTRO, nome"
#   Consulta => "CONSULTA, nome_consulta"

HEADER = 64
PORT = 5050 # Porta do servidor.
SERVER = socket.gethostbyname(socket.gethostname()) # Pega o IP da máquina automaticamente. \ ou SERVER = "192.168.0.177" <-- Ipv4
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def envia(msg):
    mensagem = msg.encode(FORMAT)
    tamanho_msg = len(mensagem)
    envia_tamanho = str(tamanho_msg).encode(FORMAT)
    envia_tamanho += b' ' * (HEADER - len(envia_tamanho))
    client.send(envia_tamanho)
    client.send(mensagem)

conectado = True
while conectado:
    print("[CADASTRO]   |   [CONSULTA]    |   [DESCONECTAR]")
    opcao = input()
    match opcao:
        case "CADASTRO":
            print("[DIGITE O NOME DE USUÁRIO]:")
            nome = input()
            envia(f"{opcao} {nome}")
            print(client.recv(2048))
        case "CONSULTA":
            print("[DIGITE O NOME DE USUÁRIO DO ENDEREÇO A SER CONSULTADO]:")
            nome = input()
            envia(f"{opcao} {nome}")
            print(client.recv(2048))
        case "DESCONECTAR":
            print("[VOCÊ SERÁ DESCONECTADO E DESVINCULADO DO SERVIDOR DE REGISTRO].")
            envia("DESCONECTAR")
            conectado = False
            print(client.recv(2048))