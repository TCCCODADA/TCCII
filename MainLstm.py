from mainModelos import Modelo

BBAS3 = 'hist_BBAS3.csv'
EA = 'hist_EA.csv'
NFLX = 'hist_NFLX.csv'
NVDA = 'hist_NVDA.csv'
PETR4 = 'hist_PETR4.csv'
TAEE11 = 'hist_TAEE11.csv'

lista_arquivos2000 = [BBAS3, EA, NFLX, NVDA, PETR4, TAEE11]
listinha = [BBAS3]

Modelo.Calculos("LSTM", 90, 1, 5, listinha)
# Lstm.LstmCalcs(7, 5, 15, listinha)
# Lstm.LstmCalcs(90, 5, 15, listinha)
# Lstm.LstmCalcs(7, 5, 200, listinha)
# Lstm.LstmCalcs(90, 5, 200, listinha)