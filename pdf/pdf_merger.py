
import os
from PyPDF2 import PdfMerger

merger = PdfMerger()

dir = './pdf/'
os.chdir(dir)

pdf_files = sorted([f for f in os.listdir('.') if f.lower().endswith('.pdf')])

for pdf in pdf_files:
    print(f"Added: {pdf}")
    merger.append(pdf)

output_file = 'merged.pdf'
merger.write("../" + output_file)
merger.close()

print(f'\n✅ All pdfs merged: {output_file}')
