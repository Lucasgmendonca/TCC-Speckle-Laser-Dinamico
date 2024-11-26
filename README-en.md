[Não fala inglês? Clique aqui](https://github.com/Lucasgmendonca/TCC-Speckle-Laser-Dinamico/blob/main/README.md)

# Dynamic Laser Speckle

## Description

The "Dynamic Laser Speckle" project is a Python application that uses libraries like OpenCV to process images and videos. The application is divided into four main modes: video preview, image capture, pixel history analysis, and numerical analysis of captured data.

## Features
The system offers the following modes of operation:

- **Video Preview (Preview)**: Displays a real-time video feed from the camera.
- **Captura de Imagens (Captcore)**: Captures and saves images from the video feed, allowing the specification of regions of interest and capture intervals.
- **Análise do Histórico de Pixels (Thspcore)**: Tracks the history of pixels in captured images with customizable selection modes.
- **Análise Numérica (Numecore)**: Performs statistical and mathematical calculations on pixel history data using methods such as Moment of Inertia and Standard Deviation.

## Project Structure

The project consists of the following modules:

- **`preview.py`**: Defines the `Preview` class for displaying a live video feed.
- **`captcore.py`**: Defines the `Captcore` class for capturing and saving video images.
- **`thspcore.py`**: Defines the `PixelHistory` class for tracking the pixel history of captured images.
- **`numecore.py`**: Defines the `NumericalAnalysis` class for performing numerical analysis on pixel history data.

## Requirements

- Python 3.x
- Python Libraries:
    - OpenCV
    - NumPy
- Tkinter (typically included in the default Python installation)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Lucasgmendonca/TCC-Speckle-Laser-Dinamico.git
    cd TCC-Speckle-Laser-Dinamico
    ```

2. Install the required dependencies:
    ```bash
    pip install opencv-python numpy
    ```

## Generated Files

- **`info.txt`**: Information about the camera and the capture process.
- **`thspcore_output.txt`**: Array of results from the thspcore function.
- **`pixel_history.txt`**: Pixel history.
- **`numerical_result.txt`**: Numerical analysis results.
- **`co_occurrence_matrix.txt`**: Co-occurrence matrix.

## Contribution

This project is an academic work (TCC) and is open for contributions. If you have suggestions or improvements, feel free to open issues or submit pull requests.

## License

This project is released for any type of use. Feel free to modify and use it in your own implementations.
