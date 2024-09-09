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
        df_sma = df_sma.set_index("Date")    
        df_sma.ta.sma(length = 10,
                      append = True) # calculando o 'SMA' onde o parametro lenght demonstra quando periodos para tras utilizaremos para calcula a média móvel

        df_sma.to_csv("Base_dados/hist_"+acao) # transformando o df em um csv e salvando na pasta "Dados historicos"

# EMA
def MM_ema(lista_acoes): # EMA tambem conhecida como Media Movel Exponencial

    for acao in lista_acoes:
        df_ema = pd.read_csv("Base_dados/hist_"+acao)
        df_ema.ta.ema(lenght = 10,
                      append = True)
        
        df_ema.to_csv("Base_dados/hist_"+acao)

# RSI
def MM_rsi(lista_acoes): # AQUI OBTEMOS O INDICADOR RSI (RELATIVE STRENGTH INDEX ou INDICE DE FORCA RELATIVA)

    """
    ESSE INDICADOR MEDE A VELOCIDADE E OS MOVIMENTOS DOS PREÇOS DE FECHAMENTO, SENDO BOM PARA DETECCAO DE REVERSOES DE PRECOS 
    """

    for acao in lista_acoes:
        df_rsi = pd.read_csv("Base_dados/hist_"+acao)
        df_rsi["RSI_10"] = ta.rsi(close = df_rsi["Close"], # UTILIZA A COLUNA DE FECHAMENTO
                                length = 10,
                                append = True)
    
        df_rsi.to_csv("Base_dados/hist_"+acao)


# MACD
# def MM_macd(lista_acoes):        

# Bollinger Bands
def MM_bb(lista_acoes): # BOLINGER BANDS nos ajuda a medir a volatilidade do ativo

    for acao in lista_acoes:
        df_bb = pd.read_csv("Base_dados/hist_"+acao)   
        
        df_bb.ta.bbands(close = df_bb['Close'],
                                length = 20,
                                append = True)        
        """
        ESTRUTURA DO INDICADOR:
            BBM(BOLLINGER BAND MIDDLE) = MEDIA MOVEL DO PRECO DE FECHAMENTO 
            BBU(BOLLINGER BAND UPPER) =  BBM + 2 DESVIOS PADRAO PARA CIMA
            BBL(BOLLINGER BAND LOWER) =  BBM + 2 DESVIOS PADRAO PARA BAIXO

        NOS RETORNA 5 COLUNAS:
            BBL_20_2.0 = RETORNA O "BBL" PARA 20 PERIODOS            
            BBM_20_2.0 = RETORNA O "BBM" PARA 20 PERIODOS
            BBU_20_2.0 = RETORNA O "BBU" PARA 20 PERIODOS
            BBB_20_2.0 = RETORNA A DIFERENCA PERCENTUAL ENTRE AS BANDAS SUPERIOR E INFERIOR (BANDWIDTH)
            BBP_20_2.0 = RETORNA A POSICAO RELATIVA DO PRECO DE FECHAMENTO EM RELACAO AS BANDAS SUPERIOR E INFERIOR, NORMALIZANDO O PRECO DENTRO
              DA FAIXA BBU - BBL
        """
        
        df_bb.to_csv("Base_dados/hist_"+acao)

# Average True Range
def MM_atr(lista_acoes): # AVERAGE TRUE RANGE (ATR) nos mostra a volatilidade de um ativo em um determinado periodo (HIGH vs LOW de um dia)

    for acao in lista_acoes:
        df_rsi = pd.read_csv("Base_dados/hist_"+acao)
        df_rsi.ta.atr(high = df_rsi['High'],
                      low = df_rsi['Low'],
                      close = df_rsi['Close'],
                      lenght = 10,
                      append = True)

        df_rsi.to_csv("Base_dados/hist_"+acao)


# Estocastico
def MM_estc(lista_acoes): # AQUI OBTEMOS O INDICADOR ESTOCASTICO, GERANDO DUAS COLUNAS

    for acao in lista_acoes:
        df_estc = pd.read_csv("Base_dados/hist_"+acao)
        stoch = ta.stoch(high=df_estc['High'],
                        low = df_estc['Low'],
                        close = df_estc['Close'],
                        k = 14, # 14 PERIODOS PARA CALCULAR O "K" (REPRESENTA SE O PRECO DE FECHAMENTO ESTA ALTO OU BAIXO COMPARADO COM OS VALORES HISTORICOS NO PERIODO INDICADO)
                        d = 3)  # 3 PERIODOS PARA CALCULA O "D" (MÉDIA MOVEL SIMPLES DE "K")
        
        df_estc['stoch_k'] = stoch["STOCHk_14_3_3"] # COLOCAMOS ESSES VALORES NO DF DA ACAO
        df_estc['stoch_d'] = stoch["STOCHd_14_3_3"]
        
        df_estc.to_csv("Base_dados/hist_"+acao)