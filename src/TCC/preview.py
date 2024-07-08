import cv2
import os

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
            cv2.putText(gray_frame, 'Pressione a tecla "q" para fazer a captura', (10, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.imshow('Preview', gray_frame) ### Exibe o frame capturado em uma janela com o título "Preview". A função imshow do OpenCV é usada para exibir imagens.
            if cv2.waitKey(1) & 0xFF == ord('q'): ### Aguarda 1 milissegundo por uma entrada do teclado. Se a tecla pressionada for 'q', o loop será interrompido e o programa será encerrado. A função waitKey retorna o código ASCII da tecla pressionada e o operador & é usado para mascarar os bits irrelevantes.
                break