import socket
import threading

HEADER = 64
PORT = 5050 # Porta do servidor.
SERVER = '192.168.1.15' # IP do servidor
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

#   Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

#   Armazenamento de usuários.          ! Pode ser trocado por armazenamento em um arquivo.
usuarios = {} # {nome : ipporta} 
conexoes_usuarios = {} # Relacionar {ipporta:conexao}

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
                    nome = msg[1]
                    porta = msg[2]
                    cadastro(nome, porta, end, conn)
                case "CONSULTA":
                    nome = msg[1]
                    endereco = consulta(nome, conn)
                case "DESCONECTAR":
                    conectado = False
                    remove(nome)
                    conn.send("[DESCONECTADO]".encode(FORMAT))
                    #   !!! FECHAR O SOCKET:?
                case "LIGAR":
                    endereco_destino = msg[1]
                    ligar(endereco_destino, conn)
                    res = msg[1]
                    print(res)
                    
            print(f"[{end}] {msg}\n[TABELA USUÁRIOS ATIVOS] {usuarios}")
    conn.close()

def aceitar_ligacao(endereco):
    print("[RESPONDENDO ACEITE LIGACAO]")
    if endereco in conexoes_usuarios:
        dest_conn = conexoes_usuarios[endereco]
        dest_conn.send(f"[ACEITA]")

#   Funcao para ligacao
def ligar(endereco_dest, conn):
    print("[LIGANDO]")
    if endereco_dest in conexoes_usuarios:
        print("[USUARIO ENCONTRADO]")
        end_ligando = conexoes_contrario[conn]
        dest_conn = conexoes_usuarios[endereco_dest]
        dest_conn.send(f"[ESTAOTELIGANDO] {end_ligando}".encode(FORMAT)) 

#   Retorna o tamanho da mensagem que o cliente está enviando.
def get_tamanho(conn: any):
    tamanho_msg = conn.recv(HEADER).decode(FORMAT)
    if tamanho_msg:
        tamanho_msg = int(tamanho_msg)
        return tamanho_msg
    return None
    
#   Função de inicialização do servidor.
def iniciar() -> None:
    ADDR_SEND = ''
    server.listen()
    while True:
        conn, end = server.accept()
        thread = threading.Thread(target=gerencia_cliente, args=(conn, end))    # Executa em thread a comunicação com a nova conexão.
        thread.start()
        print(f"[Conexões Ativas] {threading.active_count() - 1}")

#   Função de cadastro.
conexoes_contrario = {} # conn : end:porta
def cadastro(nome: str, porta: str, endereco: str, conn: any) -> None:
    if usuarios.get(nome, 0) == 0:  # Checa se o nome já não está cadastrado no sistema.
        end_client = (endereco,) + (porta,)
        end_client = (end_client[0][0],) + (end_client[1],)
        end_client = ":".join(map(str, end_client))
        usuarios[nome] = end_client
        conexoes_usuarios[end_client] = conn
        conexoes_contrario[conn] = end_client
        conn.send("[CADASTRO_REALIZADO_COM_SUCESSO]".encode(FORMAT))
        return
    conn.send("[ESTE_USUÁRIO_JÁ_ESTÁ_CADASTRADO]".encode(FORMAT))

#   Função de consulta do cliente.
def consulta(nome: str, conn: any) -> str:
    endereco = usuarios.get(nome, 0)
    conn.send(f"[ENDERECO_{nome}]: {endereco}".encode(FORMAT))
    return

#   Função de remoção de um usuário.
def remove(nome: str) -> None:
    usuarios.pop(nome)
    
#   Funcionamento
print("[...Iniciando o servidor...]")
iniciar()