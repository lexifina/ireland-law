# Irish law, change by change

The Law Reform Commission's [Revised Acts](https://revisedacts.lawreform.ie) as a git repository: every Revised Act in
its alphabetical list (Acts of the Oireachtas, the statutory instruments it revises, and the pre-1922 Acts it carries),
each in its own folder, with every revision the Commission publishes, current and previous. Each amending law is one
commit, credited to that law and dated the day its change took effect, at noon in Dublin; a law that changed several
acts on one day is one commit across them. The acts the builder cannot read back exactly are left out, and are listed
with the reason in `REPRODUCE.md`.

The Constitution (Bunreacht na hÉireann) is not in the Revised Acts, which is why it is not here.

## The questions, as git commands

| Question | Command |
| --- | --- |
| What did section 5 of the Protected Disclosures Act say on 1 January 2022? | `python tools/on_date.py 2022-01-01 protected-disclosures-act-2014 5` |
| The whole act as it stood on 1 January 2023 | `python tools/on_date.py 2023-01-01 protected-disclosures-act-2014` |
| Section 117A of the Data Protection Act in mid-2024 | `python tools/on_date.py 2024-06-01 data-protection-act-2018 117A` |
| Which law wrote each paragraph of section 5? | `git blame protected-disclosures-act-2014/section-5.md` |
| Every change to section 5, with the law and the day | `git log --follow protected-disclosures-act-2014/section-5.md` |
| Everything one law changed | `git show --stat act/2022-27` |
| What changed in an act on one day | `git show --stat protected-disclosures-act-2014/2023-01-01` |
| The amending laws with their dates | [`amendments.csv`](amendments.csv) |
| Changes two laws made between two revisions (credited to neither) | `git log --grep="credited to neither"` |
| Changes that are only the layout of a revision | `git log --grep="Kind: editorial (layout)"` |
| Changes the publisher printed with no annotation naming a law | `git log --grep="Kind: editorial (unexplained)"` |

## The dates

Each revision is "updated to" a day: it holds every amendment in force on that day. Each amendment in it carries an
annotation (an F-note) that names the law and the day the change took effect, for example "Substituted (1.01.2023) by
Protected Disclosures (Amendment) Act 2022 (27/2022), s. 4(a)(ii), S.I. No. 510 of 2022". **Commits are dated by that
day**, at noon in Dublin (Irish Standard Time, UTC+1, from the last Sunday in March to the last Sunday in October;
UTC otherwise), and every commit carries it in an `In-force:` trailer. Where an annotation gives a day on or before the
day the previous revision is updated to, but that revision does not contain the change (the Commission consolidated it
later), the commit is dated the day after the previous revision and the annotation's day is kept in
`Stated-in-force:`, so that every revision reads back from the history exactly as published.

The first commit of each act is the earliest revision the Commission publishes (for example 2018-12-26 for the Data
Protection Act 2018), not the act as enacted; its message lists the laws whose amendments it already contains.

## What "author" means

The author of a commit is the law that made the change, for example `Protected Disclosures (Amendment) Act 2022` with
the address `act-2022-27@irishstatutebook.invalid` (statutory instruments: `si-2023-375@...`), so `git blame` names the
law. A change is credited to a law when the annotations attached to the changed provision in the new revision, and not
in the one before, name that law and only that law. Where they name two laws, the change is committed by the publisher
(`Law Reform Commission, Revised Acts`), credited to neither, and names both in `Candidate:` trailers. Where the
revision prints a change without attaching its annotation, the first later revision that attaches one dated in the
interval names the law (`Evidence:` says so). Where two revisions differ only in layout (paragraph breaks, headings,
quotation marks, the order a table is read in), the commit is the publisher's and is labelled `Kind: editorial
(layout)`. Where the words changed but no new annotation of the provision names a law, the commit is the publisher's
too, labelled `Kind: editorial (unexplained)`: the change is recorded as published and credited to no law. The
committer is always `Lexifina`.

## How it is checked

`tools/check_repo.py` reads every revision of each act back from git on the day it is updated to and compares it with
that revision: file by file with the text the builder reads from the PDF, and word for word with the words of the PDF
page body. `tools/test_repo.py` checks that the commands above work. The results are in [`REPRODUCE.md`](REPRODUCE.md).

## Files

Each act is a folder. Each section is one file named after its number (`section-5.md`, `section-10A.md`), plus
`long-title.md` and `schedule-N.md`. One paragraph per line; part and chapter headings are `## ` lines at the top of
the first section they head; the second line of a section is its heading as given in the table of contents.
Annotation marks (`F12[ ... ]`) are removed; the annotations themselves are quoted in the commit messages.

## Terms

See [`LICENSE`](LICENSE). The reuse terms for the Revised Acts are not settled, so this repository is private.
