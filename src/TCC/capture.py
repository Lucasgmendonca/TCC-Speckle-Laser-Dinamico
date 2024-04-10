import cv2
import os
from datetime import datetime

def capture_images(videoInputObject, outputPath, frameGrabInterval, regionOfInterest, fileName, firstImageNumber, lastImageNumber):
    # Parâmetros internos
    VidFps = videoInputObject.get(cv2.CAP_PROP_FPS)
    VidRes = (int(videoInputObject.get(cv2.CAP_PROP_FRAME_WIDTH)), int(videoInputObject.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    ImgNum = lastImageNumber - firstImageNumber + 1
    SmpTme = 1 / (VidFps / frameGrabInterval)
    TmeOut = 20 * ImgNum * SmpTme
    PthPtt = os.path.join(outputPath, fileName)

    # Configuração da captura
    videoInputObject.set(cv2.CAP_PROP_FPS, frameGrabInterval)
    videoInputObject.set(cv2.CAP_PROP_FRAME_WIDTH, regionOfInterest[2])
    videoInputObject.set(cv2.CAP_PROP_FRAME_HEIGHT, regionOfInterest[3])

    # Captura de imagens
    print('captcore: aquisição iniciada, aguarde!')
    imgs = []
    for _ in range(ImgNum):
        ret, frame = videoInputObject.read()
        imgs.append(frame)
    print('captcore: aquisição concluída, salvando as imagens!')

    # Salvando imagens
    for idx, img in enumerate(imgs):
        filnme = PthPtt % (idx + firstImageNumber)
        cv2.imwrite(filnme, img)

    # Criação do arquivo de informações
    with open(os.path.join(outputPath, 'info.txt'), 'w') as filidt:
        # Informações da câmera
        filidt.write('Camera general information:\n')
        filidt.write(f'\t* Resolution: {VidRes[0]} x {VidRes[1]}\n')
        filidt.write(f'\t* Frame rate: {VidFps}\n\n')

        # Informações da captura
        filidt.write('Acquisition information:\n')
        filidt.write(f'\t* Date and time: {datetime.now()}\n')
        filidt.write('\t* Region of interest:\n')
        filidt.write(f'\t\t* HrzOff: {regionOfInterest[0]}\n')
        filidt.write(f'\t\t* VrtOff: {regionOfInterest[1]}\n')
        filidt.write(f'\t\t* HrzLen: {regionOfInterest[2]}\n')
        filidt.write(f'\t\t* VrtLen: {regionOfInterest[3]}\n')
        filidt.write(f'\t* Frame Grab Interval: first of every {frameGrabInterval} frame(s)\n')
        filidt.write(f'\t\t* Thus, the sampling time was {SmpTme} seconds\n\n')
        filidt.write('Camera specific configuration (at the acquisition time):\n')
        # Obter informações adicionais da câmera (se necessário)
        # Exemplo de obtenção de informações adicionais: VidObj.get(propriedade)
        # propriedade pode ser CAP_PROP_* (ver lista de propriedades em https://docs.opencv.org/4.x/d4/d15/group__videoio__flags__base.html)
    # Libera a captura de vídeo
    videoInputObject.release()