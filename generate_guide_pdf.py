import re
import os
import subprocess
import markdown
import pygments
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter

MD_PATH = "/Users/dazzelr/PycharmProjects/try.md"
HTML_PATH = "/Users/dazzelr/PycharmProjects/try.html"
PDF_PATH = "/Users/dazzelr/PycharmProjects/try.pdf"
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

with open(MD_PATH, "r", encoding="utf-8") as f:
    raw_md = f.read()

# 1. Clean math arrows \(\rightarrow\) to unicode →
clean_md = re.sub(r'\\+\(\\+rightarrow\\+\)', '→', raw_md)

# 2. Extract code blocks, replace with HTML div placeholders that markdown won't mangle
code_blocks = {}

def code_replacer(match):
    idx = len(code_blocks)
    lang = match.group(1).strip().lower() or 'python'
    code_text = match.group(2)
    key = f"CODEPLACEHOLDER{idx}"
    code_blocks[key] = (lang, code_text)
    # Use a raw HTML block: blank line, div on its own line, blank line
    return f'\n\n<div id="{key}"></div>\n\n'

processed_md = re.sub(r'```(\w*)\n(.*?)```', code_replacer, clean_md, flags=re.DOTALL)

# 3. Convert markdown to HTML
extensions = ['extra', 'tables', 'toc', 'sane_lists']
html_body = markdown.markdown(processed_md, extensions=extensions)

# 4. Build gorgeous Mac-style code cards with Pygments syntax highlighting
formatter = HtmlFormatter(style='one-dark', nowrap=True)


def render_code_card(lang, code_text):
    try:
        if lang in ['py', 'python', 'python3']:
            lexer = get_lexer_by_name('python')
            display_lang = 'Python'
        elif lang == 'json':
            lexer = get_lexer_by_name('json')
            display_lang = 'JSON'
        elif lang in ['bash', 'sh', 'shell']:
            lexer = get_lexer_by_name('bash')
            display_lang = 'Bash'
        elif lang in ['text', 'txt']:
            lexer = TextLexer()
            display_lang = 'Text'
        elif lang == 'html':
            lexer = get_lexer_by_name('html')
            display_lang = 'HTML'
        else:
            lexer = get_lexer_by_name(lang)
            display_lang = lang.upper()
    except Exception:
        lexer = TextLexer()
        display_lang = lang.upper() if lang else 'Code'

    highlighted = pygments.highlight(code_text, lexer, formatter)
    line_count = len(code_text.strip().splitlines())
    break_class = "break-avoid" if line_count <= 35 else "break-auto"

    return f'''<div class="code-card {break_class}">
    <div class="code-header">
        <div class="window-controls">
            <span class="dot dot-red"></span>
            <span class="dot dot-yellow"></span>
            <span class="dot dot-green"></span>
        </div>
        <div class="code-meta">
            <span class="code-badge">{display_lang}</span>
            <span class="code-lines">{line_count} lines</span>
        </div>
    </div>
    <div class="code-body">
        <pre><code>{highlighted}</code></pre>
    </div>
</div>'''


# 5. Replace each placeholder div with the rendered code card
for key, (lang, code_text) in code_blocks.items():
    card = render_code_card(lang, code_text)
    html_body = html_body.replace(f'<div id="{key}"></div>', card)

# 6. Enhance captions like *(Some caption text)*
html_body = re.sub(
    r'<p><em>\((.*?)\)</em></p>',
    r'<div class="caption-callout"><span class="caption-icon">ℹ</span> \1</div>',
    html_body
)

# 7. Cover banner
header_banner = '''
<div class="doc-cover break-avoid">
    <div class="cover-eyebrow">Comprehensive Academic &amp; Practical Reference</div>
    <h1 class="cover-title">Advanced Python Programming</h1>
    <p class="cover-subtitle">GUI Development &bull; Web APIs &amp; REST &bull; Microframeworks (Streamlit &amp; Flask)</p>
    <div class="cover-tags">
        <span class="tag tag-blue">PyQt5 GUI</span>
        <span class="tag tag-emerald">RESTful APIs</span>
        <span class="tag tag-purple">Requests &amp; JSON</span>
        <span class="tag tag-amber">Streamlit</span>
        <span class="tag tag-red">Flask WSGI</span>
        <span class="tag tag-cyan">Pandas &amp; NumPy</span>
    </div>
</div>
'''

