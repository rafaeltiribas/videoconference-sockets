import socket
import threading

HEADER = 64
PORT = 5050 # Porta do servidor.
SERVER = socket.gethostbyname(socket.gethostname()) # Pega o IP da máquina automaticamente.
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

#   Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

#   Armazenamento de usuários.          ! Pode ser trocado por armazenamento em um arquivo.
usuarios = {} # {nome : ipporta} 

#   Função para lidar com o processo cliente e suas requisições.
def gerencia_cliente(conn: any, end: any) -> None:
    print(f"[Nova Conexão] {end} conectado.")
    conectado = True
    while conectado:
        tamanho_msg = get_tamanho(conn)
        if tamanho_msg:
            msg = conn.recv(tamanho_msg).decode(FORMAT)
            msg = msg.split()
            match msg[0]:
                case "CADASTRO":
                    print("[NOVO CADASTRO]")
                    cadastro(msg[1], end)
                case "CONSULTA":
                    print("[CONSULTA USUÁRIO]")
                    endereco = consulta(msg[1])
                    print(f"[ENDERECO {msg[1]}]: {endereco}") # ! DEVE SER RETORNADO PARA O CLIENT
                case "DESCONECTAR":
                    print("[DESCONECTANDO USUARIO]")
                    conectado = False
            print(f"[{end}] {msg}\n[TABELA USUÁRIOS ATIVOS] {usuarios}")
    conn.close()

#   Retorna o tamanho da mensagem que o cliente está enviando.
def get_tamanho(conn: any):
    tamanho_msg = conn.recv(HEADER).decode(FORMAT)
    if tamanho_msg:
        tamanho_msg = int(tamanho_msg)
        return tamanho_msg
    return None
    
#   Função de inicialização do servidor.
def iniciar() -> None:
    server.listen()
    while True:
        conn, end = server.accept()
        thread = threading.Thread(target=gerencia_cliente, args=(conn, end))    # Executa em thread a comunicação com a nova conexão.
        thread.start()
        print(f"[Conexões Ativas] {threading.active_count() - 1}")

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
    
#   Funcionamento
print("[...Iniciando o servidor...]")
iniciar()

#   Desafio -> Retornar mensagem para o client.