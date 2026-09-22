"""Render reviewed app policy Markdown into the site's existing legal layout.
Usage: python3 scripts/sync-release-policies.py /absolute/path/to/app/legal
"""
from pathlib import Path
import html, re, sys
source=Path(sys.argv[1])
root=Path(__file__).resolve().parent.parent

def inline(value):
    value=html.escape(value, quote=False)
    value=re.sub(r'\[([^\]]+)\]\((https://[^\s)]+)\)',r'<a href="\2">\1</a>',value)
    value=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',value)
    value=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<em>\1</em>',value)
    return value

def render(md):
    lines=md[md.index('## '):].splitlines()
    out=[]; paragraph=[]; listing=False; section=False
    def flush():
        if paragraph:
            out.append('<p>'+inline(' '.join(paragraph))+'</p>');paragraph.clear()
    def close_list():
        nonlocal listing
        if listing:out.append('</ul>');listing=False
    for line in lines:
        if line.startswith('## '):
            flush();close_list()
            if section:out.append('</section>')
            title=line[3:];number=re.match(r'(\d+)\.',title)
            anchor='sec-'+number[1] if number else ('short-version' if title=='The short version' else 'why-this-policy' if title=='Why this policy exists' else 'how-caredraft-works')
            out.extend([f'<section id="{anchor}">','<h2>'+inline(title)+'</h2>']);section=True
        elif line.startswith('### '):
            flush();close_list();out.append('<h3>'+inline(line[4:])+'</h3>')
        elif line.startswith('- '):
            flush()
            if not listing:out.append('<ul>');listing=True
            out.append('<li>'+inline(line[2:])+'</li>')
        elif not line.strip() or line=='---':flush();close_list()
        else:close_list();paragraph.append(line)
    flush();close_list()
    if section:out.append('</section>')
    return '\n          '.join(out)

for filename,destination in [('privacy-policy.md','privacy/index.html'),('wa-consumer-health-data-privacy-policy.md','privacy/washington/index.html')]:
    p=root/destination;s=p.read_text();md=(source/filename).read_text()
    body=render(md)
    s=re.sub(r'(<article class="legal-body">).*?(</article>)',lambda m:m[1]+'\n          '+body+'\n        '+m[2],s,flags=re.S)
    s=re.sub(r'Last updated <strong>[^<]+</strong>', 'Last updated <strong>September 21, 2026</strong>',s)
    s=s.replace('4. Data We Receive','4. Connections &amp; Recipients')
    s=s.replace('Learn how your clinical notes and dictations remain entirely on your device.', 'Learn about local clinical storage, optional online features, providers, and your choices.')
    p.write_text(s)
    print('Updated',destination)
