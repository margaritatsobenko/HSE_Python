from ast_package import my_ast
from pdflatex import PDFLaTeX
from table_gen import main as table_gen_main


def get_latex():
    my_ast.plot_ast(my_ast.parse_ast(my_ast.read_ast()))
    table_gen_main()

    tex_document_start = '\\documentclass{article}\n\\usepackage[utf8]{inputenc}\n\\usepackage{graphicx}\n\\begin{document}\n'
    tex_image = '\\includegraphics[width=\\textwidth]{' + "artifacts/ast.pdf" + '}\n'
    tex_document_finish = '\\end{document}'

    with open("artifacts/table.tex") as t:
        tex_table = ' '.join(t.readlines())

    latex_text = tex_document_start + tex_table + tex_image + tex_document_finish
    return latex_text


def main():
    file_name = "artifacts/img_table.tex"
    with open(file_name, 'w') as t:
        t.write(get_latex())

    file_pdf = PDFLaTeX.from_texfile(file_name)
    file_pdf.create_pdf(keep_pdf_file=True)


if __name__ == '__main__':
    main()
