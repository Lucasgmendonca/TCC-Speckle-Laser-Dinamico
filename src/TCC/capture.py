import cv2
import os
from datetime import datetime

def capture_images(VidObj, OutPth, GrbItv, RegItr, FilPtt='Img%03d.bmp', ImgFst=1, ImgLst=10):
    # Parâmetros internos
    VidFps = VidObj.get(cv2.CAP_PROP_FPS)
    VidRes = (int(VidObj.get(cv2.CAP_PROP_FRAME_WIDTH)), int(VidObj.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    ImgNum = ImgLst - ImgFst + 1
    SmpTme = 1 / (VidFps / GrbItv)
    TmeOut = 20 * ImgNum * SmpTme
    PthPtt = os.path.join(OutPth, FilPtt)

    # Configuração da captura
    VidObj.set(cv2.CAP_PROP_FPS, GrbItv)
    VidObj.set(cv2.CAP_PROP_FRAME_WIDTH, RegItr[2])
    VidObj.set(cv2.CAP_PROP_FRAME_HEIGHT, RegItr[3])

    # Captura de imagens
    print('captcore: aquisição iniciada, aguarde!')
    imgs = []
    for _ in range(ImgNum):
        ret, frame = VidObj.read()
        imgs.append(frame)
    print('captcore: aquisição concluída, salvando as imagens!')

    # Salvando imagens
    for idx, img in enumerate(imgs):
        filnme = PthPtt % (idx + ImgFst)
        cv2.imwrite(filnme, img)

    # Criação do arquivo de informações
    with open(os.path.join(OutPth, 'info.txt'), 'w') as filidt:
        # Informações da câmera
        filidt.write('Camera general information:\n')
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