import numpy as np                  # Biblioteca para manipulação de arrays e operações matemáticas eficientes.
import pandas as pd                 # Biblioteca para manipulação e análise de dados, especialmente útil para trabalhar com dados em tabelas (DataFrames).
import matplotlib.pyplot as plt     # Biblioteca para criar gráficos e visualizações de dados.
import matplotlib.dates as mdates   # Biblioteca para manipulação e formatação de datas e tempos em gráficos matplotlib.
import tensorflow as tf             # Biblioteca para construir e treinar redes neurais e outros modelos de Machine Learning.
import sklearn                      # Biblioteca para tarefas de Machine Learning, incluindo pré-processamento de dados, modelos e métricas de avaliação.

from tensorflow.keras.models import Sequential                                  # Classe para criar um modelo sequencial (camada a camada) de rede neural.
from tensorflow.keras.layers import Dense, Dropout, Conv1D, Flatten                         # Importa camadas para a rede neural. Dense cria uma camada totalmente conectada, Dropout ajuda a prevenir overfitting, e LSTM é uma camada recorrente utilizada para processamento de sequências (útil em séries temporais).
from sklearn.preprocessing import MinMaxScaler                                  # Classe para normalizar os dados, escalando-os para um intervalo entre 0 e 1, útil para melhorar o desempenho dos modelos.
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score   # Importa as funções mean_absolute_error (MAE): Erro Médio Absoluto, média dos erros absolutos.
                                                                                # mean_squared_error (MSE): Erro Quadrático Médio, média dos erros ao quadrado.
                                                                                # r2_score (R²): Coeficiente de Determinação, mede a qualidade do ajuste do modelo.

import os

caminho_pasta = 'Base_dados'
lista_arquivos = [arquivo for arquivo in os.listdir(caminho_pasta) if os.path.isfile(os.path.join(caminho_pasta, arquivo))]

