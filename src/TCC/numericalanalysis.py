import numpy as np

class NumericalAnalysis:
    """Classe responsável por realizar análises numéricas no histórico de pixels."""

    def __init__(self, pixel_history_data, method_selection):
        """
        Inicializa a classe NumericalAnalysis.

        Args:
            pixel_history_data: Dados do histórico de pixels.
            method_selection: Método de análise numérica a ser utilizado.
        """
        self.pixel_history_data = pixel_history_data
        self.method_selection = method_selection

    def numecore(self):
        """Realiza a análise numérica no histórico de pixels e salva os resultados."""
        # Valores de saída padrão
        num_res = 0
        co_matr = np.zeros((256, 256))

        # Verificação de parâmetros
        if self.method_selection > 5:
            raise ValueError('numecore: unknown method of analysis!')

        # Parâmetros internos
        sts_lin = self.pixel_history_data[0].shape[0]  # Número de sinais (pixels rastreados)
        sts_row = self.pixel_history_data[0].shape[1]  # Comprimento dos sinais (número de imagens)

        # Geração da matriz de co-ocorrência (se necessário)
        if self.method_selection < 3 or self.method_selection > 4:
            co_matr = np.zeros((256, 256))
            for idx_lin in range(sts_lin):
                for idx_row in range(sts_row - 1):
                    pix_now = round(self.pixel_history_data[0][idx_lin, idx_row])  # intensidade do pixel analisado
                    pix_nxt = round(self.pixel_history_data[0][idx_lin, idx_row + 1])  # intensidade do próximo pixel
                    co_matr[pix_now, pix_nxt] += 1  # contador de ocorrências

        # Momento de inércia
        if self.method_selection == 1:
            for idx_lin in range(256):
                for idx_row in range(256):
                    num_res += co_matr[idx_lin, idx_row] * (idx_lin - idx_row) ** 2
            nrmfac = (sts_row - 1) * sts_lin  # maior quantidade de mudanças que pode ocorrer no STS analisado
            num_res /= nrmfac

        # Valor absoluto das diferenças
        if self.method_selection == 2:
            for idx_lin in range(256):
                for idx_row in range(256):
                    num_res += co_matr[idx_lin, idx_row] * abs(idx_lin - idx_row)
            nrmfac = (sts_row - 1) * sts_lin  # maior quantidade de mudanças que pode ocorrer no STS analisado
            num_res /= nrmfac

        # Desvio padrão
        if self.method_selection == 3:
            num_res = np.mean(np.std(self.pixel_history_data[0], axis=1))

        # Intensidade média do pixel
        if self.method_selection == 4:
            num_res = np.mean(self.pixel_history_data[0])

        # Novo valor absoluto das diferenças
        if self.method_selection == 5:
            for idx_lin in range(256):
                for idx_row in range(256):
                    if idx_lin + idx_row != 0:  # Adicione esta verificação
                        num_res += co_matr[idx_lin, idx_row] * (abs(idx_lin - idx_row) / (idx_lin + idx_row))
            nrmfac = (sts_row - 1) * sts_lin  # maior quantidade de mudanças que pode ocorrer no STS analisado
            num_res /= nrmfac

        # Salvando o resultado numérico em um arquivo de texto
        with open('numerical_result.txt', 'w') as file:
            file.write(f"Numerical Result: {num_res}\n")
        print("Resultado numérico salvo em 'numerical_result.txt'.")

        # Salvando a matriz de co-ocorrência em um arquivo de texto
        with open('co_occurrence_matrix.txt', 'w') as file:
            for row in co_matr:
                for value in row:
                    file.write(f"{value} ")
                file.write("\n")
        print("Matriz de co-ocorrência salva em 'co_occurrence_matrix.txt'.")

        return num_res, co_matr