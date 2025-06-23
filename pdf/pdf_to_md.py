
from pdf2docx import Converter
from markdownify import markdownify as md

from docx import Document


pdf_file = 'input.pdf'
docx_file = 'temp.docx'
cv = Converter(pdf_file)
cv.convert(docx_file)
cv.close()


doc = Document(docx_file)
html = ''
for para in doc.paragraphs:
    html += f'<p>{para.text}</p>\n'

markdown = md(html)

with open('output.md', 'w', encoding='utf-8') as f:
    f.write(markdown)
