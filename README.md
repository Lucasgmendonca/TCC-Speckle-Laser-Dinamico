# Speckle Laser Dinâmico

## Descrição

O projeto "Speckle Laser Dinâmico" é uma aplicação em Python que utiliza bibliotecas como OpenCV para processar imagens e vídeos. A aplicação é dividida em quatro modos principais: visualização de vídeo, captura de imagens, análise de histórico de pixels e análise numérica dos dados capturados.

## Estrutura do Projeto

O projeto é composto pelos seguintes módulos:

- **`preview.py`**: Define a classe `Preview` para mostrar uma pré-visualização do vídeo da câmera.
- **`captcore.py`**: Define a classe `Captcore` para capturar e salvar imagens do vídeo.
- **`thspcore.py`**: Define a classe `PixelHistory` para rastrear o histórico de pixels das imagens capturadas.
- **`numecore.py`**: Define a classe `NumericalAnalysis` para realizar análises numéricas nos dados históricos dos pixels.

## Requisitos

- Python 3.x
- OpenCV
- NumPy
- Tkinter (geralmente incluído na instalação padrão do Python)

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/Lucasgmendonca/TCC-Speckle-Laser-Dinamico.git
    cd <TCC-Speckle-Laser-Dinamico>
    ```

2. Instale as dependências necessárias:
    ```bash
    pip install opencv-python numpy
    ```

## Arquivos Gerados

- **`info.txt`**: Informações sobre a câmera e o processo de captura.
- **`thspcore_output.txt`**: Array de resultados da função thspcore.
- **`pixel_history.txt`**: Histórico de pixels.
- **`numerical_result.txt`**: Resultado numérico.
- **`co_occurrence_matrix.txt`**: Matriz de co-ocorrência.

