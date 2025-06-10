
import os
from PyPDF2 import PdfMerger

merger = PdfMerger()

pdf_files = sorted([f for f in os.listdir('.') if f.lower().endswith('.pdf')])

for pdf in pdf_files:
    print(f"Добавляется: {pdf}")
    merger.append(pdf)

output_file = 'merged.pdf'
merger.write(output_file)
merger.close()

print(f'\n✅ Все PDF объединены в файл: {output_file}')
