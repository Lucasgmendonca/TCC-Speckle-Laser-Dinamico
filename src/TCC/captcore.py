import cv2
import os
from datetime import datetime

class Captcore:
    """Classe responsável por capturar imagens da câmera."""

    def __init__(self, video_input_object, output_path, frame_grab_interval, region_of_interest, file_name, first_image_number, last_image_number):
        """
        Inicializa a classe Captcore.

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
        if not 1 <= self.frame_grab_interval <= 99:
            raise ValueError('captcore: frame grab interval must be a scalar between 0 and 99!')
        if any(val < 0 for val in self.region_of_interest[:4]):
            raise ValueError('captcore: region of interest is not consistent!')
        if any((val1 + val2) > res for val1, val2, res in zip(self.region_of_interest[:2], self.region_of_interest[2:], video_resolution)):
            raise ValueError('captcore: region of interest is not compatible with video resolution!')

        # Configuração e captura das imagens
        self.video_input_object.set(cv2.CAP_PROP_FPS, self.frame_grab_interval)
        print('captcore: acquisition started, please wait!')
        captured_frames = []
        for _ in range(number_of_images):
            ret, frame = self.video_input_object.read()
            if not ret:
                break
            x, y, w, h = self.region_of_interest
            roi_frame = frame[y:y+h, x:x+w]
            gray_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
            captured_frames.append(gray_frame)
        print('captcore: acquisition completed, saving the images!')

        # Salvando imagens
        for i, img in enumerate(captured_frames):
            filename = full_file_path % (i + self.first_image_number)
            cv2.imwrite(filename, img)

        # Criação do arquivo de informações
        with open(os.path.join(self.output_path, 'info.txt'), 'w') as file_writer: 
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