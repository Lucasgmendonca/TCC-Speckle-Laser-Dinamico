import cv2
import os
from datetime import datetime

def capture_images(OutPth, GrbItv, RegItr, FilPtt='Img%03d.bmp', ImgFst=1, ImgLst=10):
    # Inicialização
    cv2.destroyAllWindows()

    # Criação do objeto de captura de vídeo
    VidObj = cv2.VideoCapture(0)

    # Abertura da janela de visualização
    while True:
        ret, frame = VidObj.read()
        cv2.imshow('Preview', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Parâmetros internos
    VidFps = VidObj.get(cv2.CAP_PROP_FPS)
    VidRes = (int(VidObj.get(cv2.CAP_PROP_FRAME_WIDTH)), int(VidObj.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    VidDev = "Webcam"
    ImgNum = ImgLst - ImgFst + 1
    SmpTme = 1 / (VidFps / GrbItv)
    TmeOut = 20 * ImgNum * SmpTme
    PthPtt = os.path.join(OutPth, FilPtt)

    # Configuração da captura
    VidObj.set(cv2.CAP_PROP_FPS, GrbItv)
    VidObj.set(cv2.CAP_PROP_FRAME_COUNT, ImgNum)
    VidObj.set(cv2.CAP_PROP_FRAME_WIDTH, RegItr[2])
    VidObj.set(cv2.CAP_PROP_FRAME_HEIGHT, RegItr[3])
    VidObj.set(cv2.CAP_PROP_FPS, TmeOut)

    # Captura de imagens
    print('captcore: aquisição iniciada, aguarde!')
    imgs = []
    for _ in range(ImgNum):
        ret, frame = VidObj.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        imgs.append(gray_frame)
    print('captcore: aquisição concluída, salvando as imagens!')

    # Salvando imagens
    for idx, img in enumerate(imgs):
        filnme = PthPtt % (idx + ImgFst)
        cv2.imwrite(filnme, img)

    # Criação do arquivo de informações
    with open(os.path.join(OutPth, 'info.txt'), 'w') as filidt:
        # Informações da câmera
        filidt.write('Camera general information:\n')
        filidt.write(f'\t* Name: {VidDev}\n')
        filidt.write(f'\t* Resolution: {VidRes[0]} x {VidRes[1]}\n')
        filidt.write(f'\t* Frame rate: {VidFps}\n\n')

        # Informações da captura
        filidt.write('Acquisition information:\n')
        filidt.write(f'\t* Date and time: {datetime.now()}\n')
        filidt.write('\t* Region of interest:\n')
        filidt.write(f'\t\t* HrzOff: {RegItr[0]}\n')
        filidt.write(f'\t\t* VrtOff: {RegItr[1]}\n')
        filidt.write(f'\t\t* HrzLen: {RegItr[2]}\n')
        filidt.write(f'\t\t* VrtLen: {RegItr[3]}\n')
        filidt.write(f'\t* Frame Grab Interval: first of every {GrbItv} frame(s)\n')
        filidt.write(f'\t\t* Thus, the sampling time was {SmpTme} seconds\n\n')
        filidt.write('Camera specific configuration (at the acquisition time):\n')
        # Obter informações adicionais da câmera (se necessário)
        # Exemplo de obtenção de informações adicionais: VidObj.get(propriedade)
        # propriedade pode ser CAP_PROP_* (ver lista de propriedades em https://docs.opencv.org/4.x/d4/d15/group__videoio__flags__base.html)
    # Libera a captura de vídeo
    VidObj.release()

# Parâmetros de exemplo
OutPth = 'C:\\Users\\lucas\\OneDrive\\Documentos\\TCC\\Prints'
GrbItv = 10
RegItr = (0, 0, 640, 480)  # (HrzOff, VrtOff, HrzLen, VrtLen)

# Chamada da função de captura
capture_images(OutPth, GrbItv, RegItr)