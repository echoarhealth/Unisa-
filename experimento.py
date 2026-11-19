import random
import time
from busca_ordenacao import busca_sequencial, busca_binaria, ordenar_insercao


def executar_experimento():
    tamanhos = [100, 1000, 10000]
    categorias = ["pilhas/baterias", "celulares/tablets", "computadores/perifericos"]

    print(f"{'N (Registros)':<15} | {'Comp. Seq.':<12} | {'Tempo Seq. (ms)':<16} | {'Comp. Bin.':<12} | {'Tempo Bin. (ms)':<16}")
    print("-" * 80)

    for n in tamanhos:
        # Gera N registros fictícios com protocolos únicos embaralhados
        protocolos = random.sample(range(1000, 1000 + n * 10), n)
        base = [
            {
                "protocolo": p,
                "data": "18/11/2026",
                "categoria": random.choice(categorias),
                "peso_kg": round(random.uniform(0.5, 25.0), 2),
                "status": "aguardando_coleta",
            }
            for p in protocolos
        ]

        # Ordena uma vez para habilitar a pesquisa binária
        base_ordenada = ordenar_insercao(base, "protocolo")

        # Testa 100 buscas aleatórias (metade existente, metade inexistente) para média estatística
        alvos = random.sample(protocolos, 50) + [99999999 + i for i in range(50)]

        total_comp_seq = 0
        inicio_seq = time.perf_counter()
        for alvo in alvos:
            _, c_seq = busca_sequencial(base, alvo)
            total_comp_seq += c_seq
        tempo_seq_ms = (time.perf_counter() - inicio_seq) * 1000

        total_comp_bin = 0
        inicio_bin = time.perf_counter()
        for alvo in alvos:
            _, c_bin = busca_binaria(base_ordenada, alvo)
            total_comp_bin += c_bin
        tempo_bin_ms = (time.perf_counter() - inicio_bin) * 1000

        media_seq = total_comp_seq / len(alvos)
        media_bin = total_comp_bin / len(alvos)

        print(
            f"{n:<15} | {media_seq:<12.1f} | {tempo_seq_ms:<16.4f} | "
            f"{media_bin:<12.1f} | {tempo_bin_ms:<16.4f}"
        )


if __name__ == "__main__":
    executar_experimento()