import docx


def get_file_paragraphs_qty(file):
    return len(docx.Document(file).paragraphs)
