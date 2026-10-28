# Ireland: law history

This repository will hold the legislation of Ireland (IE) as a history: one file per provision and one commit per law taking effect, dated by the day it took force, with the law that made each change as the commit author. It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `ie/` in the world tree.

**Status:** no law yet. This first commit records where the law of Ireland can be read and what a build would need.

**Can it be built?** Some past versions are online. A full history needs those plus the gazette.

**This commit is a placeholder.** The first real build must replace this history from scratch and force-push. It must never append law commits on top of it: they are dated by when each law took effect, often decades earlier, so dates in `main` would run backwards and break every on-date lookup. Builders should refuse to append when the root commit is this placeholder (its subject ends "sources, before any law").

**Official sources**

- [Irish Statute Book](https://www.irishstatutebook.ie): The statute book is as enacted. The Law Reform Commission’s Revised Acts (500+) show previous versions. XML at /eli/{year}/act/{n}/enacted/en/xml.
- [BAILII](https://www.bailii.org): Mostly case law, but it has UK, Scotland, Wales, Northern Ireland and Ireland legislation databases too.

**Notes for a build from PDFs** (learned on Malta)

- Letter-spaced, justified PDF lines extract as “w o r d”. Read character boxes (for example PyMuPDF `rawdict`), keep a space only where the gap is over 0.5 pt, and treat differences in whitespace alone as no change.
- One address can serve a wrong-language or duplicate upload (212 of 5,079 in Malta). Detect the language from the text and keep one version per date.

All sources, with their status, are in [SOURCES.md](SOURCES.md). How these files were made is in [REPRODUCE.md](REPRODUCE.md).

This repository describes sources; it is not legal advice and holds no legal text yet.
