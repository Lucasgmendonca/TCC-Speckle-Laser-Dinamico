import tkinter as tk
from preview import Preview
from captcore import Captcore
from thspcore import PixelHistory
from numecore import NumericalAnalysis

class Main:

    @staticmethod
    def run(mode):
        if mode == 'camprev':
            preview = Preview()
            preview.open_preview()
            preview.video_input_object.release()

        elif mode == 'camprev_captcore':
            preview = Preview()
            #preview.open_preview()
            preview.open_preview_configured()
            output_path = 'C:\\Users\\lucas\\OneDrive\\Documentos\\TCC\\Prints'
            file_name = 'Img%03d.bmp'
            first_image_number = 1
            last_image_number = 10
            frame_grab_interval = 1
            region_of_interest = (0, 60, 640, 360)
            captcore = Captcore(preview.video_input_object, output_path, frame_grab_interval, region_of_interest, file_name, first_image_number, last_image_number)
            captcore.capture_images()
            preview.video_input_object.release()

        # elif mode == 'thspcore':
        #     output_path = 'C:\\Users\\lucas\\OneDrive\\Documentos\\TCC\\Prints'
        #     file_name = 'Img%03d.bmp'
        #     first_image_number = 1
        #     last_image_number = 10
        #     pixel_selection = 'a'
        #     selection_specific = None
        #     pixel_index = 0
        #     pix_hist = PixelHistory(output_path, file_name, first_image_number, last_image_number, pixel_selection, selection_specific, pixel_index)

        # elif mode == 'numecore':
        #     output_path = 'C:\\Users\\lucas\\OneDrive\\Documentos\\TCC\\Prints'
        #     method_selection = 5 
        #     num_analysis = NumericalAnalysis(pixel_history_data, method_selection)
        #     num_analysis.numecore()

        elif mode == 'thspcore_numecore':
            output_path = 'C:\\Users\\lucas\\OneDrive\\Documentos\\TCC\\Prints'
            file_name = 'Img%03d.bmp'
            first_image_number = 1
            last_image_number = 10
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