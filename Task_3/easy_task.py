import numpy as np


def write_file(res, file_path):
    with open(file_path, "w") as f:
        np.savetxt(f, res, fmt='%-4.0f', delimiter=' ')


class Matrix:

    def __init__(self, mat: np.ndarray):
        self.mat = mat
        self.mat_shape = mat.shape

    def check_dimension(self, other, make_matmul=False):
        if make_matmul and self.mat_shape[1] != other.mat_shape[0]:
            raise ValueError("Change the dimensions of the matrices for matrix multiplication!")

        elif self.mat_shape != other.mat_shape:
            raise ValueError("Change the dimensions of the matrices for elementwise multiplication and addition!")

    def __add__(self, other):
        self.check_dimension(other)
        res_add = [[self.mat[i, j] + other.mat[i, j] for j in range(self.mat_shape[1])]
                   for i in range(self.mat_shape[0])]
        return Matrix(np.array(res_add))

    def __mul__(self, other):
        self.check_dimension(other)
        res_mul = [[self.mat[i, j] * other.mat[i, j] for j in range(self.mat_shape[1])]
                   for i in range(self.mat_shape[0])]
        return Matrix(np.array(res_mul))

    def __matmul__(self, other):
        self.check_dimension(other, make_matmul=True)
        row_number, col_number = self.mat_shape[0], other.mat_shape[1]
        res_matmul = [[0 for _ in range(col_number)] for _ in range(row_number)]

        for i in range(row_number):
            for j in range(self.mat_shape[1]):
                for k in range(col_number):
                    res_matmul[i][j] += self.mat[i, k] * other.mat[k, j]

        return Matrix(np.array(res_matmul))


def main():
    A = np.random.randint(0, 10, (10, 10))
    B = np.random.randint(0, 10, (10, 10))

    A_mat, B_mat = Matrix(A), Matrix(B)
    write_file((A_mat + B_mat).mat, 'artifacts/easy/matrix+.txt')
    write_file((A_mat * B_mat).mat, 'artifacts/easy/matrix*.txt')
    write_file((A_mat @ B_mat).mat, 'artifacts/easy/matrix@.txt')


if __name__ == '__main__':
    np.random.seed(0)
    main()
