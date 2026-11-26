# Structure

How this repository is laid out, and how its commits are made. Names are in English, the language the Irish statute
book is searched in; the Constitution keeps its own name, Bunreacht na hÉireann.

```
bunreacht/                                  the Constitution, as amended to date
  preamble.md, article-1.md ... article-50.md (with article-42a.md)      English text
  ga/preamble.md, ga/airteagal-1.md ...                                    Irish text (it prevails, Article 25.5.4°)
  amendments/<NN>-<name>/                   each amendment Act as enacted (NN = the amendment's number)
acts/<year>/<number>-<name>/                Acts of the Oireachtas (and of the Oireachtas of Saorstát Éireann)
acts/<year>/c<chapter>-<name>/              Acts passed before 1922 that are still in force (Revised Acts only)
statutory-instruments/<year>/<number>-<name>/
```

No folder holds more than 1,000 entries: a year holds at most about 100 Acts and at most about 1,000 statutory
instruments (a year with more would be split into `0000-0999/`, `1000-1999/`).

Each act or instrument is a folder with one file per provision and a `README.md` listing them:

- Acts: `long-title.md` (number, title, long title, date of passing, enacting words), `section-<n>.md`,
  `schedule-<n>.md` (or `schedule.md` when there is one).
- Statutory instruments: `preamble.md` (the notice in Iris Oifigiúil and the enabling words), `regulation-<n>.md`
  (`article-<n>.md` for an Order, `rule-<n>.md` for Rules, `paragraph-<n>.md` for a Scheme), `schedule-<n>.md`.

A file is the provision's heading, a blank line, then its paragraphs, one per line.

## Two kinds of act folder

1. **Revised Acts** (the Law Reform Commission's consolidations): the history starts at the Commission's earliest
   revision and follows every later revision; each change is credited to the law that made it.
2. **As enacted** (every other Act, from the electronic Irish Statute Book): one commit, the Act as passed. Later
   amendments are not applied; the folder's README says so.

Statutory instruments are as made, one commit each. The amendment Acts of the Constitution are as enacted, one commit
each, and the Constitution's text as amended is one commit dated by the last amendment; earlier wordings of the
Constitution are not reconstructed yet.

## Commits

- One commit per version, dated noon Europe/Dublin on the day it took effect, with `In-force:` and `In-force-basis:`
  trailers saying which day that is and why (date of passing, date of signature, date made, or the Commission's
  annotation).
- Author: the law that made the version: the Act or instrument itself for a first version, the amending law for a
  change. Committer: Lexifina.
- Git holds no date before 1970. A commit for a day before 1970 is dated 1970-01-01 plus the number of days since
  1900-01-01 as seconds, which keeps the commits in order; its real day is `In-force:` (and `Date-note:` says so).
- `Source:` links the official text read.

## Corpus

`corpus.json` names the corpus `ie/national/acts`.
