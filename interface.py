import tkinter as tk
from tkinter import ttk
from buscar import grafo, a_estrela

nome_para_id = {p["nome"]: i for i, p in grafo.items()}


def calcular():
    origem = nome_para_id.get(cb_origem.get())
    destino = nome_para_id.get(cb_destino.get())

    if origem is None or destino is None:
        resultado.set("Selecione a origem e o destino.")
        return

    caminho, custo = a_estrela(origem, destino)
    if caminho is None:
        resultado.set("Não existe caminho entre os pontos.")
        return

    linhas = ["Melhor caminho (cruzamentos):"]
    linhas += [f"  {n + 1}. {grafo[i]['nome']}" for n, i in enumerate(caminho)]
    linhas.append(f"\nDistância total: {custo} m")
    resultado.set("\n".join(linhas))


janela = tk.Tk()
janela.title("Rotas em Floriano-PI (A*)")
janela.geometry("420x400")

nomes = list(nome_para_id.keys())

ttk.Label(janela, text="Origem (A):").pack(anchor="w", padx=10, pady=(10, 0))
cb_origem = ttk.Combobox(janela, values=nomes, state="readonly", width=45)
cb_origem.pack(padx=10)

ttk.Label(janela, text="Destino (B):").pack(anchor="w", padx=10, pady=(10, 0))
cb_destino = ttk.Combobox(janela, values=nomes, state="readonly", width=45)
cb_destino.pack(padx=10)

ttk.Button(janela, text="Calcular", command=calcular).pack(pady=15)

resultado = tk.StringVar()
ttk.Label(janela, textvariable=resultado, justify="left").pack(anchor="w", padx=10)

janela.mainloop()