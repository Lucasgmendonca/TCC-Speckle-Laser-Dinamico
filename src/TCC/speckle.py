import cv2 ### Importa a biblioteca OpenCV, que é uma biblioteca popular de visão computacional.
import os
from datetime import datetime

class Preview:
    def __init__(self):
        # Criação do objeto de captura de vídeo
        self.video_input_object = cv2.VideoCapture(0)
        ### Cria um objeto de captura de vídeo (videoInputObject) que representa a câmera.
        ### O argumento 0 indica que queremos capturar vídeo da primeira câmera disponível no sistema.
        
    # Abertura da janela de visualização
    def open_preview(self):
        while True:
            ret, frame = self.video_input_object.read() ### Lê um frame do vídeo capturado pela câmera e armazena-o nas variáveis ret (um booleano que indica se a leitura foi bem-sucedida) e frame (o próprio frame capturado).
            cv2.imshow('Preview', frame) ### Exibe o frame capturado em uma janela com o título "Preview". A função imshow do OpenCV é usada para exibir imagens.
            if cv2.waitKey(1) & 0xFF == ord('q'): ### Aguarda 1 milissegundo por uma entrada do teclado. Se a tecla pressionada for 'q', o loop será interrompido e o programa será encerrado. A função waitKey retorna o código ASCII da tecla pressionada e o operador & é usado para mascarar os bits irrelevantes.
                break

class Capture:
    def __init__(self, video_input_object, output_path, frame_grab_interval, region_of_interest, file_name, first_image_number, last_image_number):
        self.video_input_object = video_input_object
        self.output_path = output_path
        self.frame_grab_interval = frame_grab_interval
        self.region_of_interest = region_of_interest
        self.file_name = file_name
        self.first_image_number = first_image_number
        self.last_image_number = last_image_number

    def capture_images(self):
        # Parâmetros internos
        VidFps = self.video_input_object.get(cv2.CAP_PROP_FPS)
        VidRes = (int(self.video_input_object.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.video_input_object.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        ImgNum = self.last_image_number - self.first_image_number + 1
        SmpTme = 1 / (VidFps / self.frame_grab_interval)
        TmeOut = 20 * ImgNum * SmpTme
        PthPtt = os.path.join(self.output_path, self.file_name)

        # Configuração da captura
        self.video_input_object.set(cv2.CAP_PROP_FPS, self.frame_grab_interval)
        self.video_input_object.set(cv2.CAP_PROP_FRAME_WIDTH, self.region_of_interest[2])
        self.video_input_object.set(cv2.CAP_PROP_FRAME_HEIGHT, self.region_of_interest[3])

        # Captura de imagens
        print('captcore: aquisição iniciada, aguarde!')
        imgs = []
        for _ in range(ImgNum):
            ret, frame = self.video_input_object.read()
            imgs.append(frame)
        print('captcore: aquisição concluída, salvando as imagens!')

        # Salvando imagens
        for idx, img in enumerate(imgs):
            filnme = PthPtt % (idx + self.first_image_number)
            cv2.imwrite(filnme, img)

        # Criação do arquivo de informações
        with open(os.path.join(self.output_path, 'info.txt'), 'w') as filidt:
            # Informações da câmera
            filidt.write('Camera general information:\n')
            filidt.write(f'\t* Resolution: {VidRes[0]} x {VidRes[1]}\n')
            filidt.write(f'\t* Frame rate: {VidFps}\n\n')

            # Informações da captura
            filidt.write('Acquisition information:\n')
            filidt.write(f'\t* Date and time: {datetime.now()}\n')
            filidt.write('\t* Region of interest:\n')
            filidt.write(f'\t\t* HrzOff: {self.region_of_interest[0]}\n')
            filidt.write(f'\t\t* VrtOff: {self.region_of_interest[1]}\n')
            filidt.write(f'\t\t* HrzLen: {self.region_of_interest[2]}\n')
            filidt.write(f'\t\t* VrtLen: {self.region_of_interest[3]}\n')
            filidt.write(f'\t* Frame Grab Interval: first of every {self.frame_grab_interval} frame(s)\n')
            filidt.write(f'\t\t* Thus, the sampling time was {SmpTme} seconds\n\n')
            # Obter informações adicionais da câmera (se necessário)
            # Exemplo de obtenção de informações adicionais: VidObj.get(propriedade)
            # propriedade pode ser CAP_PROP_* (ver lista de propriedades em https://docs.opencv.org/4.x/d4/d15/group__videoio__flags__base.html)

class Main:
    @staticmethod
    def run():
        output_path = 'C:\\Users\\lucas\\OneDrive\\Documentos\\TCC\\Prints'
        file_name = 'Img%03d.bmp'
        first_image_number = 1
        last_image_number = 10
        frame_grab_interval = 1 ## Define o intervalo entre cada captura de imagem, em milissegundos.
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

if __name__ == "__main__":
    Main.run()