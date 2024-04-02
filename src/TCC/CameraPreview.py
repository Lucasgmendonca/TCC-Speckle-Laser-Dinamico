# Importação das bibliotecas necessárias
import cv2

# Inicialização da variável para capturar a webcam
camera = cv2.VideoCapture(0) # Escolha a câmera pelo índice

# Loop para captura e exibição de frames
while True:
    # Leitura de um frame
    ret, frame = camera.read()

    # Exibição do frame
    cv2.imshow('Preview', frame)

    # Verificação da tecla 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberação da captura da webcam
camera.release()

# Destruição de todas as janelas
cv2.destroyAllWindows()

