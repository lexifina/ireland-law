"""Builds a git repository of Irish Acts from the Law Reform Commission's Revised Acts (revisedacts.lawreform.ie), in
which every amending law is one commit, dated the day it came into force.

    python -X utf8 scripts/ireland-law/build.py [--repo ../ireland-law] [--today 2026-10-28] [--offline]
                                               [--verify-rebuild]

"""
from __future__ import annotations

import collections
import datetime as dt
import gzip
import hashlib
import re
import subprocess
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CACHE = HERE / '.cache'
SITE = 'https://revisedacts.lawreform.ie'
COMMITTER = ('Lexifina', 'ireland-law@lexifina.com')
PUBLISHER = ('Law Reform Commission, Revised Acts', 'revised-acts@lawreform.invalid')

ACTS: list[dict] = []   # every English-language Revised Act, from the alphabetical list (acts_from_alpha)

REQUESTS: list[dict] = []
_lock = threading.Lock()


# Retrieval is not part of the published record: Lexifina's own retrieval sets these two before calling main(). A rebuild
# from the published tools reads the retrieved files only (--offline).
RETRIEVE = None       # url, want -> bytes
RETRIEVE_ALL = None   # urls, one(url) -> {url: bytes}


def _retrieval_missing():
    raise SystemExit('retrieval is not part of this record: put the retrieved files in place and use --offline')


def cache_path(url: str) -> Path:
    return CACHE / hashlib.sha256(url.encode()).hexdigest()[:32]


def fetch(url: str, offline: bool = False, want: bytes = b'') -> bytes:
    """The retrieved file for a URL, keyed by the URL (so a rebuild reads the same bytes)."""
    path = cache_path(url)
    with _lock:
        REQUESTS.append({'url': url, 'file': path})
    if path.exists():
        return path.read_bytes()
    if offline:
        raise SystemExit(f'not retrieved: {url}')
    if RETRIEVE is None:
        _retrieval_missing()
    body = RETRIEVE(url, want)
    path.write_bytes(body)
    return body


def fetch_all(urls: list[str], offline: bool, want: bytes = b'') -> dict[str, bytes]:
    if offline or all(cache_path(u).exists() for u in urls):
        return {u: fetch(u, offline, want) for u in urls}
    if RETRIEVE_ALL is None:
        _retrieval_missing()
    return RETRIEVE_ALL(urls, lambda u: fetch(u, offline, want))


# ---------------------------------------------------------------- version list

