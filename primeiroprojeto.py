import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from fpdf import FPDF

def validar_valor_hora(valor, entry):
    # Adiciona "R$" apenas se o campo estiver vazio
    if not valor.startswith('R$') and valor.strip():
        entry.delete(0, tk.END)
        entry.insert(0, f'R$ {valor}')

def gerar_pdf():
    projeto = entry_projeto.get()
    horas_estimadas = entry_horas.get()
    valor_hora = entry_valor_hora.get()
    prazo = entry_prazo.get()

    if not all([projeto, horas_estimadas, valor_hora, prazo]):
        messagebox.showerror("Campos em branco", "Por favor, preencha todos os campos.")
        return

    try:
        horas_estimadas = float(horas_estimadas)
        # Removemos "R$" e possíveis espaços, mantendo apenas os dígitos e o ponto decimal
        valor_hora = float(valor_hora.replace('R$', '').replace(' ', '').replace(',', '.'))  
    except ValueError:
        messagebox.showerror("Entradas inválidas", "Por favor, insira valores numéricos para horas estimadas e valor por hora.")
        return

    valor_total = horas_estimadas * valor_hora

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.image("template.png", x=0, y=0)
    
    pdf.text(115, 145, projeto)
    pdf.text(115, 160, prazo)
    pdf.text(115, 175, str(horas_estimadas))
    pdf.text(115, 190, f'R$ {valor_hora:.2f}')
    pdf.text(115, 205, f'R$ {valor_total:.2f}')

    try:
        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if filename:
            pdf.output(filename)
            messagebox.showinfo("PDF Salvo", f"PDF salvo como {filename}")
    except Exception as e:
        messagebox.showerror("Erro ao salvar", f"Ocorreu um erro ao salvar o PDF: {str(e)}")

# Criação da janela principal
root = tk.Tk()
root.title("Gerador de PDF de Projeto")
root.geometry("400x300")
root.configure(bg="#1e1e1e")

# Estilo ttk com tema escuro e clean
style = ttk.Style()
style.theme_use("clam")

style.configure("TEntry", background="#3a3a3a", foreground="#ffffff", fieldbackground="#3a3a3a", font=("Arial", 12), borderwidth=0)
style.configure("TButton", background="#5a5a5a", foreground="#ffffff", font=("Arial", 12), borderwidth=0)
style.map("TButton", background=[('active', '#707070')])

# Frame centralizado
frame = ttk.Frame(root, padding="20", style="TFrame")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Labels e entradas de dados
label_bg_color = "#1e1e1e"
label_fg_color = "#ffffff"

fields = [
    ("Nome do Projeto:", ""),
    ("Horas Estimadas:", ""),
    ("Valor por Hora:", ""),
    ("Prazo em Horas Úteis:", "")  # Alterado o texto da label Prazo
]

entry_projeto = None
entry_horas = None
entry_valor_hora = None
entry_prazo = None

for row, (label_text, default_value) in enumerate(fields):
    label = tk.Label(frame, text=label_text, fg=label_fg_color, bg=label_bg_color, font=("Arial", 12))
    label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
    
    entry = ttk.Entry(frame, width=30)
    entry.grid(row=row, column=1, padx=10, pady=5)
    
    if label_text == "Nome do Projeto:":
        entry_projeto = entry
    elif label_text == "Horas Estimadas:":
        entry_horas = entry
    elif label_text == "Valor por Hora:":
        entry_valor_hora = entry
        entry_valor_hora.bind("<KeyRelease>", lambda event, entry=entry_valor_hora: validar_valor_hora(entry.get(), entry))
    elif label_text == "Prazo em Horas Úteis:":  # Atualizei o nome da variável correspondente
        entry_prazo = entry

# Botão para gerar o PDF
btn_gerar_pdf = ttk.Button(frame, text="Gerar PDF", command=gerar_pdf)
btn_gerar_pdf.grid(row=row+1, column=0, columnspan=2, pady=20)

# Ajustar o estilo para cantos mais arredondados
style.configure("TFrame", borderwidth=2, relief="groove", background="#1e1e1e")

# Execução da janela
root.mainloop()
