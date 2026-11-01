"""Render this article's headings, paragraphs, tables, images, and code for copying."""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parent

def inline(text):
    text = html.escape(text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img alt="\1" src="\2">', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    return re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)

lines = (ROOT / 'medium-draft.md').read_text().splitlines()
output = []
i = 0
while i < len(lines):
    line = lines[i]
    if not line.strip():
        i += 1
        continue
    if line.startswith('```'):
        language = line[3:]
        code = []
        i += 1
        while i < len(lines) and not lines[i].startswith('```'):
            code.append(lines[i])
            i += 1
        output.append('<pre><code class="language-' + html.escape(language) + '">' + html.escape('\n'.join(code)) + '</code></pre>')
        i += 1
        continue
    heading = re.match(r'^(#{1,6}) (.*)', line)
    if heading:
        level = len(heading[1])
        output.append(f'<h{level}>' + inline(heading[2]) + f'</h{level}>')
        i += 1
        continue
    if line.startswith('|'):
        rows = []
        while i < len(lines) and lines[i].startswith('|'):
            rows.append(lines[i])
            i += 1
        output.append('<table>')
        for n, row in enumerate(rows):
            cells = row.strip().strip('|').split('|')
            if all(re.fullmatch(r'\s*:?-+:?\s*', cell) for cell in cells):
                continue
            tag = 'th' if n == 0 else 'td'
            output.append('<tr>' + ''.join(f'<{tag}>' + inline(cell.strip()) + f'</{tag}>' for cell in cells) + '</tr>')
        output.append('</table>')
        continue
    paragraph = [line]
    i += 1
    while i < len(lines) and lines[i].strip() and not re.match(r'^(#|```|\|)', lines[i]):
        paragraph.append(lines[i])
        i += 1
    output.append('<p>' + inline(' '.join(paragraph)) + '</p>')

title = lines[0].lstrip('# ')
style = '''body{max-width:860px;margin:50px auto;padding:0 24px;color:#202124;font:20px/1.7 Georgia,serif}h1,h2,h3{font-family:Arial,sans-serif;line-height:1.25}h1{font-size:42px}h2{margin-top:48px;font-size:29px}pre{overflow:auto;padding:22px;background:#f3f4f6;font:15px/1.6 monospace;white-space:pre}code{font-family:monospace;font-size:.85em}pre code{font-size:inherit}img{width:100%;height:auto}table{border-collapse:collapse;width:100%;font-size:16px}td,th{border:1px solid #d1d5db;padding:12px;text-align:left}a{color:#1565c0}.notice{font:16px/1.5 Arial,sans-serif;background:#eff6ff;padding:18px;border-radius:8px;margin-bottom:36px}@media print{.notice{display:none}}'''
page = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + html.escape(title) + '</title><style>' + style + '</style></head><body><aside class="notice">Copy the rendered article below into your Medium draft. Exclude this notice. Upload diagrams separately if images do not transfer. Review code blocks and tables before publishing.</aside><article>' + '\n'.join(output) + '</article></body></html>'
(ROOT / 'medium-formatted.html').write_text(page)
print('Updated medium-formatted.html')
