"""Render reviewed app policy Markdown into the site's existing legal layout.
Usage: python3 scripts/sync-release-policies.py /absolute/path/to/app/legal

The app repo's legal/*.md files are the source of truth for the privacy
policy, the Washington notice and the Terms of Use. Each page keeps its
hand-written table of contents; the article body and the effective and
last-updated dates come from the Markdown.
"""
from pathlib import Path
import html, re, sys
source=Path(sys.argv[1])
root=Path(__file__).resolve().parent.parent

PAGES=[('privacy-policy.md','privacy/index.html'),('wa-consumer-health-data-privacy-policy.md','privacy/washington/index.html'),('terms-of-use.md','terms/index.html')]
# Where each policy lives on the site, for links between the Markdown files.
SITE_PATHS={'privacy-policy.md':'privacy/','wa-consumer-health-data-privacy-policy.md':'privacy/washington/','terms-of-use.md':'terms/'}
NAMED_ANCHORS={'The short version':'short-version','Why this policy exists':'why-this-policy','Read this first — plain-language summary':'summary'}

def inline(value, prefix):
    value=html.escape(value, quote=False)
    value=re.sub(r'\[([^\]]+)\]\((https://[^\s)]+)\)',r'<a href="\2">\1</a>',value)
    value=re.sub(r'\[([^\]]+)\]\(([a-z0-9-]+\.md)\)',lambda m:f'<a href="{prefix}{SITE_PATHS[m[2]]}">{m[1]}</a>',value)
    value=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',value)
    value=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<em>\1</em>',value)
    return value

def render(md, prefix):
    lines=md[md.index('## '):].splitlines()
    out=[]; paragraph=[]; quote=[]; listing=False; section=False
    def flush():
        if paragraph:
            out.append('<p>'+inline(' '.join(paragraph),prefix)+'</p>');paragraph.clear()
        if quote:
            out.append('<div class="legal-callout"><p>'+inline(' '.join(quote),prefix)+'</p></div>');quote.clear()
    def close_list():
        nonlocal listing
        if listing:out.append('</ul>');listing=False
    for line in lines:
        if line.startswith('## '):
            flush();close_list()
            if section:out.append('</section>')
            title=line[3:];number=re.match(r'(\d+)\.',title)
            anchor='sec-'+number[1] if number else NAMED_ANCHORS.get(title,'how-caredraft-works')
            out.extend([f'<section id="{anchor}">','<h2>'+inline(title,prefix)+'</h2>']);section=True
        elif line.startswith('### '):
            flush();close_list();out.append('<h3>'+inline(line[4:],prefix)+'</h3>')
        elif line.startswith('>'):
            close_list();quote.append(line[1:].strip())
        elif line.startswith('- '):
            flush()
            if not listing:out.append('<ul>');listing=True
            out.append('<li>'+inline(line[2:],prefix)+'</li>')
        elif not line.strip() or line=='---':flush();close_list()
        else:close_list();paragraph.append(line)
    flush();close_list()
    if section:out.append('</section>')
    return '\n          '.join(out)

def header_date(md, label):
    return re.search(r'^\*\*'+label+r':\*\* (.+)$',md,flags=re.M)[1].strip()

for filename,destination in PAGES:
    p=root/destination;s=p.read_text();md=(source/filename).read_text()
    prefix='../'*(len(Path(destination).parts)-1)
    body=render(md,prefix)
    s=re.sub(r'(<article class="legal-body">).*?(</article>)',lambda m:m[1]+'\n          '+body+'\n        '+m[2],s,flags=re.S)
    s=re.sub(r'Effective date <strong>[^<]+</strong>','Effective date <strong>'+header_date(md,'Effective Date')+'</strong>',s)
    s=re.sub(r'Last updated <strong>[^<]+</strong>','Last updated <strong>'+header_date(md,'Last Updated')+'</strong>',s)
    s=s.replace('4. Data We Receive','4. Connections &amp; Recipients')
    s=s.replace('Learn how your clinical notes and dictations remain entirely on your device.', 'Learn about local clinical storage, optional online features, providers, and your choices.')
    p.write_text(s)
    print('Updated',destination)
