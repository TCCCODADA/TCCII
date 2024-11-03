# !pip install numpy pandas matplotlib scikit-learn tensorflow keras shap

import numpy as np                  # Biblioteca para manipulação de arrays e operações matemáticas eficientes.
import pandas as pd                 # Biblioteca para manipulação e análise de dados, especialmente útil para trabalhar com dados em tabelas (DataFrames).
import matplotlib.pyplot as plt     # Biblioteca para criar gráficos e visualizações de dados.
import matplotlib.dates as mdates   # Biblioteca para manipulação e formatação de datas e tempos em gráficos matplotlib.
import tensorflow as tf             # Biblioteca para construir e treinar redes neurais e outros modelos de Machine Learning.
import sklearn                      # Biblioteca para tarefas de Machine Learning, incluindo pré-processamento de dados, modelos e métricas de avaliação.
import shap                         # Biblioteca para explicar previsões de modelos de Machine Learning de forma interpretável.

from tensorflow.keras.models import Sequential                                  # Classe para criar um modelo sequencial (camada a camada) de rede neural.
from tensorflow.keras.layers import Dense, Dropout, LSTM                        # Importa camadas para a rede neural. Dense cria uma camada totalmente conectada, Dropout ajuda a prevenir overfitting, e LSTM é uma camada recorrente utilizada para processamento de sequências (útil em séries temporais).
from sklearn.preprocessing import MinMaxScaler                                  # Classe para normalizar os dados, escalando-os para um intervalo entre 0 e 1, útil para melhorar o desempenho dos modelos.
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score   # Importa as funções mean_absolute_error (MAE): Erro Médio Absoluto, média dos erros absolutos.
                                                                                # mean_squared_error (MSE): Erro Quadrático Médio, média dos erros ao quadrado.
                                                                                # r2_score (R²): Coeficiente de Determinação, mede a qualidade do ajuste do modelo.

import os
import time

tempo_inicial_total = time.time()

caminho_pasta = 'Base_dados'
lista_arquivos = [arquivo for arquivo in os.listdir(caminho_pasta) if os.path.isfile(os.path.join(caminho_pasta, arquivo))]
dias = 90
acuracias = {}

