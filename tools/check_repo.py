"""Checks the git repository against the official text: every revision of every act, read back from git with
tools/on_date.py on the day it is updated to, must equal that revision.

    python -X utf8 scripts/ireland-law/check_repo.py [--repo ../ireland-law] [--no-record]

Two checks per revision, from the cached PDFs (no network):
1. File by file: the act's files in git on that day are exactly the files the builder makes from that revision's PDF
   (same set of files, same bytes).
2. Word for word: the whole act printed by on_date.py has the same text in the same order as the body of the PDF, read
   independently of the builder: PyMuPDF's own span text (not the builder's character-gap reading), lines in page
   order, none of the builder's paragraph, heading, title or layout rules. The two are compared character by character
   with white space removed (some PDFs hold no space glyphs, so the span text runs words together). Left out on both
   sides, because the two sides set them differently: section headings (in the PDF the marginal or bold heading, or a
   plain line directly above the section number; in the repository the table of contents' title), part and chapter
   headings and chapter titles (12pt and larger, or italic after the heading, in the PDF; '## ' lines in the
   repository), annotation marks and brackets, footnote reference numbers, hyphens. Schedules (tables, whose cells the
   PDF holds in no reading order) are compared as the multiset of their letters and digits; they start at a schedule
   heading ('SCHEDULE 2', 'FIRST SCHEDULE') after the act's last section (one before it is quoted) and, in the
   repository, in the act's schedule files. Also left out: the annotations under each provision (8-8.9pt, from their
   heading or first note to the next line of text, with any heading they quote in a larger size), and the margin notes
   beside a schedule's rules (where the sections' marginal headings stand). Small print outside the annotations (a
   table set in 8pt) is text, and so are the cells of a table set out in a section, wherever they stand.
The result is written to verification.json next to this script (unless --no-record), for REPRODUCE.md.
"""
import argparse
import collections
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402

TOKEN = re.compile(r'\w+')   # for counting words


def tokens(text: str) -> list[str]:
    """The text as its characters in order, without white space: some revisions' PDFs hold no space glyphs, so
    PyMuPDF's span text runs words together ('hasthemeaning'), and where a space falls cannot be compared."""
    text = re.sub(r'F\d+\[', ' ', text)
    text = text.replace('[', ' ').replace(']', ' ').replace('-', '').replace('\u00ad', '')
    text = text.translate({0x201c: '"', 0x201d: '"', 0x2018: "'", 0x2019: "'"})
    return list(re.sub(r'\s', '', text))


# the cover lines repeated at the top of a revision's last pages
COVER = re.compile(r'(Number \d+ of \d{4}|Updated to .*|.*\bREVISED( Updated to .*)?|[A-Z ()]+ ACT \d{4})')


def letters(text: str) -> list[str]:
    """A schedule's letters and digits: its table cells are held in no reading order, and words broken over lines
    inside a cell are joined to the next cell's words, so only what it contains is compared, not the order."""
    text = re.sub(r'F\d+\[', ' ', text)
    return sorted(re.sub(r'\W|_', '', text))


def dict_lines(raw: bytes) -> list[dict]:
    """The PDF's lines as PyMuPDF's get_text('dict') gives them (cached by the PDF's sha256: reading is the slow part)."""
    import gzip
    import hashlib
    path = build.CACHE / f'olines1-{hashlib.sha256(raw).hexdigest()[:24]}.json.gz'
    if path.exists():
        return json.loads(gzip.decompress(path.read_bytes()).decode('utf-8'))
    lines = _dict_lines(raw)
    tmp = path.with_suffix('.tmp')
    tmp.write_bytes(gzip.compress(json.dumps(lines, ensure_ascii=False, separators=(',', ':')).encode('utf-8'), 6, mtime=0))
    tmp.replace(path)
    return lines


