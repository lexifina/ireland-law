"""Functional smoke test of the built Irish law repository: the things a reader does with it work. Standard library only.

    python -X utf8 scripts/ireland-law/test_repo.py [--repo ../ireland-law] [--record]
    python -X utf8 tools/test_repo.py                   # from inside the repository

It asserts that:
1. `git blame` on a changed provision names an amending law as author of its lines;
2. tools/on_date.py gives the text before and after a known amendment, and each equals the file at that law's tag;
3. `git log --follow` on a file lists its amending laws in the order they took effect;
4. every tag resolves to a commit, and every commit has an `In-force:` trailer;
5. no commit is authored by Lexifina except the documentation commit (the last one);
6. every git or tool command in the README's table runs and prints something.
With --record the result is written to verification.json next to this script (for REPRODUCE.md).
"""
import argparse
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAW = re.compile(r'^(act|si|bps)-\d{4}-\d+@irishstatutebook\.invalid$')    # matched against the author's email
PUBLISHER = 'revised-acts@lawreform.invalid'


def default_repo() -> Path:
    if (HERE.parent / '.git').exists():
        return HERE.parent
    return HERE.parents[2] / 'ireland-law'


class Smoke:
    def __init__(self, repo: Path):
        self.repo = repo
        self.results: list[tuple[str, bool, str]] = []

    def git(self, *args: str) -> str:
        out = subprocess.run(['git', *args], cwd=self.repo, capture_output=True, text=True, encoding='utf-8')
        if out.returncode:
            raise AssertionError(f'git {" ".join(args)}: {out.stderr.strip()}')
        return out.stdout

    def tool(self, *args: str) -> str:
        out = subprocess.run([sys.executable, 'tools/on_date.py', *args], cwd=self.repo, capture_output=True, text=True,
                             encoding='utf-8')
        if out.returncode:
            raise AssertionError(f'on_date {" ".join(args)}: {out.stderr.strip()}')
        return out.stdout

    def check(self, name: str, fn):
        try:
            detail = fn() or ''
            self.results.append((name, True, detail))
            print(f'PASS {name}: {detail}')
        except AssertionError as exc:
            self.results.append((name, False, str(exc)))
            print(f'FAIL {name}: {exc}')

    # 1
    def blame(self):
        path = 'protected-disclosures-act-2014/section-5.md'
        out = self.git('blame', '--line-porcelain', 'main', '--', path)
        authors = {l[12:].strip().strip('<>') for l in out.splitlines() if l.startswith('author-mail ')}
        assert authors, 'no blame output'
        assert all(LAW.match(a) or a == PUBLISHER for a in authors), f'unexpected authors {authors}'
        assert 'act-2022-27@irishstatutebook.invalid' in authors, f'Act 27 of 2022 not among the authors {authors}'
        assert len(authors) >= 2, f'only {authors}'
        return f'{path} lines by {", ".join(sorted(authors))}'

    # 2
    def on_date(self):
        done = []
        for act, prov, path, tag, before, after in [
                ('protected-disclosures-act-2014', '5', 'protected-disclosures-act-2014/section-5.md', 'act/2022-27',
                 '2022-12-31', '2023-01-01'),
                ('data-protection-act-2018', '12', 'data-protection-act-2018/section-12.md', 'act/2026-9',
                 '2026-06-11', '2026-06-12')]:
            # a law with commits on several days has one tag per day (act/2022-27/2023-01-01), else one (act/2022-27)
            tags = set(self.git('tag', '-l', f'{tag}', f'{tag}/*').split())
            tag = f'{tag}/{after}' if f'{tag}/{after}' in tags else tag
            assert tag in tags, f'no tag {tag}'
            a, b = self.tool(before, act, prov), self.tool(after, act, prov)
            assert a and b and a != b, f'{path}: no change between {before} and {after}'
            assert b == self.git('show', f'{tag}:{path}'), f'{path} on {after} is not the file at {tag}'
            assert a == self.git('show', f'{tag}~1:{path}'), f'{path} on {before} is not the file before {tag}'
            done.append(f'{path} {before} != {after}')
        whole = self.tool('2020-01-01', 'protected-disclosures-act-2014')
        assert '\n5. (1)' in whole and '\n10A. ' not in whole, 'the act on 2020-01-01 lacks section 5 or has section 10A'
        assert '\n10A. (1)' in self.tool('2023-01-01', 'protected-disclosures-act-2014'), 'no section 10A on 2023-01-01'
        return '; '.join(done)

    # 3
    def follow(self):
        checked = []
        for path in ('protected-disclosures-act-2014/section-5.md', 'protected-disclosures-act-2014/section-10.md',
                     'data-protection-act-2018/section-117A.md'):
            out = self.git('log', '--follow', '--format=%ae%x09%(trailers:key=In-force,valueonly,separator=)', 'main', '--', path)
            rows = [l.split('\t') for l in out.splitlines() if l]
            assert len(rows) >= 2, f'{path}: {len(rows)} commits'
            days = [d.strip() for _, d in rows]
            assert days == sorted(days, reverse=True), f'{path}: not in date order {days}'
            assert all(LAW.match(a) or a == PUBLISHER for a, _ in rows), f'{path}: authors {[a for a, _ in rows]}'
            assert sum(1 for a, _ in rows if LAW.match(a)) >= 2, f'{path}: fewer than two laws'
            checked.append(f'{path} {len(rows)} commits')
        return '; '.join(checked)

    # 4
    def tags_and_trailers(self):
        tags = self.git('tag').split()
        assert tags, 'no tags'
        for t in tags:
            self.git('rev-parse', '--verify', '-q', f'{t}^{{commit}}')
        rows = self.git('log', '--format=%H%x09%an%x09%(trailers:key=In-force,valueonly,separator=)', 'main').splitlines()
        bad = [r for r in rows if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', r.split('\t')[2].strip())]
        assert not bad, f'{len(bad)} commits without a well-formed In-force, e.g. {bad[:2]}'
        return f'{len(tags)} tags resolve; all {len(rows)} commits carry In-force'

    # 5
    def lexifina(self):
        rows = [r.split('\t') for r in self.git('log', '--format=%H%x09%an%x09%ae%x09%cn', 'main').splitlines()]
        by_lex = [r for r in rows if r[1] == 'Lexifina']
        assert len(by_lex) == 1 and by_lex[0] == rows[0], f'{len(by_lex)} commits by Lexifina'
        assert all(r[3] == 'Lexifina' for r in rows), 'a committer other than Lexifina'
        emails = {r[2] for r in rows[1:]}
        assert all(LAW.match(a) or a == PUBLISHER for a in emails), f'unexpected authors {emails - {PUBLISHER}}'
        return f'only the documentation commit {rows[0][0][:10]} is by Lexifina; {len(emails)} distinct authors'

    # 6
    def readme(self):
        text = (self.repo / 'README.md').read_text(encoding='utf-8')
        table = text[text.index('## The questions'):text.index('## The dates')]
        cmds = [c for c in re.findall(r'`([^`]+)`', table) if c.startswith(('git ', 'python '))]
        assert len(cmds) >= 8, f'only {len(cmds)} commands found'
        for c in cmds:
            args = shlex.split(c)
            if args[0] == 'python':
                args[0] = sys.executable
            out = subprocess.run(args, cwd=self.repo, capture_output=True, text=True, encoding='utf-8')
            assert out.returncode == 0, f'{c}: exit {out.returncode} {out.stderr.strip()[:200]}'
            assert out.stdout.strip(), f'{c}: printed nothing'
        return f'{len(cmds)} README commands ran and printed output'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default=None)
    ap.add_argument('--record', action='store_true')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    s = Smoke(Path(args.repo) if args.repo else default_repo())
    s.check('blame names a law', s.blame)
    s.check('text before and after an amendment', s.on_date)
    s.check('log --follow in date order', s.follow)
    s.check('tags resolve, In-force on every commit', s.tags_and_trailers)
    s.check('only the documentation commit is by Lexifina', s.lexifina)
    s.check('README commands run', s.readme)
    ok = all(r[1] for r in s.results)
    print(f'{sum(r[1] for r in s.results)}/{len(s.results)} passed')
    if args.record:
        p = HERE / 'verification.json'
        rec = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
        rec['smoke'] = {'passed': sum(r[1] for r in s.results), 'total': len(s.results),
                        'results': [{'test': n, 'ok': o, 'detail': d} for n, o, d in s.results]}
        p.write_text(json.dumps(rec, indent=1, sort_keys=True, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    raise SystemExit(0 if ok else 1)


if __name__ == '__main__':
    main()
