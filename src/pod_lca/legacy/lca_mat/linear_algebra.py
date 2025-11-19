from numpy import matrix, zeros

__author__ = ["POD/LCA Team"]
__copyright__ = "Univrsity of Washington"
__license__ = "MIT License"
__email__ = "kiun@uw.edu"
__version__ = "0.1.0"


class LinearAlgebra:

    @staticmethod
    def mat_data_to_np_mat(mat_data):
        """Convert the matrix data in dictionary to a numpy matrix.
        Matrix data is kept in a dictionary of dictionaries, where the outer dictionary key is column number (process)
        and the inner dictionary key is the row numbern (inventory item) and the value is the value (qty) on the
        corresponding entry of the matrix.
        """

        no_col = len(mat_data)
        no_row = 0
        for col in mat_data.keys():
            max_nnz_row = max(mat_data[col].keys())
            if max_nnz_row > no_row:
                no_row = max_nnz_row

        mat = zeros((no_row + 1, no_col))

        for col in mat_data.keys():
            for row in mat_data[col].keys():
                mat[row][col] = mat_data[col][row]

        return mat

    @staticmethod
    def matrix_inverse(mat_data):
        """Returns the inverse of a matrix."""

        mat = matrix(LinearAlgebra.mat_data_to_np_mat(mat_data))

        return mat.I

    @staticmethod
    def matrix_pseudo_inverse(mat_data):
        """Returns the Moore-Penrose pseudo inverse of a matrix."""

        mat = matrix(LinearAlgebra.mat_data_to_np_mat(mat_data))

        return ((mat.transpose * mat).I).transporse
