import docx


def get_file_paragraphs_qty(file):
    paragraphs = docx.Document(file).paragraphs
    text = ''
    for paragraph in paragraphs:
        text += f'{paragraph.text}\n'
    return len(text.strip().split('\n\n'))
