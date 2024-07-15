import cv2
import os
import numpy as np

class PixelHistory:

    def __init__(self, image_path, file_name, first_image_number, last_image_number, pixel_selection, selection_specifier):
        self.image_path = image_path
        self.file_name = file_name
        self.first_image_number = first_image_number
        self.last_image_number = last_image_number
        self.pixel_selection = pixel_selection
        self.selection_specifier = selection_specifier
        
    def track_pixel_history(self):
        if self.pixel_selection == 'a':
            if self.selection_specifier is not None:
                raise ValueError("For 'pixel_selection' = 'a', 'selection_specifier' must be None.")
        elif self.pixel_selection == 'h':
            if self.selection_specifier not in ['m', 'e'] and not (isinstance(self.selection_specifier, int) and 0 < self.selection_specifier < 361):
                raise ValueError("For 'pixel_selection' = 'h', 'selection_specifier' must be 'm', 'e', or a number greater than 0 and less than 361.")
        elif self.pixel_selection == 'v':
            if self.selection_specifier not in ['m', 'e'] and not (isinstance(self.selection_specifier, int) and 0 < self.selection_specifier < 641):
                raise ValueError("For 'pixel_selection' = 'v', 'selection_specifier' must be 'm', 'e', or a number greater than 0 and less than 641.")
        elif self.pixel_selection == 'r':
            if not (isinstance(self.selection_specifier, int) and 0 < self.selection_specifier < 230401):
                raise ValueError("For 'pixel_selection' = 'r', 'selection_specifier' must be a number greater than 0 and less than 230401.")
        else:
            raise ValueError(f"Unknown pixel selection mode: {self.pixel_selection}")

        full_file_pattern = os.path.join(self.image_path, self.file_name)
        num_images = self.last_image_number - self.first_image_number + 1

        first_image_file = full_file_pattern % self.first_image_number
        img_pix = cv2.imread(first_image_file, cv2.IMREAD_GRAYSCALE)
        img_lin, img_row = img_pix.shape

        pix_his = [None] * 3
        if self.pixel_selection == 'a':
            pix_his[0] = np.zeros((img_lin * img_row, num_images), dtype=np.int32)
            pix_his[2] = [img_lin, img_row]
        elif self.pixel_selection == 'h':
            pix_his[0] = np.zeros((img_row, num_images), dtype=np.int32)
            if self.selection_specifier == 'm':
                pix_his[2] = round(img_lin / 2)
            elif self.selection_specifier == 'e':
                pix_his[2] = img_lin-1
            else:
                pix_his[2] = self.selection_specifier
        elif self.pixel_selection == 'v':
            pix_his[0] = np.zeros((img_lin, num_images), dtype=np.int32)
            if self.selection_specifier == 'm':
                pix_his[2] = round(img_row / 2)
            elif self.selection_specifier == 'e':
                pix_his[2] = img_row-1
            else:
                pix_his[2] = self.selection_specifier
        elif self.pixel_selection == 'r':
            if self.selection_specifier < 1:
                num_pix = round(img_lin * img_row * self.selection_specifier)
            else:
                num_pix = self.selection_specifier
            pix_his[0] = np.zeros((num_pix, num_images), dtype=np.int32)
            pix_his[2] = np.column_stack((np.random.randint(0, img_lin, num_pix), np.random.randint(0, img_row, num_pix)))
        else:
            raise ValueError('thspcore: unknown pixel selection mode!')

        pix_his[1] = self.pixel_selection

        for idx_img in range(num_images):
            image_file = full_file_pattern % (idx_img + self.first_image_number)
            img_pix = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE).astype(np.int32)
            if self.pixel_selection == 'a':
                for idx_lin in range(img_lin):
                    aux_ini = img_row * idx_lin
                    aux_fin = img_row * (idx_lin + 1)
                    pix_his[0][aux_ini:aux_fin, idx_img] = img_pix[idx_lin, :]
            elif self.pixel_selection == 'h':
                pix_his[0][:, idx_img] = img_pix[pix_his[2], :]
            elif self.pixel_selection == 'v':
                pix_his[0][:, idx_img] = img_pix[:, pix_his[2]]
            elif self.pixel_selection == 'r':
                for idx_pix in range(num_pix):
                    pix_his[0][idx_pix, idx_img] = img_pix[pix_his[2][idx_pix, 0], pix_his[2][idx_pix, 1]]

        # Saving the result (array) to a text file
        with open('thspcore_output.txt', 'w') as f:
            print(pix_his, file=f)
        print("Results saved in 'thspcore_output.txt'.")

        # Saving pixel history to a text file
        with open('pixel_history.txt', 'w') as file:
            for array in pix_his[0]:
                for value in array:
                    file.write(f"{value} ")
                file.write("\n")
        print("Pixel history saved in 'pixel_history.txt'")
