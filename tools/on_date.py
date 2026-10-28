"""Prints an act, or one provision of it, as it stood on a given day, from this repository's history.

    python tools/on_date.py 2023-01-01 protected-disclosures-act-2014 5     # section 5 on 1 January 2023
    python tools/on_date.py 2022-01-01 protected-disclosures-act-2014       # the whole act on 1 January 2022
    python tools/on_date.py 2024-06-01 data-protection-act-2018 117A
    python tools/on_date.py 2024-06-01 data-protection-act-2018 schedule-1

Each commit carries the day its change took effect in an `In-force:` trailer, which is the source of truth (not the
commit date). The text in force on a day is the last commit on or before it. Standard library only.
"""
import datetime as dt
import re
import subprocess
import sys


def git(*args: str) -> str:
    return subprocess.run(['git', *args], capture_output=True, text=True, encoding='utf-8', check=True).stdout


def suffix_key(s: str, others: set) -> tuple:
    """Where a section's letters put it among the others of its number: an inserted section follows the one it is
    named after (31A, 31AA, 31AB, 31B), but once a number's letters have run to Z the next ones carry on after Z
    (33Z, 33AA, ..., 33AZ, then 33BA or 33AAA), as the Revised Acts print them."""
    if len(s) <= 1:
        return (0, s)
    full, x = 'Z' in others, 'A'
    while full and x <= 'Z':
        family = {t[1:] for t in others if len(t) > 1 and t[0] == x}
        if s[0] == x:
            return (1, x, suffix_key(s[1:], family))
        full, x = 'Z' in family, chr(ord(x) + 1)
    return (0, s[0], suffix_key(s[1:], {t[1:] for t in others if len(t) > 1 and t[0] == s[0]}))


UNIT = re.compile(r'(section|regulation|article|rule|schedule)-(\d+)([A-Z]*)')


def ordered(paths: list) -> list:
    """An act's files in order: long title, sections by number and letters, schedules by number."""
    letters = {}
    for p in paths:
        m = UNIT.fullmatch(p.rsplit('/', 1)[-1][:-3])
        if m:
            letters.setdefault((m.group(1) == 'schedule', int(m.group(2))), set()).add(m.group(3))

    def key(p):
        name = p.rsplit('/', 1)[-1][:-3]
        m = UNIT.fullmatch(name)
        if m:
            g = (m.group(1) == 'schedule', int(m.group(2)))
            return (2 if g[0] else 1, g[1], suffix_key(m.group(3), letters[g]))
        return (0 if name == 'long-title' else 3, 0, (0, name))
    return sorted(paths, key=key)


def file_for(key: str) -> str:
    """'5' or '10A' -> section-5.md / section-10A.md; anything else is a file name ('schedule-1', 'long-title')."""
    if re.fullmatch(r'\d+[A-Za-z]*', key):
        return f'section-{key.upper()}.md'
    return key if key.endswith('.md') else f'{key}.md'


def commit_on(day: str, act: str) -> str:
    out = git('log', '--format=%H%x09%(trailers:key=In-force,valueonly,separator=)', 'main', '--', act)
    for line in out.splitlines():
        h, _, d = line.partition('\t')
        if d.strip() and d.strip() <= day:
            return h
    return ''


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    day, act = sys.argv[1], sys.argv[2].rstrip('/')
    dt.date.fromisoformat(day)
    commit = commit_on(day, act)
    if not commit:
        sys.exit(f'{act} is not in the record on {day}.')
    if len(sys.argv) > 3:
        name = file_for(sys.argv[3])
        try:
            sys.stdout.write(git('show', f'{commit}:{act}/{name}'))
        except subprocess.CalledProcessError:
            sys.exit(f'{act}/{name} was not in the text on {day}.')
        return
    files = [f for f in git('ls-tree', '-r', '--name-only', commit, f'{act}/').split('\n')
             if f.endswith('.md') and not f.endswith('/README.md')]
    files = ordered(files)
    # every file in one `git cat-file --batch` call, not one `git show` per file
    data = subprocess.run(['git', 'cat-file', '--batch'], input=''.join(f'{commit}:{f}\n' for f in files).encode(),
                          capture_output=True, check=True).stdout
    pos = 0
    for _ in files:
        nl = data.index(b'\n', pos)
        size = int(data[pos:nl].split()[2])
        sys.stdout.write(data[nl + 1:nl + 1 + size].decode('utf-8') + '\n')
        pos = nl + 1 + size + 1


if __name__ == '__main__':
    main()
