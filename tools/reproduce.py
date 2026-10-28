"""Writes data/versions.json, corpus.json and REPRODUCE.md into the Irish law repository, from the facts of the build
that made it. Called by build.py; kept apart so the record of how the repository was made reads as one document.

The results of the checks (check_repo.py, test_repo.py and the rebuild that compares hashes) are read from
verification.json next to this file, which check_repo.py, `test_repo.py --record` and `build.py --verify-rebuild` write.
They describe the build before the one that writes this file, from the same data; a rebuild with the same data and the
same verification.json gives the same hashes."""
from __future__ import annotations

import datetime as dt
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent


def write_manifest(repo: Path, built: list[dict], today: str):
    """Every revision the text comes from, with the sha256 of its PDF, so a rebuild can show it read the same bytes."""
    out = {'built': today, 'source': 'https://revisedacts.lawreform.ie', 'acts': [{
        'eli': b['act']['eli'], 'title': b['title'], 'slug': b['act']['slug'],
        'versions': [{'updated_to': v['updated_to'], 'listed': v['listed'], 'pdf': v['url'], 'sha256': v['sha256'],
                      **({'replaces_listing': v['replaces']} if v.get('replaces') else {}),
                      **({'preferred_to_unannotated_listing': v['replaces_unannotated']}
                         if v.get('replaces_unannotated') else {})} for v in b['versions']],
    } for b in built]}
    (repo / 'data').mkdir(exist_ok=True)
    (repo / 'data' / 'versions.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8',
                                                 newline='\n')


def write_corpus(repo: Path, built: list[dict], log: list[dict], today: str):
    days = [e['day'] for e in log]
    corpus = {
        'corpus': 'ie/national/acts',
        'name': f'Irish law: the Revised Acts of the Law Reform Commission ({len(built)} acts, every published revision)',
        'acts': [b['laws'][b['key']]['label'] for b in built],
        'history_from': min(days),
        'built': today,
        'dates': {'commit': 'in-force', 'other_trailers': ['Stated-in-force'],
                  'time': '12:00 Europe/Dublin (UTC, UTC+1 in summer time)'},
        'scope': {
            'trailer': 'Applies',
            'when_absent': 'this corpus records no scope notes (no commit carries Applies:); the absence is not a '
                           'statement that the change reaches every case',
            'default_reach': {
                'rule': 'presumption against retrospective effect',
                'meaning': 'an enactment is presumed not to affect rights and obligations accrued, or acts done, before '
                           'it takes effect, unless it says so expressly or by necessary implication; the Oireachtas may '
                           'not declare acts to be infringements of the law which were not so at the date of their '
                           'commission',
                'authority': 'Bunreacht na h\u00c9ireann, Article 15.5.1\u00b0 ("The Oireachtas shall not declare acts to '
                             'be infringements of the law which were not so at the date of their commission."); '
                             'Interpretation Act 2005, section 27(1) (effect of repeal)',
                'decided_here': False,
            },
        },
        'tool': 'tools/on_date.py',
        'in_force_trailer': 'In-force',
        'record_to': max(d for d in days if d <= today),
        'citation': {
            'file': '([a-z0-9-]+)/section-0*([0-9]+[A-Z]*)\\.md',
            'cites': '([Ss]ection|s\\.) ?{n}([^0-9A-Za-z]|$)',
        },
        'label': 'Ireland',
        'language': 'en',
        'checked_on': today,
        'history': 'in-force',
        'record_note': f'Checked against the official source on {today}.',
    }
    (repo / 'corpus.json').write_text(json.dumps(corpus, ensure_ascii=False, indent=2) + '\n', encoding='utf-8',
                                      newline='\n')


