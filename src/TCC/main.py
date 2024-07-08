import tkinter as tk
from preview import Preview
from capture import Capture
from pixel_history import PixelHistory
from numericalanalysis import NumericalAnalysis

class Main:

    @staticmethod
    def run(mode):
        output_path = 'C:\\Users\\lucas\\OneDrive\\Documentos\\TCC\\Prints'
        file_name = 'Img%03d.bmp'
        first_image_number = 1
        last_image_number = 10
        
        if mode == 'camprev_captcore':
            frame_grab_interval = 1 
            region_of_interest = (0, 60, 640, 360)
            preview = Preview(region_of_interest)
            preview.open_preview()
            capture = Capture(preview.video_input_object, output_path, frame_grab_interval, region_of_interest, file_name, first_image_number, last_image_number)
            capture.capture_images()
            preview.video_input_object.release()

        elif mode == 'thspcore_numecore':
            pixel_selection = 'a'
            selection_specific = None
            pixel_index = 0
            pix_hist = PixelHistory(output_path, file_name, first_image_number, last_image_number, pixel_selection, selection_specific, pixel_index)
            pixel_history_data = pix_hist.track_pixel_history()
            method_selection = 5 
            num_analysis = NumericalAnalysis(pixel_history_data, method_selection)
            num_analysis.numecore()

    @staticmethod
    def choose_mode():
        root = tk.Tk()
        root.title("Speckle Laser Dinâmico")

        def start_mode(mode):
            root.destroy()
            Main.run(mode)

        tk.Label(root, text="Escolha a função a ser executada:").pack(pady=10)
        
        button_width = 50
        
        tk.Button(root, text="1. Visualização da câmera e Captura das imagens (captcore)", width=button_width, command=lambda: start_mode('camprev_captcore')).pack(pady=5)
        tk.Button(root, text="2. Análise das imagens (thspcore & numecore)", width=button_width, command=lambda: start_mode('thspcore_numecore')).pack(pady=5)
        
        root.mainloop()

if __name__ == "__main__":
    Main.choose_mode()