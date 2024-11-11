import networkx as nx
from main import dados


def criar_grafo():

    """
    Cria um grafo direcionado representando as disciplinas e seus pré-requisitos.
    Cada nó representa uma disciplina, e cada aresta representa uma relação de pré-requisito.
    Os nós possuem atributos como nome, prioridade e semestre.
    Returns:
        grafo (DiGraph): Um grafo direcionado onde cada nó é uma disciplina e
                         cada aresta representa um pré-requisito.
    """

    # Criar o grafo direcionado
    grafo = nx.DiGraph()

    # Acessar o primeiro elemento da lista e obter as materias
    materias = dados[0]['materias']

    # Adicionar disciplinas ao grafo
    for materia in materias:
        codigo = materia['codigo']
        nome = materia['nome']
        pre_requisitos = materia['pre_requisitos']
        prioridade = materia.get('pre_requisitos_contagem', 0)  # Obtém a prioridade, assume 1 se não estiver definido
        semestre = materia.get('semestre', 1)

        # Adicionar nó com os dados da matéria
        grafo.add_node(codigo, nome=nome, pre=pre_requisitos, prioridade=prioridade, semestre=semestre)

        # Adicionar arestas para cada pré-requisito com o peso baseado na prioridade
        for pre_requisito in pre_requisitos:
            grafo.add_edge(pre_requisito, codigo, weight=prioridade)

    # Adicionar arestas para os pré-requisitos
    for materia in materias:
        for pre_requisito in materia['pre_requisitos']:
            grafo.add_edge(pre_requisito, materia['codigo'])
    
    return grafo

# Opcional: Exibir o grafo ou verificar nós e arestas
# print("Nós do grafo:", grafo.nodes(data=True))
# print("Arestas do grafo:", grafo.edges())


# disciplinas_completadas = {'F1'}  # Exemplo de disciplinas já cursadas
# semestre_atual = 3  # Suponhamos que estamos no terceiro semestre
# semestre_recomendado  = []  # Aqui armazenaremos as disciplinas do semestre



# Executar a função para obter o fluxo do semestre
# obter_disciplinas_semestre(grafo, disciplinas_completadas, semestre_atual)

# # Exibir as disciplinas recomendadas para o semestre, ordenadas por semestre e prioridade
# print("Disciplinas recomendadas para o semestre (por semestre e prioridade):")
# for codigo in semestre_recomendado:
#     # Obtém os dados da disciplina a partir do grafo
#     dados = grafo.nodes[codigo]
#     prioridade = dados.get('prioridade', 1)
#     semestre = dados.get('semestre', 1)
    
#     # Imprime o código da disciplina, o semestre e a sua prioridade
#     print(f"Disciplina: {codigo}, Semestre: {semestre}, Prioridade: {prioridade}")

from collections import deque

from collections import deque

# Função para determinar quais disciplinas podem ser cursadas, ordenadas por prioridade

def obter_disciplinas_semestre(grafo, disciplinas_completadas, semestre_atual):
    """
    Obtém uma lista de disciplinas recomendadas para o próximo semestre, utilizando BFS e respeitando os pré-requisitos.

    Args:
        grafo (DiGraph): O grafo com as disciplinas e seus pré-requisitos.
        disciplinas_completadas (set): Conjunto de códigos das disciplinas já cursadas.
        semestre_atual (int): O semestre em que o aluno está atualmente.

    Returns:
        list: Lista de disciplinas recomendadas, ordenadas por semestre e prioridade.
    """
    recomendadas = []
    visitados = set(disciplinas_completadas)
    fila = deque()

    # Adiciona disciplinas iniciais que o aluno pode cursar
    for codigo, dados in grafo.nodes(data=True):
        semestre = dados.get('semestre', 1)
        pre_requisitos = dados.get('pre', [])

        # Apenas disciplinas até o semestre atual, sem pré-requisitos ou com pré-requisitos já cumpridos
        if semestre <= semestre_atual and codigo not in visitados:
            if all(pre in disciplinas_completadas for pre in pre_requisitos):
                fila.append((codigo, dados))
                visitados.add(codigo)

    # Executa BFS para explorar disciplinas que se tornam elegíveis
    while fila:
        codigo, dados = fila.popleft()
        prioridade = dados.get('prioridade', 1)
        semestre = dados.get('semestre', 1)
        
        # Adiciona a disciplina à lista de recomendadas
        recomendadas.append((codigo, prioridade, semestre))

        # Adiciona as disciplinas dependentes (sucessores) na fila se se tornarem elegíveis
        for dependente in grafo.successors(codigo):
            if dependente not in visitados:
                dados_dependente = grafo.nodes[dependente]
                pre_requisitos = dados_dependente.get('pre', [])
                
                # Verifica se todos os pré-requisitos foram completados
                if all(pre in visitados for pre in pre_requisitos) and dados_dependente.get('semestre', 1) <= semestre_atual:
                    fila.append((dependente, dados_dependente))
                    visitados.add(dependente)

    # Ordena as disciplinas recomendadas por semestre (crescente) e prioridade (decrescente)
    recomendadas.sort(key=lambda x: (x[2], -x[1]))

    # Retorna apenas os códigos das disciplinas na ordem desejada
    return [codigo for codigo, _, _ in recomendadas]