def write_reproduce(repo: Path, built: list[dict], log: list[dict], tags: dict, requests: list[dict], today: str,
                    left_out: list[dict] | None = None):
    write_corpus(repo, built, log, today)
    blob = subprocess.run(['git', 'hash-object', str(HERE / 'build.py')], capture_output=True, text=True).stdout.strip()
    pyv = subprocess.run(['python', '--version'], capture_output=True, text=True).stdout.strip()
    gitv = subprocess.run(['git', '--version'], capture_output=True, text=True).stdout.strip()
    try:
        import pymupdf
        mupdfv = pymupdf.VersionBind
    except Exception:
        mupdfv = '?'
    ver = json.loads((HERE / 'verification.json').read_text(encoding='utf-8')) if (HERE / 'verification.json').exists() else {}
    files = {r['file'] for r in requests if r['file'].exists()}
    retrieved = ', '.join(sorted({dt.date.fromtimestamp(f.stat().st_mtime).isoformat() for f in files})) or today
    n_pdf = len({r['url'] for r in requests if not r['url'].endswith('/alpha')})
    count = lambda k: sum(1 for c in log if c['kind'] == k)
    n_late = sum(1 for c in log if c['stated'])
    rows = '\n'.join(
        f'| {b["title"]} | {b["laws"][b["key"]]["label"]} | `{b["act"]["slug"]}/` | {len(b["versions"])} | '
        f'{b["versions"][0]["updated_to"]} to {b["versions"][-1]["updated_to"]} | {len(b["versions"][-1]["units"])} |'
        for b in built)
    labelled = []
    for c in log:
        if c['kind'] in ('candidates', 'unexplained', 'early'):
            labelled.append(f'- {c["slug"]} {c["day"]}: {c["kind"]}, {", ".join(c["keys"])}')
        if c['stated']:
            labelled.append(f'- {c["slug"]} {c["day"]}: consolidated late (annotation gives {c["stated"]}), '
                            f'{", ".join(c["keys"])}')
    left = chr(10).join(f'| {x["title"]} | `{x["eli"]}` | {x["why"]} |' for x in (left_out or [])) or '| none | | |'
    layout = [f'{c["slug"]} {c["day"]} ({", ".join(c["keys"])})' for c in log if c['kind'] == 'layout']
    chk, det, smoke = ver.get('check', {}), ver.get('rebuild', {}), ver.get('smoke', {})
    check_line = (f'`{chk["versions"]} revisions checked ({chk["files"]} files), {chk["mismatches"]} mismatches; '
                  f'{chk["wordcheck"]} revisions in order against the PDF text ({chk["words"]} words), {chk["word_mismatches"]} '
                  f'mismatches`' if chk else '(not yet run)')
    rebuild_line = (f'A second build from the same cache into an empty folder gave the same history: the last law commit '
                    f'was `{det["history_tip"]}` in both, and every one of the {det["commits"]} law commits and '
                    f'{det["tags"]} tags had the same hash.' if det.get('identical') else '(not yet run)')
    smoke_lines = ('\n'.join(f'   - {"pass" if r["ok"] else "FAIL"}: {r["test"]}: {r["detail"]}' for r in smoke['results'])
                   if smoke else '   (not yet run)')
    smoke_head = f'{smoke["passed"]} of {smoke["total"]} passed' if smoke else 'not yet run'
    text = f"""# How this repository was made

This file records where every part of this repository comes from, how it was built, how it was checked, what was done
by hand, and what an AI model did and did not do. The build writes it, so it describes the build that made this
commit.

## Short version

```sh
git clone https://github.com/lexifina/ireland-law && cd ireland-law
pip install pymupdf
python -X utf8 tools/build.py --repo ../rebuilt --today {today}
git -C ../rebuilt rev-parse main        # the same hash as this repository's main
python -X utf8 tools/check_repo.py --repo ../rebuilt
python -X utf8 tools/test_repo.py --repo ../rebuilt
```

`tools/build.py` needs Python 3.12 or later with PyMuPDF (`pymupdf`), and git. It reads the Revised Acts site (or its
own cache, `.cache/` next to the script) and writes this repository into `--repo`. With the same PDFs and the same
`--today` it gives the same commits with the same hashes. `data/versions.json` lists every revision with the sha256 of
its PDF; the Commission replaces revisions as it updates them, and then the hashes change too.

## Sources

All legal text, and all dates and amending laws, come from the **Revised Acts** of the Law Reform Commission of
Ireland (https://revisedacts.lawreform.ie). Nothing was typed in, summarised or rewritten. The build read the
alphabetical list (`/revacts/alpha`, which links each act's current and previous revisions as PDFs, with the day each
was listed) and {n_pdf} revision PDFs:

| Act | Number | Folder | Revisions | Updated to | Files today |
| --- | --- | --- | ---: | --- | ---: |
{rows}

Left out: the Revised Acts in the list that the builder cannot read back exactly (`left_out.json` next to the builder,
which is part of the build's input, or a revision PDF the reader cannot read). Their text is not in this repository.

| Act | ELI | Why |
| --- | --- | --- |
{left}

The data was retrieved on {retrieved}, at most four requests at a time and a request started at most every 0.4
seconds, with the user agent `lexifina-watch/1.0 (+https://lexifina.com/watch; corpus@lexifina.com)`. robots.txt on
the site disallows nothing. No bulk download exists; the eISB XML (irishstatutebook.ie) has the acts as enacted only,
not revised text or past versions. Reuse terms: see LICENSE (not settled for the Revised Acts; the repository is
private).

## The build, step by step

1. `python -X utf8 scripts/ireland-law/build.py` in Lexifina's own repository fetched the data into its cache and
   wrote this repository. `tools/build.py` here is the same file (git blob `{blob}`), with `tools/reproduce.py`, which
   writes this file, `tools/check_repo.py` and `tools/test_repo.py`. Every later build ran with `--offline`.
2. `python -X utf8 scripts/ireland-law/check_repo.py` read every revision of each act back from this repository with
   `tools/on_date.py`, on the day it is updated to, and compared it file by file with the text the builder reads from
   that PDF; then it compared the whole act, in order, with the PDF's body text read with a different PyMuPDF
   extraction (span text, not the builder's character positions) and without the builder's paragraph, heading and
   layout rules: character by character with white space removed (some PDFs hold no space glyphs), headings left out on
   both sides, schedules as the letters and digits they contain. Result: {check_line}.
3. `python -X utf8 scripts/ireland-law/test_repo.py --record` ran the functional smoke test ({smoke_head}):
{smoke_lines}
4. `python -X utf8 scripts/ireland-law/build.py --offline --verify-rebuild` built the repository a second time from
   the same cache into a temporary folder and compared the hashes. {rebuild_line}
5. The build was run once more to write these results into this file, and the final `main` was rebuilt again and
   compared hash for hash before it was pushed.

It ran with {pyv}, PyMuPDF {mupdfv} and {gitv} on Windows 11.

## How the text and the commits are derived

- **Revisions.** Each PDF says "Updated to <day>"; that day is the revision's day. Two listings updated to the same day
  are one revision (the later listing, unless the later one was printed without its annotations and the earlier
  with them: then the annotated one, `preferred_to_unannotated_listing` in `data/versions.json`). Revisions are
  ordered by that day.
- **Text.** PyMuPDF's character positions give the words (a space where the gap between two letters exceeds a
  threshold, or where the PDF has a space glyph). Running heads, page numbers, footnotes (below 8pt), footnote
  reference numbers (below 7pt) and the annotation notes (8\u20139pt) are taken out of the body; the notes are kept for
  the commit messages. The text starts at the long title and ends at "About this Revised Act". A section starts at a bold
  number ("12. "); its heading is the title the table of contents gives it. Annotation marks `F12[ ... ]` are removed.
  A word broken at a line end is joined with or without its hyphen as the act's other revisions write it.
- **One layout.** The PDFs of different years break the same words differently. So that a change of layout is not a
  change of law: a paragraph starting with a small letter runs on from the one before; a definition run on after
  another ("...; \u2018data\u2019 means ...") starts its own paragraph; consecutive part and chapter headings are joined and
  split again before each PART/CHAPTER; spaces inside quotation marks are dropped. Differences that remain, where no
  word changed, are commits labelled `Kind: editorial (layout)`: {', '.join(layout) or 'none'}.
- **Causes.** For each provision that changed between two revisions, the annotations attached to it in the newer one,
  and not present anywhere in the older one, name the law and the day ("Substituted (1.01.2023) by ... (27/2022)"). One
  law: the change is that law's commit, on that day. Where a note quotes an amendment made through another act ("as
  inserted (26.12.2018) by ..."), the dated law is the one credited. More than one law: credited to neither
  (`Candidate:`). No note attached, but a later revision attaches one dated in the interval: that law, with an
  `Evidence:` trailer. A day after the newer revision's own day: printed early, the publisher's, not credited. A day on
  or before the older revision's day: consolidated late, dated the day after the older revision, the stated day in
  `Stated-in-force:`.
- **Counts.** {count('start')} first-revision commits, {count('law')} law commits ({n_late} of them consolidated late),
  {count('candidates')} credited to neither of two laws, {count('early')} printed early, {count('unexplained')}
  unexplained, {count('layout')} layout; {len(tags)} tags; one documentation commit.

Labelled commits:

{chr(10).join(labelled) or '- none'}

## Dates

Author and committer dates are noon in Dublin on the `In-force:` day: UTC+1 from the last Sunday in March to the day
before the last Sunday in October (`start <= day < end`), UTC otherwise, written out in the builder because the build
machine has no time-zone database. No day in this corpus is before 1970. The committer is
`Lexifina <ireland-law@lexifina.com>`. The documentation commit is dated the day the PDFs were retrieved.

## Limits

1. The history starts at the earliest revision the Commission publishes, not at enactment.
2. Between two revisions the text of each provision is known only at the two ends: two laws changing one provision in
   that interval cannot be separated.
3. Schedules are tables; their cells are read in the order the PDF holds them, which is not always the order a reader
   sees. A schedule is compared across revisions as the letters and digits it contains.
4. English only; the Revised Acts are in English.

## People and models

The builder, checker and tests were written by an AI agent (Claude, Anthropic, model Opus 5.5) working for Lexifina, under
the instructions of Lexifina's staff. No AI model wrote, summarised or edited legal text, and no model runs at build
time: the commit messages quote the Commission's annotations and are otherwise fixed templates.

## Prior art

- The Law Reform Commission's Revised Acts and its classified list of legislation.
- The electronic Irish Statute Book (irishstatutebook.ie), with each act's legislation directory ("affected by").
- legalize-dev (github.com/legalize-dev), law as git repositories for several countries.
"""
    (repo / 'REPRODUCE.md').write_text(text, encoding='utf-8', newline='\n')
