import os
import sys

# Diretório raiz do projeto
raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
caminho_pasta_codigos = os.path.join(raiz, "Códigos_Modelos")
sys.path.append(caminho_pasta_codigos)

from mainModelos import Modelo

caminho_pasta_dados = os.path.join(raiz, "Base_dados")

BBAS3 = f'{caminho_pasta_dados}/hist_BBAS3.csv'
EA = f'{caminho_pasta_dados}/hist_EA.csv'
NFLX = f'{caminho_pasta_dados}/hist_NFLX.csv'
NVDA = f'{caminho_pasta_dados}/hist_NVDA.csv'
PETR4 = f'{caminho_pasta_dados}/hist_PETR4.csv'
TAEE11 = f'{caminho_pasta_dados}/hist_TAEE11.csv'

lista_arquivos2000 = [BBAS3, EA, NFLX, NVDA, PETR4, TAEE11]
listinha = [BBAS3]

Modelo.Calculos("LSTM", 90, 1, 5, listinha)
# Lstm.LstmCalcs(7, 5, 15, listinha)
# Lstm.LstmCalcs(90, 5, 15, listinha)
# Lstm.LstmCalcs(7, 5, 200, listinha)
# Lstm.LstmCalcs(90, 5, 200, listinha)