MONTHS = {m: i + 1 for i, m in enumerate('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split())}


def list_date(s: str) -> str:
    d, m, y = s.split()
    return f'{int(y):04d}-{MONTHS[m[:3]]:02d}-{int(d):02d}'


def history(act: dict, offline: bool) -> list[dict]:
    """The act's published revisions, oldest first, from the alphabetical list. Revisions that point at the same file
    (a re-listing) are one version, dated by its first listing."""
    page = fetch(f'{SITE}/revacts/alpha', offline, b'<!doctype')
    s = page.decode('utf-8')
    rows = re.findall(r'<tr class="[^"]*" data-eli="%s/en" style="[^"]*">(.*?)</tr>' % re.escape(act['eli']), s, re.S)
    out = []
    for b in rows:
        m = re.search(r'class="updated">\s*<span>([^<]*)', b)
        links = re.findall(r'href="([^"]+)"', b)
        if not m or not links:
            continue
        url = links[0].replace('&amp;', '&')
        if url.startswith('/'):
            url = SITE + url
        out.append({'listed': list_date(m.group(1).strip()), 'url': url})
    out.reverse()
    seen: dict[str, dict] = {}
    versions = []
    for v in out:
        if v['url'] in seen:
            continue
        seen[v['url']] = v
        versions.append(v)
    return versions


def unit_kind(eli: str, title: str) -> str:
    """What the numbered provisions of a Revised Act are called: sections of an Act; regulations, articles or rules of a
    statutory instrument (by its title)."""
    if eli.split('/')[1] != 'si':
        return 'section'
    t = re.sub(r'\s*\(Repealed\)$', '', title)
    if re.search(r'\bOrder\b', t):
        return 'article'
    if re.search(r'\bRules\b', t):
        return 'rule'
    return 'regulation'


def acts_from_alpha(offline: bool) -> list[dict]:
    """Every English-language Revised Act in the alphabetical list, oldest first by year and number: its ELI, a folder
    name made from its title (without '(Repealed)'), and its title as listed."""
    import html
    page = fetch(f'{SITE}/revacts/alpha', offline, b'<!doctype').decode('utf-8')
    acts: dict[str, dict] = {}
    for eli, b in re.findall(r'<tr class="[^"]*" data-eli="([^"]*)/en" style="[^"]*">(.*?)</tr>', page, re.S):
        m = re.search(r'<a href="/eli/[^"]*/front/revised/en/html"[^>]*>([^<]*)</a>', b)
        if eli in acts or not m:
            continue
        title = re.sub(r'\s+', ' ', html.unescape(m.group(1))).strip()
        short = re.sub(r'\s*\(Repealed\)$', '', title).rstrip('.')
        slug = re.sub(r'[^a-z0-9]+', '-', short.lower()).strip('-')
        acts[eli] = {'eli': eli, 'slug': slug, 'short': short, 'listed_title': title, 'unit': unit_kind(eli, title)}
    out = sorted(acts.values(), key=lambda a: (int(a['eli'].split('/')[0]), a['eli'].split('/')[1], int(a['eli'].split('/')[2])))
    slugs = [a['slug'] for a in out]
    assert len(set(slugs)) == len(slugs), 'two acts with one folder name'
    return out


# ---------------------------------------------------------------- the PDF reader

def spans_text(spans) -> str:
    return ''.join(s['text'] for s in spans)


NOISE = re.compile(r'\s*(F\d+\[?|\[|\])\s*')
MARK = re.compile(r'F(\d+)\[')
SECTION = re.compile(r'^(\d+[A-Z]{0,3})\.(?: |\u2014)')
ORDINALS = ['FIRST', 'SECOND', 'THIRD', 'FOURTH', 'FIFTH', 'SIXTH', 'SEVENTH', 'EIGHTH', 'NINTH', 'TENTH', 'ELEVENTH',
            'TWELFTH', 'THIRTEENTH', 'FOURTEENTH', 'FIFTEENTH', 'SIXTEENTH', 'SEVENTEENTH', 'EIGHTEENTH', 'NINETEENTH',
            'TWENTIETH']
# an old Act's schedule heading: 'FIRST SCHEDULE.', 'THE SECOND SCHEDULE'
ORDINAL_SCHEDULE = r'(?:THE )?(' + '|'.join(ORDINALS) + r') SCHEDULE\.?'
SCHEDULE_LINE = r'(?:SCHEDULE(?: \d+[A-Z]*)?\.?|' + ORDINAL_SCHEDULE + ')'


SCHEDULE_LINE_RE = re.compile(SCHEDULE_LINE)
FOOTNOTE = re.compile(r'\s*O\.? ?J\.? (?:No\.? )?[LC] ?\d')   # a footnote citing the Official Journal
SIGNED = re.compile(r'Done at [A-Z][\w\-]+')     # a treaty's or directive's signature line
REF_NOTE = re.compile(r'(?:Sections?|Sects?\.|Articles?|Regulations?|Rules?|Paragraphs?) [0-9A-Z(),\- and]{1,40}\.?')


def unmarked(t: str) -> str:
    return re.sub(r'F\d+\[|\]', '', t).strip()     # a line's text without the annotation marks
NOTE_ID = re.compile(r'^([FCEM])(\d+)$')


LINES = 1   # bump when page_lines() changes (its output is cached apart from the reader's rules, which are fast)


def page_lines(raw: bytes) -> list[list[dict]]:
    """Every text line of every page, with its spans (text, size, font, origin), in reading order: the slow part of
    reading a PDF (PyMuPDF character positions), cached by the PDF's sha256 so a change in the rules applied to the lines
    re-reads no PDF."""
    import json
    path = CACHE / f'lines{LINES}-{hashlib.sha256(raw).hexdigest()[:24]}.json.gz'
    if path.exists():
        return json.loads(gzip.decompress(path.read_bytes()).decode('utf-8'))
    pages = _page_lines(raw)
    tmp = path.with_suffix('.tmp')
    tmp.write_bytes(gzip.compress(json.dumps(pages, ensure_ascii=False, separators=(',', ':')).encode('utf-8'), 6, mtime=0))
    tmp.replace(path)
    return pages


def _page_lines(raw: bytes) -> list[list[dict]]:
    import pymupdf
    doc = pymupdf.open(stream=raw, filetype='pdf')
    pages = []
    for pn, page in enumerate(doc):
        lines = []
        for b in page.get_text('rawdict')['blocks']:
            if b['type'] != 0:
                continue
            for l in b['lines']:
                sp = []
                prev = None
                has_space = any(c['c'] == ' ' for s_ in l['spans'] for c in s_['chars'])
                for s_ in l['spans']:
                    out = []
                    for c in s_['chars']:
                        if c['c'] == ' ':
                            out.append(' ')
                        else:
                            if prev is not None and c['bbox'][0] - prev > (0.9 if has_space else 0.6):
                                out.append(' ')
                            out.append(c['c'])
                        prev = c['bbox'][2]
                    t = ''.join(out)
                    if s_['size'] < 7.0 and t.strip().isdigit():
                        continue      # a footnote reference (its number changes between revisions)
                    if t:
                        sp.append({'text': t, 'size': s_['size'], 'font': s_['font'], 'origin': list(s_['origin'])})
                if not sp or not spans_text(sp).strip():
                    continue
                big = max(sp, key=lambda s: s['size'])
                lines.append({'page': pn, 'x': l['bbox'][0], 'y': big['origin'][1], 'size': round(big['size'], 1),
                              'spans': sp, 'text': spans_text(sp)})
        lines.sort(key=lambda l: (l['y'], l['x']))
        pages.append(lines)
    return pages


def read_pdf_lines(raw: bytes) -> tuple[list[dict], dict, str | None]:
    """Body lines (in reading order) and the annotation notes of one revision."""
    body, notes, upd = [], {}, None
    cur_note = None
    in_block = False          # inside the annotations under a provision (from their heading or first note)
    held: list[dict] = []     # lines in another size inside an annotation: a heading the annotation quotes

    def keep(l):
        nonlocal upd
        um = re.search(r'Updated to (\d{1,2}) (\w+) (\d{4})', l['text'])
        if um and upd is None:
            upd = f'{int(um.group(3)):04d}-{MONTHS[um.group(2)[:3]]:02d}-{int(um.group(1)):02d}'
        if not COVER.fullmatch(l['text'].strip()) and not (l['size'] <= 9.0 and FOOTNOTE.match(l['text'])):
            body.append(l)    # (a footnote citing the Official Journal, set small at the foot of a page, is not text)

    def release():
        for h in held:
            keep(h)
        held.clear()
    for lines in page_lines(raw):
        for l in lines:
            if l['y'] < 72 or l['y'] > 800:
                continue
            if l['size'] < 8.0:
                if held and cur_note:     # a table in the annotation, below the headings it quotes
                    for h in held:
                        notes[cur_note] += ' ' + h['text'].strip()
                    held.clear()
                continue          # footnotes at the foot of a page
            if 8.0 <= l['size'] <= 8.9:
                f = l['spans'][0]
                m = NOTE_ID.match(f['text'].strip())
                if m and 'Bold' in f['font']:
                    release()
                    cur_note = m.group(1) + m.group(2)
                    notes[cur_note] = spans_text(l['spans'][1:]).strip()
                    in_block = True
                elif 'Bold' in f['font'] and l['text'].strip().rstrip(':') in (
                        'Annotations', 'Amendments', 'Editorial Notes', 'Modifications (not altering text)'):
                    release()
                    cur_note = None
                    in_block = True
                elif not in_block:
                    if not FOOTNOTE.match(l['text']):
                        keep(l)   # small print outside the annotations: a table set in 8pt is text (not a footnote)
                elif cur_note:
                    # the annotation goes on after lines in another size: they were a heading it quotes
                    for h in held:
                        notes[cur_note] += ' ' + h['text'].strip()
                    held.clear()
                    notes[cur_note] += ' ' + l['text'].strip()
                continue
            if cur_note and l['size'] not in (9.0, 10.0) and len(held) < 6:
                held.append(l)
                continue
            release()
            cur_note = None
            in_block = False
            keep(l)
    release()
    ref = [l['x'] for l in body if l['size'] == 10.0 and re.match(r'\(\d+\) ', l['text'])]
    ref_x = sorted(ref)[len(ref) // 2] if ref else 179
    # Where quoted amendments ('(1) ...' set further in) outnumber the act's own subsections, that median lands right of
    # the text column and the column itself would be taken for margin: the bold section numbers mark the column too.
    sec = [l['x'] for l in body if l['size'] == 10.0 and is_bold(l['spans'][0])
           and re.match(r'(F\d+\[)?\d+[A-Z]{0,3}\.', l['spans'][0]['text'].strip())]
    if sec:
        ref_x = min(ref_x, sorted(sec)[len(sec) // 2])
    margin_cols = margin_columns(body, ref_x)
    table = False
    for l in body:
        t = l['text'].strip()
        if t == 'TABLE':
            table = True        # a table set out in a section can run out into the margin column: its cells are text
        elif table and is_bold(l['spans'][0]) and re.match(r'(F\d+\[)?\d+[A-Z]{0,3}\.', t) or SCHEDULE_LINE_RE.fullmatch(unmarked(t)):
            table = False       # until the next section (or schedule)
        # in a table, a cell is text; a note naming the section a schedule belongs to ('Section 2.') is not a cell
        cell = (table and not REF_NOTE.fullmatch(t)) or SIGNED.match(t) is not None
        in_col = not margin_cols or any(-8 <= l['x'] - c <= 12 for c in margin_cols)
        l['margin'] = (in_col or REF_NOTE.fullmatch(t) is not None) and l['x'] < ref_x - 40 \
            and 9.0 <= l['size'] <= 10.0 and not cell
        l['ref_x'] = ref_x
    return body, notes, upd


def margin_columns(lines: list[dict], ref_x: float) -> set[int]:
    """Where the marginal headings stand (9-10pt, left of the text column, after the contents): every x that holds
    at least 5 of them and 5% of all. A line left of the text column elsewhere is text (a table's far-left cells,
    'Done at Brussels, ...'), unless it is a reference note ('Section 93.')."""
    try:
        first = text_start(lines)[1]
    except AssertionError:
        first = 0
    cols = collections.Counter(round(l['x']) for l in lines[first:]
                               if 9.0 <= round(l['size'], 1) <= 10.0 and l['x'] < ref_x - 40)
    total = sum(cols.values())
    return {x for x, k in cols.items() if k >= 5 and k >= total * 0.05} or set(cols)


def is_bold(sp) -> bool:
    return 'Bold' in sp['font']


def paragraphs(body: list[dict]) -> list[dict]:
    """Group lines into paragraphs by the vertical gap (a continuation line is about 11pt below, a new paragraph 17pt
    or more), then join a paragraph that runs across a page break."""
    paras = []
    prev = None
    for l in body:
        new = True
        if prev is not None:
            gap = (l['y'] - prev['y']) if l['page'] == prev['page'] else None
            if gap is not None:
                new = gap > 15 or l['size'] != prev['size']
            else:
                t = l['text'].strip()
                new = bool(re.match(r'^(\(\w+\)|\d+[A-Z]*\.(?: |\()|F\d+\[|[\u201c"]|[A-Z ]{6,}$)', t)) or is_bold(l['spans'][0]) \
                    or l['size'] != prev['size']
        if not new and is_bold(l['spans'][0]) and re.match(r'^(F\d+\[)?\d+[A-Z]{0,3}\.(?: \(?\w|\(|\u2014)', l['text'].strip()):
            new = True       # a bold marginal heading directly above its section line
        if re.fullmatch(SCHEDULE_LINE, unmarked(l['text'])) or (
                prev is not None and re.fullmatch(SCHEDULE_LINE, unmarked(prev['text']))):
            new = True       # a schedule's heading, and the line after it, start paragraphs of their own
        if centred_italic(l) != centred_italic(prev):
            new = True       # a cross-heading in italics, centred over the text (old Acts), is a paragraph of its own
        if new:
            paras.append({'lines': [l], 'size': l['size']})
        else:
            paras[-1]['lines'].append(l)
        prev = l
    return paras


def centred_italic(l: dict | None) -> bool:
    return l is not None and l['x'] > l['ref_x'] + 40 and all(
        'Italic' in s['font'] for s in l['spans'] if s['text'].strip() and not NOISE.fullmatch(s['text']))


VOCAB: set[str] = set()
HY = chr(1)   # a line-end hyphen nobody can decide on yet: resolved against every revision's words


def join_lines(texts: list[str]) -> str:
    out = ''
    for t in texts:
        t = re.sub(r'\s+', ' ', t.strip())
        if not out:
            out = t
            continue
        if re.search(r'\w-$', out) and re.match(r'[a-z]', t):
            out = out[:-1] + HY + t
        else:
            out += ' ' + t
    return out


def strip_markers(paras: list[dict]):
    """Remove the 'F12[' ... ']' annotation brackets. Records which notes each paragraph carries."""
    stack: list[bool] = []
    for p in paras:
        raw = join_lines([l['text'] for l in p['lines']])
        first = next((s for s in p['lines'][0]['spans'] if not NOISE.fullmatch(s['text'])), p['lines'][0]['spans'][0])
        p['bold'] = all(is_bold(s) for l in p['lines'] for s in l['spans'] if not NOISE.fullmatch(s['text']) and s['text'].strip())
        p['bold_start'] = is_bold(first)
        out, marks, i = [], [], 0
        while i < len(raw):
            m = MARK.match(raw, i)
            if m:
                stack.append(True)
                marks.append('F' + m.group(1))
                i = m.end()
                continue
            c = raw[i]
            if c == '[':
                stack.append(False)
                out.append(c)
            elif c == ']':
                # a closing bracket with no opening one is an annotation bracket whose mark the revision left out
                if stack and not stack.pop():
                    out.append(c)
            else:
                out.append(c)
            i += 1
        p['text'] = re.sub(r'\s+', ' ', ''.join(out)).strip()
        p['text'] = re.sub(r'^(\d+[A-Z]{0,3})\.\(', r'\1. (', p['text'])   # '117A.(1)' is set as '117A. (1)' elsewhere
        p['marks'] = marks
    return paras


def suffix_key(s: str, others: set[str]) -> tuple:
    """Where a section's letters put it among the others of its number. An inserted section follows the one it is
    named after (31A, 31AA, 31AB, 31B); but once a number's letters have run to Z, the next ones carry on after Z
    (33Y, 33Z, 33AA, ..., 33AZ, then 33BA or 33AAA), as the Revised Acts print them; an insertion elsewhere still
    follows its own section (33S, 33SA, 33T)."""
    if len(s) <= 1:
        return (0, s)
    full, x = 'Z' in others, 'A'
    while full and x <= 'Z':
        family = {t[1:] for t in others if len(t) > 1 and t[0] == x}
        if s[0] == x:
            return (1, x, suffix_key(s[1:], family))
        full, x = 'Z' in family, chr(ord(x) + 1)
    return (0, s[0], suffix_key(s[1:], {t[1:] for t in others if len(t) > 1 and t[0] == s[0]}))


def ordered(keys) -> list[str]:
    """Unit keys in the act's order: long title, sections by number (and letters, suffix_key), schedules."""
    keys = list(keys)
    letters: dict[tuple, set[str]] = {}
    for k in keys:
        m = re.fullmatch(r'(section|regulation|article|rule|schedule)-(\d+)([A-Z]*)', k)
        if m:
            letters.setdefault((m.group(1) == 'schedule', int(m.group(2))), set()).add(m.group(3))

    def key(k):
        m = re.fullmatch(r'(section|regulation|article|rule|schedule)-(\d+)([A-Z]*)', k)
        if m:
            g = (m.group(1) == 'schedule', int(m.group(2)))
            return (2 if g[0] else 1, g[1], suffix_key(m.group(3), letters[g]))
        return (0 if k == 'long-title' else 3, 0, (0, k))
    return sorted(keys, key=key)


def sec_order(key: str) -> tuple:
    m = re.fullmatch(r'(?:section|regulation|article|rule)-(\d+)([A-Z]*)', key)
    if m:
        return (1, int(m.group(1)), m.group(2))   # 31A, 31AA, 31AB, 31B: the Irish order
    m = re.fullmatch(r'schedule-(\d+)([A-Z]*)', key)
    if m:
        return (2, int(m.group(1)), m.group(2))
    return (0 if key == 'long-title' else 3, 0, key)


ENACT = re.compile(r'\s*(?:F\d+\[)?be ?it ?(?:therefore ?|further ?)?enacted', re.I)   # spaces optional: some PDFs' span text has none
MAKE = re.compile(r'.*\bhereby (?:make|makes|order|orders|prescribe|prescribes)\b', re.I)
AN_ACT = re.compile(r'\s*(?:F\d+\[)?an ?act(?![a-su-z])', re.I)


def text_start(lines: list[dict]) -> tuple[int, int]:
    """Where the text starts after the cover and the contents: (the enacting line, the first line of the text).
    An Act: its enacting formula ('Be it enacted ...', 'BE IT THEREFORE ENACTED ...'), the text starting at the long
    title above it ('An Act ...'). A statutory instrument: the line that makes it ('... hereby make(s) the following
    Regulations'), the text starting at the first line of that recital. An old Act printed without an enacting formula:
    its long title."""
    start = next((i for i, l in enumerate(lines) if ENACT.match(l['text'])), None)
    if start is not None:
        j = start
        while j > 0 and not AN_ACT.match(lines[j]['text']):
            j -= 1
        return start, (j if AN_ACT.match(lines[j]['text']) else start)
    # 'hereby' at the end of one line and 'makes the following Regulations' on the next count too
    start = next((i for i, l in enumerate(lines) if l['page'] > 0 and (MAKE.match(l['text']) or (
        re.search(r'\bhereby$', l['text'].strip()) and i + 1 < len(lines)
        and MAKE.match('hereby ' + lines[i + 1]['text'].strip())))), None)
    if start is not None:
        j = start
        while j > 0 and lines[j - 1]['page'] == lines[j]['page'] and 0 < lines[j]['y'] - lines[j - 1]['y'] <= 16 \
                and not re.search(r'[A-Z]{4}', lines[j - 1]['text'][:12]):
            j -= 1
        return start, j
    start = next((i for i, l in enumerate(lines) if l['page'] > 0 and AN_ACT.match(l['text'])), None)
    assert start is not None, 'no enacting formula'
    return start, start


CAPS = "A-ZÁÉÍÓÚ0-9 ()’',.&-"     # capitals (with the Irish fadas), figures, punctuation
TITLE_END = rf"(?:[{CAPS}]* )?ACTS? \d{{4}}"                 # the last line of an act's title in capitals ('ACT 2010')
TITLE_CAPS = rf"(?!(?:PART|CHAPTER|SCHEDULE)\b)[{CAPS}]{{3,}}"   # an earlier line of it


def end_matter(lines: list[dict], i: int) -> bool:
    """Where the Commission's end matter starts: 'About this Revised Act', or (some revisions) a heading
    'Introduction' over 'This Revised Act presents the text ...'."""
    t = lines[i]['text'].strip()
    return t.startswith('About this Revised Act') or (
        t == 'Introduction' and i + 1 < len(lines) and lines[i + 1]['text'].strip().startswith('This Revised Act presents'))


def read_version(raw: bytes) -> dict:
    pending_head[0] = ''
    hold_marks[0] = []
    body, notes, upd = read_pdf_lines(raw)
    # the text starts after the cover lines: 'Updated to ...' precedes the long title
    start, j = text_start(body)
    # The end matter ('About this Revised Act', set in the margin column in some layouts) and the act's title in
    # capitals above it are not law: the text ends there.
    end = next((i for i in range(j, len(body)) if end_matter(body, i)), None)
    if end is not None:
        if end > j + 1 and re.fullmatch(r'\d{4}', body[end - 1]['text'].strip()) \
                and re.fullmatch(TITLE_CAPS, body[end - 2]['text'].strip()) and body[end - 2]['text'].strip().endswith(('ACT', 'ACTS')):
            end -= 1    # the title's year on a line of its own ('... PROCEDURES) ACT' / '2013')
            body[end - 1] = {**body[end - 1], 'text': body[end - 1]['text'].strip() + ' ' + body[end]['text'].strip()}
        if end > j and re.fullmatch(TITLE_END, body[end - 1]['text'].strip()):
            end -= 1
            # a long title runs over two or three lines in capitals, on the same page in the same size (not a
            # schedule's heading in capitals before it: 'REPEALS')
            where = (body[end]['page'], body[end]['size'])
            for _ in range(2):
                if end > j and re.fullmatch(TITLE_CAPS, body[end - 1]['text'].strip()) \
                        and (body[end - 1]['page'], body[end - 1]['size']) == where:
                    end -= 1
        body = body[:end]
    if body[j:]:
        body[j]['margin'] = False      # the long title's first line can hang out to the left, into the margin column
    main = [l for l in body[j:] if not l['margin']]
    margin = [l for l in body[j:] if l['margin']]
    clusters = []
    for l in margin:
        if clusters and clusters[-1]['page'] == l['page'] and l['y'] - clusters[-1]['y1'] <= 12:
            clusters[-1]['lines'].append(l['text'].strip())
            clusters[-1]['y1'] = l['y']
        else:
            clusters.append({'page': l['page'], 'y0': l['y'], 'y1': l['y'], 'lines': [l['text'].strip()]})
    for c in clusters:
        t = ''
        for x in c['lines']:
            t = t[:-1] + x if re.search(r'[a-z]-$', t) and x[:1].islower() else (t + ' ' + x if t else x)
        c['text'] = re.sub(r'\s+', ' ', t).strip()
    paras = strip_markers(paragraphs(main))
    # how many lines stand on each line's row: a table's row has several (its bold column heads are no heading)
    rows = collections.Counter((l['page'], round(l['y'])) for l in main)
    units: dict[str, dict] = {}
    unit_notes: dict[str, list[str]] = {}
    cur = None
    heads: list[str] = []
    last_num = 0
    in_sched = False
    ended = False

    def open_unit(key, label):
        nonlocal cur
        cur = {'key': key, 'label': label, 'lines': [], 'marks': []}
        units[key] = cur

    open_unit('long-title', 'Long title')
    # The end matter and the act's title above it were cut off at line level (above); a paragraph 'About this Revised
    # Act' left here (none should be) still ends the text, but no capitals line before it is taken for the title (the
    # last schedule's heading, 'AMENDMENT TO HEALTH (REPAYMENT SCHEME) ACT 2006', is law).
    end_at = next((i for i, p in enumerate(paras) if p['text'].startswith('About this Revised Act')), len(paras))
    toc = contents_titles(body[:start])
    toc_sections = [(i, SECTION.match(p['text']).group(1)) for i, p in enumerate(paras[:end_at])
                    if p['bold_start'] and SECTION.match(p['text'])
                    and (not toc or SECTION.match(p['text']).group(1) in toc)]   # where its sections start (strictly)
    for pi, p in enumerate(paras):
        if pi == end_at:
            ended = True
        t = p['text']
        if not t:
            if cur is not None:
                cur['marks'] += p['marks']
            continue
        sm = re.match(r'^SCHEDULE\b\s*(\d*[A-Z]*)\.?\s*$', t) if p['size'] >= 11 or t.isupper() else None
        om = re.fullmatch(ORDINAL_SCHEDULE, t)
        if om and not sm:     # old Acts: 'THE FIRST SCHEDULE.', 'SECOND SCHEDULE' -> schedule-1, schedule-2
            num = str(ORDINALS.index(om.group(1).upper()) + 1)
            sm = type('M', (), {'group': staticmethod(lambda i, num=num: num)})()
        # Later schedules' headings are not always set larger; inside the schedules, 'SCHEDULE <the next number>' on
        # a line of its own opens the next one (a quoted schedule would not carry the next number in sequence).
        nxt = in_sched and sm and re.fullmatch(r'\d+', sm.group(1) or '') and cur['key'].startswith('schedule-') \
            and re.fullmatch(r'\d+', cur['key'][9:]) and int(sm.group(1)) == int(cur['key'][9:]) + 1
        # A schedule heading before the act's last sections is quoted (a schedule inserted into another Act by a
        # section): the act's own schedules follow its sections.
        quoted = sm and not in_sched and any(i > pi and f'section-{k}' not in units
                                             and last_num < int(re.match(r'\d+', k).group()) <= last_num + 3
                                             for i, k in toc_sections)
        if (sm and not in_sched or (sm and in_sched and p['size'] >= 11) or nxt) and not quoted \
                and f'schedule-{sm.group(1) or "1"}' not in units:     # a quoted schedule of the same number is text
            in_sched = True
            n = sm.group(1) or '1'
            open_unit(f'schedule-{n}', f'Schedule {n}')
            cur['lines'] += heads + [t]
            heads = []
            cur['marks'] += p['marks']
            continue
        if in_sched:
            if ended:
                continue
            cur['lines'].append(t)
            cur['marks'] += p['marks']
            continue
        # An act with no schedule: the Commission's end matter ('About this Revised Act', under the act's title in
        # capitals) follows the last section, and is not law.
        if ended or t.startswith('About this Revised Act'):
            ended = True
            if pending_head[0] and pending_head[0].isupper():
                pending_head[0] = ''
            if cur['lines'] and cur['lines'][-1].isupper() and re.search(r' ACTS? \d{4}$', cur['lines'][-1]):
                cur['lines'].pop()
            continue
        # a chapter's title: italic, centred (a two-line title's first line can start left of the text column)
        worded = [sp for l in p['lines'] for sp in l['spans'] if re.search(r'[^\W\d_]', sp['text'])]
        italic = bool(worded) and all('Italic' in sp['font'] for sp in worded)   # a full stop after it can be upright
        alone = all(rows[(l['page'], round(l['y']))] == 1 for l in p['lines'])   # not a cell of a table's row
        if p['size'] >= 11 or (italic and alone and p['size'] >= 9.0 and len(t) < 200 and (heads or
                                                           max(l['x'] for l in p['lines']) > p['lines'][0]['ref_x'] + 40)):
            heads.append(f'## {t}')
            hold_marks[0] += p['marks']     # an inserted part brings its heading: the note goes with the next section
            continue
        if heads and (re.fullmatch(r'(?:PART|CHAPTER|Part|Chapter) (?:\d+[A-Z]*|[IVXLC]+[A-Z]?)', t)
                      or REF_NOTE.fullmatch(t) or (
                # the title in the text size right under a bare 'PART IIB' / 'Chapter I' line
                re.fullmatch(r'## (?:PART|CHAPTER|Part|Chapter) (?:\d+[A-Z]*|[IVXLC]+[A-Z]?)\s*\W?', heads[-1])
                and re.match(r'[A-Z]', t) and len(t) < 150 and not t.endswith(('.', ';', ':', ',', '\u2014'))
                and not SECTION.match(t)) or (
                re.match(r'## [A-Z]', heads[-1]) and t == t.upper() and re.search(r'[A-Z]{3}', t)
                and len(t) < 200 and not SECTION.match(t) and not re.match(r'(F\d+\[)?\d', t))):
            # a chapter's heading in the text size under a part's ('Chapter 1A'), or a part's title in capitals
            heads.append(f'## {t}')     # a part's title in capitals under its heading ('PART IIIC —' / 'CERTIFICATE OF ...')
            hold_marks[0] += p['marks']
            continue
        num = SECTION.match(t)
        if num and p['bold_start']:
            for c in clusters:
                if c['page'] == p['lines'][0]['page'] and -4 <= p['lines'][0]['y'] - c['y0'] <= 14 and not c.get('used'):
                    c['used'] = True
                    # the heading without its annotation mark ('F217[Responsibilities ...]'): the mark is kept
                    # as the section's note below, not as text
                    pending_head[0] = re.sub(r'\]$', '', MARK.sub('', c['text'])) if MARK.search(c['text']) \
                        else c['text']
                    hold_marks[0] += ['F' + x for x in MARK.findall(c['text'])]   # a mark set in the margin heading
                    break
            n = int(re.match(r'\d+', num.group(1)).group())
            # a section of this act: next in the numbering, and in its contents (a quoted section inserted into another
            # Act by this one, '30A.' after this act's section 27, is not)
            if last_num <= n <= last_num + 3 and f'section-{num.group(1)}' not in units \
                    and in_contents(num.group(1), toc, last_num):
                last_num = n
                before = cur
                open_unit(f'section-{num.group(1)}', f'Section {num.group(1)}')
                cur['lines'] += heads
                heads = []
                if not pending_head[0] and before is not None and before['lines']:
                    tail = before['lines'][-1]
                    if re.match(r'[A-Z]', tail) and len(tail) < 300 and not tail.endswith(('.', ';', ':', ','))                             and not tail.startswith('## ') and len(before['lines']) > 1:
                        pending_head[0] = before['lines'].pop()
                if cur is not None and pending_head[0]:
                    cur['lines'].append(pending_head[0])
                    pending_head[0] = ''
                cur['lines'].append(t)
                cur['marks'] += p['marks'] + hold_marks[0]
                hold_marks[0] = []
                continue
        if p['bold'] and 9.0 <= p['size'] < 11 and not t.endswith(('.', ';', ':')) and len(t) < 400 and not num \
                and re.search(r'[^\W\d_]', t) and rows[(p['lines'][0]['page'], round(p['lines'][0]['y']))] == 1:
            pending_head[0] = (pending_head[0] + ' ' + t).strip() if pending_head[0] else t
            hold_marks[0] += p['marks']
            continue
        if heads and (not re.match(r'[A-Z]', t) or len(t) >= 100 or t.endswith(('.', ';', ':', ',', '—'))
                      or SCHEDULE_LINE_RE.fullmatch(t) or not alone):     # (or a table's row)
            # headings followed by text that is not a section of this act (a Part or Chapter inserted by a quoted
            # amendment) belong here, not at the top of this act's next section
            cur['lines'] += heads
            heads = []
        elif heads and not pending_head[0] and alone and min(l['x'] for l in p['lines']) > p['lines'][0]['ref_x'] + 40:
            # a short line set centred, alone, under headings is one more heading ('PART 3' / 'Basic Provisions'; '"Article 1' /
            # 'Purpose'): it stays with them, after them, and is never taken for (and replaced by) a section's title
            heads.append(f'## {t}')
            hold_marks[0] += p['marks']
            continue
        if pending_head[0]:
            cur['lines'].append(pending_head[0])
            pending_head[0] = ''
        cur['lines'].append(t)
        cur['marks'] += p['marks'] + hold_marks[0]
        hold_marks[0] = []
    if heads and cur is not None:
        cur['lines'] += heads       # headings after the last section's text (none should be): kept, not dropped
    titles = contents_titles(body[:start])
    apply_titles(units, titles)
    for k, u in list(units.items()):
        if not u['lines']:
            del units[k]
            continue
        u['text'] = '\n\n'.join(u['lines']) + '\n'
        u['notes'] = sorted({notes[m] for m in u['marks'] if m in notes})
    return {'updated_to': upd, 'units': units, 'notes': notes}


HEAD_SPLIT = re.compile(r' (?=(?:PART|CHAPTER|Chapter) \d+[A-Z]*\b)')


def canon_lines(lines: list[str]) -> list[str]:
    """One layout for every revision. The PDFs set a list's closing words ('and', 'shall be liable ...') as their own
    paragraph in one revision and run them on in the next, and break part and chapter headings differently, so: a
    paragraph that starts with a small letter runs on from the one before, consecutive headings are joined and split
    again before each PART/CHAPTER/Chapter, and no space is kept between two opening quotes."""
    out: list[str] = []
    heads: list[str] = []

    def flush():
        if heads:
            out.extend('## ' + h for h in HEAD_SPLIT.split(' '.join(heads)))
            heads.clear()
    for t in lines:
        t = re.sub('([\u201c\u2018"]) (?=[\u2018\u201c])', r'\1', t)
        t = re.sub('(?<!^##) +(?=[\u201d\u2019])', '', t)     # not the space after a heading's '##'
        t = re.sub('([\u201c\u2018]) +', r'\1', t)
        if t.startswith('## '):
            heads.append(t[3:])
            continue
        flush()
        if out and not out[-1].startswith('## ') and re.match(r'[a-z]', t):
            out[-1] += ' ' + t
        else:
            out.append(t)
    flush()
    return [d for t in out for d in ([t] if t.startswith('## ') else DEF_SPLIT.split(t))]


# a definition run on after the one before it ('...; \u2018data\u2019 means ...') starts its own paragraph
DEF_SPLIT = re.compile('(?<=[;\u2014]) (?=[\u2018\u201c][^\u2019\u201d]{1,120}[\u2019\u201d]'
                       '(?:(?:,| and| or) [\u2018\u201c][^\u2019\u201d]{1,120}[\u2019\u201d])* '
                       '(?:means|includes|has|have|shall|does|in relation)\\b)')


pending_head = ['']
hold_marks = [[]]


PARSER = 34   # bump when the reader changes, so cached readings are not reused


def parsed_path(sha: str) -> Path:
    return CACHE / f'parsed{PARSER}-{sha[:24]}.json'


def parse_to_cache(url: str, offline: bool):
    import json
    raw = fetch(url, offline)
    parsed = read_version(raw)
    parsed['units'] = {k: {'key': u['key'], 'label': u['label'], 'text': u['text'], 'notes': u['notes']}
                       for k, u in parsed['units'].items()}
    parsed_path(hashlib.sha256(raw).hexdigest()).write_text(json.dumps(parsed, ensure_ascii=False, sort_keys=True),
                                                            encoding='utf-8', newline='\n')


def rename_units(units: dict, unit: str) -> dict:
    """The reader names numbered provisions 'section-N'; in a statutory instrument they are regulations, articles or
    rules."""
    if unit == 'section':
        return units
    out = {}
    for k, u in units.items():
        if k.startswith('section-'):
            num = k[len('section-'):]
            k = f'{unit}-{num}'
            u = {**u, 'key': k, 'label': f'{unit.capitalize()} {num}'}
        out[k] = u
    return out


def canon_text(text: str) -> str:
    return '\n\n'.join(canon_lines(text.rstrip('\n').split('\n\n'))) + '\n'


def load_versions(act: dict, offline: bool) -> list[dict]:
    import json
    versions = history(act, offline)
    raws = fetch_all([v['url'] for v in versions], offline, b'%PDF')
    todo = []
    for v in versions:
        v['sha256'] = hashlib.sha256(raws[v['url']]).hexdigest()
        err = parsed_path(v['sha256']).with_suffix('.err')
        if err.exists():
            raise RuntimeError(f'unreadable revision {v["url"]}: {err.read_text(encoding="utf-8")}')
        if not parsed_path(v['sha256']).exists() and v['url'] not in todo:
            todo.append(v['url'])
    if todo:
        # Reading a PDF takes seconds: each is read once, then kept in the cache.
        for url in todo:
            parse_to_cache(url, offline)
    for v in versions:
        parsed = json.loads(parsed_path(v['sha256']).read_text(encoding='utf-8'))
        for u in parsed['units'].values():
            u['text'] = canon_text(u['text'])
        v['updated_to'] = parsed['updated_to']
        v['units'] = rename_units(parsed['units'], act.get('unit', 'section'))
        v['notes'] = parsed['notes']
    gv: set[str] = set()
    for v in versions:
        for u in v['units'].values():
            gv.update(w.lower() for w in re.findall(r"[\w'-]+", u['text'].replace(HY, ' ')))

    def resolve(m):
        left, right = m.group(1), m.group(2)
        if f'{left}-{right}'.lower() in gv:
            return f'{left}-{right}'
        if (left + right).lower() in gv:
            return left + right
        return f'{left}-{right}'
    for v in versions:
        for u in v['units'].values():
            if HY in u['text']:
                u['text'] = HY_PAIR.sub(resolve, u['text'])
    versions.sort(key=lambda v: (v['updated_to'], v['listed']))
    # Two listings updated to the same day: the later listing is the one the Commission kept, and is the version --
    # unless the later one was printed without its annotations (no F-marks, no notes: the Child Care Act 1991 listed
    # 19 Aug 2020, a reprint of the 12 May 2020 revision) while the earlier carries them. Then the annotated one is the
    # version: the same text, and the notes that say which law made each change.
    annotated = lambda v: any(k.startswith('F') for k in v['notes'])
    by_day: dict[str, dict] = {}
    for v in versions:
        before = by_day.get(v['updated_to'])
        if before is not None:
            if annotated(before) and not annotated(v):
                before['replaces_unannotated'] = v['url']
                continue
            v['replaces'] = before['url']
        by_day[v['updated_to']] = v
    return list(by_day.values())

COVER = re.compile(r'(Number \d+ of \d{4}|Updated to .*|.*\bREVISED( Updated to .*)?)')


def norm(text: str | None, key: str = '') -> str:
    """What counts as the same text: no part headings or marginal heading, no white space (layout differs between
    revisions); a schedule is compared as its sorted words, because its tables are read in a different order from one
    layout to the next."""
    if not text:
        return ''
    lines = [l for l in text.split('\n') if l.strip() and not l.startswith('## ')]
    if key.startswith(('section', 'regulation', 'article', 'rule')):
        while lines and not re.match(r'(\d+[A-Z]{0,3})\.(?: |\u2014)', lines[0]):
            lines.pop(0)
        while len(lines) > 1 and re.match(r'[A-Z]', lines[-1]) and len(lines[-1]) < 300 \
                and not lines[-1].endswith(('.', ';', ':', ',')):
            lines.pop()
    t = '\n'.join(lines)
    t = t.translate({0x201c: '"', 0x201d: '"', 0x2018: "'", 0x2019: "'"})
    if key.startswith('schedule'):
        # A schedule's tables are read cell by cell in a different order, and broken over lines at different places,
        # from one layout to the next: it is compared as the letters and digits it contains, without the table's
        # column headings, which are repeated on every page the table runs to.
        t = re.sub(r'Item\b(?:[^()]*\(\d\)){4}', '', t)
        return ''.join(sorted(re.sub(r'\W', '', t)))
    return re.sub(r'\s+', '', t)


def same_letters(a: str, b: str) -> bool:
    """The same letters and digits, in any order: a table inside a section whose cells a later layout reads in another
    order (a repeal table's columns), with no word changed."""
    f = lambda t: sorted(re.sub(r'[\W_]', '', HY_RE.sub('', t)))
    return f(a) == f(b)


def in_contents(key: str, toc: dict, last: int | None = None) -> bool:
    """May '30A' be a section of this act? A plain number in sequence always may (some contents are read only in
    part), and so may a lettered one inserted after the section it is named after ('18A' after 18; some revisions'
    contents leave the inserted sections out). One that jumps ahead ('30A' after this act's section 27: a quoted
    section inserted into another Act) must be in the contents."""
    return key.isdigit() or not toc or key in toc or (last is not None and int(re.match(r'\d+', key).group()) == last)


def contents_titles(lines: list[dict]) -> dict[str, str]:
    """Section number -> title, from the table of contents before the text."""
    out: dict[str, str] = {}
    i = 0
    while i < len(lines):
        l = lines[i]
        m = re.match(r'(\d+[A-Z]{0,3})\. (\S.*)$', l['text'].strip())
        skip = 1
        if not m and re.fullmatch(r'\d+[A-Z]{0,3}\.', l['text'].strip()) and i + 1 < len(lines)                 and lines[i + 1]['page'] == l['page'] and abs(lines[i + 1]['y'] - l['y']) <= 2 and lines[i + 1]['x'] > l['x']:
            # the number and the title set as two lines on one row ('271.' / 'Close season for oysters.')
            m = re.match(r'(\d+[A-Z]{0,3})\. (\S.*)$', l['text'].strip() + ' ' + lines[i + 1]['text'].strip())
            skip = 2
        if m and l['size'] == 10.0:
            title = m.group(2)
            j = i + skip
            while j < len(lines) and lines[j]['page'] == l['page'] and 0 < lines[j]['y'] - lines[j - 1]['y'] <= 14 \
                    and lines[j]['x'] >= l['x'] and not re.match(r'(\d+[A-Z]{0,3}\. |PART |CHAPTER |SCHEDULE|Chapter )', lines[j]['text'].strip()) \
                    and lines[j]['size'] == 10.0:
                nxt = lines[j]['text'].strip()
                title = title[:-1] + HY + nxt if re.search(r'\w-$', title) and nxt[:1].islower() else title + ' ' + nxt
                j += 1
            title = re.sub(r'\]$', '', MARK.sub('', title)) if MARK.search(title) else title   # an inserted section's mark
            out.setdefault(m.group(1), re.sub(r'\s+', ' ', title).strip())
            i = j
        else:
            i += 1
    return out


def apply_titles(units: dict, titles: dict[str, str]):
    """The marginal heading of each section is its title in the contents (the layout of the heading changes between
    revisions, so detecting it on the page is unreliable): drop whatever was taken for a heading and put the title."""
    keys = ordered(k for k in units if k.startswith('section-'))
    flat = lambda t: re.sub(r'[^a-z0-9]', '', HY_RE.sub('', t).lower())
    for n, k in enumerate(keys):
        u = units[k]
        num = k.split('-', 1)[1]
        title = titles.get(num)
        if not title:
            continue
        nxt = titles.get(keys[n + 1].split('-', 1)[1]) if n + 1 < len(keys) else None
        lines = u['lines']
        if nxt and len(lines) > 1 and flat(lines[-1]) == flat(nxt):
            lines.pop()
        heads = []
        while lines and lines[0].startswith('## '):
            heads.append(lines.pop(0))
        while lines and not re.match(r'\d+[A-Z]{0,3}\.(?: |\u2014)', lines[0]):
            lines.pop(0)
        u['lines'] = heads + [title] + lines


HY_RE = re.compile(chr(1))
HY_PAIR = re.compile(r"([\w'-]*\w)" + HY + r'(\w+)')   # a word broken at a line-end hyphen


# ---------------------------------------------------------------- the annotations: which law made a change, and when

NOTE_DATED = re.compile(r'\((\d{1,2})\.(\d{1,2})\.(\d{4})\) by (.+?) \((\d+/\d{4}|S\. ?I\. No\. \d+ of \d{4})\)')
NOTE_LAW = re.compile(r'(?:by )?([^()]{0,200}?) ?\((\d+/\d{4}|S\. ?I\. No\. \d+ of \d{4})\)')


def clean_note(n: str) -> str:
    """Notes are read from the page like the text: a word broken over two lines ('Regu- lations') is joined again."""
    return re.sub(r'\s+', ' ', re.sub(r'(?<=[a-z])- (?=[a-z])', '', n)).strip()


def law_key(ident: str) -> str:
    """'27/2022' -> 'act/2022/27'; 'S.I. No. 375 of 2023' -> 'si/2023/375'."""
    m = re.fullmatch(r'(\d+)/(\d{4})', ident)
    if m:
        return f'act/{m.group(2)}/{int(m.group(1))}'
    m = re.fullmatch(r'S\. ?I\. No\. (\d+) of (\d{4})', ident)
    return f'si/{m.group(2)}/{int(m.group(1))}'


def law_label(key: str) -> str:
    kind, y, n = key.split('/')
    if kind == 'bps':
        return f'{y} c. {n}'
    return f'No. {n} of {y}' if kind == 'act' else f'S.I. No. {n} of {y}'


def law_url(key: str) -> str:
    kind, y, n = key.split('/')
    if kind == 'bps':
        return f'{SITE}/eli/{y}/bps/{n}/front/revised/en/html'
    return f'https://www.irishstatutebook.ie/eli/{y}/{kind}/{n}/{"enacted" if kind == "act" else "made"}/en/html'


def author_of(key: str, laws: dict) -> tuple[str, str]:
    kind, y, n = key.split('/')
    return laws[key]['name'], f'{kind}-{y}-{n}@irishstatutebook.invalid'


def tag_of(key: str) -> str:
    kind, y, n = key.split('/')
    return f'{kind}/{y}-{n}'


def read_note(n: str) -> dict | None:
    """The law and the day of one textual amendment note ('F12 Substituted (1.01.2023) by ... Act 2022 (27/2022), s. 5').
    Where the note quotes an amendment made through another act ('Substituted by A (7/2004), ... as inserted (26.12.2018)
    by B (39/2018)'), the dated one is the law that changed this text."""
    n = clean_note(n)
    m = NOTE_DATED.search(n)
    if m:
        return {'key': law_key(m.group(5)), 'name': m.group(4).strip(), 'day': f'{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}',
                'note': n}
    m = NOTE_LAW.search(n)
    if m:
        return {'key': law_key(m.group(2)), 'name': m.group(1).strip(), 'day': None, 'note': n}
    return None


def next_day(day: str) -> str:
    d = dt.date.fromisoformat(day) + dt.timedelta(days=1)
    while d in (last_sunday(d.year, 3), last_sunday(d.year, 10)):
        d += dt.timedelta(days=1)   # not a day the clocks change: noon is unambiguous, but keep clear of them
    return d.isoformat()


def build_act(act: dict, offline: bool) -> dict:
    versions = load_versions(act, offline)
    laws: dict[str, dict] = {}
    names: dict[str, dict[str, int]] = {}
    days: dict[str, set] = {}
    for v in versions:
        for u in v['units'].values():
            for n in u['notes']:
                r = read_note(n)
                if r:
                    names.setdefault(r['key'], {})
                    if r['day']:
                        names[r['key']][r['name']] = names[r['key']].get(r['name'], 0) + 1
                        days.setdefault(r['key'], set()).add(r['day'])
    for k in sorted(names):
        best = sorted(names[k].items(), key=lambda x: (-x[1], x[0]))
        laws[k] = {'key': k, 'name': best[0][0] if best else law_label(k), 'label': law_label(k), 'url': law_url(k),
                   'days': sorted(days.get(k, ()))}
    y_, kind_, n_ = act['eli'].split('/')
    own = f'{kind_}/{y_}/{int(n_)}'
    laws.setdefault(own, {'key': own, 'name': act['short'], 'label': law_label(own), 'url': law_url(own), 'days': []})
    laws[own]['name'] = act['short']
    changes, problems = [], []
    for prev, cur in zip(versions, versions[1:]):
        lo, hi = prev['updated_to'], cur['updated_to']
        keys = ordered(set(prev['units']) | set(cur['units']))
        changed = [k for k in keys if (prev['units'].get(k) or {}).get('text') != (cur['units'].get(k) or {}).get('text')]
        groups: dict[tuple, list[str]] = {}
        info: dict[str, dict] = {}
        for k in changed:
            p, c = prev['units'].get(k), cur['units'].get(k)
            if p and c and (norm(p['text'], k) == norm(c['text'], k) or same_letters(p['text'], c['text'])):
                g = (hi, 'layout', '')
                info[k] = {'why': 'layout'}
            else:
                # a note the earlier revision already carried (on any provision: text moves between sections) is
                # not what changed this text
                old = {clean_note(n) for n in prev['notes'].values()}
                new = [read_note(n) for n in (c or {}).get('notes', []) if clean_note(n) not in old]
                new = [r for r in new if r]
                for r in new:
                    if r['day'] is None and len(laws[r['key']]['days']) == 1:
                        r['day'], r['day_from'] = laws[r['key']]['days'][0], 'other notes of the same instrument'
                new = [r for r in new if r['day']]
                if not new and c:
                    # The revision printed the change without attaching its annotation (no F-mark in the text): the
                    # first later revision that attaches to this provision a note the earlier revision did not have,
                    # dated within this interval, names the law.
                    for later in versions[versions.index(cur) + 1:]:
                        seen = old
                        lu = later['units'].get(k)
                        cand = [read_note(n) for n in (lu or {}).get('notes', []) if clean_note(n) not in seen]
                        cand = [r for r in cand if r and r['day'] and lo < r['day'] <= hi]
                        if cand:
                            for r in cand:
                                r['later'] = later['updated_to']
                            new = cand
                            break
                lk = sorted({r['key'] for r in new})
                if not new:
                    g = (hi, 'unexplained', '')
                    info[k] = {'why': 'no new annotation'}
                else:
                    stated = max(r['day'] for r in new)
                    if stated > hi:
                        g = (hi, 'early', '|'.join(lk))
                        info[k] = {'why': 'printed early', 'stated': stated, 'notes': new}
                    else:
                        day = stated if stated > lo else next_day(lo)
                        kind_ = 'law' if len(lk) == 1 else 'candidates'
                        g = (day, kind_, '|'.join(lk), stated if stated <= lo else '')
                        info[k] = {'why': 'annotation', 'stated': stated, 'notes': new}
            groups.setdefault(g, []).append(k)
            if g[1] in ('unexplained', 'candidates', 'early'):
                problems.append(f'{hi} {k} ({g[1]})')
        changes.append({'lo': lo, 'hi': hi, 'prev': prev, 'cur': cur, 'groups': groups, 'info': info})
    return {'act': act, 'versions': versions, 'laws': laws, 'changes': changes, 'problems': problems, 'key': own,
            'title': act['short']}


# ---------------------------------------------------------------- the git repository

def git(repo: Path, *args: str, env: dict | None = None, input: str | None = None) -> str:
    # Bytes, not text mode: on Windows text mode turns '\n' on stdin into '\r\n', and commit messages would carry CRs.
    out = subprocess.run(['git', *args], cwd=repo, capture_output=True, env=env,
                         input=input.encode('utf-8') if input is not None else None)
    if out.returncode:
        raise SystemExit(f'git {" ".join(args)} failed: {out.stderr.decode("utf-8", "replace")}')
    return out.stdout.decode('utf-8').replace('\r\n', '\n')


def last_sunday(year: int, month: int) -> dt.date:
    d = (dt.date(year, month + 1, 1) if month < 12 else dt.date(year + 1, 1, 1)) - dt.timedelta(days=1)
    return d - dt.timedelta(days=(d.weekday() + 1) % 7)


def dublin_offset(day: dt.date) -> int:
    """Hours ahead of UTC at noon on a day in Dublin (written out: this machine has no tz database). Irish Standard Time
    (UTC+1) from the last Sunday in March to the last Sunday in October, as in the EU summer-time rules (the clocks move
    at 1:00 UTC, so noon on the first Sunday is summer time and noon on the last is not); UTC otherwise. Every day in
    this corpus is after 1981, from when these rules apply."""
    assert day.year >= 1981, day
    return 1 if last_sunday(day.year, 3) <= day < last_sunday(day.year, 10) else 0


def commit_date(day: str) -> str:
    d = dt.date.fromisoformat(day)
    off = dublin_offset(d)
    stamp = int(dt.datetime(d.year, d.month, d.day, 12, tzinfo=dt.timezone(dt.timedelta(hours=off))).timestamp())
    return f'@{stamp} +0{off}00'


def file_name(key: str) -> str:
    return f'{key}.md'


def write_unit(repo: Path, slug: str, key: str, unit: dict | None):
    path = repo / slug / file_name(key)
    if unit is None:
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(unit['text'], encoding='utf-8', newline='\n')


KIND_ORDER = {'law': 1, 'candidates': 2, 'early': 3, 'unexplained': 4, 'layout': 5}


def plan_commits(built: list[dict]) -> list[tuple]:
    """The commits in order. A law that changed several acts on one day is one commit (its parts, one per act, in the
    order of the acts); everything the publisher did is one commit per act."""
    commits = []
    merged: dict[tuple, dict] = {}
    for ai, b in enumerate(built):
        commits.append((b['versions'][0]['updated_to'], 0, ai, '', {'kind': 'start', 'b': b}))
        for ch in b['changes']:
            for g, keys in ch['groups'].items():
                part = {'kind': g[1], 'b': b, 'ch': ch, 'g': g, 'keys': keys}
                if g[1] == 'law':
                    k = (g[0], g[2], g[3])
                    if k in merged:
                        merged[k]['parts'].append(part)
                        continue
                    part = merged[k] = {'kind': 'law', 'g': g, 'parts': [part], 'b': b}
                commits.append((g[0], KIND_ORDER[g[1]], ai, g[2], part))
    commits.sort(key=lambda c: c[:4])
    return commits


def law_message(c: dict):
    """The message of a law's commit: one act as before; several acts, each act's part in turn under its title."""
    parts = c['parts']
    if len(parts) == 1:
        return change_message(parts[0]['b'], parts[0])
    pieces = [change_message(p['b'], p) for p in parts]
    b0, lk = parts[0]['b'], c['g'][2]
    law = b0['laws'][lk]
    nprov = sum(len(p['keys']) for p in parts)
    msg = [f'{law["name"]}: {len(parts)} acts, {nprov} provisions', '', f'{law["name"]} ({law["label"]})', '']
    for p, (_, m, _) in zip(parts, pieces):
        msg += [f'{p["b"]["act"]["short"]}:', ''] + m[4:]
    trailers: dict[str, list[str]] = {}
    for _, _, tr in pieces:
        for t in tr:
            k, v = t.split(': ', 1)
            if v not in trailers.setdefault(k, []):
                trailers[k].append(v)
    return pieces[0][0], msg, [f'{k}: {v}' for k, vs in trailers.items() for v in vs]


def wrap(text: str, width: int = 100) -> list[str]:
    import textwrap
    return textwrap.wrap(text, width, break_long_words=False, break_on_hyphens=False) or ['']


def labels_of(b: dict, ch: dict, keys: list[str]) -> list[str]:
    return [(ch['cur']['units'].get(k) or ch['prev']['units'][k])['label'] for k in keys]


def listing(ch: dict, keys: list[str]) -> list[str]:
    by: dict[str, list[str]] = {}
    for k in keys:
        p, c = ch['prev']['units'].get(k), ch['cur']['units'].get(k)
        name = 'Inserted' if p is None else 'Removed' if c is None else 'Changed'
        by.setdefault(name, []).append((c or p)['label'])
    return [f'{n}: {", ".join(by[n])}' for n in ('Inserted', 'Changed', 'Removed') if n in by]


def subject(short: str, labels: list[str], tail: str) -> str:
    s = f'{short}: {", ".join(labels)} ({tail})'
    if len(s) <= 100 or len(labels) == 1:
        return s
    return f'{short}: {len(labels)} provisions ({tail})'


def start_message(b: dict):
    v = b['versions'][0]
    law = b['laws'][b['key']]
    earlier = sorted({read_note(n)['key'] for u in v['units'].values() for n in u['notes'] if read_note(n)} - {b['key']})
    msg = [f'{b["act"]["short"]} ({law["label"]}), as revised to {v["updated_to"]}', '']
    msg += wrap(f'The act as the Law Reform Commission\'s first published revision gives it, updated to {v["updated_to"]}. '
                'No earlier revision is published, so this text already includes the amendments in force by that day'
                + (f', made by: {", ".join(b["laws"][k]["name"] + " (" + b["laws"][k]["label"] + ")" for k in earlier)}.'
                   if earlier else '.'))
    msg.append('')
    trailers = ['Kind: Act', f'In-force: {v["updated_to"]}', 'Evidence: first published revision (the date it is updated to)',
                f'Source: {law["url"]}', f'Consolidated: {v["url"]}']
    return author_of(b['key'], b['laws']), msg, trailers


def change_message(b: dict, c: dict):
    ch, g, keys = c['ch'], c['g'], c['keys']
    short = b['act']['short']
    labels = labels_of(b, ch, keys)
    affecting = ', '.join(f'{short} {l}' for l in labels)
    kind_ = g[1]
    day = g[0]
    trailers = []
    if kind_ in ('law', 'candidates'):
        lks = g[2].split('|')
        notes = sorted({r['note'] for k in keys for r in ch['info'][k]['notes']})
        if kind_ == 'law':
            law = b['laws'][lks[0]]
            author = author_of(lks[0], b['laws'])
            msg = [subject(short, labels, law['name']), '', law['name'] + f' ({law["label"]})', ''] + listing(ch, keys) + ['']
        else:
            author = PUBLISHER
            msg = [subject(short, labels, 'two laws, credited to neither'), '']
            msg += wrap('The annotations to these provisions name more than one law that changed them between the '
                        f'revisions updated to {ch["lo"]} and {ch["hi"]}, and the revisions do not show the text between '
                        'them, so the change is credited to neither.') + [''] + listing(ch, keys) + ['']
        msg += ['The annotations:', '']
        msg += [f'> {n}' for n in notes] + ['']
        if g[3]:
            msg += wrap(f'The annotation gives {g[3]} as the day this took effect, but the revision updated to {ch["lo"]} '
                        'does not contain it: the Commission consolidated it later. The record dates it the day after '
                        'that revision, so that every revision reads back from the history as published.') + ['']
            trailers.append(f'Stated-in-force: {g[3]}')
        later = sorted({r['later'] for k in keys for r in ch['info'][k]['notes'] if r.get('later')})
        if later:
            msg += wrap(f'The revision updated to {ch["hi"]} prints this text without attaching an annotation to it; '
                        f'the annotation quoted above is attached to it in the revision updated to {", ".join(later)}.') + ['']
            trailers.append('Evidence: annotation first printed in the later revision updated to ' + ', '.join(later))
        derived = sorted({r['key'] for k in keys for r in ch['info'][k]['notes'] if r.get('day_from')})
        trailers.append('Evidence: annotation (date and law) in the revision updated to ' + ch['hi'])
        if derived:
            trailers.append('Evidence: the day for ' + ', '.join(law_label(x) for x in derived) +
                            ' is from other annotations of the same instrument (this one gives none)')
        trailers += [f'In-force: {day}', f'Affecting: {affecting}']
        if kind_ == 'law':
            trailers += [f'Kind: {"Act" if lks[0].startswith("act/") else "Statutory instrument"}', f'Source: {b["laws"][lks[0]]["url"]}']
        else:
            trailers += [f'Candidate: {b["laws"][x]["name"]} ({b["laws"][x]["label"]})' for x in lks]
    elif kind_ == 'early':
        author = PUBLISHER
        lks = g[2].split('|')
        stated = max(ch['info'][k]['stated'] for k in keys)
        msg = [subject(short, labels, 'printed before its stated day'), '']
        msg += wrap(f'The revision updated to {ch["hi"]} prints this change, but its annotation gives {stated}, after the '
                    'day the revision is updated to. It is recorded on the revision\'s day as the publisher\'s text and '
                    'credited to no law.') + [''] + listing(ch, keys) + ['']
        trailers += [f'In-force: {day}', f'Affecting: {affecting}', f'Stated-in-force: {stated}']
        trailers += [f'Candidate: {b["laws"][x]["name"]} ({b["laws"][x]["label"]})' for x in lks]
    elif kind_ == 'unexplained':
        author = PUBLISHER
        msg = [subject(short, labels, 'change no annotation explains'), '']
        msg += wrap(f'The text changed between the revisions updated to {ch["lo"]} and {ch["hi"]}, but no new annotation '
                    'of these provisions names a law that changed it, so the change is credited to no law.') + [''] + listing(ch, keys) + ['']
        trailers += [f'In-force: {day}', f'Affecting: {affecting}', 'Kind: editorial (unexplained)']
    else:
        author = PUBLISHER
        msg = [subject(short, labels, 'layout of the revision'), '']
        msg += wrap(f'The revision updated to {ch["hi"]} sets the same words differently from the one updated to '
                    f'{ch["lo"]} (paragraph breaks, headings, quotation marks or the order a table is read in). No word of '
                    'the law changed, and no law is credited.') + [''] + listing(ch, keys) + ['']
        trailers += [f'In-force: {day}', f'Affecting: {affecting}', 'Kind: editorial (layout)']
    trailers.append(f'Consolidated: {ch["cur"]["url"]}')
    return author, msg, trailers


def ident(who: tuple[str, str], when: str) -> bytes:
    stamp, off = when[1:].split()
    return f'{who[0]} <{who[1]}> {stamp} {off}'.encode('utf-8')


def write_repo(repo: Path, built: list[dict], docs: Path, today: str) -> tuple[list[dict], dict]:
    import os
    import shutil
    import tempfile
    remote = None
    if (repo / '.git').exists():
        out = subprocess.run(['git', 'remote', 'get-url', 'origin'], cwd=repo, capture_output=True, text=True)
        remote = out.stdout.strip() or None

    def force(fn, path, _exc):
        os.chmod(path, 0o700)
        fn(path)
    if repo.exists():
        for p in repo.iterdir():
            shutil.rmtree(p, onexc=force) if p.is_dir() else p.unlink()
    repo.mkdir(parents=True, exist_ok=True)
    git(repo, 'init', '-q', '-b', 'main')
    git(repo, 'config', 'core.autocrlf', 'false')
    if remote:
        git(repo, 'remote', 'add', 'origin', remote)
    tags: dict[str, int] = {}
    law_days: dict[str, list[tuple[str, int]]] = {}
    log = []
    tmp = tempfile.NamedTemporaryFile('wb', suffix='.fi', delete=False)
    out = tmp

    def data(b: bytes):
        out.write(b'data %d\n' % len(b))
        out.write(b)
        out.write(b'\n')
    mark = 0
    for c in plan_commits(built):
        day, c = c[0], c[4]
        assert day <= today, (day, today)
        ops: list[tuple[str, str, dict | None]] = []
        if c['kind'] == 'start':
            b = c['b']
            slug = b['act']['slug']
            for key, u in sorted(b['versions'][0]['units'].items()):
                ops.append((slug, key, u))
            author, msg, trailers = start_message(b)
            entries = [(slug, list(b['versions'][0]['units']))]
            law = b['key']
        else:
            if c['kind'] == 'law':
                author, msg, trailers = law_message(c)
                parts = c['parts']
                law = c['g'][2]
            else:
                author, msg, trailers = change_message(c['b'], c)
                parts = [c]
                law = None
            entries = []
            for p in parts:
                slug = p['b']['act']['slug']
                for k in p['keys']:
                    ops.append((slug, k, p['ch']['cur']['units'].get(k)))
                entries.append((slug, p['keys']))
        mark += 1
        when = commit_date(day)
        out.write(b'commit refs/heads/main\nmark :%d\n' % mark)
        out.write(b'author ' + ident(author, when) + b'\n')
        out.write(b'committer ' + ident(COMMITTER, when) + b'\n')
        data(('\n'.join(msg).rstrip('\n') + '\n\n' + '\n'.join(trailers) + '\n').encode('utf-8'))
        for slug, key, u in ops:
            path = f'{slug}/{file_name(key)}'.encode('utf-8')
            if u is None:
                out.write(b'D ' + path + b'\n')
            else:
                out.write(b'M 100644 inline ' + path + b'\n')
                data(u['text'].encode('utf-8'))
        out.write(b'\n')
        for slug, keys in entries:
            tags[f'{slug}/{day}'] = mark
            log.append({'day': day, 'slug': slug, 'kind': c['kind'], 'law': law, 'author': author[0], 'units': len(keys),
                        'keys': keys, 'stated': c['g'][3] if c['kind'] in ('law', 'candidates') else ''})
        if law:
            ds = law_days.setdefault(law, [])
            if ds and ds[-1][0] == day:
                ds[-1] = (day, mark)
            else:
                ds.append((day, mark))
    for law, ds in sorted(law_days.items()):
        if len(ds) == 1:
            tags[tag_of(law)] = ds[0][1]
        else:
            for day, m in ds:
                tags[f'{tag_of(law)}/{day}'] = m
    for name, m in sorted(tags.items()):
        out.write(f'reset refs/tags/{name}\nfrom :{m}\n\n'.encode('utf-8'))
    out.write(b'done\n')
    tmp.close()
    marks = Path(tmp.name + '.marks')
    with open(tmp.name, 'rb') as fh:
        res = subprocess.run(['git', 'fast-import', '--quiet', '--done', f'--export-marks={marks}'], cwd=repo, stdin=fh,
                             capture_output=True)
    if res.returncode:
        raise SystemExit('fast-import: ' + res.stderr.decode('utf-8', 'replace'))
    os.unlink(tmp.name)
    sha = dict(l.split(' ') for l in marks.read_text().split('\n') if l)
    marks.unlink()
    tags_sha = {name: sha[f':{m}'] for name, m in tags.items()}
    stage = Path(tempfile.mkdtemp(prefix='doc', dir=repo.parent))   # the documentation files, apart from the law
    for p in sorted(docs.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:
            dest = stage / p.relative_to(docs)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(p.read_bytes())
    (stage / 'tools').mkdir(parents=True, exist_ok=True)
    for name in ('build.py', 'reproduce.py', 'check_repo.py', 'test_repo.py'):
        (stage / 'tools' / name).write_bytes((HERE / name).read_bytes())
    for b in built:
        (stage / b['act']['slug']).mkdir(parents=True, exist_ok=True)
    write_tables(stage, built, log)
    from reproduce import write_manifest, write_reproduce
    write_manifest(stage, built, today)
    write_reproduce(stage, built, log, tags_sha, REQUESTS, today, LEFT_OUT)
    gate_published(stage, {b['act']['slug'] for b in built})
    when = commit_date(today)
    msg = f'Documentation, tables, tools and REPRODUCE.md\n\nNo law text changes.\n\nIn-force: {today}\nKind: documentation\n'
    with open(tmp.name, 'wb') as out:
        out.write(b'commit refs/heads/main\n')
        out.write(b'author ' + ident(COMMITTER, when) + b'\n')
        out.write(b'committer ' + ident(COMMITTER, when) + b'\n')
        data(msg.encode('utf-8'))
        out.write(b'from refs/heads/main^0\n')
        for f in sorted(stage.rglob('*')):
            if f.is_file():
                out.write(b'M 100644 inline ' + f.relative_to(stage).as_posix().encode('utf-8') + b'\n')
                data(f.read_bytes())
        out.write(b'\ndone\n')
    with open(tmp.name, 'rb') as fh:
        res = subprocess.run(['git', 'fast-import', '--quiet', '--done'], cwd=repo, stdin=fh, capture_output=True)
    if res.returncode:
        raise SystemExit('fast-import: ' + res.stderr.decode('utf-8', 'replace'))
    os.unlink(tmp.name)
    shutil.rmtree(stage, onexc=force)
    if CHECKOUT[0]:
        git(repo, 'reset', '-q', '--hard', 'main')     # a working tree for the checks that read files
    return log, tags_sha


def gate_published(repo: Path, law_dirs: set[str]):
    """The last step before the documentation commit: every file outside the act folders (the docs, tables, data and
    tools) goes through Lexifina's publish gate, which scrubs this machine's home path and refuses the build if a file
    that must stay private would be published. Law text is never passed to it."""
    import os
    import sys
    sys.path.append(str(HERE.parent / 'gitlaw_common'))
    try:
        from publish_gate import publish_gate
    except ImportError:          # an outside reader rebuilding from the published tools: no private rule to apply
        if os.environ.get('GITLAW_PUBLIC_REBUILD') != '1':
            raise SystemExit('publish gate missing: run from lexifina/scripts, or set GITLAW_PUBLIC_REBUILD=1')

        def publish_gate(files):
            return files
    paths = [f for f in repo.rglob('*') if f.is_file() and '.git' not in f.relative_to(repo).parts
             and f.relative_to(repo).parts[0] not in law_dirs]
    files = {f.relative_to(repo).as_posix(): f.read_bytes() for f in paths}
    for name, data in publish_gate(files).items():
        if data != files[name]:
            (repo / name).write_bytes(data)


def write_tables(repo: Path, built: list[dict], log: list[dict]):
    import csv
    import io
    rows = []
    for b in built:
        for e in log:
            if e['slug'] == b['act']['slug'] and e['law']:
                law = b['laws'][e['law']]
                rows.append({'act': b['act']['short'], 'in_force': e['day'], 'stated_in_force': e['stated'] or e['day'],
                             'law': law['name'], 'number': law['label'], 'provisions': e['units'],
                             'note': 'the act as first revised' if e['kind'] == 'start' else '', 'source': law['url']})
    rows.sort(key=lambda r: (r['in_force'], r['act'], r['number']))
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0]), lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    (repo / 'amendments.csv').write_text(buf.getvalue(), encoding='utf-8', newline='\n')
    for b in built:
        last = b['versions'][-1]
        counts: dict[str, int] = {}
        lastday: dict[str, str] = {}
        for e in log:
            if e['slug'] == b['act']['slug'] and e['kind'] not in ('start', 'layout'):
                for k in e['keys']:
                    counts[k] = counts.get(k, 0) + 1
                    lastday[k] = e['day']
        out = [f'# {b["title"]}', '', f'{b["laws"][b["key"]]["label"]} \u00b7 <{b["laws"][b["key"]]["url"]}>', '',
               f'{len(b["versions"])} revisions by the Law Reform Commission, updated to {b["versions"][0]["updated_to"]} '
               f'(the first) to {last["updated_to"]} (the latest).', '',
               '| Provision | File | Changes | Last changed |', '| --- | --- | ---: | --- |']
        for k in ordered(last['units']):
            out.append(f'| {last["units"][k]["label"]} | [{file_name(k)}]({file_name(k)}) | {counts.get(k, 0)} | {lastday.get(k, "")} |')
        (repo / b['act']['slug'] / 'README.md').write_text('\n'.join(out) + '\n', encoding='utf-8', newline='\n')


# ---------------------------------------------------------------- main

LEFT_OUT: list[dict] = []
CHECKOUT = [True]    # check out the built repository (a rebuild made only to compare hashes needs none)


def _build_one(act: dict, offline: bool = True):
    """build_act for one act, or why it failed (run in a pool)."""
    try:
        return build_act(act, offline)
    except Exception as exc:
        return f'{type(exc).__name__}: {exc}'[:200]


def left_out_acts() -> dict[str, str]:
    """Acts left out on purpose (left_out.json next to this script): an act whose revisions the reader cannot read
    back exactly, with the reason. The list is part of the build's input, so a rebuild leaves out the same acts."""
    import json
    p = HERE / 'left_out.json'
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}


def _parse_one(url: str) -> str:
    try:
        parse_to_cache(url, True)
        return ''
    except BaseException as exc:      # noqa: BLE001 (MemoryError too: the act is left out, the build goes on)
        err = f'{type(exc).__name__}: {exc}'[:200]
        sha = hashlib.sha256(fetch(url, True)).hexdigest()
        parsed_path(sha).with_suffix('.err').write_text(err, encoding='utf-8', newline='\n')
        return err


def preparse(acts: list[dict], offline: bool):
    """Reads every revision PDF not yet read (PyMuPDF takes seconds per PDF) in a pool of 4 processes."""
    from multiprocessing.pool import ThreadPool
    todo = []
    for a in acts:
        for v in history(a, offline):
            raw = fetch(v['url'], offline, b'%PDF')
            pp = parsed_path(hashlib.sha256(raw).hexdigest())
            if not pp.exists() and not pp.with_suffix('.err').exists() and v['url'] not in todo:
                todo.append(v['url'])
    if not todo:
        return
    print(f'reading {len(todo)} PDFs', flush=True)
    # Four reader processes at a time, each a fresh interpreter reading a few PDFs (a process pool here broke as a
    # whole when one worker died); a batch whose process fails is read again one PDF at a time, twice, and only a
    # PDF whose reader process fails both times is recorded as unreadable.
    import sys

    def run(chunk: list[str], tries: int = 2) -> list[tuple[str, str]]:
        r = subprocess.run([sys.executable, '-X', 'utf8', str(HERE / 'build.py'), '--parse-urls', *chunk],
                           capture_output=True, text=True, encoding='utf-8', errors='replace', stdin=subprocess.DEVNULL)
        if r.returncode == 0:
            return [(u, e) for u, e in (l.split('\t', 1) for l in r.stdout.splitlines() if '\t' in l) if e]
        if len(chunk) > 1:
            return [x for u in chunk for x in run([u])]
        if tries > 1:
            return run(chunk, tries - 1)
        err = f'reader process failed (exit {r.returncode}): {r.stderr.strip()[-150:]}'
        sha = hashlib.sha256(fetch(chunk[0], True)).hexdigest()
        parsed_path(sha).with_suffix('.err').write_text(err, encoding='utf-8', newline='\n')
        return [(chunk[0], err)]
    chunks = [todo[i:i + 4] for i in range(0, len(todo), 4)]
    with ThreadPool(4) as pool:
        for res in pool.imap(run, chunks):
            for url, err in res:
                print('  unreadable:', url, err, flush=True)


def data_day() -> str:
    """The day the source PDFs were retrieved (the newest of them in the cache), so the documentation commit made by a
    rebuild on any later day carries the same date."""
    files = [p for p in CACHE.iterdir() if p.name != '.gitignore' and not p.name.startswith('parsed')] if CACHE.exists() else []
    if not files:
        return dt.date.today().isoformat()
    return dt.date.fromtimestamp(max(p.stat().st_mtime for p in files)).isoformat()


def main():
    import argparse
    import json
    import os
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default=str(ROOT.parent / 'ireland-law'))
    ap.add_argument('--offline', action='store_true', help='read only the cache; fail on anything not cached')
    ap.add_argument('--today', default=None, help='the build day (default: the day the cached data was retrieved)')
    ap.add_argument('--verify-rebuild', action='store_true',
                    help='build again into a temporary folder from the cache, compare every hash with --repo, and record the result')
    ap.add_argument('--no-checkout', action='store_true', help='leave the built repository without a working tree')
    ap.add_argument('--parse-urls', nargs='+', help=argparse.SUPPRESS)   # a reader process started by preparse()
    args = ap.parse_args()
    if args.parse_urls:
        for url in args.parse_urls:
            print(f'{url}\t{_parse_one(url)}', flush=True)
        return
    if args.verify_rebuild:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out = subprocess.run([os.sys.executable, '-X', 'utf8', str(HERE / 'build.py'), '--offline', '--no-checkout',
                                  '--repo', tmp]
                                 + (['--today', args.today] if args.today else []), capture_output=True, text=True)
            if out.returncode:
                raise SystemExit(out.stderr)

            def hashes(r):
                log = git(Path(r), 'log', '--format=%H', 'main').split()
                tags = dict(l.split(' ', 1)[::-1] for l in git(Path(r), 'show-ref', '--tags').split('\n') if l)
                return log, tags
            a, b = hashes(args.repo), hashes(tmp)
            same_history = a[0][1:] == b[0][1:]
            rec = {'identical': same_history and a[1] == b[1], 'history_tip': a[0][1], 'commits': len(a[0]) - 1,
                   'tags': len(a[1]), 'main_identical': a[0][0] == b[0][0], 'main': a[0][0], 'rebuilt_main': b[0][0]}
            print(json.dumps(rec, indent=1))
            p = HERE / 'verification.json'
            ver = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
            ver['rebuild'] = {k: rec[k] for k in ('identical', 'history_tip', 'commits', 'tags')}
            p.write_text(json.dumps(ver, indent=1, sort_keys=True) + '\n', encoding='utf-8', newline='\n')
            for f in Path(tmp).rglob('*'):
                os.chmod(f, 0o700)
            raise SystemExit(0 if rec['identical'] else 1)
    CHECKOUT[0] = not args.no_checkout
    ACTS[:] = acts_from_alpha(args.offline)
    preparse(ACTS, args.offline)
    left_out = left_out_acts()
    built, failed = [], []
    todo = [a for a in ACTS if a['eli'] not in left_out]
    if args.offline:
        import multiprocessing
        with multiprocessing.get_context('spawn').Pool(4) as pool:   # four processes: the act readings are cached
            results = pool.map(_build_one, todo, chunksize=4)
    else:
        results = [_build_one(a, False) for a in todo]
    done = {a['eli']: r for a, r in zip(todo, results)}
    for a in ACTS:
        if a['eli'] in left_out:
            failed.append({'eli': a['eli'], 'title': a['short'], 'why': left_out[a['eli']]})
        elif isinstance(done[a['eli']], str):
            failed.append({'eli': a['eli'], 'title': a['short'], 'why': done[a['eli']]})
        else:
            built.append(done[a['eli']])
    LEFT_OUT[:] = failed
    print(f'{len(built)} acts built, {len(failed)} left out')
    today = args.today or data_day()
    for b in built:
        n = sum(len(ks) for ch in b['changes'] for ks in ch['groups'].values())
        print(f'{b["act"]["slug"]}: {len(b["versions"])} versions {b["versions"][0]["updated_to"]}..'
              f'{b["versions"][-1]["updated_to"]}, {len(b["versions"][-1]["units"])} units, {n} unit changes, '
              f'{len(b["problems"])} not credited to one law')
        for p in b['problems']:
            print('   ', p)
    log, tags = write_repo(Path(args.repo), built, HERE / 'repo', today)
    print(f'repo: {len(log)} commits + 1 documentation commit, {len(tags)} tags -> {args.repo}')


if __name__ == '__main__':
    main()
