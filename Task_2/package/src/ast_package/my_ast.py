import ast

import matplotlib.pyplot as plt
import networkx as nx


def read_ast(path="fib.py"):
    # прочитаем код Фибоначчи как текст
    with open(path, 'r') as f:
        code = f.read()

    ast_parse = ast.parse(code)

    return ast_parse


def parse_ast(ast_parse):
    # сюда будем сохранять все операции, полученные из ast
    answer = {"name": ast_parse.body[0].name}

    for b in ast_parse.body[0].body:
        # print(b)
        if isinstance(b, ast.Assign):
            variable_name = b.targets[0].id
            values = [b.value.elts[0].n, b.value.elts[1].n]

            answer["assign"] = answer.get("assign", []) + [variable_name + ' = ' + str(values)]

        elif isinstance(b, ast.If):
            variable_name_1 = b.test.values[0].left.id
            number_1 = b.test.values[0].comparators[0].n
            variable_name_2 = b.test.values[1].left.id
            number_2 = b.test.values[1].comparators[0].n

            operation_1 = b.test.values[0].ops[0]
            operation_2 = b.test.values[1].ops[0]
            com_op = b.test.op
            first_part, second_part, op = '', '', ''

            if isinstance(operation_1, ast.Eq):
                first_part = str(variable_name_1) + ' == ' + str(number_1)
            if isinstance(operation_2, ast.Eq):
                second_part = str(variable_name_2) + ' == ' + str(number_2)

            if isinstance(com_op, ast.Or):
                op = ' or '

            body = b.body[0].value.value.id

            answer["if"] = answer.get("if", []) + [('if ' + first_part + op + second_part, body)]

        elif isinstance(b, ast.For):
            first_val = b.iter.args[0].n
            second_val = b.iter.args[1].id
            ind_iter = b.target.id
            cycle = 'for ' + str(ind_iter) + ' in range(' + str(first_val) + ', ' + str(second_val) + ')'

            func = b.body[0].value.func.attr
            var = b.body[0].value.func.value.id
            inner_op = b.body[0].value.args[0].op  # Add
            first_term_val = b.body[0].value.args[0].left.value.id
            first_term_val_op = b.body[0].value.args[0].left.slice.value.op  # Sub

            if isinstance(first_term_val_op, ast.Sub):
                first_term_ind = str(b.body[0].value.args[0].left.slice.value.left.id) + ' - ' + str(
                    b.body[0].value.args[0].left.slice.value.right.n)

            first_term = str(first_term_val) + '[' + str(first_term_ind) + ']'

            second_term_val = b.body[0].value.args[0].right.value.id
            second_term_val_op = b.body[0].value.args[0].right.slice.value.op  # Sub
            if isinstance(second_term_val_op, ast.Sub):
                second_term_ind = str(b.body[0].value.args[0].right.slice.value.left.id) + ' - ' + str(
                    b.body[0].value.args[0].right.slice.value.right.n)

            second_term = str(second_term_val) + '[' + str(second_term_ind) + ']'

            cycle_body = ''
            if isinstance(inner_op, ast.Add):
                cycle_body = first_term + ' + ' + second_term

            cycle_body = str(var) + '.' + str(func) + '(' + cycle_body + ')'

            answer["for"] = answer.get("for", []) + [[cycle, cycle_body]]

        elif isinstance(b, ast.Return):
            variable_name = b.value.id

            answer["return"] = answer.get("return", []) + ['return ' + variable_name]

    return answer


def plot_ast(ast_info):
    fig, ax = plt.subplots(dpi=128, figsize=(8, 8))

    nodes = [(0, 1), (0, 2), (0, 3), (0, 4), (4, 5), (3, 6)]
    positions = {0: (5, 5), 1: (4, 4.5), 2: (10, 4), 3: (5, 4),
                 4: (6.5, 4.3), 5: (6.5, 3.5), 6: (3.5, 3.5)}

    edge_labels = {(0, 1): "assign", (0, 2): "return", (0, 3): "if",
                   (0, 4): "for", (4, 5): "'for' body", (3, 6): "return"}

    G = nx.DiGraph(nodes)

    nx.draw_networkx_edges(G, positions)

    nx.draw_networkx_labels(G, positions, labels={0: ast_info["name"]}, bbox={'boxstyle': 'round', 'facecolor': 'blue',
                                                                              'alpha': 0.7}, font_size=10)
    nx.draw_networkx_labels(G, positions, labels={1: ast_info["assign"][0]},
                            bbox={'boxstyle': 'round', 'facecolor': 'orange'},
                            font_size=10)
    nx.draw_networkx_labels(G, positions, labels={5: ast_info["for"][0][1]},
                            bbox={'boxstyle': 'round', 'facecolor': 'blue',
                                  'alpha': 0.5}, font_size=10)

    nx.draw_networkx_labels(G, positions, labels={2: ast_info["return"][0].split()[1], 6: ast_info["if"][0][1]},
                            bbox={'boxstyle': 'round', 'facecolor': 'green', 'alpha': 0.5}, font_size=10)
    nx.draw_networkx_labels(G, positions, labels={3: ast_info["if"][0][0][3:]},
                            bbox={'boxstyle': 'round', 'facecolor': 'red'},
                            font_size=10)

    nx.draw_networkx_labels(G, positions, labels={4: ast_info["for"][0][0]},
                            bbox={'boxstyle': 'round', 'facecolor': 'red',
                                  'alpha': 0.5}, font_size=10)

    nx.draw_networkx_edge_labels(G, positions, edge_labels=edge_labels)

    ax = plt.gca()
    ax.margins(0.20)
    ax.axis("off")

    plt.savefig("artifacts/ast.pdf")

    plt.show()


if __name__ == '__main__':
    plot_ast(parse_ast(read_ast()))
