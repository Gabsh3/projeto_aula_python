import tkinter as tk
from tkinter import messagebox, Toplevel
import mysql.connector
from datetime import datetime

# Inicializa o banco de dados e cria tabelas
def inicializar_banco():
    db = mysql.connector.connect(host="localhost", user="root", password="root")
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS restaurante")
    cursor.execute("USE restaurante")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
            prato VARCHAR(50), quantidade INT, data_adicionado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS retiradas (
            prato VARCHAR(50), quantidade INT, data_retirada TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()
    cursor.close()
    db.close()

# Estoque inicial
estoque = {p: 0 for p in ['macarronada', 'strogonoff', 'feijoada', 'parmegiana', 'lasanha']}

# Atualiza o menu de pratos
def atualizar_menu_pratos():
    prato_menu['menu'].delete(0, 'end')
    for prato in estoque:
        prato_menu['menu'].add_command(label=prato, command=tk._setit(prato_var, prato))
    prato_var.set('Escolha um prato')

# Adiciona produto ao estoque e banco de dados
def adicionar_produto(prato, quantidade):
    estoque[prato] += quantidade
    db = mysql.connector.connect(host="localhost", user="root", password="root", database="restaurante")
    cursor = db.cursor()
    cursor.execute("INSERT INTO estoque (prato, quantidade, data_adicionado) VALUES (%s, %s, %s)",
                   (prato, quantidade, datetime.now()))
    db.commit()
    cursor.close()
    db.close()
    messagebox.showinfo("Produto Adicionado", f"{quantidade} {prato}(s) adicionados ao estoque.")
    atualizar_menu_pratos()

# Realiza uma retirada do estoque
def fazer_pedido(prato, quantidade):
    if estoque.get(prato, 0) < quantidade:
        messagebox.showwarning("Estoque Insuficiente", f"Estoque insuficiente para {prato}. Atual: {estoque.get(prato, 0)}.")
        return
    estoque[prato] -= quantidade
    db = mysql.connector.connect(host="localhost", user="root", password="root", database="restaurante")
    cursor = db.cursor()
    cursor.execute("INSERT INTO retiradas (prato, quantidade, data_retirada) VALUES (%s, %s, %s)",
                   (prato, quantidade, datetime.now()))
    db.commit()
    cursor.close()
    db.close()
    messagebox.showinfo("Retirada Realizada", f"Retirada de {quantidade} {prato}(s) realizada.")

# Lida com a entrada da retirada
def realizar_retirada():
    prato = prato_var.get()
    quantidade = quantidade_var.get()
    if quantidade.isdigit() and int(quantidade) > 0:
        fazer_pedido(prato, int(quantidade))
    else:
        messagebox.showwarning("Entrada Inválida", "Insira uma quantidade válida.")

# Adiciona itens ao estoque
def adicionar_estoque():
    prato = prato_var.get()
    quantidade = quantidade_var.get()
    if quantidade.isdigit() and int(quantidade) > 0:
        if messagebox.askyesno("Confirmação", f"Deseja adicionar {quantidade} {prato}(s) ao estoque?"):
            adicionar_produto(prato, int(quantidade))
    else:
        messagebox.showwarning("Entrada Inválida", "Insira uma quantidade válida.")

# Limpa todos os registros
def limpar_registros():
    if messagebox.askyesno("Confirmação", "Você tem certeza que deseja limpar todos os registros?"):
        db = mysql.connector.connect(host="localhost", user="root", password="root", database="restaurante")
        cursor = db.cursor()
        cursor.execute("DELETE FROM estoque")
        cursor.execute("DELETE FROM retiradas")
        db.commit()
        cursor.close()
        db.close()
        messagebox.showinfo("Registros Limpos", "Todos os registros foram limpos com sucesso.")
        global estoque
        estoque.clear()
        estoque.update({p: 0 for p in ['macarronada', 'strogonoff', 'feijoada', 'parmegiana', 'lasanha']})
        atualizar_menu_pratos()

# Mostra o estoque atual
def mostrar_estoque():
    estoque_window = Toplevel(root)
    estoque_window.title("Estoque Atual")
    tk.Label(estoque_window, text="Estoque Atual:", font=("Arial", 14)).pack(pady=10)
    estoque_text = "\n".join([f"{prato}: {quantidade} items" for prato, quantidade in estoque.items()])
    tk.Label(estoque_window, text=estoque_text or "Nenhum item no estoque.", font=("Arial", 12)).pack(pady=10)

# Mostra registros de adições e retiradas
def mostrar_registros():
    registros_window = Toplevel(root)
    registros_window.title("Registros de Adições e Retiradas")
    db = mysql.connector.connect(host="localhost", user="root", password="root", database="restaurante")
    cursor = db.cursor()

    cursor.execute("SELECT prato, quantidade, DATE_FORMAT(data_adicionado, '%d/%m/%Y %H:%i:%s') FROM estoque")
    adicoes = cursor.fetchall()
    adicoes_text = "\n".join([f"{data[0]}: {data[1]} itens, Adicionado em: {data[2]}" for data in adicoes]) or "Nenhum registro de adição."

    cursor.execute("SELECT prato, quantidade, DATE_FORMAT(data_retirada, '%d/%m/%Y %H:%i:%s') FROM retiradas")
    retiradas = cursor.fetchall()
    retiradas_text = "\n".join([f"{data[0]}: {data[1]} itens, Retirado em: {data[2]}" for data in retiradas]) or "Nenhum registro de retirada."

    tk.Label(registros_window, text="Registro de Adições:").pack(pady=10)
    tk.Label(registros_window, text=adicoes_text).pack(pady=5)
    tk.Label(registros_window, text="Registro de Retiradas:").pack(pady=10)
    tk.Label(registros_window, text=retiradas_text).pack(pady=5)

    cursor.close()
    db.close()

# Inicia o banco de dados e a interface
inicializar_banco()
root = tk.Tk()
root.title("Cantinho da Vó - Controle de Estoque")
root.geometry("400x600")

# Criação da interface
tk.Label(root, text="Cantinho da Vó", font=("Arial", 20)).pack(pady=20)
prato_var = tk.StringVar(value="Escolha um prato")
prato_menu = tk.OptionMenu(root, prato_var, 'Escolha um prato')
prato_menu.pack(pady=5)
atualizar_menu_pratos()

quantidade_var = tk.StringVar()
tk.Entry(root, textvariable=quantidade_var).pack(pady=5)

# Estilo dos botões
button_style = {"bg": "#FCA311", "fg": "#1F1F2B", "font": ("Arial", 12, "bold"), "padx": 10, "pady": 5}
tk.Button(root, text="Retirar do Estoque", command=realizar_retirada, **button_style).pack(pady=10)
tk.Button(root, text="Adicionar ao Estoque", command=adicionar_estoque, **button_style).pack(pady=5)
tk.Button(root, text="Mostrar Estoque", command=mostrar_estoque, **button_style).pack(pady=10)
tk.Button(root, text="Mostrar Registros", command=mostrar_registros, **button_style).pack(pady=10)
tk.Button(root, text="Limpar Registros", command=limpar_registros, **button_style).pack(pady=5)

root.mainloop()
