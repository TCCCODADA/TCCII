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
def MM_rsi(lista_acoes):

    for acao in lista_acoes:
        df_rsi = pd.read_csv("Base_dados/hist_"+acao)
        df_rsi.ta.rsi()


# MACD
# def MM_macd(lista_acoes):

# Bollinger Bands
# def MM_bb():

# Average True Range
def MM_atr(lista_acoes): # AVERAGE TRUE RANGE (ATR) nos mostra a volatilidade de um ativo em um determinado periodo (HIGH vs LOW de um dia)

    for acao in lista_acoes:
        df_rsi = pd.read_csv("Base_dados/hist_"+acao)

        df_rsi.ta.atr(high = df_rsi['High'],
                      low = df_rsi['Low'],
                      close = df_rsi['Close'],
                      lenght = 10,
                      append=True)

        df_rsi.to_csv("Base_dados/hist_"+acao)


# Estocastico
def MM_estc(lista_acoes): # AQUI OBTEMOS O INDICADOR ESTOCASTICO, GERANDO DUAS COLUNAS

    for acao in lista_acoes:
        df_estc = pd.read_csv("Base_dados/hist_"+acao)

        stoch = ta.stoch(high=df_estc['High'],
                        low = df_estc['Low'],
                        close = df_estc['Close'],
                        k=14, # 14 PERIODOS PARA CALCULAR O "K" (REPRESENTA SE O PRECO DE FECHAMENTO ESTA ALTO OU BAIXO COMPARADO COM OS VALORES HISTORICOS NO PERIODO INDICADO)
                        d=3)  # 3 PERIODOS PARA CALCULA O "D" (MÉDIA MOVEL SIMPLES DE "K")
        
        df_estc['stoch_k'] = stoch["STOCHk_14_3_3"] # COLOCAMOS ESSES VALORES NO DF DA ACAO
        df_estc['stoch_d'] = stoch["STOCHd_14_3_3"]
        
        df_estc.to_csv("Base_dados/hist_"+acao)

# Dados fundamentalistas
# def MM_fund():