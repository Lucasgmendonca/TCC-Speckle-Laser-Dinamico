import cv2

def open_preview():
    cv2.destroyAllWindows()

    # Criação do objeto de captura de vídeo
    VidObj = cv2.VideoCapture(0)

    # Abertura da janela de visualização
    while True:
        ret, frame = VidObj.read()
        cv2.imshow('Preview', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break