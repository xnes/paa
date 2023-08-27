
import pandas as pd
from IPython.display import display
import re

columbia_db = pd.read_csv('Disease-Symptom-Knowledge-Database-Columbia-edu.csv', sep=';')
columbia_db['Disease'] = columbia_db['Disease'].fillna(method='ffill') # Preenche os valores nulos com o valor da linha anterior
columbia_db['Disease'] = columbia_db['Disease'].apply(lambda x: re.sub(r'UMLS:C\d+_', '', x) if pd.notnull(x) else x) # Remove o prefixo UMLS:Código_
columbia_db['Symptom'] = columbia_db['Symptom'].apply(lambda x: re.sub(r'UMLS:C\d+_', '', x) if pd.notnull(x) else x) # Remove o prefixo UMLS:Código_
columbia_db = columbia_db.drop(columns=['Count of Disease Occurrence']) # Remove colunas desnecessárias
columbia_db = columbia_db.dropna() # Remove linhas com valores nulos
display(columbia_db.head())
print('Número de doenças:', len(columbia_db['Disease'].unique()), '\nNúmero de sintomas:', len(columbia_db['Symptom'].unique()))


import networkx as nx
import matplotlib.pyplot as plt

# Criando um grafo direcionado
G = nx.DiGraph()

for i, linha in columbia_db.iterrows():
    G.add_node(linha['Disease'], color="red")
    G.add_node(linha['Symptom'], color="yellow")
    G.add_edge(linha['Symptom'], linha['Disease'])

# Obtendo a lista de cores dos nós
node_colors = [data["color"] for _, data in G.nodes(data=True)]

# Aumentar o tamanho da área de exibição
plt.figure(figsize=(15, 9))  # Definindo o tamanho da figura (largura x altura)

# Desenhando o grafo
pos = nx.spring_layout(G, scale=0.6)  # Layout para a visualização
nx.draw(G, pos, with_labels=True, node_size=1000, node_color=node_colors, font_size=10, font_color="black") #, font_weight="bold", arrowsize=20)
plt.show()