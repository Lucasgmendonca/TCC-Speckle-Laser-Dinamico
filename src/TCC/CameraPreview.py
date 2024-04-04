# Importação das bibliotecas necessárias
import cv2

class Main:
    # Inicialização da variável para capturar a webcam
    vidObj = cv2.VideoCapture(0) # Escolha a câmera pelo índice

    # Loop para captura e exibição de frames
    while True:
        # Leitura de um frame
        ret, frame = vidObj.read()

        # Exibição do frame
        cv2.imshow('Preview', frame)

        # Verificação da tecla 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberação da captura da webcam
    vidObj.release()

    # Destruição de todas as janelas
    cv2.destroyAllWindows()

    outPth = 'C:\\Users\\lucas\\OneDrive\\Documentos\\TCC\\Prints'
    filPtt = 'Img%03d.bmp'
    imgFst = 1
    imgLst = 5
    grbItv = 1
    regItr = [0, 0, 640, 480]

    vidCapPro = VidCapPro()
    vidCapPro.captcore(vidObj, outPth, filPtt, imgFst, imgLst, grbItv, regItr)



