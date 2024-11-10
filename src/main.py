import json
import pandas as pd

# Caminho do arquivo JSON na pasta `data`
caminho_arquivo = '../data/materias_software.json'

# Carregar o JSON
with open(caminho_arquivo, 'r', encoding='utf-8') as file:
    dados = json.load(file)

# Transformar o JSON em um DataFrame
disciplinas_software = pd.json_normalize(dados, record_path=['materias'])

contagem_pre_requisitos = {materia['codigo']: 0 for materia in disciplinas_software.to_dict(orient='records')}

# Contar quantas vezes cada matéria aparece como pré-requisito
for materia in disciplinas_software.to_dict(orient='records'):
    for pre_requisito in materia['pre_requisitos']:
        if pre_requisito in contagem_pre_requisitos:
            contagem_pre_requisitos[pre_requisito] += 1

# Adicionar a contagem de pré-requisitos ao DataFrame
disciplinas_software['pre_requisitos_contagem'] = disciplinas_software['codigo'].map(contagem_pre_requisitos)

disciplinas_obrigatorias = disciplinas_software[disciplinas_software['obrigatorio'] == "1"]
disciplinas_nao_obrigatorias = disciplinas_software[disciplinas_software['obrigatorio'] == "0"]

# Atualizar o dicionário 'dados' para incluir a contagem de pré-requisitos
for materia in dados[0]['materias']:
    materia['pre_requisitos_contagem'] = contagem_pre_requisitos.get(materia['codigo'], 0)

# Salvar o JSON atualizado de volta ao arquivo
with open(caminho_arquivo, 'w', encoding='utf-8') as file:
    json.dump(dados, file, ensure_ascii=False, indent=4)

# print(disciplinas_software)


