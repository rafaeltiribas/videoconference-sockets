import socket
import threading

# SOCKET
PORT = 5050 # Porta do servidor.
SERVER = socket.gethostbyname(socket.gethostname()) # Pega o IP da máquina automaticamente.
ADDR = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

#   Armazenamento de usuários.          ! Pode ser trocado por armazenamento em um arquivo.
usuarios = {} # {nome : ipporta} 

#   Função de cadastro.
def cadastro(nome: str, endereco: str) -> None:
    if usuarios.get(nome, 0) == 0:  # Checa se o nome já não está cadastrado no sistema.
        usuarios[nome] = endereco
        print("Novo usuário cadastrado.")
        return
    print("Usuário já cadastrado.")

#   Função de consulta do cliente.
def consulta(nome: str) -> str:
    return usuarios.get(nome, 0)

#   Função de remoção de um usuário.
def remove(nome: str) -> None:
    usuarios.pop(nome)

# Testes.
#cadastro("rafael", "123123")
#cadastro("rafael", "123123123")
#print(usuarios)
#print(consulta("rafael"))
#remove("rafael")
#print(usuarios)