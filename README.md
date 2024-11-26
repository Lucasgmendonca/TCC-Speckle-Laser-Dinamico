[Don't speak Portuguese? Click here](https://github.com/Lucasgmendonca/TCC-Speckle-Laser-Dinamico/blob/main/README-en.md)

# Speckle Laser Dinâmico

## Descrição

O projeto "Speckle Laser Dinâmico" é uma aplicação em Python que utiliza bibliotecas como OpenCV para processar imagens e vídeos. A aplicação é dividida em quatro modos principais: visualização de vídeo, captura de imagens, análise de histórico de pixels e análise numérica dos dados capturados.

## Funcionalidades
O sistema oferece os seguintes modos de operação:

- **Visualização de Vídeo (Preview)**: Exibe a pré-visualização do feed de vídeo da câmera em tempo real.
- **Captura de Imagens (Captcore)**: Captura e salva imagens do feed de vídeo, permitindo especificar a região de interesse e intervalos de captura.
- **Análise do Histórico de Pixels (Thspcore)**: Rastreia o histórico de pixels em imagens capturadas, com modos de seleção personalizáveis.
- **Análise Numérica (Numecore)**: Realiza cálculos estatísticos e matemáticos sobre o histórico de pixels utilizando métodos como Momento de Inércia e Desvio Padrão.

## Estrutura do Projeto

O projeto é composto pelos seguintes módulos:

- **`preview.py`**: Define a classe `Preview` para mostrar uma pré-visualização do vídeo da câmera.
- **`captcore.py`**: Define a classe `Captcore` para capturar e salvar imagens do vídeo.
- **`thspcore.py`**: Define a classe `PixelHistory` para rastrear o histórico de pixels das imagens capturadas.
- **`numecore.py`**: Define a classe `NumericalAnalysis` para realizar análises numéricas nos dados históricos dos pixels.

## Requisitos

- Python 3.x
- Bibliotecas Python:
    - OpenCV
    - NumPy
- Tkinter (geralmente incluído na instalação padrão do Python)

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/Lucasgmendonca/TCC-Speckle-Laser-Dinamico.git
    cd TCC-Speckle-Laser-Dinamico
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

## Contribuição

Este projeto é um trabalho acadêmico (TCC) e está aberto para contribuições. Caso tenha sugestões ou melhorias, sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está liberado para qualquer tipo de uso. Sinta-se livre para modificá-lo e utilizá-lo em suas próprias implementações.
