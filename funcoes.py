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
# def MM_macd():

# Bollinger Bands
# def MM_bb():

# Average True Range
# def MM_atr():

# Estocastico
# def MM_estc():

# Dados fundamentalista
# def MM_fund():