import copy
import numpy as np
from easy_task import Matrix as Matrix_main


def write_file(res, file_path):
    with open(file_path, "w") as f:
        np.savetxt(f, res, fmt='%-4.0f', delimiter=' ')


class Mixin:
    def __ne__(self, other):
        return not ((self.mat == other.mat).all())

    def __eq__(self, other):
        return (self.mat == other.mat).all()

    def __hash__(self):
        return int(np.prod(self.mat))  # hash = произведение элементов матрицы


class Matrix(Matrix_main, Mixin):
    cache = {}

    def old_matmul(self, other):
        self.check_dimension(other, make_matmul=True)
        row_number, col_number = self.mat_shape[0], other.mat_shape[1]
        res_matmul = [[0 for _ in range(col_number)] for _ in range(row_number)]

        for i in range(row_number):
            for j in range(self.mat_shape[1]):
                for k in range(col_number):
                    res_matmul[i][j] += self.mat[i, k] * other.mat[k, j]

        return res_matmul

    def __matmul__(self, other):
        h_1, h_2 = hash(self), hash(other)
        if (h_1, h_2) in self.cache:
            return Matrix(self.cache[(h_1, h_2)])

        res_matmul = self.old_matmul(other)
        self.cache[(h_1, h_2)] = np.array(res_matmul)

        return Matrix(self.cache[(h_1, h_2)])


def main():
    A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    B = np.random.randint(0, 10, (3, 3))
    C = np.array([[1, 4, 7], [2, 5, 8], [3, 6, 9]])
    D = copy.deepcopy(B)

    A_mat, B_mat, C_mat, D_mat = Matrix(A), Matrix(B), Matrix(C), Matrix(D)
    AB_mat = A_mat @ B_mat
    CD_mat = C_mat @ D_mat

    assert (hash(A_mat) == hash(C_mat)) and (A_mat != C_mat) and (B_mat == D_mat)

    write_file(A_mat.mat, 'artifacts/hard/A.txt')
    write_file(B_mat.mat, 'artifacts/hard/B.txt')
    write_file(C_mat.mat, 'artifacts/hard/C.txt')
    write_file(D_mat.mat, 'artifacts/hard/D.txt')

    write_file(AB_mat.mat, 'artifacts/hard/AB.txt')
    hash_ = Matrix(np.array([[hash(AB_mat), hash(CD_mat)]]))
    write_file(hash_.mat, 'artifacts/hard/hash.txt')

    Matrix.cache = {}
    CD_mat = C_mat @ D_mat

    assert AB_mat != CD_mat
    write_file(CD_mat.mat, 'artifacts/hard/CD.txt')


if __name__ == '__main__':
    np.random.seed(0)
    main()