def _dict_lines(raw: bytes) -> list[dict]:
    import pymupdf
    doc = pymupdf.open(stream=raw, filetype='pdf')
    lines = []
    for pn, page in enumerate(doc):
        pl = []
        for b in page.get_text('dict')['blocks']:
            for l in b.get('lines', []):
                spans = [s for s in l['spans'] if not (s['size'] < 7.0 and s['text'].strip().isdigit())]
                if not spans or not ''.join(s['text'] for s in spans).strip():
                    continue
                size = max(s['size'] for s in spans)
                y = max(spans, key=lambda s: s['size'])['origin'][1]
                pl.append({'page': pn, 'x': l['bbox'][0], 'y': y, 'size': size, 'text': ''.join(s['text'] for s in spans),
                           'first_bold': 'Bold' in spans[0]['font'],
                           'italic': all('Italic' in s['font'] for s in spans if s['text'].strip()),
                           'bold': all('Bold' in s['font'] for s in spans if re.search(r'[^\W\d_]', s['text'])
                                       and not re.fullmatch(r'\s*F\d+\s*', s['text']))})
        pl.sort(key=lambda l: (l['y'], l['x']))
        lines += [l for l in pl if 72 <= l['y'] <= 800 and l['size'] >= 9.0]
    return lines


NOTE_ID = re.compile(r'[FCEM]\d+')
NOTE_HEADS = ('Annotations', 'Amendments', 'Editorial Notes', 'Modifications (not altering text)')


def note_start(l: dict) -> bool:
    """A line that starts annotations: their heading, or a note's number ('F12'), in bold."""
    first = l['spans'][0]
    return 'Bold' in first['font'] and (NOTE_ID.fullmatch(first['text'].strip()) is not None
                                        or l['text'].strip().rstrip(':') in NOTE_HEADS)


def small_print(raw: bytes) -> tuple[set[tuple[int, int]], list[dict]]:
    """The 8-8.9pt print, which dict_lines() leaves out with the footnotes (read here from build.page_lines(), the
    builder's own reading of the lines; only which lines are text is decided here): the annotations under a provision
    run from their heading ('Annotations', 'Amendments:') or first note ('F12', in bold) to the next line of text, and
    are not text, nor are lines in a larger size set inside one with the annotation going on below them (a heading it
    quotes: 'SCHEDULE 12' / 'PART 2'): their (page, y) is the first result. Small print outside them (a table set in
    8pt) is text: those lines are the second, in the form dict_lines() gives."""
    quoted, extra = set(), []
    block = False       # an annotation runs on over a page break
    ls = [{**l, 'page': pn} for pn, page in enumerate(build.page_lines(raw)) for l in page if 72 <= l['y'] <= 800]
    i = 0
    while i < len(ls):
        l = ls[i]
        if l['size'] < 8.0:     # footnote print: no text (and inside an annotation, part of it)
            i += 1
            continue
        small = 8.0 <= l['size'] <= 8.9
        if small and note_start(l):
            block = True
        elif small and not block and not build.FOOTNOTE.match(l['text']):
            spans = [s for s in l['spans'] if s['text']]
            extra.append({'page': l['page'], 'x': l['x'], 'y': l['y'], 'size': l['size'], 'text': l['text'],
                          'first_bold': 'Bold' in spans[0]['font'],
                          'italic': all('Italic' in s['font'] for s in spans if s['text'].strip()),
                          'bold': all('Bold' in s['font'] for s in spans if re.search(r'[^\W\d_]', s['text'])
                                      and not re.fullmatch(r'\s*F\d+\s*', s['text']))})
        elif not small and block and l['size'] not in (9.0, 10.0):
            k = i
            while k < len(ls) and 8.9 < ls[k]['size'] and ls[k]['size'] not in (9.0, 10.0) and k - i < 6:
                k += 1
            if k < len(ls) and (ls[k]['size'] < 8.0 or ls[k]['size'] <= 8.9 and not note_start(ls[k])):
                quoted.update((m['page'], round(m['y'])) for m in ls[i:k])
                i = k
                continue
            block = False
        elif not small:
            block = False
        i += 1
    return quoted, extra


