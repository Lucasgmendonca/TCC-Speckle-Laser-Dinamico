import cv2 ### Importa a biblioteca OpenCV, que é uma biblioteca popular de visão computacional.
import os ### Importa o módulo 'os', que fornece funções para interagir com o sistema operacional, permitindo manipulação de caminhos de arquivos, diretórios, etc.
from datetime import datetime

import numpy as np ### Importa a classe datetime do módulo datetime, que permite trabalhar com datas e horários em Python.

class Preview:
    """Classe responsável por exibir uma pré-visualização da câmera."""

    def __init__(self): 
        """Inicializa a classe Preview."""
        self.video_input_object = cv2.VideoCapture(0) ### Criação do objeto de captura de vídeo
        ### Cria um objeto de captura de vídeo (videoInputObject) que representa a câmera.
        ### O argumento 0 indica que queremos capturar vídeo da primeira câmera disponível no sistema.
        
    def open_preview(self):
        """Abre uma janela para visualização da câmera."""
        while True:
            ret, frame = self.video_input_object.read() ### Lê um frame do vídeo capturado pela câmera e armazena-o nas variáveis ret (um booleano que indica se a leitura foi bem-sucedida) e frame (o próprio frame capturado).
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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
            raise ValueError('captcore: region of interest is not compatible with video resolution!') ### Inconsistente se a soma da posição e do tamanho da região de interesse (horizontal ou vertical) 

        # Configuração da captura
        self.video_input_object.set(cv2.CAP_PROP_FPS, self.frame_grab_interval) ### Configura as propriedades do objeto de entrada de vídeo para o intervalo de captura de quadros.
        self.video_input_object.set(cv2.CAP_PROP_FRAME_WIDTH, self.region_of_interest[2]) ### Configura as propriedades do objeto de entrada de vídeo para as dimensões da região de interesse.
        self.video_input_object.set(cv2.CAP_PROP_FRAME_HEIGHT, self.region_of_interest[3]) ### Configura as propriedades do objeto de entrada de vídeo para as dimensões da região de interesse.

        # Captura de imagens
        print('captcore: acquisition started, please wait!')
        captured_frames = []
        for _ in range(number_of_images):
            ret, frame = self.video_input_object.read() ### Lê um frame do vídeo capturado pela câmera e armazena-o nas variáveis ret (um booleano que indica se a leitura foi bem-sucedida) e frame (o próprio frame capturado).
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
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

    def __init__(self, image_path, image_pattern, first_image_number, last_image_number, pixel_selection, selection_specifier=None):
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

        # Caminho completo do padrão de arquivos
        full_file_pattern = os.path.join(self.image_path, self.image_pattern)
        # Número de imagens a serem consideradas
        num_images = self.last_image_number - self.first_image_number + 1

        # Leitura da primeira imagem para obter o tamanho e a colormap
        first_image_file = full_file_pattern % self.first_image_number
        img_pix = cv2.imread(first_image_file, cv2.IMREAD_GRAYSCALE)
        img_lin, img_row = img_pix.shape

        # Inicialização do histórico de pixels
        pix_his = [None] * 5
        if self.pixel_selection == 'a': # Todos os pixels na imagem
            pix_his[0] = np.zeros((img_lin * img_row, num_images), dtype=np.float32)
            pix_his[2] = [img_lin, img_row]
        elif self.pixel_selection == 'h': # Todos os pixels em uma linha
            pix_his[0] = np.zeros((img_row, num_images), dtype=np.float32)
            if self.selection_specifier == 'm':
                pix_his[2] = round(img_lin / 2)
            elif self.selection_specifier == 'e':
                pix_his[2] = img_lin
            else:
                pix_his[2] = self.selection_specifier
        elif self.pixel_selection == 'v': # Todos os pixels em uma coluna
            pix_his[0] = np.zeros((img_lin, num_images), dtype=np.float32)
            if self.selection_specifier == 'm':
                pix_his[2] = round(img_row / 2)
            elif self.selection_specifier == 'e':
                pix_his[2] = img_row
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
        pix_his[3] = None # Nenhum mapa RGB necessário para imagens em tons de cinza

        for idx_img in range(num_images):
            image_file = full_file_pattern % (idx_img + self.first_image_number)
            img_pix = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE).astype(np.float32)
            if self.pixel_selection == 'a':
                pix_his[0][:, idx_img] = img_pix.flatten()
                # OU
                # for idx_lin in range(img_lin):
                #     aux_ini = img_row * idx_lin
                #     aux_fin = img_row * (idx_lin + 1)
                #     pix_his[0][aux_ini:aux_fin, idx_img] = img_pix[idx_lin, :]
            elif self.pixel_selection == 'h':
                pix_his[0][:, idx_img] = img_pix[pix_his[3], :]
            elif self.pixel_selection == 'v':
                pix_his[0][:, idx_img] = img_pix[:, pix_his[3]]
            elif self.pixel_selection == 'r':
                for idx_pix in range(num_pix):
                    # OU
                    # for idx_pix in range(pix_his[0].shape[0]):
                    pix_his[0][idx_pix, idx_img] = img_pix[pix_his[3][idx_pix, 0], pix_his[3][idx_pix, 1]]
        return pix_his


class Main:
    """Classe principal para executar o programa."""
    
    @staticmethod
    def run():
        output_path = 'C:\\Users\\lucas\\OneDrive\\Documentos\\TCC\\Prints'
        file_name = 'Img%03d.bmp'
        first_image_number = 1
        last_image_number = 10
        frame_grab_interval = 1 ### Define o intervalo entre cada captura de imagem, em milissegundos.
        region_of_interest = (0, 0, 640, 480) ### (a, b, x, y)
        ### a: É o deslocamento horizontal (ou posição) da região de interesse a partir da extremidade esquerda da imagem ou vídeo.
        ### b: É o deslocamento vertical (ou posição) da região de interesse a partir da extremidade superior da imagem ou vídeo.
        ### x: É o comprimento horizontal da região de interesse.
        ### y: É o comprimento vertical da região de interesse.

        preview = Preview()
        preview.open_preview()

        capture = Capture(preview.video_input_object, output_path, frame_grab_interval, region_of_interest, file_name, first_image_number, last_image_number)
        capture.capture_images()

        # Libera a captura de vídeo
        preview.video_input_object.release()

        pixel_selection = 'a'  # Modo de seleção de pixels: 'a', 'h', 'v', 'r'
        selection_specific = None  # Pode ser 'm', 'e' ou um número específico dependendo do modo

        pix_hist = PixelHistory(output_path, file_name, first_image_number, last_image_number, pixel_selection, selection_specific)
        pixel_history_data = pix_hist.track_pixel_history()

        # Exemplo de saída do histórico de pixels
        print(pixel_history_data)

        # Salvando o resultado em um arquivo de texto
        with open('output.txt', 'w') as f:
            print(pixel_history_data, file=f)

        print("Resultados salvos em 'output.txt'.")

        # Salvando o resultado em um arquivo de texto
        with open('pixel_history.txt', 'w') as file:
            for array in pixel_history_data[0]:  # A matriz está na primeira posição da lista
                for value in array:
                    file.write(f"{value} ")
                file.write("\n")

        print("Resultado salvo em pixel_history.txt")



if __name__ == "__main__":
    Main.run()