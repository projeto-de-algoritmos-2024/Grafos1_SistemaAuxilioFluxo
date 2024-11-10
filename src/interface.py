import tkinter as tk
from tkinter import ttk, messagebox
from grafo import criar_grafo, obter_disciplinas_semestre
from main import dados


grafo = criar_grafo()

# Função para lidar com os dados inseridos pelo usuário
def calcular_recomendacoes():
    try:
        # Obter as matérias selecionadas pelo usuário
        disciplinas_completadas = {codigo for codigo, var in disciplinas_selecionadas.items() if var.get()}
        semestre_atual = int(semestre_var.get())

        # Obter as disciplinas recomendadas para o semestre atual
        disciplinas_recomendadas = obter_disciplinas_semestre(grafo, disciplinas_completadas, semestre_atual)

        if not disciplinas_recomendadas:
            resultado_var.set("Nenhuma disciplina recomendada para este semestre.")
        else:
            # Exibir as disciplinas recomendadas
            resultado_var.set("\n".join(disciplinas_recomendadas))
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um semestre válido!")

# Função para limpar as seleções
def limpar_selecao():
    semestre_var.set("")  # Limpa o campo de semestre
    for var in disciplinas_selecionadas.values():
        var.set(False)  # Limpa todas as seleções de checkboxes
    resultado_var.set("")  # Limpa o resultado

# Criar a janela principal
root = tk.Tk()
root.title("Recomendação de Disciplinas")

# Adicionar título
titulo_label = tk.Label(root, text="Sistema de Recomendação de Disciplinas", font=("Arial", 14, "bold"))
titulo_label.pack(pady=10)

# Frame para o semestre atual
semestre_frame = tk.Frame(root)
semestre_frame.pack(pady=10, padx=20, fill="x")

tk.Label(semestre_frame, text="Semestre atual:", anchor="w").pack(side="left", padx=10)
semestre_var = tk.StringVar()
semestre_entry = tk.Entry(semestre_frame, textvariable=semestre_var, width=10)
semestre_entry.pack(side="left", padx=5)

# Frame para as disciplinas cursadas
disciplinas_frame = tk.Frame(root)
disciplinas_frame.pack(pady=10, padx=20, fill="both", expand=True)

tk.Label(disciplinas_frame, text="Selecione as disciplinas que você já cursou:", font=("Arial", 12)).pack(anchor="w", padx=10)

# Canvas para rolagem
canvas = tk.Canvas(disciplinas_frame)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(disciplinas_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)
scrollable_frame = tk.Frame(canvas)

# Adicionando checkboxes dinamicamente
materias = dados[0]['materias']
disciplinas_selecionadas = {}

for materia in materias:
    codigo = materia['codigo']
    nome = materia['nome']
    var = tk.BooleanVar()  # Variável que armazena o estado da checkbox
    check = tk.Checkbutton(scrollable_frame, text=nome, variable=var)
    check.pack(anchor="w", padx=10, pady=5)
    disciplinas_selecionadas[codigo] = var  # Armazenar a variável para cada matéria

# Adicionar o frame rolável ao canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Atualizar a região rolável ao adicionar as matérias
scrollable_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Frame para os botões
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Botões para calcular e limpar
submit_button = tk.Button(button_frame, text="Calcular Disciplinas Recomendadas", command=calcular_recomendacoes)
submit_button.pack(side="left", padx=10)

limpar_button = tk.Button(button_frame, text="Limpar Seleções", command=limpar_selecao)
limpar_button.pack(side="left", padx=10)

# Exibir as disciplinas recomendadas
resultado_label = tk.Label(root, text="Disciplinas recomendadas para o semestre:", font=("Arial", 12))
resultado_label.pack(pady=5)

# Usando um Text widget para mostrar as recomendações de forma mais organizada
resultado_var = tk.StringVar()
resultado_text = tk.Text(root, height=10, width=50, wrap="word", font=("Arial", 10))
resultado_text.pack(pady=5)

# Função para atualizar o resultado no widget Text
def atualizar_resultado():
    resultado_text.delete(1.0, tk.END)
    resultado_text.insert(tk.END, resultado_var.get())

# Atualiza a interface
resultado_var.trace("w", lambda *args: atualizar_resultado())

# Iniciar a interface gráfica
root.mainloop()