def official(raw: bytes) -> tuple[list[str], list[str]]:
    """The words of the PDF's sections (in order) and of its schedules (as a multiset), read with get_text('dict')."""
    quoted, extra = small_print(raw)
    lines = [l for l in dict_lines(raw) if not any((l['page'], round(l['y']) + d) in quoted for d in (-1, 0, 1))
             and not (l['size'] <= 9.0 and build.FOOTNOTE.match(l['text']))]   # Official Journal footnotes
    if extra:
        lines = sorted(lines + extra, key=lambda l: (l['page'], l['y'], l['x']))
    ref = sorted(l['x'] for l in lines if round(l['size'], 1) == 10.0 and re.match(r'\(\d+\) ', l['text']))
    ref_x = ref[len(ref) // 2] if ref else 179
    # the text column is also where the bold section numbers stand (quoted '(1)' lines can outnumber the act's own)
    sec = sorted(l['x'] for l in lines if round(l['size'], 1) == 10.0 and l['first_bold']
                 and re.match(r'(F\d+\[)?\d+[A-Z]{0,3}\.', l['text'].strip()))
    if sec:
        ref_x = min(ref_x, sec[len(sec) // 2])
    start = build.text_start(lines)[1]
    # the margin column: where the 9pt marginal headings mostly stand; anything further left is text (a wide table)
    margin_cols = build.margin_columns(lines, ref_x)
    in_col = lambda l: not margin_cols or any(-8 <= l['x'] - c <= 12 for c in margin_cols)
    # the act's last section: a bold section number in the text column, continuing the numbering; a schedule heading
    # before it is quoted (a schedule inserted into another Act), and the act's own schedules come after it
    # (a numbered paragraph of a schedule can carry on the numbering: a section must be in the act's contents too)
    toc = build.contents_titles(lines[:start])
    last_sec, top = start, 0
    for n, l in enumerate(lines[start:], start):
        if l['text'].strip().startswith('About this Revised Act'):
            break
        m = re.match(r'(?:F\d+\[)?((\d+)[A-Z]{0,3})\.(?: |—|\()', l['text'].strip())
        # (a section line opening with an annotation mark, 'F12[9.—', whose number the dict reading does not show as
        # bold, counts when the contents list it)
        if m and (l['first_bold'] or (toc and l['text'].lstrip().startswith('F'))) and round(l['size'], 1) == 10.0 \
                and ref_x - 15 <= l['x'] <= ref_x + 30 and top < int(m.group(2)) <= top + 3 \
                and (not toc or m.group(1) in toc):
            top, last_sec = int(m.group(2)), n
    # where the marginal headings of the sections stand
    mx = collections.Counter(round(l['x']) for l in lines[start:last_sec + 1]
                             if round(l['size'], 1) == 9.0 and l['x'] < ref_x - 40)
    margin_xs = list(mx)
    body, sched = [], []
    sched_meta = []      # (page, size) of each schedule line, for the title above the end matter
    in_sched = after_head = bold_head = plain_head = margin_ref = table = False
    for n, l in enumerate(lines[start:], start):
        t = l['text'].strip()
        if t.startswith('About this Revised Act') or (t == 'Introduction' and n + 1 < len(lines)
                                                       and lines[n + 1]['text'].strip().startswith('This Revised Act presents')):
            # the act's title in capitals above the end matter is not law (a capitals title inside a schedule is)
            last = sched if in_sched else body
            meta = sched_meta if in_sched else None
            text_of = (lambda x: x) if in_sched else (lambda x: x[0])
            if len(last) > 1 and re.fullmatch(r'\d{4}', text_of(last[-1])) \
                    and re.fullmatch(build.TITLE_CAPS, text_of(last[-2])) and text_of(last[-2]).endswith(('ACT', 'ACTS')):
                year = text_of(last.pop())      # the title's year on a line of its own
                if meta is not None:
                    meta.pop()
                if in_sched:
                    last[-1] = last[-1] + ' ' + year
                else:
                    last[-1] = [last[-1][0] + ' ' + year] + last[-1][1:]
            where_of = (lambda: meta[-1]) if in_sched else (lambda: tuple(last[-1][2:4]))
            if last and re.fullmatch(build.TITLE_END, text_of(last[-1])):
                where = where_of()
                last.pop()
                if meta is not None:
                    meta.pop()
                for _ in range(2):      # a title over two or three lines, on the same page in the same size
                    if last and re.fullmatch(build.TITLE_CAPS, text_of(last[-1])) and where_of() == where:
                        last.pop()
                        if meta is not None:
                            meta.pop()
            break
        if re.fullmatch(r'(?:SCHEDULE( (?:\d+[A-Z]*|[A-Z]{1,2}))?\.?|' + build.ORDINAL_SCHEDULE + ')',
                        re.sub(r'F\d+\[|\]', '', t)) \
                and (l['size'] >= 11 or not in_sched) and n > last_sec:
            in_sched = True
        if in_sched:
            ref = r'\d+[A-Z]*(?:\([0-9a-zA-Z]+\))*'
            if l['x'] < ref_x - 40 and 9.0 <= round(l['size'], 1) <= 10.0 and len(t) < 50 and (re.fullmatch(
                    rf'(Sections?|Sects?\.|Articles?|Regulations?|Rules?|Parts?)(?: {ref}(?:(?:, | and | to |, and |-){ref})*(?:,| and| to)? ?\.?)?', t)
                    or (margin_ref and margin_ref[0] == l['page'] and 0 < l['y'] - margin_ref[1] < 16
                        and re.fullmatch(rf'(?:and |to )?{ref}(?:(?:, | and | to |-){ref})*(?:,| and| to)? ?\.?', t))):
                margin_ref = (l['page'], l['y'])    # a body line beside it can come between its lines
                continue    # the margin note beside a schedule's heading naming the section(s) it belongs to
            if in_col(l) and l['x'] < ref_x - 40:
                margin_ref = False
                if 9.0 <= round(l['size'], 1) <= 10.0 and any(-3 < l['x'] - x < 20 for x in margin_xs):
                    continue    # a marginal note beside a schedule's rule or paragraph (old Acts), set like the body's
            if not re.fullmatch(r'Number \d+ of \d{4}|Updated to .*|.*\bREVISED( Updated to .*)?', t):
                sched.append(t)
                sched_meta.append((l['page'], round(l['size'], 1)))
            continue
        # Headings are not left out but marked: the comparison may pass over a marked line on either side (a heading
        # one side sets and the other does not), never over a word of the text.
        if t == 'TABLE':
            table = True        # a table set out in a section: its cells can stand in the margin column
        elif l['first_bold'] and re.match(r'(F\d+\[)?\d+[A-Z]{0,3}\.', t):
            table = False
        if (in_col(l) or build.REF_NOTE.fullmatch(t)) and l['x'] < ref_x - 40 and 9.0 <= round(l['size'], 1) <= 10.0 \
                and n != start \
                and not (table and not build.REF_NOTE.fullmatch(t)) and not build.SIGNED.match(t):
            body.append([t, True, l['page'], round(l['size'], 1)])
            continue        # a marginal heading (not the long title's first line, which can hang into the margin)
        if re.fullmatch(r'Number \d+ of \d{4}|Updated to .*|.*\bREVISED( Updated to .*)?', t):
            continue        # the cover lines (the builder drops them wherever they stand)
        bare = re.sub(r'F\d+\[', '', t)
        if l['bold'] and l['size'] >= 9.0 and (re.search(r'[^\W\d_]', bare) or bold_head) and not re.match(
                r'(F\d+\[)?\d+[A-Z]{0,3}\.|be it enacted', t, re.I):
            bold_head = True
            body.append([t, True, l['page'], round(l['size'], 1)])
            continue        # a section heading set above the section (in later layouts), with its last line ('2000')
        bold_head = False
        if l['size'] >= 11 or (l['italic'] and l['size'] >= 9.0 and re.search(r'[^\W\d_]', t) and len(t) < 200 and (
                after_head or l['x'] > ref_x + 40 or l['x'] < ref_x - 10)):
            after_head = True
            body.append([t, True, l['page'], round(l['size'], 1)])
            continue        # a part or chapter heading, or a chapter's title (italic, after its heading)
        after_head = False
        if re.match(r'(F\d+\[)?\d+[A-Z]{0,3}\.(?: |\u2014)', t) and body and plain_head \
                and re.match('[A-Z]', body[-1][0]) and len(body[-1][0]) < 120 \
                and not (len(body) > 1 and re.match('["\u201c]?(PART|CHAPTER) ', body[-2][0])) \
                and not re.search('[.;:,\u2014][\\]\u201d\u2019"]*$', body[-1][0]):
            body[-1][1] = True      # a section heading in plain type on the line above the section (in some layouts)
        plain_head = not re.match(r'(F\d+\[)?\d+[A-Z]{0,3}\.(?: |\u2014)', t)
        if body and not body[-1][1] and re.search(r'\w-$', body[-1][0]) and t[:1].islower():
            body[-1][0] = body[-1][0][:-1] + t
        else:
            body.append([t, False, l['page'], round(l['size'], 1)])
    return marked(body), letters(' '.join(sched))


def marked(entries: list) -> list[tuple[str, bool, int]]:
    # (character, is it in a heading line, which line) for every character of the text, white space removed
    return [(c, bool(f), n) for n, (t, f, *_) in enumerate(entries) for c in tokens(t)]


def agree(o: list, r: list) -> tuple[bool, int, int]:
    """The text proper the same, with every heading line left out on both sides; or, failing that, the same with some
    heading lines passed over (align)."""
    if [x[0] for x in o if not x[1]] == [x[0] for x in r if not x[1]]:
        return True, len(o), len(r)
    return align(o, r)


DEPTH = 14   # passes over heading lines the look-ahead may make (a run of repealed sections between split headings)


def align(o: list, r: list, look: int = 40) -> tuple[bool, int, int]:
    # Walks the two texts character by character. Where they differ, a heading line (marked) on either side, or one on
    # each, may be passed over -- one just passed through (a marginal heading 'material from' read as the text's
    # 'material from') or the one at the point of difference, whichever makes the next characters agree -- and
    # nothing else: every character of the text proper must be matched in order. Returns (agree, where the official
    # text stops agreeing, where the repository's does).
    import bisect

    def spans(m):
        out = {}
        for k, (_, f, n) in enumerate(m):
            if f:
                a = out.get(n)
                out[n] = (a[0] if a else k, k + 1)
        return sorted(out.values())
    uo, ur = spans(o), spans(r)
    so, sr = [a for a, _ in uo], [a for a, _ in ur]
    # the look-ahead compares the text proper only: a marginal heading's next line can fall inside it
    po = [k for k, x in enumerate(o) if not x[1]]
    pr = [k for k, x in enumerate(r) if not x[1]]
    co = lambda k, l: [o[q][0] for q in po[bisect.bisect_left(po, k):bisect.bisect_left(po, k) + l]]
    cr = lambda k, l: [r[q][0] for q in pr[bisect.bisect_left(pr, k):bisect.bisect_left(pr, k) + l]]

    def recent(units, starts, k, sync):
        # heading lines that start after the last skip and at or before k, nearest first, plus the one containing k
        out = []
        n = bisect.bisect_right(starts, k)
        for a, b in reversed(units[max(0, n - 6):n]):
            if a >= sync:
                out.append((a, b))
            elif k < b:
                out.append((k, b))
        return out
    def ends(m, units, starts, b):
        # the end of the heading line, and of up to three more heading lines straight after it
        out = [b]
        while len(out) < 4 and b < len(m) and m[b][1]:
            b = units[bisect.bisect_right(starts, b) - 1][1]
            out.append(b)
        return out

    def candidates(i, j, si, sj):
        ro, rr = recent(uo, so, i, si), recent(ur, sr, j, sj)
        cands = []
        for a, b in ro:
            if j - (i - a) >= sj:
                cands += [(e, j - (i - a)) for e in ends(o, uo, so, b)]
        for a, b in rr:
            if i - (j - a) >= si:
                cands += [(i - (j - a), e) for e in ends(r, ur, sr, b)]
        for ao, bo in ro:
            for ar, br in rr:
                if i - ao == j - ar:        # both rewound to the same matched point: nothing else is passed over
                    cands += [(eo, er) for eo in ends(o, uo, so, bo) for er in ends(r, ur, sr, br)]
        return list(dict.fromkeys(cands))

    def walk(i, j):
        while i < len(o) and j < len(r) and o[i][0] == r[j][0]:
            i += 1
            j += 1
        return i, j

    memo: dict = {}

    def ahead(i, j, need, depth):
        # does the walk from (i, j) match `need` more characters (or reach both ends), passing over heading lines as
        # the walk itself would, at most `depth` times? (a run of repealed sections '42.--...' between split marginal
        # headings needs several passes within a few characters)
        key = (i, j, need, depth)
        if key in memo:
            return memo[key]
        si, sj = i, j
        i2, j2 = walk(i, j)
        got = i2 - i
        if got >= need or (i2 == len(o) and j2 == len(r)):
            res = True
        elif depth == 0:
            res = False
        else:
            res = any(ahead(c[0], c[1], need - got, depth - 1) for c in candidates(i2, j2, si, sj)[:8])
        memo[key] = res
        return res

    i = j = si = sj = 0
    for _ in range(200000):
        i, j = walk(i, j)
        if i == len(o) and j == len(r):
            return True, i, j
        good = [c for c in candidates(i, j, si, sj) if ahead(c[0], c[1], look, DEPTH)]
        if not good:
            return False, i, j
        i, j = good[0]
        si, sj = i, j
    return False, i, j


def repo_words(text: str, sched_at: int = 0) -> tuple[list[str], list[str]]:
    # sched_at: how many paragraphs the act's files other than its schedules hold (the schedules print after them)
    paras = [p for p in text.split('\n') if p.strip()]
    body, sched = [], []
    in_sched = False
    for i, p in enumerate(paras):
        # the schedules start at a schedule heading in the act's schedule files, not at one quoted in a section
        if re.fullmatch(r'(?:SCHEDULE( (?:\d+[A-Z]*|[A-Z]{1,2}))?\.?|' + build.ORDINAL_SCHEDULE + ')', p.strip()) \
                and i >= sched_at:
            in_sched = True
        if p.startswith('## ') and not in_sched:
            body.append([p[3:], True])
            continue
        if not in_sched and i + 1 < len(paras) and re.match(r'\d+[A-Z]{0,3}\.(?: |\u2014)', paras[i + 1]) \
                and not re.match(r'\d+[A-Z]{0,3}\.(?: |\u2014)', p):
            body.append([p, True])
            continue        # a section's title (from the table of contents)
        if in_sched:
            sched.append(p)
        else:
            body.append([p, False])
    return marked(body), letters(' '.join(sched).replace('## ', ''))


def pre_schedule(files: dict[str, str]) -> int:
    """The number of paragraphs in an act's files before its schedules (file name -> text)."""
    return sum(len([p for p in t.split('\n') if p.strip()]) for f, t in files.items() if not f.startswith('schedule-'))


def tool(repo: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, 'tools/on_date.py', *args], cwd=repo, capture_output=True, text=True,
                          encoding='utf-8')


def files_at(repo: str, commit: str, slug: str) -> dict[str, str]:
    """The act's files at a commit, read with one ls-tree and one cat-file --batch (not one git show per file)."""
    out = subprocess.run(['git', 'ls-tree', '-r', commit, f'{slug}/'], cwd=repo, capture_output=True,
                         text=True, encoding='utf-8').stdout.split('\n')
    blobs = []
    for line in out:
        if not line:
            continue
        info, f = line.split('\t', 1)
        if f.endswith('.md') and not f.endswith('/README.md'):
            blobs.append((f[len(slug) + 1:], info.split()[2]))
    if not blobs:
        return {}
    data = subprocess.run(['git', 'cat-file', '--batch'], cwd=repo, input=''.join(f'{sha}\n' for _, sha in blobs).encode(),
                          capture_output=True).stdout
    res, pos = {}, 0
    for name, _ in blobs:
        nl = data.index(b'\n', pos)
        size = int(data[pos:nl].split()[2])
        res[name] = data[nl + 1:nl + 1 + size].decode('utf-8')
        pos = nl + 1 + size + 1
    return res


def check_act(job: tuple) -> dict:
    """Both checks for every revision of one act (run in a pool: one act per task)."""
    act, repo, only = job
    out = {'eli': act['eli'], 'slug': act['slug'], 'versions': 0, 'files': 0, 'bad': 0, 'words': 0, 'wbad': 0,
           'nwords': 0, 'lines': []}
    try:
        versions = build.load_versions(act, offline=True)
    except Exception as exc:
        out['lines'].append(f'UNREADABLE {act["slug"]}: {exc}'[:300])
        out['bad'] += 1
        return out
    for v in versions:
        if only and v['updated_to'] not in only:
            continue
        expected = {build.file_name(k): u['text'] for k, u in v['units'].items()}
        day = v['updated_to']
        commit = subprocess.run([sys.executable, '-B', '-c', 'import sys; sys.path.insert(0, "tools"); import on_date; '
                                 f'print(on_date.commit_on("{day}", "{act["slug"]}"))'],
                                cwd=repo, capture_output=True, text=True).stdout.strip()
        got = files_at(repo, commit, act['slug']) if commit else {}
        out['versions'] += 1
        out['files'] += len(expected)
        if got != expected:
            out['bad'] += 1
            diff = sorted(set(got) ^ set(expected)) or [k for k in expected if got.get(k) != expected[k]]
            out['lines'].append(f'MISMATCH {act["slug"]} {day}: {diff[:5]}')
        whole = tool(repo, day, act['slug'])
        out['words'] += 1
        try:
            ob, os_ = official(build.fetch(v['url'], offline=True))
        except Exception as exc:
            ob, os_ = [(c, False, 0) for c in f'unreadable: {exc}'], []
        rb, rs = repo_words(whole.stdout, pre_schedule(got))
        out['nwords'] += len(TOKEN.findall(whole.stdout))
        ok, i, j = agree(ob, rb) if not whole.returncode else (False, 0, 0)
        if not ok or collections.Counter(os_) != collections.Counter(rs):
            out['wbad'] += 1
            oc, rc = ''.join(x[0] for x in ob), ''.join(x[0] for x in rb)
            out['lines'].append(
                f'WORDS {act["slug"]} {day}: official {len(ob)} vs repo {len(rb)} characters; first difference at '
                f'{i}/{j}: {oc[max(0, i - 60):i + 60]!r} / {rc[max(0, j - 60):j + 60]!r}; schedules '
                f'official-repo {dict(collections.Counter(os_) - collections.Counter(rs))} '
                f'repo-official {dict(collections.Counter(rs) - collections.Counter(os_))}'[:1500])
    return out


def main():
    from multiprocessing.pool import ThreadPool
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default=str(build.ROOT.parent / 'ireland-law'))
    ap.add_argument('--no-record', action='store_true')
    ap.add_argument('--only', nargs='*', help='check only these days (for debugging; not recorded)')
    ap.add_argument('--acts', nargs='*', help='check only these ELIs (for debugging; not recorded)')
    ap.add_argument('--job', help=argparse.SUPPRESS)   # one act, in a process started by main()
    args = ap.parse_args()
    sys.stdout.reconfigure(line_buffering=True)
    if args.job:
        act = next(a for a in build.acts_from_alpha(True) if a['eli'] == args.job)
        print(json.dumps(check_act((act, args.repo, args.only))))
        return
    manifest = json.loads((Path(args.repo) / 'data' / 'versions.json').read_text(encoding='utf-8'))
    built = {a['eli'] for a in manifest['acts']}
    acts = [a for a in build.acts_from_alpha(True) if a['eli'] in built and (not args.acts or a['eli'] in args.acts)]
    versions = files = bad = words = wbad = nwords = 0
    per_act, failing = {}, {}
    # Four checker processes at a time, one act each, started from threads (a process pool here broke as a whole
    # when one worker died: BrokenProcessPool, WinError 6).
    def run(a):
        cmd = [sys.executable, '-X', 'utf8', str(HERE / 'check_repo.py'), '--repo', args.repo, '--job', a['eli']]
        cmd += ['--only', *args.only] if args.only else []
        r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace',
                           stdin=subprocess.DEVNULL)
        if r.returncode:
            return {'eli': a['eli'], 'slug': a['slug'], 'versions': 0, 'files': 0, 'bad': 1, 'words': 0, 'wbad': 0,
                    'nwords': 0, 'lines': [f'CHECKER FAILED {a["slug"]}: {r.stderr.strip()[-200:]}']}
        return json.loads(r.stdout)
    with ThreadPool(4) as pool:
        for r in pool.imap(run, acts):
            for line in r['lines']:
                print(line)
            versions += r['versions']
            files += r['files']
            bad += r['bad']
            words += r['words']
            wbad += r['wbad']
            nwords += r['nwords']
            per_act[r['slug']] = r['versions']
            if r['bad'] or r['wbad']:
                failing[r['eli']] = (r['lines'][0] if r['lines'] else 'mismatch')[:300]
    print(f'{versions} revisions checked ({files} files), {bad} mismatches; {words} revisions in order against the PDF text '
          f'({nwords} words), {wbad} mismatches; {len(acts)} acts, {len(failing)} with a mismatch')
    (HERE / 'check_failing.json').write_text(json.dumps(failing, indent=1, sort_keys=True) + '\n', encoding='utf-8',
                                            newline='\n')
    if not args.no_record and not args.only and not args.acts:
        p = HERE / 'verification.json'
        rec = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
        rec['check'] = {'versions': versions, 'files': files, 'mismatches': bad, 'wordcheck': words,
                        'words': nwords, 'word_mismatches': wbad, 'acts': len(acts)}
        p.write_text(json.dumps(rec, indent=1, sort_keys=True) + '\n', encoding='utf-8', newline='\n')
    raise SystemExit(1 if bad or wbad else 0)


if __name__ == '__main__':
    main()
