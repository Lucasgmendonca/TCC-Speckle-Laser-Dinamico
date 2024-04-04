import cv2
import os
from datetime import datetime
from preview import open_preview
from capture import capture_images

OutPth = 'C:\\Users\\lucas\\OneDrive\\Documentos\\TCC\\Prints'
GrbItv = 10
RegItr = (0, 0, 640, 480)  # (HrzOff, VrtOff, HrzLen, VrtLen)

# Criação do objeto de captura de vídeo
VidObj = cv2.VideoCapture(0)

# Chamada da função para abrir o preview
open_preview()

# Chamada da função de captura
capture_images(VidObj, OutPth, GrbItv, RegItr)
