from p3Rede_Conv1d_Dropout_Flatten_Dense_90 import Conv1d


BBAS3 = 'hist_BBAS3.csv'
EA = 'hist_EA.csv'
NFLX = 'hist_NFLX.csv'
NVDA = 'hist_NVDA.csv'
PETR4 = 'hist_PETR4.csv'
TAEE11 = 'hist_TAEE11.csv'

lista_arquivos2000 = [BBAS3, EA, NFLX, NVDA, PETR4, TAEE11]

#Conv1d.Conv1dCalcs(7, 1, 1, lista_arquivos2000)
Conv1d.Conv1dCalcs(90, 2, 5, lista_arquivos2000)
