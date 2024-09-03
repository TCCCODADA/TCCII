import matplotlib.pyplot as plt
import pandas_ta as ta
import yfinance as yf
import pandas as pd


# DADOS HISTORICOS
def hist_data(data_inicio, data_fim, lista_acoes): # FUNCAO PARA OBTERMOS OS DADOS HISTORICOS DAS ACOES INDICADAS NA LISTA

    for acao in lista_acoes:    
        data = yf.download(acao, start=data_inicio, end=data_fim) # baixa os dados historicos das acoes colocadas na lista "lista_acoes"

        data_df_pandas = pd.DataFrame(data) # transforma os dados baixados em um DataFrame pandas para podermos transforma-lo em um csv    
        data_df_pandas.to_csv("Base_dados/hist_"+acao) # transformando o df em um csv e salvando na pasta "Dados historicos"

# SMA
def MM_sma(lista_acoes):

    for acao in lista_acoes:
        df_sma = pd.read_csv("Base_dados/hist_"+acao)
        df_sma = df_sma.set_index('Date')
        df_sma.ta.sma(length=10, append=True) # calculando o 'SMA' onde o parametro lenght demonstra quando periodos para tras utilizaremos para calcula a média móvel

        df_sma.to_csv("Base_dados/hist_"+acao) # transformando o df em um csv e salvando na pasta "Dados historicos"

# EMA
def MM_ema(lista_acoes): # EMA tambem conhecida como Media Movel Exponencial

    for acao in lista_acoes:
        df_ema = pd.read_csv("Base_dados/hist_"+acao)
        df_ema.ta.ema(lenght=10, append=True)
        
        df_ema.to_csv("Base_dados/hist_"+acao)

# RSI
# def MM_rsi():

# MACD
def MM_macd(lista_acoes):

    short_window = 12
    long_window = 24 
    signal_window = 9

    for acao in lista_acoes:
        df = pd.read_csv("Base_dados/hist_"+acao)     
        

        #Cálculo das EMAs de curto e longo prazo
        df['EMA12'] = df['Close'].ewm(span=short_window, adjust=False).mean()
        df['EMA26'] = df['Close'].ewm(span=long_window, adjust=False).mean()
        
        # Cálculo da linha MACD
        df['MACD'] = df['EMA12'] - df['EMA26']
        
        # Cálculo da linha de sinal
        df['Signal_Line'] = df['MACD'].ewm(span=signal_window, adjust=False).mean()
        
        # Cálculo do histograma
        df['Histogram'] = df['MACD'] - df['Signal_Line']
        
        

        # Exemplo de DataFrame com preços de fechamento
        data = {'Close': [100, 102, 105, 103, 108, 110, 107, 105, 103, 102]}
        df = pd.DataFrame(data)

        # Aplicar o MACD
        # df = MM_macd(df)
        print(df)
        return df
        df_ema.to_csv("Base_dados/hist_"+acao)
lista_acoes = [    
    'PETR4.SA',    # Petrobras
    'TAEE11.SA',   # Taesa    
    'NVDA',        # Nvidia
    'BBAS3.SA',    # Bradesco
    'NFLX',        # Netflix     
    'EA',          # EA
    'TSLA']        # Tesla

data_inicio = '2020-01-01' # data de inicio do historico que voce deseja obter
data_fim = '2023-12-31'    # data final do perido para o historico
# FORMATO-> "AAAA-MM-DD" 
MM_macd(lista_acoes)
# Bollinger Bands
# def MM_bb():

# Average True Range
# def MM_atr():

# Estocastico
# def MM_estc():

# Dados fundamentalista
# def MM_fund():