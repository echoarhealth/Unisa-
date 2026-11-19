# Sistema de Gerenciamento e Rastreamento de Resíduos Eletrônicos (E-Lixo)

Projeto Integrador: **Laboratório de Programação** — Universidade Santo Amaro (**UNISA**)  
Curso Superior de Tecnologia em Gestão da Tecnologia da Informação

## Autor
* **Nome:** Renato dos Santos Rocha  
* **RA:** 6109144  
* **Orientador:** Prof. Me. Patrick Araújo  

---

## Sobre o Projeto
Aplicação desenvolvida em **Python 3** para o controle, rastreamento e gestão de descartes de lixo eletrônico em pontos de coleta comunitários. O sistema opera em interface de terminal estruturada em 5 telas funcionais e utiliza persistência de dados em arquivo CSV (`descartes_elixo.csv`).

### Funcionalidades Principais
1. **Menu Principal (Tela 1):** Painel com total de registros, lotes aguardando na fila e massa acumulada (kg).
2. **Registro de Descarte (Tela 2):** Cadastro de lotes com validação de protocolo único, data (`dd/mm/aaaa`), categoria fixa (5 tipos de resíduos) e peso positivo.
3. **Rastreamento de Protocolo (Tela 3):** Consulta comparativa utilizando **Pesquisa Sequencial** e **Pesquisa Binária**, exibindo o número de comparações realizadas.
4. **Ranking de Impacto Ambiental (Tela 4):** Ordenação decrescente por peso implementada manualmente via **Insertion Sort** (Ordenação por Inserção).
5. **Fila de Destinação e Relatório (Tela 5):** Controle de expedição para recicladoras em estrutura de **Fila (FIFO)** e geração de relatório consolidado por categoria.

---

## Estrutura de Arquivos
* `sistema.py`: Programa principal contendo as 5 telas, validações de entrada, manipulação de fila e persistência em CSV.
* `busca_ordenacao.py`: Módulo com implementações manuais de pesquisa sequencial, pesquisa binária (iterativa e recursiva), ordenação por inserção e operações de fila.
* `experimento.py`: Script de avaliação experimental de desempenho (comparações médias e tempo de execução para bases de 100, 1.000 e 10.000 registros).

---

## Como Executar
Certifique-se de ter o **Python 3** instalado e mantenha os três arquivos na mesma pasta. No terminal, execute:

```bash
# Para iniciar o sistema principal
python3 sistema.py

# Para executar o experimento de desempenho
python3 experimento.py
