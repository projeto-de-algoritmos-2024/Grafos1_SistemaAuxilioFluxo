import networkx as nx
from main import dados


def criar_grafo():
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


# Função para determinar quais disciplinas podem ser cursadas, ordenadas por prioridade
def obter_disciplinas_semestre(grafo, disciplinas_completadas, semestre_atual):
    semestre_recomendado  = []
    candidatas = []
    for codigo, dados in grafo.nodes(data=True):
        pre_requisitos = dados.get('pre', [])
        prioridade = dados.get('prioridade', 1)
        semestre = dados.get('semestre', 1)

        # Verifica se a disciplina não foi completada e se todos os pré-requisitos foram atendidos
        if codigo not in disciplinas_completadas and all(pre in disciplinas_completadas for pre in pre_requisitos):
            if semestre < semestre_atual:
                candidatas.append((codigo, prioridade, semestre))  # Adiciona a disciplina e sua prioridade
            elif semestre == semestre_atual:
                candidatas.append((codigo, prioridade, semestre))  # Adiciona as matérias do semestre atual também

   # Ordena as disciplinas primeiro por semestre (menor primeiro), depois por prioridade
    candidatas.sort(key=lambda x: (x[2], -x[1]))  # Ordena por semestre ascendente e prioridade descendente
    
    # Adiciona as disciplinas recomendadas ao semestre atual
    for codigo, prioridade, semestre in candidatas:
        semestre_recomendado.append(codigo)

    return semestre_recomendado

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



