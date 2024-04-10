import cv2 ### Importa a biblioteca OpenCV, que é uma biblioteca popular de visão computacional.
from preview import open_preview
from capture import capture_images

# Configurações
outputPath = 'C:\\Users\\lucas\\OneDrive\\Documentos\\TCC\\Prints'
fileName = 'Img%03d.bmp'
firstImageNumber = 1 
lastImageNumber = 10
frameGrabInterval = 10 ## Define o intervalo entre cada captura de imagem, em milissegundos.
regionOfInterest = (0, 0, 640, 480)  ### (a, b, x, y)
### a: É o deslocamento horizontal (ou posição) da região de interesse a partir da extremidade esquerda da imagem ou vídeo.
### b: É o deslocamento vertical (ou posição) da região de interesse a partir da extremidade superior da imagem ou vídeo.
### x: É o comprimento horizontal da região de interesse.
### y: É o comprimento vertical da região de interesse.

# Criação do objeto de captura de vídeo
videoInputObject = cv2.VideoCapture(0)
### Cria um objeto de captura de vídeo (videoInputObject) que representa a câmera.
### O argumento 0 indica que queremos capturar vídeo da primeira câmera disponível no sistema.

# Chamada da função para abrir o preview
# open_preview(videoInputObject)
open_preview()

# Chamada da função de captura
capture_images(videoInputObject, outputPath, frameGrabInterval, regionOfInterest, fileName, firstImageNumber, lastImageNumber)
