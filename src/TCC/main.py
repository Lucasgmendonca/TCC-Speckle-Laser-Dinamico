import tkinter as tk

import numpy as np
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
            output_path = 'C:\\TCC\\Prints' # Output Path
            file_name = 'Img%03d.bmp' # Images file name Pattern
            first_image_number = 1 # First Image number
            last_image_number = 10 # Last Image number
            frame_grab_interval = 1 # frame Grab Interval
            region_of_interest = (0, 60, 640, 360) # Region of Interest = [HrzOff VrtOff HrzLen VrtLen]
            # HrzOff: horizontal offset from the left video border (in pixels)
            # VrtOff: vertical offset from the top video border (in pixels)
            # HrzLen: width of the window (in pixels)
            # VrtLen: height of the window (in pixels)
            captcore = Captcore(preview.video_input_object, output_path, frame_grab_interval, region_of_interest, file_name, first_image_number, last_image_number)
            captcore.capture_images()
            preview.video_input_object.release()

        elif mode == 'thspcore':
            image_path = 'C:\\TCC\\Prints' # Path to Images folder
            file_name = 'Img%03d.bmp' # Images file name Pattern
            first_image_number = 1 # First Image number
            last_image_number = 128 # Last Image number
            pixel_selection = 'a'   
            # Pixel Selection mode:
            # 'a' - all pixels in the image
            # 'h' - all pixels in a line
            # 'v' - all pixels in a row
            # 'r' - random pixels in the image
            selection_specific = None
            # Pixel Selection Specifications
            # 'a' mode
            #     None - this parameter is disregarded in this mode
            # 'h' mode
            #     'm' - middle line
            #     'e' - end line
            #     ### - line number
            # 'v' mode
            #     'm' - middle row
            #     'e' - end row
            #     ### - row number
            # 'r' mode
            #     ### - number of pixels (relative if ### < 1)
            thspcore = PixelHistory(image_path, file_name, first_image_number, last_image_number, pixel_selection, selection_specific)
            thspcore.track_pixel_history()

        elif mode == 'numecore':
            pixel_history_data = np.loadtxt('pixel_history.txt')
            method_selection = 2
            # Method Selection
            # '1' - Moment of Inertia (MoI)
            # '2' - Absolute Value of Diferences (AVD)
            # '3' - Standard Deviation (SD)
            # '4' - Average Pixel Intensity (API)
            # '5' - New Absolute Value of Diferences (New AVD)
            numecore = NumericalAnalysis(pixel_history_data, method_selection)
            numecore.numecore()

    @staticmethod
    def choose_mode():
        root = tk.Tk()
        root.title("Speckle Laser Dinâmico")

        def start_mode(mode):
            root.destroy()
            Main.run(mode)

        tk.Label(root, text="Choose the function to be performed:").pack(pady=10)
        
        button_width = 50
        
        tk.Button(root, text="1. Only Preview ", width=button_width, command=lambda: start_mode('camprev')).pack(pady=5)
        tk.Button(root, text="2. Preview + Captcore", width=button_width, command=lambda: start_mode('camprev_captcore')).pack(pady=5)
        tk.Button(root, text="3. thspcore", width=button_width, command=lambda: start_mode('thspcore')).pack(pady=5)
        tk.Button(root, text="4. numecore", width=button_width, command=lambda: start_mode('numecore')).pack(pady=5)
        
        root.mainloop()

if __name__ == "__main__":
    Main.choose_mode()