for a in range(5):
    for arq in lista_arquivos:
        tempo_inicial_loop = time.time()

        # Carregar dados
        df = pd.read_csv(f'Base_dados/{arq}', parse_dates=['Date'])
        df = df.sort_values('Date')

        arq = arq[:-4]

        # Defina o caminho da nova pasta que você quer criar
        caminho = f'Bases_Rede/{dias}_dias/Resultados_LSTM_Dropout_Dense/{arq}'

        # Cria a pasta se ela não existir
        if not os.path.exists(caminho):
            os.makedirs(caminho)

        # Calcular o índice para dividir a base
        tot_linhas = len(df)
        indice_divisao = int(tot_linhas * 0.7)

        # Dividir a base de dados
        base_70 = df.iloc[:indice_divisao]
        base_30 = df.iloc[indice_divisao:]

        # Salvar os primeiros 70% em outro arquivo CSV
        if os.path.exists(f'{caminho}/{arq}_Training.csv'):
            os.remove(f'{caminho}/{arq}_Training.csv')
        base_70.to_csv(f'{caminho}/{arq}_Training.csv', index=False)

        # Salvar os últimos 30% em um novo arquivo CSV
        if os.path.exists(f'{caminho}/{arq}_Test.csv'):
            os.remove(f'{caminho}/{arq}_Test.csv')
        base_30.to_csv(f'{caminho}/{arq}_Test.csv', index=False)

        base = pd.read_csv(f'{caminho}/{arq}_Training.csv')

        # Coluna "OPEN" será utilizada para realizar as previsões
        base_treinamento = base.iloc[:, 1:2].values

        # Pré-Processamento - Normalizar valores
        normalizador = MinMaxScaler(feature_range=(0, 1))
        base_treinamento_normalizada = normalizador.fit_transform(base_treinamento)

        X = [] # Previsores
        y = [] # Preços Reais

        for i in range(dias, len(base_treinamento_normalizada)):  # 90 Preços Anteriores para prever o preço atual
            X.append(base_treinamento_normalizada[i - dias:i, 0])
            y.append(base_treinamento_normalizada[i, 0])

        X, y = np.array(X), np.array(y)

        # ===== ESTRUTURA DA REDE NEUREAL RECORRENTE===== #
        regressor = Sequential()

        # 1° Camada de LSTM
        regressor.add(LSTM(units=100, return_sequences=True, input_shape=(X.shape[1], 1)))
        regressor.add(Dropout(0.3))

        # 2° Camada de LSTM
        regressor.add(LSTM(units=50, return_sequences=True))
        regressor.add(Dropout(0.3))

        # 3° Camada de LSTM
        regressor.add(LSTM(units=50, return_sequences=True))
        regressor.add(Dropout(0.3))

        # 4° e Última Camada de LSTM
        regressor.add(LSTM(units=50))
        regressor.add(Dropout(0.3))

        # Camada Dense (Totalmente Conectada)
        regressor.add(Dense(units=1, activation='linear'))


        # Compilação do modelo
        regressor.compile(optimizer='rmsprop', loss='mean_squared_error', metrics=['mean_absolute_error'])


        # ========== Treinamento ========== #
        print(f"\nIniciando Treinamento: {arq}")
        treinamento = regressor.fit(X, y, epochs=15, batch_size=32)
        epoca = len(treinamento.epoch)


        # Acessando o valor do mean_absolute_error da última epoch
        valor_mean_absolute_error = treinamento.history['mean_absolute_error'][-1]

        # Acessando o valor do loss da última epoch
        valor_loss = treinamento.history['loss'][-1]


        # ========== PREVISÕES DOS PREÇOS DAS AÇÕES ========== #
        base_teste = pd.read_csv(f'{caminho}/{arq}_Test.csv')
        y_teste = base_teste.iloc[:, 1:2].values

        # Juntando as duas bases em uma só
        base_completa = pd.concat((base['Open'], base_teste['Open']), axis=0)
        entradas = base_completa[len(base_completa) - len(base_teste) - dias:].values

        # Preparação dos dados de entrada
        entradas_novo = entradas.reshape(-1, 1)
        entradas_novo = normalizador.transform(entradas_novo)

        X_teste = []
        
        for i in range(dias, len(entradas_novo)):
            X_teste.append(entradas_novo[i - dias:i, 0])

        X_teste = np.array(X_teste)
        X_teste = np.reshape(X_teste, (X_teste.shape[0], X_teste.shape[1], 1))

        # Calcula Previsão
        previsoes = regressor.predict(X_teste)
        previsoes = normalizador.inverse_transform(previsoes)

        # Evitando divisão por zero
        y_teste = np.where(y_teste == 0, 1e-10, y_teste)

        # 1. Mean Absolute Error (MAE)
        mae = mean_absolute_error(y_teste, previsoes)
        print(f"{arq} - Erro Médio Absoluto - Mean Absolute Error (MAE): {mae}")

        # 2. Mean Squared Error (MSE)
        mse = mean_squared_error(y_teste, previsoes)
        print(f"{arq} - Erro Quadrático Médio - Mean Squared Error (MSE): {mse}")

        # 3. R² Score (Coeficiente de Determinação)
        r2 = r2_score(y_teste, previsoes)
        print(f"{arq} - Coeficiente de Determinação - R² Score: {r2}")

        # 4. Mean Absolute Percentage Error (MAPE)
        mape = np.mean(np.abs((y_teste - previsoes) / y_teste)) * 100
        print(f"{arq} - Erro Percentual Absoluto Médio - Mean Absolute Percentage Error (MAPE): {mape:.2f}%")

        # 5. Acurácia
        acuracia = 100 - mape
        print(f"{arq} - Acurácia: {acuracia:.2f}%")

        # 6. Mean Absolute Error
        print(f'{arq} - Mean Absolute Error da Última Epoch: {valor_mean_absolute_error:.4f}')

        # 7. Mean Absolute Error
        print(f'{arq} - Loss da Última Epoch: {valor_loss:.4f}')

        # Garantir que a coluna 'Date' esteja no formato datetime
        base_teste['Date'] = pd.to_datetime(base_teste['Date'])

        plt.figure(figsize=(15, 6))  # Ajuste a largura para 10 e altura para 6
        plt.plot(base_teste['Date'], y_teste, color= 'blue', label= 'Preço Real')
        plt.plot(base_teste['Date'], previsoes, color= 'red', label= 'Preços Previstos')
        plt.title(f"Previsões dos Preços das Ações {arq[5:]}")
        plt.xlabel("Tempo")
        plt.ylabel("Valor")

        # Configurar o eixo X para exibir datas corretamente
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Exibir no formato "Ano-Mês"
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Colocar um marcador por mês
        plt.gcf().autofmt_xdate()  # Rotaciona as etiquetas das datas para melhor legibilidade

        plt.legend(loc='upper left')  # Ajuste da posição da legenda para o canto superior esquerdo

        # Calculando o tempo de execução do loop atual
        tempo_final_loop = time.time()
        tempo_total_loop = tempo_final_loop - tempo_inicial_loop
        print(f"{arq} - Tempo de Execução: {tempo_total_loop:.2f} seg.\n")


        # Adicionar texto com os indicadores
        textstr = '\n'.join((
            f"MAE - Erro Médio Absoluto: {mae:.4f}",
            f"MSE - Erro Quadrático Médio: {mse:.4f}",
            f"R² - Coeficiente de Determinação: {r2:.4f}",
            f"MAPE - Erro Percentual Absoluto Médio: {mape:.2f}%",
            f"Acurácia: {acuracia:.2f}%",
            f'Mean Absolute Error da Última Epoch: {valor_mean_absolute_error:.4f}',
            f'Lossda Última Epoch: {valor_loss:.4f}',
            f'Tempo de Execução: {tempo_total_loop:.2f} seg.'
        ))

        # Definir a posição do texto no gráfico (mais ao lado para não sobrepor o gráfico)
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.4)
        plt.gca().text(1.05, 0.5, textstr, transform=plt.gca().transAxes, fontsize=10,
                    verticalalignment='center', bbox=props)

        # Ajuste o layout para que tudo fique bem visível
        plt.tight_layout()

        datas_teste = base_teste.iloc[:, 0:1].values
        igual_ou_nao = previsoes == y_teste

        # Salvando previsões e métricas em um arquivo CSV
        resultados = pd.DataFrame({
            'Data': datas_teste.flatten(),
            'Preço Real': y_teste.flatten(),
            'Preços Previstos': previsoes.flatten(),
            'Erro Absoluto': np.abs(y_teste.flatten() - previsoes.flatten()),
            'Erro Percentual': (np.abs(y_teste.flatten() - previsoes.flatten()) / y_teste.flatten()) * 100,
            'Erro Médio Absoluto (MAE)': mae,
            'Erro Quadrático Médio (MSE)': mse,
            'Coeficiente de Determinação (R²)': r2,
            'Erro Percentual Absoluto Médio (MAPE) (%)': mape,
            'Acurácia (%)': acuracia,
            'Valores Iguais?': igual_ou_nao.flatten(),
            'Mean Absolute Error da Última Epoch': valor_mean_absolute_error,
            'Lossda Última Epoch': valor_loss,
            'Tempo de Execução': tempo_total_loop
        })

        nome_arquivo_resultado = f'{caminho}/Resultados_Previsoes_{arq}_{epoca}_LSTM_Dropout_Dense.csv'
        count_res = 1

        while os.path.exists(nome_arquivo_resultado):
            nome_arquivo_resultado = f'{caminho}/Resultados_Previsoes_{arq}_{epoca}_LSTM_Dropout_Dense_{count_res}.csv'
            count_res += 1

        resultados.to_csv(nome_arquivo_resultado, index=False)

        nome_arquivo_foto = f'{caminho}/Previsao_{arq}_{epoca}_LSTM_Dropout_Dense.png'
        count_fot = 1

        while os.path.exists(nome_arquivo_foto):
            nome_arquivo_foto = f'{caminho}/Previsao_{arq}_{epoca}_LSTM_Dropout_Dense_{count_fot}.png'
            count_fot += 1
            
        plt.savefig(nome_arquivo_foto, dpi=300, bbox_inches='tight')

        acuracias[arq] = acuracia
        # plt.savefig(f'{caminho}/Previsao_{arq}.png', dpi=300, bbox_inches='tight')  # Salva a imagem com alta resolução   

        # plt.show()

    # Calculando o tempo total de execução de todos os loops
    tempo_final_total = time.time()
    tempo_execucao_total = (tempo_final_total - tempo_inicial_total) / 60
    print(f"Tempo Total de execução: {tempo_execucao_total:.2f} Minutos.")
    for i, j in acuracias.items():
        print(f'Teste {dias} Dias: {i} {j}\n')