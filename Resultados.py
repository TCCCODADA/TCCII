class Resultados:
    def __init__(self, MAE, MSE, R, MAPE, Acuracia, MeanAbsoluteErrEpoch, LossEpoch, Temp):
        self.MAE = MAE
        self.MSE = MSE
        self.R = R
        self.MAPE = MAPE
        self.Acuracia = Acuracia
        self.MeanAbsoluteErrEpoch = MeanAbsoluteErrEpoch
        self.LossEpoch = LossEpoch
        self.Temp = Temp

    @staticmethod
    def calcular_e_escrever_media(lista_resultados, execucoes, dias, epocas, nome_arquivo, rede):
        # Calculando a média para cada métrica
        media = Resultados(
            sum(r.MAE for r in lista_resultados) / execucoes,
            sum(r.MSE for r in lista_resultados) / execucoes,
            sum(r.R for r in lista_resultados) / execucoes,
            sum(r.MAPE for r in lista_resultados) / execucoes,
            sum(r.Acuracia for r in lista_resultados) / execucoes,
            sum(r.MeanAbsoluteErrEpoch for r in lista_resultados) / execucoes,
            sum(r.LossEpoch for r in lista_resultados) / execucoes,
            sum(r.Temp for r in lista_resultados) / execucoes
        )

        # Abrindo o arquivo para escrever as médias
        with open(nome_arquivo, "a") as arquivo:
            # Escrevendo as médias no arquivo com o formato apropriado
            arquivo.write("\n--- Novas Medias ---\n")
            arquivo.write(f"{rede}\n")
            arquivo.write(f"Dias: {dias}\n")
            arquivo.write(f"Execucoes: {execucoes}\n")
            arquivo.write(f"Epocas: {epocas}\n")
            arquivo.write(f"MAE: {media.MAE}\n")
            arquivo.write(f"MSE: {media.MSE}\n")
            arquivo.write(f"R: {media.R}\n")
            arquivo.write(f"MAPE: {media.MAPE}\n")
            arquivo.write(f"Acuracia: {media.Acuracia}\n")
            arquivo.write(f"Mean Absolute Erro Epoch: {media.MeanAbsoluteErrEpoch}\n")
            arquivo.write(f"Loss Epoch: {media.LossEpoch}\n")    
            arquivo.write(f"Temp: {media.Temp}\n")

    @staticmethod
    def tempExec(lista_resultados, dias, rede):
        # Calculando a média para cada métrica
        tempMedio = sum(r for r in lista_resultados) / len(lista_resultados)

        # Abrindo o arquivo para escrever as médias
        with open("Media_Resultados/TempoMed.txt", "a") as arquivo:
            # Escrevendo as médias no arquivo com o formato apropriado
            arquivo.write("\n--- Novas Medias ---\n")
            arquivo.write(f"{rede}\n")
            arquivo.write(f"Dias: {dias}\n")
            arquivo.write(f"Tempo medio: {tempMedio}\n")


