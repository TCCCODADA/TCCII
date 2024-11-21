from p3Rede_GRU_Dropout_Dense_90 import Gru

BBAS3 = 'hist_BBAS3.csv'
EA = 'hist_EA.csv'
NFLX = 'hist_NFLX.csv'
NVDA = 'hist_NVDA.csv'
PETR4 = 'hist_PETR4.csv'
TAEE11 = 'hist_TAEE11.csv'

lista_arquivos2000 = [BBAS3, EA, NFLX, NVDA, PETR4, TAEE11]

Gru.GruCalcs(7, 1, 1, lista_arquivos2000)
Gru.GruCalcs(90, 1, 1, lista_arquivos2000)