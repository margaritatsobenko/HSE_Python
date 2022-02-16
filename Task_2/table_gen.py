def str_transform(row):
    return ' & '.join(list(map(str, row))) + ' \\\\' + ' \hline' + '\n'


def get_row_list(input_list):
    rows_file = list(map(str_transform, input_list))
    return rows_file


def get_l_row(num_l):
    str_file = '\\begin{tabular}{' + '|l' * num_l + '|' + '}' + '\n' + '\hline' + '\n'
    return str_file


def write_file(file_name, row_list, row_l):
    with open(file_name, "w") as file1:
        file1.write("\\begin{table}[]\n")
        file1.write(row_l)
        for row in row_list:
            file1.write(row)
        file1.write('\\end{tabular}\n')
        file1.write('\\end{table}\n')


def main():
    s = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
    num_l = len(s[0])

    row_file = get_row_list(s)
    str_file = get_l_row(num_l)

    write_file("artifacts/table.tex", row_file, str_file)


if __name__ == '__main__':
    main()
