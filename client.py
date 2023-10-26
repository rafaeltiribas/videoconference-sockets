import socket

#   socket
HEADER = 64
PORT = 5050 # Porta do servidor.
SERVER = socket.gethostbyname(socket.gethostname()) # Pega o IP da máquina automaticamente. \ ou SERVER = "192.168.0.177" <-- Ipv4
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DESCONECTAR"
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

envia("Rafael, 192.168.0.177")
envia(DISCONNECT_MESSAGE)