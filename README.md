# videoconference-sockets
Esse é um trabalho realizado para a matéria de Redes de Computadores II na Universidade Federal Fluminense e tem como objetivo desenvolver uma aplicação de videoconferência descentralizada utilizando sockets.

# Etapa 1
Nesta etapa, é necessário implementar um socket TCP que interconecte os clientes e o servidor.

# server.py 
Armazenar e imprimir uma tabela dinâmica contendo informações dos clientes;
Imprimir mensagem de confirmação de registro de novo usuário;
Caso o usuário já esteja cadastrado, imprimir mensagem informando esta condição;
Responder aos clientes o nome de um nó conectado e seus respectivos endereços e números de porta, quando assim solicitado;
Caso o cliente solicite o fim da conexão, o servidor deve responder com mensagem de encerramento e, depois, fechar o socket.

# client.py
Registrar-se no servidor utilizando um nome e um IP exclusivos e indicando a porta apta para receber o pedido de chamada;
Realizar consultas de endereços de portas por nomes específicos dos usuários;
Caso o cliente deseje se desvincular do servidor de registro, ele deve enviar uma mensagem com esta solicitação.
