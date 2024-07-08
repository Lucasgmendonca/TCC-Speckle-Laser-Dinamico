import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

class PixelHistory:
    """Classe responsável por analisar e armazenar o histórico de pixels de uma série de imagens."""

    def __init__(self, image_path, image_pattern, first_image_number, last_image_number, pixel_selection, selection_specifier, pixel_index):
        """
        Inicializa a classe PixelHistory.

        Args:
            image_path: Caminho para a pasta onde as imagens estão armazenadas.
            image_pattern: Padrão de nome dos arquivos de imagem.
            first_image_number: Número da primeira imagem a ser considerada.
            last_image_number: Número da última imagem a ser considerada.
            pixel_selection: Modo de seleção de pixels ('a', 'h', 'v', 'r').
            selection_specifier: Especificador de seleção (opcional, depende do modo de seleção de pixels).
            pixel_index: Índice do pixel a ser plotado.
        """

        self.image_path = image_path
        self.image_pattern = image_pattern
        self.first_image_number = first_image_number
        self.last_image_number = last_image_number
        self.pixel_selection = pixel_selection
        self.selection_specifier = selection_specifier
        self.pixel_index = pixel_index
        
    def track_pixel_history(self):
        """Rastreia o histórico de pixels nas imagens capturadas."""

        # Consistência de parâmetros
        if self.pixel_selection == 'a':
            if self.selection_specifier is not None:
                raise ValueError("For 'pixel_selection' = 'a', 'selection_specifier' must be None.")
        elif self.pixel_selection in ['h', 'v']:
            if self.selection_specifier not in ['m', 'e']:
                raise ValueError("For 'pixel_selection' = 'h' or 'v', 'selection_specifier' must be 'm' or 'e'.")
        elif self.pixel_selection == 'r':
            if not (isinstance(self.selection_specifier, int) and 0 < self.selection_specifier < 230401):
                raise ValueError("For 'pixel_selection' = 'r', 'selection_specifier' must be a number greater than 0 and less than 230401.")
        else:
            raise ValueError(f"Unknown pixel selection mode: {self.pixel_selection}")

        # Caminho completo do padrão de arquivos
        full_file_pattern = os.path.join(self.image_path, self.image_pattern)
        # Número de imagens a serem consideradas
        num_images = self.last_image_number - self.first_image_number + 1

        # Leitura da primeira imagem para obter o tamanho e a colormap
        first_image_file = full_file_pattern % self.first_image_number
        img_pix = cv2.imread(first_image_file, cv2.IMREAD_GRAYSCALE)
        img_lin, img_row = img_pix.shape

        # Inicialização do histórico de pixels
        pix_his = [None] * 3
        if self.pixel_selection == 'a': # Todos os pixels na imagem
            pix_his[0] = np.zeros((img_lin * img_row, num_images), dtype=np.float32)
            pix_his[2] = [img_lin, img_row]
        elif self.pixel_selection == 'h': # Todos os pixels em uma linha
            pix_his[0] = np.zeros((img_row, num_images), dtype=np.float32)
            if self.selection_specifier == 'm':
                pix_his[2] = round(img_lin / 2)
            elif self.selection_specifier == 'e':
                pix_his[2] = img_lin-1
            else:
                pix_his[2] = self.selection_specifier
        elif self.pixel_selection == 'v': # Todos os pixels em uma coluna
            pix_his[0] = np.zeros((img_lin, num_images), dtype=np.float32)
            if self.selection_specifier == 'm':
                pix_his[2] = round(img_row / 2)
            elif self.selection_specifier == 'e':
                pix_his[2] = img_row-1
            else:
                pix_his[2] = self.selection_specifier
        elif self.pixel_selection == 'r': # Pixels aleatórios na imagem
            if self.selection_specifier < 1:
                num_pix = round(img_lin * img_row * self.selection_specifier)
            else:
                num_pix = self.selection_specifier
            pix_his[0] = np.zeros((num_pix, num_images), dtype=np.float32)
            pix_his[2] = np.column_stack((np.random.randint(0, img_lin, num_pix), np.random.randint(0, img_row, num_pix)))
        else:
            raise ValueError('thspcore: unknown pixel selection mode!')

        pix_his[1] = self.pixel_selection

        for idx_img in range(num_images):
            image_file = full_file_pattern % (idx_img + self.first_image_number)
            img_pix = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE).astype(np.float32)
            if self.pixel_selection == 'a':
                for idx_lin in range(img_lin):
                    aux_ini = img_row * idx_lin
                    aux_fin = img_row * (idx_lin + 1)
                    pix_his[0][aux_ini:aux_fin, idx_img] = img_pix[idx_lin, :]
            elif self.pixel_selection == 'h':
                pix_his[0][:, idx_img] = img_pix[pix_his[2], :]
            elif self.pixel_selection == 'v':
                pix_his[0][:, idx_img] = img_pix[:, pix_his[2]]
            elif self.pixel_selection == 'r':
                for idx_pix in range(num_pix):
                    pix_his[0][idx_pix, idx_img] = img_pix[pix_his[2][idx_pix, 0], pix_his[2][idx_pix, 1]]

        # Salvando o resultado em um arquivo de texto
        with open('output.txt', 'w') as f:
            print(pix_his, file=f)
        print("Resultados salvos em 'output.txt'.")

        # Salvando o histórico dos pixels em um arquivo de texto
        with open('pixel_history.txt', 'w') as file:
            for array in pix_his[0]:  # A matriz está na primeira posição da lista
                for value in array:
                    file.write(f"{value} ")
                file.write("\n")
        print("Histórico dos pixels salvo em 'pixel_history.txt'")

        # Salvando o gráfico do histórico de intensidade do pixel escolhido
        plt.figure()
        plt.plot(range(self.first_image_number, self.last_image_number + 1), pix_his[0][self.pixel_index], label=f'Pixel {self.pixel_index + 1}')
        plt.xlabel('Número da Imagem')
        plt.ylabel('Intensidade')
        plt.title('Histórico de Intensidade de Pixel')
        plt.legend()
        plt.savefig('pixel_history_plot.png')
        plt.close()
        print("Gráfico do histórico dos pixels salvo em 'pixel_history_plot.png'")
        
        return pix_his
