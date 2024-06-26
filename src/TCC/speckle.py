import cv2 ### Importa a biblioteca OpenCV, que é uma biblioteca popular de visão computacional.
import os ### Importa o módulo 'os', que fornece funções para interagir com o sistema operacional, permitindo manipulação de caminhos de arquivos, diretórios, etc.
from datetime import datetime ### Importa a classe datetime do módulo datetime, que permite trabalhar com datas e horários em Python.
import numpy as np ### Importa a biblioteca NumPy, que oferece suporte a arrays e matrizes multidimensionais, junto com uma coleção de funções matemáticas de alto nível para operar nesses arrays, e a renomeia como 'np' para facilitar o acesso às suas funções e classes.
import matplotlib.pyplot as plt ### Importa o módulo pyplot da biblioteca Matplotlib, esse módulo fornece uma interface fácil de usar para criar e personalizar gráficos em Python, e o renomeia como 'plt' para facilitar o acesso às suas funções.

class Preview:
    """Classe responsável por exibir uma pré-visualização da câmera."""

    def __init__(self, region_of_interest): 
        """Inicializa a classe Preview."""
        self.video_input_object = cv2.VideoCapture(0) ### Criação do objeto de captura de vídeo
        ### Cria um objeto de captura de vídeo (videoInputObject) que representa a câmera.
        ### O argumento 0 indica que queremos capturar vídeo da primeira câmera disponível no sistema.
        self.region_of_interest = region_of_interest  # Define a região de interesse
        
    def open_preview(self):
        """Abre uma janela para visualização da câmera."""
        while True:
            ret, frame = self.video_input_object.read() ### Lê um frame do vídeo capturado pela câmera e armazena-o nas variáveis ret (um booleano que indica se a leitura foi bem-sucedida) e frame (o próprio frame capturado).
            if not ret:
                break
            # Aplicando a região de interesse
            x, y, w, h = self.region_of_interest  # Obtém a região de interesse
            roi_frame = frame[y:y+h, x:x+w] ### Esta linha extrai a região de interesse do frame capturado usando as coordenadas obtidas anteriormente.
            gray_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY) ### O frame da região de interesse é convertido para escala de cinza usando a função cvtColor do OpenCV.
            cv2.imshow('Preview', gray_frame) ### Exibe o frame capturado em uma janela com o título "Preview". A função imshow do OpenCV é usada para exibir imagens.
            if cv2.waitKey(1) & 0xFF == ord('q'): ### Aguarda 1 milissegundo por uma entrada do teclado. Se a tecla pressionada for 'q', o loop será interrompido e o programa será encerrado. A função waitKey retorna o código ASCII da tecla pressionada e o operador & é usado para mascarar os bits irrelevantes.
                break


