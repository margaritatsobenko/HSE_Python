import numpy as np


class Mixin:
    def __init__(self, mat):
        self.mat = mat

    def write_file(self, file_path):
        with open(file_path, "w") as f:
            np.savetxt(f, self.mat, fmt='%-4.0f', delimiter=' ')

    @property
    def mat(self):
        return self._mat

    @mat.setter
    def mat(self, mat):
        self._mat = mat

    def __str__(self):
        return '\n'.join(['  '.join(map(str, i)) for i in self.mat])


class Matrix(Mixin, np.lib.mixins.NDArrayOperatorsMixin):
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        return Matrix(ufunc(inputs[0].mat, inputs[1].mat))


def main():
    A = np.random.randint(0, 10, (10, 10))
    B = np.random.randint(0, 10, (10, 10))

    A_mat, B_mat = Matrix(A), Matrix(B)
    print(A_mat)
    (A_mat + B_mat).write_file('artifacts/medium/matrix+.txt')
    (A_mat * B_mat).write_file('artifacts/medium/matrix*.txt')
    (A_mat @ B_mat).write_file('artifacts/medium/matrix@.txt')


if __name__ == '__main__':
    np.random.seed(0)
    main()
