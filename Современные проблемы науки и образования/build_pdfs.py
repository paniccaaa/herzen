from pathlib import Path
import re
from html import escape

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'output' / 'pdf'
OUT.mkdir(parents=True, exist_ok=True)
FONTS = Path('/System/Library/Fonts/Supplemental')
for suffix, filename in [('', 'Times New Roman.ttf'), ('-Bold', 'Times New Roman Bold.ttf'),
                         ('-Italic', 'Times New Roman Italic.ttf')]:
    pdfmetrics.registerFont(TTFont('TNR' + suffix, str(FONTS / filename)))
pdfmetrics.registerFontFamily('TNR', normal='TNR', bold='TNR-Bold', italic='TNR-Italic', boldItalic='TNR-Bold')

JOBS = [
    ('Модуль_1', 'Модуль_1_Профессиональная_задача', 12, 2),
    ('Задание_2.2', 'Задание_2.2_Учебная_мотивация', 13.4, 1),
    ('Лекция_4.1', 'Лекция_4.1_Аналитический_конспект', 14, 2),
    ('Модуль_4', 'Модуль_4_Профессиональная_задача', 18, 3),
    ('Итоговая_задача', 'Итоговая_профессиональная_задача', 14, 2),
]

def inline(text):
    pattern = r'\[([^\]]+)\]\((https?://[^)]+)\)'
    pieces = []
    at = 0
    for match in re.finditer(pattern, text):
        pieces.append(escape(text[at:match.start()]))
        pieces.append('<link href="' + escape(match.group(2), quote=True) + '" color="#214b70">' + escape(match.group(1)) + '</link>')
        at = match.end()
    pieces.append(escape(text[at:]))
    result = ''.join(pieces)
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', result)

def validate(text, name):
    forbidden = re.findall(r'[\u2010-\u2015\u2190-\u21ff\u27f0-\u27ff\u2900-\u297f]|(?:-\x3e)|(?:\x3c-)', text)
    if forbidden:
        raise ValueError(f'{name}: forbidden characters {forbidden}')

def build(source, target, leading, expected):
    text = (ROOT / 'Исходники' / (source + '.md')).read_text()
    validate(text, source)
    base = ParagraphStyle('body', fontName='TNR', fontSize=12, leading=leading,
                          alignment=TA_JUSTIFY, spaceAfter=5, allowWidows=0, allowOrphans=0)
    heading = ParagraphStyle('heading', parent=base, fontName='TNR-Bold',
                             alignment=TA_LEFT, spaceBefore=7, spaceAfter=5, keepWithNext=True)
    title = ParagraphStyle('title', parent=heading, spaceBefore=0, spaceAfter=8)
    cell = ParagraphStyle('cell', parent=base, alignment=TA_LEFT, spaceAfter=0)
    doc = SimpleDocTemplate(str(OUT / (target + '.pdf')), pagesize=A4,
                            rightMargin=19*mm, leftMargin=21*mm,
                            topMargin=16*mm, bottomMargin=17*mm,
                            title=text.splitlines()[0][2:], author='Адаменко Семён Сергеевич')
    story = []
    blocks = re.split(r'\n\s*\n', text.strip())
    for block in blocks:
        if block.strip() == '[[PAGEBREAK]]':
            story.append(PageBreak())
        elif block.startswith('# '):
            story.append(Paragraph(inline(block[2:].strip()), title))
        elif block.startswith('## '):
            story.append(Paragraph(inline(block[3:].strip()), heading))
        elif block.startswith('|'):
            rows = []
            for line in block.splitlines():
                if re.match(r'^\|[\s|:-]+\|$', line):
                    continue
                rows.append([Paragraph(inline(x.strip()), cell) for x in line.strip('|').split('|')])
            proportions = [0.23, 0.34, 0.43] if source == 'Лекция_4.1' else [0.26, 0.36, 0.38]
            table = Table(rows, colWidths=[doc.width * x for x in proportions], repeatRows=1, hAlign='LEFT')
            table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#eef1f4')),
                ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#a5abb1')),
                ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            story.extend([table, Spacer(1, 6)])
        else:
            story.append(Paragraph(inline(' '.join(block.splitlines())), base))

    def footer(canvas, _):
        canvas.setFont('TNR', 10)
        canvas.setFillColor(colors.HexColor('#444444'))
        canvas.drawCentredString(A4[0] / 2, 10*mm, str(canvas.getPageNumber()))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    from pypdf import PdfReader
    pdf = PdfReader(OUT / (target + '.pdf'))
    n = len(pdf.pages)
    extracted = '\n'.join(p.extract_text() or '' for p in pdf.pages)
    validate(extracted, target)
    print(f'{target}: {n} pages, expected {expected}; {len(extracted)} characters')
    if n != expected:
        raise ValueError(f'{target}: pagination {n}, expected {expected}')

if __name__ == '__main__':
    for job in JOBS:
        build(*job)
