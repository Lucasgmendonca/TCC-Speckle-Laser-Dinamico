import numpy as np

class NumericalAnalysis:

    def __init__(self, pixel_history_data, method_selection):
        self.pixel_history_data = pixel_history_data
        self.method_selection = method_selection

    def numecore(self):
        num_res = 0
        co_matr = np.zeros((256, 256), dtype=np.int32)

        if self.method_selection > 5:
            raise ValueError('numecore: unknown method of analysis!')

        sts_lin = self.pixel_history_data.shape[0]
        sts_row = self.pixel_history_data.shape[1]

        if self.method_selection < 3 or self.method_selection > 4:
            for idx_lin in range(sts_lin):
                for idx_row in range(sts_row - 1):
                    pix_now = round(self.pixel_history_data[idx_lin, idx_row])
                    pix_nxt = round(self.pixel_history_data[idx_lin, idx_row + 1])
                    co_matr[pix_now, pix_nxt] += 1 

        if self.method_selection == 1:
            for idx_lin in range(256):
                for idx_row in range(256):
                    num_res += co_matr[idx_lin, idx_row] * (idx_lin - idx_row) ** 2
            nrmfac = (sts_row - 1) * sts_lin
            num_res /= nrmfac

        if self.method_selection == 2:
            for idx_lin in range(256):
                for idx_row in range(256):
                    num_res += co_matr[idx_lin, idx_row] * abs(idx_lin - idx_row)
            nrmfac = (sts_row - 1) * sts_lin 
            num_res /= nrmfac

        if self.method_selection == 3:
            num_res = np.mean(np.std(self.pixel_history_data, axis=1))

        if self.method_selection == 4:
            num_res = np.mean(self.pixel_history_data)

        if self.method_selection == 5:
            for idx_lin in range(256):
                for idx_row in range(256):
                    if idx_lin + idx_row != 0:
                        num_res += co_matr[idx_lin, idx_row] * (abs(idx_lin - idx_row) / (idx_lin + idx_row))
            nrmfac = (sts_row - 1) * sts_lin
            num_res /= nrmfac

        # Saving the numeric result to a text file
        with open('numerical_result.txt', 'w') as file:
            file.write(f"Numerical Result: {num_res}\n")
        print("Numeric result saved in 'numerical_result.txt'.")

        # Saving the co-occurrence matrix to a text file
        with open('co_occurrence_matrix.txt', 'w') as file:
            for row in co_matr:
                for value in row:
                    file.write(f"{value} ")
                file.write("\n")
        print("Co-occurrence matrix saved in 'co_occurrence_matrix.txt'.")