import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class AplicaçaoTarefas:
    def __init__(self, root):
        """
        Inicializa a aplicação de Planeamento Semanal de Tarefas.
        Configura a janela principal e os novos elementos de interface (Treeview).
        """
        self.root = root
        self.root.title("Gestor de Tarefas - Planeamento Semanal")
        self.root.geometry("850x650") # Janela ligeiramente maior para caber a nova coluna
        self.root.config(bg="#f4f4f9")

        # Configurar estilo para a Tabela (Treeview)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#d9e1e8")
        style.configure("Treeview", font=("Helvetica", 11), rowheight=30)

        # Título principal na interface
        titulo_label = tk.Label(self.root, text="O Meu Planeamento Semanal", font=("Helvetica", 18, "bold"), bg="#f4f4f9", fg="#333333")
        titulo_label.pack(pady=15)

        # Frame de Entrada de dados
        frame_entrada = tk.Frame(self.root, bg="#f4f4f9")
        frame_entrada.pack(pady=10)

        # Campo: Nome da Tarefa
        tk.Label(frame_entrada, text="Tarefa:", font=("Helvetica", 12), bg="#f4f4f9").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entrada_tarefa = tk.Entry(frame_entrada, font=("Helvetica", 12), width=35, bd=2, relief=tk.GROOVE)
        self.entrada_tarefa.grid(row=0, column=1, padx=10, pady=5)

        # Campo: Descrição
        tk.Label(frame_entrada, text="Descrição:", font=("Helvetica", 12), bg="#f4f4f9").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entrada_desc = tk.Entry(frame_entrada, font=("Helvetica", 12), width=35, bd=2, relief=tk.GROOVE)
        self.entrada_desc.grid(row=1, column=1, padx=10, pady=5)

        # Campo: Dia da Semana (Combobox / Menu Suspenso)
        tk.Label(frame_entrada, text="Dia da Semana:", font=("Helvetica", 12), bg="#f4f4f9").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        dias_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
        self.combo_dia = ttk.Combobox(frame_entrada, values=dias_semana, font=("Helvetica", 12), width=33, state="readonly")
        self.combo_dia.set("Segunda-feira") # Valor por defeito
        self.combo_dia.grid(row=2, column=1, padx=10, pady=5)

        # Campo: Horário (Combobox com horas das 6h às 22h)
        tk.Label(frame_entrada, text="Horário:", font=("Helvetica", 12), bg="#f4f4f9").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        # Gera uma lista de horários das 06:00 até às 22:00
        horarios = [f"{str(h).zfill(2)}:00" for h in range(6, 23)] 
        self.combo_horario = ttk.Combobox(frame_entrada, values=horarios, font=("Helvetica", 12), width=33, state="readonly")
        self.combo_horario.set("08:00") # Valor por defeito
        self.combo_horario.grid(row=3, column=1, padx=10, pady=5)

        # Botão para adicionar a tarefa
        botao_adicionar = tk.Button(frame_entrada, text="Adicionar ao Calendário", bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), bd=0, padx=20, pady=5, cursor="hand2", command=self.adicionar_tarefa)
        botao_adicionar.grid(row=4, column=0, columnspan=2, pady=15)

        # Frame para conter a tabela (Treeview) e a barra de rolagem
        frame_lista = tk.Frame(self.root, bg="#f4f4f9")
        frame_lista.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

        # Barra de rolagem
        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Tabela (Treeview) com as novas colunas
        self.tabela = ttk.Treeview(frame_lista, columns=("Tarefa", "Descrição", "Dia", "Horário"), show='headings', yscrollcommand=scrollbar.set)
        
        # Cabeçalhos da Tabela
        self.tabela.heading("Tarefa", text="Tarefa")
        self.tabela.heading("Descrição", text="Descrição")
        self.tabela.heading("Dia", text="Dia da Semana")
        self.tabela.heading("Horário", text="Horário")

        # Configuração da largura das colunas
        self.tabela.column("Tarefa", width=180, anchor=tk.W)
        self.tabela.column("Descrição", width=250, anchor=tk.W)
        self.tabela.column("Dia", width=120, anchor=tk.CENTER)
        self.tabela.column("Horário", width=100, anchor=tk.CENTER)

        self.tabela.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tabela.yview)

        # Frame para os botões de ação na parte inferior
        frame_botoes = tk.Frame(self.root, bg="#f4f4f9")
        frame_botoes.pack(pady=15)

        # Botão para eliminar a tarefa selecionada
        botao_eliminar = tk.Button(frame_botoes, text="Eliminar Tarefa", bg="#f44336", fg="white", font=("Helvetica", 11, "bold"), bd=0, padx=10, pady=5, cursor="hand2", command=self.eliminar_tarefa)
        botao_eliminar.pack(side=tk.LEFT, padx=10)

        # Botão para limpar a semana toda
        botao_limpar = tk.Button(frame_botoes, text="Limpar Semana", bg="#ff9800", fg="white", font=("Helvetica", 11, "bold"), bd=0, padx=10, pady=5, cursor="hand2", command=self.limpar_tarefas)
        botao_limpar.pack(side=tk.LEFT, padx=10)

    def adicionar_tarefa(self):
        """
        Lê os dados dos campos e adiciona uma nova linha na tabela.
        """
        tarefa = self.entrada_tarefa.get().strip()
        descricao = self.entrada_desc.get().strip()
        dia = self.combo_dia.get()
        horario = self.combo_horario.get()

        if tarefa != "":
            # Insere os dados na tabela, incluindo o horário
            self.tabela.insert("", tk.END, values=(tarefa, descricao, dia, horario))
            # Limpa os campos de texto após adicionar
            self.entrada_tarefa.delete(0, tk.END)
            self.entrada_desc.delete(0, tk.END)
            self.entrada_tarefa.focus() # Volta a focar na caixa de texto principal
        else:
            messagebox.showwarning("Aviso", "O nome da tarefa não pode estar vazio.")

    def eliminar_tarefa(self):
        """
        Elimina o item que estiver atualmente selecionado na tabela.
        """
        selecionado = self.tabela.selection() # Devolve uma lista (tuplo) com o ID dos itens selecionados
        if selecionado:
            for item in selecionado:
                self.tabela.delete(item)
        else:
            messagebox.showwarning("Aviso", "Por favor, selecione uma tarefa da tabela para eliminar.")

    def limpar_tarefas(self):
        """
        Remove todas as tarefas do planeamento semanal após pedir confirmação.
        """
        if not self.tabela.get_children():
            messagebox.showinfo("Informação", "O seu planeamento já está vazio.")
            return

        resposta = messagebox.askyesno("Confirmar", "Tem a certeza que deseja eliminar o planeamento de toda a semana?")
        if resposta:
            for item in self.tabela.get_children():
                self.tabela.delete(item)

if __name__ == "__main__":
    janela_principal = tk.Tk()
    
    # Podemos definir um tamanho mínimo para a janela não ficar distorcida
    janela_principal.minsize(700, 450)
    
    app = AplicaçaoTarefas(janela_principal)
    janela_principal.mainloop()