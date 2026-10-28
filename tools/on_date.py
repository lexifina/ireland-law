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


def order(path: str) -> tuple:
    """The order of an act's files: long title, sections by number, schedules by number."""
    name = path.rsplit('/', 1)[1][:-3]
    m = re.fullmatch(r'(?:section|regulation|article|rule)-(\d+)([A-Z]*)', name)
    if m:
        return (1, int(m.group(1)), m.group(2))   # 31A, 31AA, 31AB, 31B
    m = re.fullmatch(r'schedule-(\d+)([A-Z]*)', name)
    if m:
        return (2, int(m.group(1)), m.group(2))
    return (0 if name == 'long-title' else 3, 0, name)


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
    files.sort(key=order)
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
