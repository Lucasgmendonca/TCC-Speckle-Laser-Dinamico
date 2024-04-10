import cv2 ### Importa a biblioteca OpenCV, que é uma biblioteca popular de visão computacional.

#def open_preview(videoInputObject):
def open_preview():
    cv2.destroyAllWindows() ### Fecha todas as janelas abertas anteriormente pelo OpenCV, para garantir que não haja nenhuma janela aberta antes de abrir a nova janela de visualização.

    videoInputObject = cv2.VideoCapture(0)

    # Abertura da janela de visualização
    while True:
        ret, frame = videoInputObject.read() ### Lê um frame do vídeo capturado pela câmera e armazena-o nas variáveis ret (um booleano que indica se a leitura foi bem-sucedida) e frame (o próprio frame capturado).
        cv2.imshow('Preview', frame) ### Exibe o frame capturado em uma janela com o título "Preview". A função imshow do OpenCV é usada para exibir imagens.
        if cv2.waitKey(1) & 0xFF == ord('q'): ### Aguarda 1 milissegundo por uma entrada do teclado. Se a tecla pressionada for 'q', o loop será interrompido e o programa será encerrado. A função waitKey retorna o código ASCII da tecla pressionada e o operador & é usado para mascarar os bits irrelevantes.
            break