for arq in lista_arquivos:
    # Carregar dados
    df = pd.read_csv(f'Base_dados/{arq}', parse_dates=['Date'])
    df = df.sort_values('Date')

    # Defina o caminho da nova pasta que você quer criar
    caminho = f'Bases_Rede/{arq}'

    # Cria a pasta se ela não existir
    if not os.path.exists(caminho):
        os.makedirs(caminho)

    # Coluna "OPEN" será utilizada para realizar as previsões
    base_treinamento = df.iloc[:, 1:2].values

    # Pré-Processamento - Normalizar valores
    normalizador = MinMaxScaler(feature_range=(0, 1))
    base_treinamento_normalizada = normalizador.fit_transform(base_treinamento)

    X = [] # Previsores
    y = [] # Preços Reais

    for i in range(90, len(base_treinamento_normalizada)):  # 90 Preços Anteriores para prever o preço atual
        X.append(base_treinamento_normalizada[i - 90:i, 0])
        y.append(base_treinamento_normalizada[i, 0])

    X, y = np.array(X), np.array(y)

    # ===== ESTRUTURA DA REDE NEUREAL RECORRENTE===== #
    regressor = Sequential()

    # 1ª Camada de Convolução 1D
    regressor.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(X.shape[1], 1)))
    regressor.add(Dropout(0.2))

    # 2ª Camada de Convolução 1D
    regressor.add(Conv1D(filters=32, kernel_size=3, activation='relu'))
    regressor.add(Dropout(0.2))

    # 3ª Camada de Convolução 1D
    regressor.add(Conv1D(filters=16, kernel_size=3, activation='relu'))
    regressor.add(Dropout(0.2))

    # Flatten para achatar a saída da Conv1D
    regressor.add(Flatten())

    # Camada Dense (Totalmente Conectada)
    regressor.add(Dense(units=1, activation='linear'))

    camadas = []
    camadas.append("Conv1D")
    camadas.append("Dropout")
    camadas.append("Flatten")
    camadas.append("Dense")

    # Compilação do modelo
    regressor.compile(optimizer='rmsprop', loss='mean_squared_error', metrics=['mean_absolute_error'])

    # ========== Treinamento ========== #
    print(f"\nIniciando Treinamento: {arq}")
    treinamento = regressor.fit(X, y, epochs=50, batch_size=32)
    epoca = len(treinamento.epoch)

    # Acessando o valor do mean_absolute_error da última epoch
    valor_mean_absolute_error = treinamento.history['mean_absolute_error'][-1]

    # ========== PREVISÕES DOS PREÇOS DAS AÇÕES ========== #
    entradas = base_treinamento_normalizada[-90:].reshape(-1, 1)

    X_teste = []
    for i in range(5):  # Prever os próximos 5 dias úteis
        X_teste.append(entradas[-90:, 0])
        entrada = regressor.predict(np.array(X_teste[-1]).reshape(1, 90, 1))
        entradas = np.append(entradas, entrada).reshape(-1, 1)

    previsoes = normalizador.inverse_transform(entradas[-5:])

    # 1. Mean Absolute Error (MAE)
    mae = mean_absolute_error(y[-5:], previsoes)
    print(f"{arq} - Erro Médio Absoluto - Mean Absolute Error (MAE): {mae}")

    # 2. Mean Squared Error (MSE)
    mse = mean_squared_error(y[-5:], previsoes)
    print(f"{arq} - Erro Quadrático Médio - Mean Squared Error (MSE): {mse}")

    # 3. R² Score (Coeficiente de Determinação)
    r2 = r2_score(y[-5:], previsoes)
    print(f"{arq} - Coeficiente de Determinação - R² Score: {r2}")

    # 4. Mean Absolute Percentage Error (MAPE)
    mape = np.mean(np.abs((y[-5:] - previsoes) / y[-5:])) * 100
    print(f"{arq} - Erro Percentual Absoluto Médio - Mean Absolute Percentage Error (MAPE): {mape:.2f}%")

    # 5. Acurácia
    acuracia = 100 - mape
    print(f"{arq} - Acurácia: {acuracia:.2f}%")

    # 6. Mean Absolute Error
    print(f'Mean Absolute Error da Última Epoch: {valor_mean_absolute_error:.4f}')

    # Garantir que a coluna 'Date' esteja no formato datetime
    datas_previsao = pd.date_range(df['Date'].iloc[-1] + pd.Timedelta(days=1), periods=5, freq='B')

    plt.figure(figsize=(15, 6))  # Ajuste a largura para 10 e altura para 6
    plt.plot(df['Date'], base_treinamento, color= 'blue', label= 'Preço Real')
    plt.plot(datas_previsao, previsoes, color= 'red', label= 'Preços Previstos')
    plt.title(f"Previsões dos Preços das Ações {arq[5:]}")
    plt.xlabel("Tempo")
    plt.ylabel("Valor")

    # Configurar o eixo X para exibir datas corretamente
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Exibir no formato "Ano-Mês"
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Colocar um marcador por mês
    plt.gcf().autofmt_xdate()  # Rotaciona as etiquetas das datas para melhor legibilidade

    plt.legend(loc='upper left')  # Ajuste da posição da legenda para o canto superior esquerdo

    # Adicionar texto com os indicadores
    textstr = '\n'.join((
        f"MAE - Erro Médio Absoluto: {mae:.4f}",
        f"MSE - Erro Quadrático Médio: {mse:.4f}",
        f"R² - Coeficiente de Determinação: {r2:.4f}",
        f"MAPE - Erro Percentual Absoluto Médio: {mape:.2f}%",
        f"Acurácia: {acuracia:.2f}%",
        f'Mean Absolute Error da Última Epoch: {valor_mean_absolute_error:.4f}'
    ))

    # Definir a posição do texto no gráfico (mais ao lado para não sobrepor o gráfico)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.4)
    plt.gca().text(1.05, 0.5, textstr, transform=plt.gca().transAxes, fontsize=10,
                verticalalignment='center', bbox=props)

    # Ajuste o layout para que tudo fique bem visível
    plt.tight_layout()

    nome_arquivo_foto = f'Bases_Rede/{arq}/Previsao_{arq}_{epoca}_{camadas[0]}_{camadas[1]}_{camadas[2]}_{camadas[3]}.png'
    count_fot = 1

    while os.path.exists(nome_arquivo_foto):
        nome_arquivo_foto = f'Bases_Rede/{arq}/Previsao_{arq}_{epoca}_{camadas[0]}_{camadas[1]}_{camadas[2]}_{camadas[3]}_{count_fot}.png'
        count_fot += 1
        
    plt.savefig(nome_arquivo_foto, dpi=300, bbox_inches='tight')
    # plt.savefig(f'Bases_Rede/{arq}/Previsao_{arq}.png', dpi=300, bbox_inches='tight')  # Salva a imagem com alta resolução   

    # plt.show()

    # Salvando previsões e métricas em um arquivo CSV
    resultados = pd.DataFrame({
        'Data': datas_previsao,
        'Preços Previstos': previsoes.flatten(),
        'Erro Médio Absoluto (MAE)': mae,
        'Erro Quadrático Médio (MSE)': mse,
        'Coeficiente de Determinação (R²)': r2,
        'Erro Percentual Absoluto Médio (MAPE) (%)': mape,
        'Acurácia (%)': acuracia
    })

    nome_arquivo_resultado = f'Bases_Rede/{arq}/Resultados_Previsoes_{arq}_{epoca}_{camadas[0]}_{camadas[1]}_{camadas[2]}_{camadas[3]}.csv'
    count_res = 1

    while os.path.exists(nome_arquivo_resultado):
        nome_arquivo_resultado = f'Bases_Rede/{arq}/Resultados_Previsoes_{arq}_{epoca}_{camadas[0]}_{camadas[1]}_{camadas[2]}_{camadas[3]}_{count_res}.csv'
        count_res += 1

    resultados.to_csv(nome_arquivo_resultado, index=False)
