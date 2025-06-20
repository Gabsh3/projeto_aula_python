# projeto_aula_python
controle_de_estoque
 Sistema de Controle de Estoque
Este é um sistema simples de controle de estoque para um restaurante, desenvolvido com Python, Tkinter para a interface gráfica e MySQL para armazenamento de dados. Ideal para pequenos estabelecimentos que precisam registrar entradas e saídas de pratos do estoque de forma prática e visual.

🧠 Funcionalidades
Cadastro de pratos e controle de estoque: O sistema permite adicionar pratos ao estoque ou retirar para pedidos.

Interface gráfica intuitiva com botões e menus usando a biblioteca tkinter.

Registros persistentes em banco de dados MySQL, tanto para adições quanto para retiradas de pratos.

Visualização do estoque atual em tempo real.

Visualização de registros de todas as entradas e saídas com data e hora.

Opção para limpar todos os registros, reiniciando o estoque.

🔧 Tecnologias utilizadas
Python 3

Tkinter (interface gráfica)

MySQL (armazenamento de dados)

Biblioteca mysql-connector-python para conexão com o banco de dados

datetime para registrar data e hora das movimentações

📋 Funcionalidade dos Arquivos
inicializar_banco()
Cria o banco de dados e as tabelas (estoque e retiradas) caso ainda não existam.

adicionar_produto(prato, quantidade)
Adiciona uma quantidade de um prato ao estoque e registra no banco.

fazer_pedido(prato, quantidade)
Remove uma quantidade do prato do estoque (se houver disponibilidade) e registra no banco.

realizar_retirada() e adicionar_estoque()
Funções conectadas aos botões da interface que chamam as ações de adicionar ou retirar.

mostrar_estoque()
Abre uma nova janela com a visualização atual dos pratos e suas quantidades.

mostrar_registros()
Abre uma janela mostrando todos os registros de adições e retiradas com data e hora.

limpar_registros()
Apaga todos os dados do banco e reseta o estoque na memória.