# 8. Assemble final HTML document
CSS = r'''
:root {
    --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    --font-mono: 'JetBrains Mono', 'Fira Code', 'SF Mono', Menlo, Consolas, monospace;
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --text-main: #0f172a;
    --text-body: #334155;
    --border-color: #e2e8f0;
    --border-dark: #cbd5e1;
    --code-bg: #1e222b;
    --code-header-bg: #171920;
    --code-border: #2e3440;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: var(--font-sans);
    font-size: 13.5px;
    line-height: 1.68;
    color: var(--text-body);
    background: #ffffff;
    padding: 2.5rem 3.5rem;
    max-width: 900px;
    margin: 0 auto;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
}

@page {
    size: A4 portrait;
    margin: 16mm 14mm 16mm 14mm;
}

@media print {
    body { padding: 0 !important; max-width: 100% !important;
           -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
    .code-card, .code-header, .code-body, .doc-cover, table, .caption-callout {
        -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important;
    }
    .code-card { box-shadow: none !important; }
}

.break-avoid { page-break-inside: avoid !important; break-inside: avoid !important; }
.break-auto  { page-break-inside: auto !important;  break-inside: auto !important;  }

/* ───── COVER BANNER ───── */
.doc-cover {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: 12px; padding: 2.2rem 2.4rem; margin-bottom: 2.5rem;
    color: #fff; box-shadow: 0 10px 25px -5px rgba(15,23,42,.15);
}
.cover-eyebrow { text-transform: uppercase; font-size: 8pt; font-weight: 700;
                  letter-spacing: .12em; color: #38bdf8; margin-bottom: .5rem; }
.cover-title   { font-size: 24pt; font-weight: 800; color: #fff; letter-spacing: -.025em;
                  line-height: 1.2; margin-bottom: .6rem; border: none !important; padding: 0 !important; }
.cover-subtitle{ font-size: 11pt; color: #94a3b8; margin-bottom: 1.2rem; line-height: 1.5; }
.cover-tags    { display: flex; flex-wrap: wrap; gap: 7px; }
.tag           { font-size: 8pt; font-weight: 600; padding: 3px 10px; border-radius: 20px; letter-spacing: .02em; }
.tag-blue    { background: rgba(56,189,248,.18);  color: #7dd3fc; border: 1px solid rgba(56,189,248,.3); }
.tag-emerald { background: rgba(52,211,153,.18);  color: #6ee7b7; border: 1px solid rgba(52,211,153,.3); }
.tag-purple  { background: rgba(192,132,252,.18); color: #d8b4fe; border: 1px solid rgba(192,132,252,.3); }
.tag-amber   { background: rgba(251,191,36,.18);  color: #fde047; border: 1px solid rgba(251,191,36,.3); }
.tag-red     { background: rgba(248,113,113,.18); color: #fca5a5; border: 1px solid rgba(248,113,113,.3); }
.tag-cyan    { background: rgba(34,211,238,.18);  color: #67e8f9; border: 1px solid rgba(34,211,238,.3); }

/* ───── TYPOGRAPHY ───── */
h1, h2, h3, h4, h5, h6 { color: var(--text-main); font-weight: 700; line-height: 1.3;
                           page-break-after: avoid !important; break-after: avoid !important; }

h1 { font-size: 19pt; font-weight: 800; letter-spacing: -.025em;
     margin-top: 2.8rem; margin-bottom: 1.1rem;
     padding-bottom: .6rem; border-bottom: 2px solid var(--primary); color: #0f172a; }
h2 { font-size: 15pt; font-weight: 700; letter-spacing: -.015em;
     margin-top: 2.2rem; margin-bottom: .85rem;
     padding-bottom: .4rem; border-bottom: 1px solid var(--border-color); color: #1e293b; }
h3 { font-size: 12.5pt; font-weight: 600; margin-top: 1.6rem; margin-bottom: .6rem;
     color: var(--primary-dark); }
h4 { font-size: 11pt; font-weight: 600; margin-top: 1.2rem; margin-bottom: .45rem; color: #475569; }

p      { margin-bottom: .9rem; }
strong { font-weight: 600; color: var(--text-main); }
ul, ol { margin-top: .4rem; margin-bottom: 1rem; padding-left: 1.6rem; }
li     { margin-bottom: .4rem; }
li > ul, li > ol { margin-top: .3rem; margin-bottom: .3rem; }
hr     { border: none; height: 1px; background: #e2e8f0; margin: 2rem 0; }

/* ───── INLINE CODE ───── */
code {
    font-family: var(--font-mono); font-size: .88em;
    background: #f1f5f9; color: #0369a1;
    padding: 2px 6px; border-radius: 4px; border: 1px solid #e2e8f0; font-weight: 500;
}

/* ───── TABLES ───── */
table { width: 100%; border-collapse: collapse; margin: 1.4rem 0; font-size: 9.5pt;
        background: #fff; border: 1px solid var(--border-color); border-radius: 8px;
        overflow: hidden; page-break-inside: avoid !important; break-inside: avoid !important;
        box-shadow: 0 1px 3px rgba(0,0,0,.04); }
thead { background: #f8fafc; border-bottom: 2px solid var(--border-dark); }
th    { padding: 9px 13px; text-align: left; font-weight: 700; color: #0f172a;
        letter-spacing: .02em; font-size: 9pt; text-transform: uppercase; }
td    { padding: 8px 13px; border-bottom: 1px solid var(--border-color); vertical-align: top; }
tr:nth-child(even) { background: #fbfcfe; }
tr:last-child td   { border-bottom: none; }

/* ───── CAPTION CALLOUT ───── */
.caption-callout {
    background: #f0fdf4; border-left: 3.5px solid #22c55e; color: #166534;
    padding: 8px 14px; border-radius: 0 6px 6px 0; font-size: 9pt; font-style: italic;
    margin: -.4rem 0 1.2rem 0; display: flex; align-items: center; gap: 8px;
}
.caption-icon { font-style: normal; font-size: 11pt; color: #16a34a; font-weight: bold; }

/* ───── CODE BLOCK CARDS ───── */
.code-card {
    margin: 1.3rem 0; border-radius: 9px; overflow: hidden;
    border: 1px solid var(--code-border); background: var(--code-bg);
    box-shadow: 0 4px 15px rgba(0,0,0,.09);
}
.code-header {
    background: var(--code-header-bg); padding: 7px 14px;
    display: flex; align-items: center; justify-content: space-between;
    border-bottom: 1px solid rgba(255,255,255,.07);
}
.window-controls { display: inline-flex; gap: 6px; align-items: center; }
.dot            { width: 9.5px; height: 9.5px; border-radius: 50%; display: inline-block; }
.dot-red    { background: #ff5f56; }
.dot-yellow { background: #ffbd2e; }
.dot-green  { background: #27c93f; }
.code-meta  { display: inline-flex; align-items: center; gap: 8px; }
.code-badge {
    font-family: var(--font-mono); font-size: 7.5pt; font-weight: 700;
    color: #61afef; text-transform: uppercase; letter-spacing: .06em;
    padding: 2px 7px; background: rgba(97,175,239,.12);
    border-radius: 4px; border: 1px solid rgba(97,175,239,.25);
}
.code-lines { font-family: var(--font-sans); font-size: 7.5pt; color: #64748b; }

.code-body {
    padding: 13px 17px; background: var(--code-bg); overflow-x: auto;
}
.code-body pre  { margin: 0; padding: 0; background: transparent !important; }
.code-body code {
    font-family: var(--font-mono) !important; font-size: 8.7pt !important;
    line-height: 1.58 !important; background: transparent !important;
    border: none !important; padding: 0 !important; color: #abb2bf !important;
    white-space: pre-wrap !important; word-break: break-word !important; font-weight: 400 !important;
}

/* ───── ONE-DARK SYNTAX TOKEN COLORS ───── */
.code-body .k,  .code-body .kd, .code-body .kn,
.code-body .kp, .code-body .kr, .code-body .kt { color: #c678dd !important; font-weight: 600; }
.code-body .kc { color: #e5c07b !important; font-weight: 600; }

.code-body .s,  .code-body .s1, .code-body .s2, .code-body .sa,
.code-body .sb, .code-body .sc, .code-body .dl, .code-body .sd,
.code-body .se, .code-body .sh, .code-body .sx, .code-body .sr,
.code-body .ss { color: #98c379 !important; }
.code-body .si { color: #e5c07b !important; }

.code-body .nf, .code-body .fm { color: #61afef !important; font-weight: 600; }
.code-body .nc, .code-body .ne { color: #e5c07b !important; font-weight: 600; }
.code-body .nb, .code-body .bp { color: #56b6c2 !important; }

.code-body .c,  .code-body .c1, .code-body .cm,
.code-body .cs, .code-body .ch { color: #7f848e !important; font-style: italic; }

.code-body .m,  .code-body .mi, .code-body .mf,
.code-body .mh, .code-body .mo, .code-body .il { color: #d19a66 !important; }

.code-body .o,  .code-body .ow { color: #56b6c2 !important; }
.code-body .nd { color: #e5c07b !important; font-weight: 600; }
.code-body .p  { color: #abb2bf !important; }

.code-body .n,  .code-body .nn, .code-body .na,
.code-body .nv, .code-body .vi { color: #e06c75 !important; }
'''

html_doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Advanced Python Programming Guide</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,600&family=JetBrains+Mono:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
<style>
{CSS}
</style>
</head>
<body>

{header_banner}

{html_body}

</body>
</html>
'''

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_doc)

print(f"HTML generated: {HTML_PATH} ({os.path.getsize(HTML_PATH):,} bytes)")

# Verify all placeholders were replaced
unreplaced = html_doc.count('CODEPLACEHOLDER')
if unreplaced:
    print(f"WARNING: {unreplaced} unreplaced code placeholders remain!")
else:
    print(f"All {len(code_blocks)} code blocks rendered successfully.")

# 9. Generate PDF via headless Chrome
print("Generating PDF via Google Chrome...")
proc = subprocess.run([
    CHROME_PATH,
    "--headless=new",
    "--no-pdf-header-footer",
    "--disable-gpu",
    f"--print-to-pdf={PDF_PATH}",
    HTML_PATH
], capture_output=True, text=True)

if proc.returncode == 0 and os.path.exists(PDF_PATH):
    size_kb = os.path.getsize(PDF_PATH) / 1024
    print(f"PDF generated: {PDF_PATH} ({size_kb:.0f} KB)")
else:
    print(f"Chrome error (code {proc.returncode}): {proc.stderr[:500]}")
