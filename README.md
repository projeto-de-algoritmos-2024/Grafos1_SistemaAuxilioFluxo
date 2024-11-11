# Sistema de Auxilio ao Fluxo 

Projeto desenvolvido para a disciplina de Projeto de Algoritmos, ministrada pelo professor Mauricio Serrano. O objetivo deste projeto é auxiliar os alunos na escolha das disciplinas para o próximo semestre, considerando as matérias já cursadas anteriormente.

## Contribuidores
<center>
<table style="margin-left: auto; margin-right: auto;">
    <tr>
        <td align="center">
            <a href="https://github.com/Hellen159">
                <img style="border-radius: 50%;" src="https://github.com/Hellen159.png" width="150px;"/>
                <h5 class="text-center"> <br> Hellen Faria Matrícula: 202016480 </h5>
            </a>
        </td>
      <td align="center">
            <a href="https://github.com/deboracaires">
                <img style="border-radius: 50%;" src="https://github.com/deboracaires.png" width="150px;"/>
                <h5 class="text-center"> <br> Debora Caires Matrícula: 222015103</h5>
            </a>
        </td>
    </tr>
</table>
    
## Estrutura do Projeto 
   A estrutura do projeto é composta por: 
   1. **main.py**: Script principal do projeto. Ele permite que o usuário selecione uma disciplina inicial, visualize o grafo completo e explore as disciplinas disponíveis usando busca em largura (BFS) e busca em profundidade (DFS). O script também exibe o tempo de execução dessas buscas e recomenda disciplinas com base no semestre e nos pré-requisitos.
   2. **grafo.py**: Define funções para criação do grafo das disciplinas e funções auxiliares, como obter_disciplinas_semestre, que recomenda disciplinas para o próximo semestre com base em uma lógica de BFS. Também possui a função visualizar_grafo para exibir o grafo das disciplinas e seus pré-requisitos.
   3. **interface.py**: Contém uma interface gráfica utilizando Tkinter, permitindo que o usuário selecione as disciplinas já cursadas e visualize recomendações de disciplinas para o próximo semestre.
   4. **materias_software.json**: Arquivo de dados contendo todas as disciplinas do curso de software. Cada disciplina possui informações como o código, nome, semestre, pré-requisitos, obrigatoriedade e prioridade.

## Como executar o projeto
1. Pré-requisitos
Certifique-se de que você possui o Python 3 instalado. Para o projeto, as bibliotecas networkx e matplotlib são necessárias. Você pode instalá-las com:

```pip install networkx matplotlib```

2. Executar o Script
   
```pythom src/grafo.py```
ou
```python src/interface.py```

Ao executar o arquivo **grafo.py** o usuário será solicitado a inserir o código de uma disciplina inicial e então o sistema exibirá o grafo completo das disciplinas e os pré-requisitos.
Além disso, no próprio código o usuário pode inserir quais disciplinas cursou e será exibido as recomendações de disciplinas que o usuário pode cursar. Executando o arquivo **interface.py**, o usuário poderá visualizar melhor o sistema de recomendação das disciplinas.

