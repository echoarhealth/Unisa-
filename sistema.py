import csv
from datetime import datetime
from busca_ordenacao import (
    busca_sequencial,
    busca_binaria,
    ordenar_insercao,
    enfileirar_lote,
    desenfileirar_lote,
)

ARQUIVO_CSV = "descartes_elixo.csv"
CAMPOS = ["protocolo", "data", "categoria", "peso_kg", "status"]
CATEGORIAS_VALIDAS = [
    "pilhas/baterias",
    "celulares/tablets",
    "computadores/perifericos",
    "cabos/acessorios",
    "eletroportateis",
]

descartes = []
fila_destinacao = []


# --- Persistência de Dados ---

def carregar_dados():
    """Lê os registros salvos no arquivo CSV ao iniciar o programa."""
    descartes.clear()
    fila_destinacao.clear()
    try:
        with open(ARQUIVO_CSV, mode="r", newline="", encoding="utf-8") as arq:
            leitor = csv.DictReader(arq)
            for linha in leitor:
                registro = {
                    "protocolo": int(linha["protocolo"]),
                    "data": linha["data"],
                    "categoria": linha["categoria"],
                    "peso_kg": float(linha["peso_kg"]),
                    "status": linha["status"],
                }
                descartes.append(registro)
                if registro["status"] == "aguardando_coleta":
                    enfileirar_lote(fila_destinacao, registro)
    except FileNotFoundError:
        pass


def salvar_dados():
    """Grava a lista de registros atualizada no arquivo CSV."""
    with open(ARQUIVO_CSV, mode="w", newline="", encoding="utf-8") as arq:
        escritor = csv.DictWriter(arq, fieldnames=CAMPOS)
        escritor.writeheader()
        escritor.writerows(descartes)


# --- Funções de Validação ---

def ler_inteiro_positivo(mensagem):
    while True:
        entrada = input(mensagem).strip()
        if entrada.isdigit() and int(entrada) > 0:
            return int(entrada)
        print("Erro: informe um número inteiro positivo válido.")


def ler_real_positivo(mensagem):
    while True:
        entrada = input(mensagem).strip().replace(",", ".")
        try:
            valor = float(entrada)
            if valor > 0:
                return valor
            print("Erro: o peso deve ser maior que zero.")
        except ValueError:
            print("Erro: digite um valor numérico válido para o peso.")


def ler_data_valida(mensagem):
    while True:
        data_str = input(mensagem).strip()
        try:
            datetime.strptime(data_str, "%d/%m/%Y")
            return data_str
        except ValueError:
            print("Erro: formato inválido. Utilize dd/mm/aaaa (ex.: 18/11/2026).")


def exibir_tabela(lista_registros):
    if not lista_registros:
        print("Nenhum registro encontrado.")
        return
    print("-" * 78)
    print(f"{'PROT.':<8} | {'DATA':<12} | {'CATEGORIA':<25} | {'PESO (kg)':<10} | {'STATUS'}")
    print("-" * 78)
    for r in lista_registros:
        print(
            f"{r['protocolo']:<8} | {r['data']:<12} | {r['categoria']:<25} | "
            f"{r['peso_kg']:<10.2f} | {r['status']}"
        )
    print("-" * 78)


# --- TELA 2: Registro de Descarte ---

# --- TELA 2: Registro de Descarte ---

def tela_cadastrar():
    print("\n=== [TELA 2] REGISTRO DE DESCARTE DE E-LIXO ===")
    protocolo = ler_inteiro_positivo("Número do protocolo (único): ")

    pos, _ = busca_sequencial(descartes, protocolo)
    if pos != -1:
        print(f"Atenção: já existe um registro com o protocolo {protocolo}.")
        return

    data = ler_data_valida("Data da entrega (dd/mm/aaaa): ")

    print("\nCategorias aceitas:")
    for idx, cat in enumerate(CATEGORIAS_VALIDAS, start=1):
        print(f"  {idx} - {cat}")

    while True:
        escolha = input("Escolha o número (1 a 5) ou digite o nome da categoria: ").strip().lower()
        if escolha.isdigit() and 1 <= int(escolha) <= len(CATEGORIAS_VALIDAS):
            categoria = CATEGORIAS_VALIDAS[int(escolha) - 1]
            break
        elif escolha in CATEGORIAS_VALIDAS:
            categoria = escolha
            break
        else:
            print("Categoria inválida. Digite um número de 1 a 5 ou o nome exato listado acima.")

    peso = ler_real_positivo("Peso do lote (kg): ")

    novo_registro = {
        "protocolo": protocolo,
        "data": data,
        "categoria": categoria,
        "peso_kg": peso,
        "status": "aguardando_coleta",
    }

    descartes.append(novo_registro)
    enfileirar_lote(fila_destinacao, novo_registro)
    salvar_dados()
    print(f"Sucesso: protocolo {protocolo} ({categoria}) cadastrado e inserido na fila de destinação.")
# --- TELA 3: Rastreamento de Protocolo (Busca Sequencial vs. Binária) ---