class Capture:
    """Classe responsável por capturar imagens da câmera."""
    
    def __init__(self, video_input_object, output_path, frame_grab_interval, region_of_interest, file_name, first_image_number, last_image_number):
        """
        Inicializa a classe Capture.

        Args:
            video_input_object: Objeto de entrada de vídeo (câmera).
            output_path: Caminho para salvar as imagens capturadas.
            frame_grab_interval: Intervalo entre cada captura de imagem, em milissegundos.
            region_of_interest: Região de interesse para captura de imagem.
            file_name: Nome do arquivo de imagem.
            first_image_number: Número da primeira imagem a ser capturada.
            last_image_number: Número da última imagem a ser capturada.
        """
        self.video_input_object = video_input_object
        self.output_path = output_path
        self.frame_grab_interval = frame_grab_interval
        self.region_of_interest = region_of_interest
        self.file_name = file_name
        self.first_image_number = first_image_number
        self.last_image_number = last_image_number

    def capture_images(self):
        """Captura imagens da câmera."""

        # Parâmetros internos
        frames_per_second = self.video_input_object.get(cv2.CAP_PROP_FPS)
        video_resolution = (int(self.video_input_object.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.video_input_object.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        number_of_images = self.last_image_number - self.first_image_number + 1
        sampling_time = 1 / (frames_per_second / self.frame_grab_interval)
        full_file_path = os.path.join(self.output_path, self.file_name)

        # Consistência de parâmetros
        if not 1 <= self.frame_grab_interval <= 99: ### Inconsistente para qualquer valor menor que 1 ou maior que 99
            raise ValueError('captcore: frame grab interval must be a scalar between 0 and 99!')
        if any(val < 0 for val in self.region_of_interest[:4]): ### Inconsistente para quaisquer valores negativos para a posição ou deslocamento
            raise ValueError('captcore: region of interest is not consistent!')
        if any((val1 + val2) > res for val1, val2, res in zip(self.region_of_interest[:2], self.region_of_interest[2:], video_resolution)):
            raise ValueError('captcore: region of interest is not compatible with video resolution!')

        # Configuração da captura
        self.video_input_object.set(cv2.CAP_PROP_FPS, self.frame_grab_interval) ### Configura as propriedades do objeto de entrada de vídeo para o intervalo de captura de quadros.

        # Captura de imagens
        print('captcore: acquisition started, please wait!')
        captured_frames = []
        for _ in range(number_of_images):
            ret, frame = self.video_input_object.read() ### Lê um frame do vídeo capturado pela câmera e armazena-o nas variáveis ret (um booleano que indica se a leitura foi bem-sucedida) e frame (o próprio frame capturado).
            if not ret:
                break
            # Aplicando a região de interesse
            x, y, w, h = self.region_of_interest
            roi_frame = frame[y:y+h, x:x+w]
            gray_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
            captured_frames.append(gray_frame) ### Após a leitura do frame, ele é adicionado à lista captured_frames usando o método append(). Isso significa que cada frame capturado será armazenado nesta lista.
        print('captcore: acquisition completed, saving the images!')

        # Salvando imagens
        for i, img in enumerate(captured_frames):
            filename = full_file_path % (i + self.first_image_number) ### Para cada iteração do loop, esta linha cria o nome do arquivo onde a imagem será salva.
            cv2.imwrite(filename, img) ### Esta linha salva a imagem atual no arquivo especificado por filename.

        # Criação do arquivo de informações
        with open(os.path.join(self.output_path, 'info.txt'), 'w') as file_writer: ### Esta linha abre um arquivo chamado 'info.txt' no modo de escrita ('w') dentro do diretório especificado por self.output_path. O with garante que o arquivo seja fechado corretamente após o uso.
            # Informações da câmera
            file_writer.write('Camera general information:\n')
            file_writer.write(f'\t* Resolution: {video_resolution[0]} x {video_resolution[1]}\n')
            file_writer.write(f'\t* Frame rate: {frames_per_second}\n\n')

            # Informações da captura
            file_writer.write('Acquisition information:\n')
            file_writer.write(f'\t* Date and time: {datetime.now()}\n')
            file_writer.write('\t* Region of interest:\n')
            file_writer.write(f'\t\t* Horizontal Offset: {self.region_of_interest[0]}\n')
            file_writer.write(f'\t\t* Vertical Offset: {self.region_of_interest[1]}\n')
            file_writer.write(f'\t\t* Horizontal Length: {self.region_of_interest[2]}\n')
            file_writer.write(f'\t\t* Vertical Length: {self.region_of_interest[3]}\n')
            file_writer.write(f'\t* Frame Grab Interval: first of every {self.frame_grab_interval} frame(s)\n')
            file_writer.write(f'\t\t* Thus, the sampling time was {sampling_time} seconds\n\n')
            ### Lista de outras propriedades disponíveis em https://docs.opencv.org/4.x/d4/d15/group__videoio__flags__base.html


class PixelHistory:
    """Classe responsável por analisar e armazenar o histórico de pixels de uma série de imagens."""

    def __init__(self, image_path, image_pattern, first_image_number, last_image_number, pixel_selection, selection_specifier):
        """
        Inicializa a classe PixelHistory.

        Args:
            image_path: Caminho para a pasta onde as imagens estão armazenadas.
            image_pattern: Padrão de nome dos arquivos de imagem.
            first_image_number: Número da primeira imagem a ser considerada.
            last_image_number: Número da última imagem a ser considerada.
            pixel_selection: Modo de seleção de pixels ('a', 'h', 'v', 'r').
            selection_specifier: Especificador de seleção (opcional, depende do modo de seleção de pixels).
        """

        self.image_path = image_path
        self.image_pattern = image_pattern
        self.first_image_number = first_image_number
        self.last_image_number = last_image_number
        self.pixel_selection = pixel_selection
        self.selection_specifier = selection_specifier
        
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
                # pix_his[0][:, idx_img] = img_pix.flatten()
                # OU
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
                    # OU
                    # for idx_pix in range(pix_his[0].shape[0]):
                    pix_his[0][idx_pix, idx_img] = img_pix[pix_his[2][idx_pix, 0], pix_his[2][idx_pix, 1]]
        return pix_his


class SavePixelHistory:
    """Classe responsável por salvar o histórico de pixels e o gráfico do histórico."""

    def __init__(self, pixel_history_data, first_image_number, last_image_number, pixel_index):
        """
        Inicializa a classe SavePixelHistory.

        Args:
            pixel_history_data: Dados do histórico de pixels.
            first_image_number: Número da primeira imagem.
            last_image_number: Número da última imagem.
            pixel_index: Índice do pixel a ser plotado.
        """
        self.pixel_history_data = pixel_history_data
        self.first_image_number = first_image_number
        self.last_image_number = last_image_number
        self.pixel_index = pixel_index

    def save(self):
        """Salva os dados do histórico de pixels em arquivos de texto e o gráfico em um arquivo de imagem."""
        # Salvando o resultado em um arquivo de texto
        with open('output.txt', 'w') as f:
            print(self.pixel_history_data, file=f)
        print("Resultados salvos em 'output.txt'.")

        # Salvando o histórico dos pixels em um arquivo de texto
        with open('pixel_history.txt', 'w') as file:
            for array in self.pixel_history_data[0]:  # A matriz está na primeira posição da lista
                for value in array:
                    file.write(f"{value} ")
                file.write("\n")
        print("Histórico dos pixels salvo em 'pixel_history.txt'")

        # Salvando o gráfico do histórico de intensidade do pixel escolhido
        plt.figure()
        plt.plot(range(self.first_image_number, self.last_image_number + 1), self.pixel_history_data[0][self.pixel_index], label=f'Pixel {self.pixel_index + 1}')
        plt.xlabel('Número da Imagem')
        plt.ylabel('Intensidade')
        plt.title('Histórico de Intensidade de Pixel')
        plt.legend()
        plt.savefig('pixel_history_plot.png')
        plt.close()
        print("Gráfico do histórico dos pixels salvo em 'pixel_history_plot.png'")

        


class SaveAnalysisResults:
    """Classe responsável por salvar os resultados da análise numérica e a matriz de co-ocorrência."""

    def __init__(self, numerical_result, co_occurrence_matrix):
        """Inicializa a classe SaveAnalysisResults.

        Args:
            numerical_result: Resultado numérico da análise.
            co_occurrence_matrix: Matriz de co-ocorrência.
        """
        self.numerical_result = numerical_result
        self.co_occurrence_matrix = co_occurrence_matrix

    def save(self):
        # Salvando o resultado numérico em um arquivo de texto
        with open('numerical_result.txt', 'w') as file:
            file.write(f"Numerical Result: {self.numerical_result}\n")
        print("Resultado numérico salvo em 'numerical_result.txt'.")

        # Salvando a matriz de co-ocorrência em um arquivo de texto
        with open('co_occurrence_matrix.txt', 'w') as file:
            for row in self.co_occurrence_matrix:
                for value in row:
                    file.write(f"{value} ")
                file.write("\n")
        print("Matriz de co-ocorrência salva em 'co_occurrence_matrix.txt'.")


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
            """Realiza a análise numérica no histórico de pixels."""
            # Valores de saída padrão
            num_res = 0
            co_matr = np.zeros((256, 256))

            # Verificação de parâmetros
            if (self.method_selection > 5):
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

            return num_res, co_matr


class Main:
    """Classe principal para executar o programa."""
    
    @staticmethod
    def run():
        output_path = 'C:\\Users\\lucas\\OneDrive\\Documentos\\TCC\\Prints'
        file_name = 'Img%03d.bmp'
        first_image_number = 1
        last_image_number = 10
        frame_grab_interval = 1 ### Define o intervalo entre cada captura de imagem, em milissegundos.
        region_of_interest = (0, 60, 640, 360) ### (a, b, x, y)
        ### a: É o deslocamento horizontal (ou posição) da região de interesse a partir da extremidade esquerda da imagem ou vídeo.
        ### b: É o deslocamento vertical (ou posição) da região de interesse a partir da extremidade superior da imagem ou vídeo.
        ### x: É o comprimento horizontal da região de interesse.
        ### y: É o comprimento vertical da região de interesse.
        pixel_selection = 'a'  # Modo de seleção de pixels: 'a', 'h', 'v', 'r'
        selection_specific = None  # Pode ser 'm', 'e' ou um número específico dependendo do modo
        pixel_index = 0  # Índice do pixel escolhido
        method_selection = 5  # Método de análise: '1', '2', '3', '4', '5'

        preview = Preview(region_of_interest)
        preview.open_preview()


        ### captcore ###

        capture = Capture(preview.video_input_object, output_path, frame_grab_interval, region_of_interest, file_name, first_image_number, last_image_number)
        capture.capture_images()

        # Libera a captura de vídeo
        preview.video_input_object.release()


        ### thspcore ###

        pix_hist = PixelHistory(output_path, file_name, first_image_number, last_image_number, pixel_selection, selection_specific)
        pixel_history_data = pix_hist.track_pixel_history()

        # Salvando o histórico de pixels e o gráfico em arquivos
        save_pixel_history = SavePixelHistory(pixel_history_data, first_image_number, last_image_number, pixel_index)
        save_pixel_history.save()


        ### numecore ###

        # Análise numérica do histórico de pixels
        num_analysis = NumericalAnalysis(pixel_history_data, method_selection)
        num_res, co_matr = num_analysis.numecore()

        # Salvando os resultados da análise numérica e a matriz de co-ocorrência
        save_analysis_results = SaveAnalysisResults(num_res, co_matr)
        save_analysis_results.save()

if __name__ == "__main__":
    Main.run()