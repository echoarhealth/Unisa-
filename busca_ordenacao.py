# Módulo de algoritmos de busca, ordenação manual e estrutura de fila

def busca_sequencial(registros, protocolo):
    """
    Percorre a lista item a item até localizar o protocolo.
    Retorna uma tupla (indice, comparacoes). Se não encontrar, indice = -1.
    """
    comparacoes = 0
    for i in range(len(registros)):
        comparacoes += 1
        if registros[i]["protocolo"] == protocolo:
            return i, comparacoes
    return -1, comparacoes


def busca_binaria(registros_ordenados, protocolo):
    """
    Divide a lista previamente ordenada por 'protocolo' ao meio a cada passo.
    Retorna uma tupla (indice, comparacoes). Se não encontrar, indice = -1.
    """
    inicio = 0
    fim = len(registros_ordenados) - 1
    comparacoes = 0

    while inicio <= fim:
        meio = (inicio + fim) // 2
        comparacoes += 1
        valor_meio = registros_ordenados[meio]["protocolo"]

        if valor_meio == protocolo:
            return meio, comparacoes
        elif valor_meio < protocolo:
            inicio = meio + 1
        else:
            fim = meio - 1

    return -1, comparacoes


def busca_binaria_recursiva(registros_ordenados, protocolo, inicio, fim):
    """
    Versão recursiva da pesquisa binária.
    Retorna o índice do registro ou -1 caso não exista.
    """
    if inicio > fim:
        return -1

    meio = (inicio + fim) // 2
    valor_meio = registros_ordenados[meio]["protocolo"]

    if valor_meio == protocolo:
        return meio
    elif valor_meio < protocolo:
        return busca_binaria_recursiva(registros_ordenados, protocolo, meio + 1, fim)
    else:
        return busca_binaria_recursiva(registros_ordenados, protocolo, inicio, meio - 1)


def ordenar_insercao(registros, chave, decrescente=False):
    """
    Implementação manual do método Insertion Sort (sem uso de sorted/sort).
    Preserva a lista original operando sobre uma cópia.
    """
    lista = registros[:]
    for i in range(1, len(lista)):
        atual = lista[i]
        j = i - 1

        if not decrescente:
            while j >= 0 and lista[j][chave] > atual[chave]:
                lista[j + 1] = lista[j]
                j -= 1
        else:
            while j >= 0 and lista[j][chave] < atual[chave]:
                lista[j + 1] = lista[j]
                j -= 1

        lista[j + 1] = atual
    return lista


# --- Estrutura de Dados Avançada: Fila (FIFO) para Destinação de Lotes ---

def enfileirar_lote(fila, registro):
    """Adiciona um lote de e-lixo ao final da fila de destinação."""
    fila.append(registro)


def desenfileirar_lote(fila):
    """Remove e retorna o primeiro lote da fila (FIFO) para envio à recicladora."""
    if len(fila) == 0:
        return None
    return fila.pop(0)