def tela_buscar():
    print("\n=== [TELA 3] RASTREAMENTO DE PROTOCOLO ===")
    if not descartes:
        print("Base de dados vazia.")
        return

    protocolo = ler_inteiro_positivo("Digite o protocolo para rastrear: ")

    # 1. Execução da Pesquisa Sequencial na lista original
    idx_seq, comp_seq = busca_sequencial(descartes, protocolo)

    # 2. Ordenação prévia por protocolo e execução da Pesquisa Binária
    ordenados = ordenar_insercao(descartes, "protocolo", decrescente=False)
    idx_bin, comp_bin = busca_binaria(ordenados, protocolo)

    if idx_bin != -1:
        print("\nLote localizado com sucesso:")
        exibir_tabela([ordenados[idx_bin]])
    else:
        print(f"\nProtocolo {protocolo} não encontrado no sistema.")

    print(f"Comparações realizadas -> Pesquisa Sequencial: {comp_seq} | Pesquisa Binária: {comp_bin}")


# --- TELA 4: Ranking de Impacto (Ordenação Manual por Peso) ---

def tela_ranking():
    print("\n=== [TELA 4] RANKING DE IMPACTO AMBIENTAL (MAIOR PARA MENOR PESO) ===")
    if not descartes:
        print("Base de dados vazia.")
        return

    ranking_peso = ordenar_insercao(descartes, "peso_kg", decrescente=True)
    exibir_tabela(ranking_peso)


# --- TELA 5: Fila de Destinação e Relatório Ambiental ---

def tela_fila_e_relatorio():
    print("\n=== [TELA 5] FILA DE DESTINAÇÃO E RELATÓRIO AMBIENTAL ===")
    print("1 - Visualizar fila de lotes aguardando coleta")
    print("2 - Despachar próximo lote da fila para recicladora (FIFO)")
    print("3 - Gerar relatório consolidado por categoria")
    sub = input("Escolha uma opção: ").strip()

    if sub == "1":
        print(f"\nTotal na fila de espera: {len(fila_destinacao)} lote(s)")
        exibir_tabela(fila_destinacao)

    elif sub == "2":
        lote = desenfileirar_lote(fila_destinacao)
        if lote is None:
            print("A fila de destinação está vazia.")
        else:
            lote["status"] = "enviado_reciclagem"
            salvar_dados()
            print(f"Lote protocolo {lote['protocolo']} ({lote['peso_kg']:.2f} kg de {lote['categoria']}) enviado à recicladora!")

    elif sub == "3":
        if not descartes:
            print("Sem dados para gerar relatório.")
            return

        total_geral = sum(r["peso_kg"] for r in descartes)
        media_geral = total_geral / len(descartes)
        maior = max(descartes, key=lambda x: x["peso_kg"])
        menor = min(descartes, key=lambda x: x["peso_kg"])

        print("\n--- RELATÓRIO AMBIENTAL CONSOLIDADO ---")
        print(f"Total de descartes registrados : {len(descartes)}")
        print(f"Peso total arrecadado          : {total_geral:.2f} kg")
        print(f"Peso médio por lote            : {media_geral:.2f} kg")
        print(f"Maior lote                     : Prot. {maior['protocolo']} ({maior['peso_kg']:.2f} kg - {maior['categoria']})")
        print(f"Menor lote                     : Prot. {menor['protocolo']} ({menor['peso_kg']:.2f} kg - {menor['categoria']})")
        print("\nDistribuição por Categoria:")
        for cat in CATEGORIAS_VALIDAS:
            itens_cat = [r["peso_kg"] for r in descartes if r["categoria"] == cat]
            soma_cat = sum(itens_cat)
            print(f"  - {cat:<25}: {len(itens_cat):>2} lote(s) | {soma_cat:>7.2f} kg")
    else:
        print("Opção inválida.")


# --- TELA 1: Menu Principal ---

def menu_principal():
    carregar_dados()
    while True:
        peso_acumulado = sum(r["peso_kg"] for r in descartes)
        print("\n" + "=" * 62)
        print("  SISTEMA DE GESTÃO DE E-LIXO COMUNITÁRIO (TELA 1 - PRINCIPAL)")
        print(f"  Registros: {len(descartes)} | Na Fila: {len(fila_destinacao)} | Acumulado: {peso_acumulado:.2f} kg")
        print("=" * 62)
        print("  1 - Registrar novo descarte (Tela 2)")
        print("  2 - Listar todos os descartes")
        print("  3 - Rastrear protocolo (Busca Sequencial e Binária - Tela 3)")
        print("  4 - Ranking de impacto por peso (Tela 4)")
        print("  5 - Fila de destinação e Relatório ambiental (Tela 5)")
        print("  0 - Encerrar sistema")
        print("=" * 62)

        opcao = input("Selecione uma opção: ").strip()

        if opcao == "1":
            tela_cadastrar()
        elif opcao == "2":
            print("\n--- LISTAGEM GERAL DE DESCARTES ---")
            exibir_tabela(descartes)
        elif opcao == "3":
            tela_buscar()
        elif opcao == "4":
            tela_ranking()
        elif opcao == "5":
            tela_fila_e_relatorio()
        elif opcao == "0":
            print("Sistema encerrado. Dados salvos com segurança.")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_principal()