import matplotlib.pyplot as plt

def visualizar_grafo(grafo):
    """
    Visualiza o grafo das disciplinas e seus pré-requisitos.
    Args:
        grafo (DiGraph): O grafo das disciplinas com pré-requisitos.
    """
    pos = nx.spring_layout(grafo)
    plt.figure(figsize=(12, 8))
    nx.draw(grafo, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold", edge_color="gray")
    edge_labels = nx.get_edge_attributes(grafo, "weight")
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels, font_size=8)
    plt.title("Grafo de Disciplinas e Pré-requisitos")
    plt.show()

def visualizar_arvore(grafo, ordem_visita):
    """
    Visualiza a árvore gerada a partir de uma busca BFS ou DFS.

    Args:
        grafo (DiGraph): O grafo original das disciplinas.
        ordem_visita (list): Lista de disciplinas visitadas na ordem de descoberta.
    """
    # Criar um subgrafo apenas com os nós e arestas da ordem de visita
    arvore = grafo.subgraph(ordem_visita).copy()

    # Gerar a visualização
    pos = nx.spring_layout(arvore)  # Layout para a árvore
    plt.figure(figsize=(10, 6))
    nx.draw(arvore, pos, with_labels=True, node_size=2000, node_color="lightgreen", font_size=10, font_weight="bold", edge_color="gray")
    edge_labels = nx.get_edge_attributes(arvore, "weight")
    nx.draw_networkx_edge_labels(arvore, pos, edge_labels=edge_labels, font_size=8)
    plt.title("Árvore de Dependências a Partir da Disciplina Inicial")
    plt.show()

from collections import deque

def bfs_dependentes(grafo, disciplina_inicial):
    """
    Realiza uma busca em largura (BFS) para encontrar disciplinas que têm a disciplina_inicial como pré-requisito.

    Args:
        grafo (DiGraph): O grafo das disciplinas.
        disciplina_inicial (str): O código da disciplina inicial para a busca.

    Returns:
        list: Lista de disciplinas que dependem da disciplina inicial, na ordem de descoberta.
    """
    visitados = set()
    fila = deque([disciplina_inicial])
    dependentes = []

    while fila:
        disciplina = fila.popleft()
        if disciplina not in visitados:
            visitados.add(disciplina)
            for dependente in grafo.successors(disciplina):  # Busca os nós que têm `disciplina` como pré-requisito
                if dependente not in visitados:
                    dependentes.append(dependente)
                    fila.append(dependente)
    
    return dependentes

def dfs_dependentes(grafo, disciplina_inicial):
    """
    Realiza uma busca em profundidade (DFS) para encontrar disciplinas que têm a disciplina_inicial como pré-requisito.

    Args:
        grafo (DiGraph): O grafo das disciplinas.
        disciplina_inicial (str): O código da disciplina inicial para a busca.

    Returns:
        list: Lista de disciplinas que dependem da disciplina inicial, na ordem de descoberta.
    """
    visitados = set()
    pilha = [disciplina_inicial]
    dependentes = []

    while pilha:
        disciplina = pilha.pop()
        if disciplina not in visitados:
            visitados.add(disciplina)
            for dependente in grafo.successors(disciplina):  # Busca os nós que têm `disciplina` como pré-requisito
                if dependente not in visitados:
                    dependentes.append(dependente)
                    pilha.append(dependente)

    return dependentes

if __name__ == "__main__":
    # Criar o grafo a partir dos dados
    grafo = criar_grafo()

    disciplinas_completadas = {"F1", "C1", "OO"} # alterar de acordo com as disciplinas cursadas
    semestre_atual = 3  

    recomendadas = obter_disciplinas_semestre(grafo, disciplinas_completadas, semestre_atual)
    print("Disciplinas recomendadas para o semestre atual:")
    for codigo in recomendadas:
        dados = grafo.nodes[codigo]
        print(f"Disciplina: {codigo}, Semestre: {dados.get('semestre', 1)}, Prioridade: {dados.get('prioridade', 1)}")

    # Solicitar que o usuário insira uma disciplina inicial
    disciplina_inicial = input("Digite o código da disciplina inicial: ")

    # Validar se a disciplina existe no grafo
    if disciplina_inicial not in grafo.nodes:
        print(f"A disciplina '{disciplina_inicial}' não existe no grafo.")
    else:
        # Mostrar o grafo completo
        print("Exibindo o grafo completo das disciplinas...")
        visualizar_grafo(grafo)

        bfs_resultado = bfs_dependentes(grafo, disciplina_inicial)
        print(f"Disciplinas alcançáveis por BFS a partir de '{disciplina_inicial}': {bfs_resultado}")


        dfs_resultado = dfs_dependentes(grafo, disciplina_inicial)
        print(f"Disciplinas alcançáveis por DFS a partir de '{disciplina_inicial}': {dfs_resultado}")

        # Mostrar as árvores resultantes
        print("Exibindo a árvore de dependências resultante do BFS...")
        visualizar_arvore(grafo, bfs_resultado)

        print("Exibindo a árvore de dependências resultante do DFS...")
        visualizar_arvore(grafo, dfs_resultado)

