# Public preview prepared — 2026-07-23

A public landing page now introduces the project and links to the continuous
50-card browser reviewer. A GitHub Actions workflow deploys the `GermanAnki/`
directory to GitHub Pages on every push to `main`.

`REDDIT_POST.md` contains a transparent r/German feedback request that explains
the AI-assisted workflow, independent authorship, planned audio experiment, and
the specific linguistic and pedagogical questions on which feedback is needed.
`GITHUB_PAGES.md` records the one-time Pages setup and expected public URL.

The repository was made public and GitHub Pages was configured to use GitHub
Actions. The expected demo URL was added to the README and Reddit draft; the
resulting push triggers the first deployment.

The repository was initialized independently so it cannot accidentally commit
into the unrelated parent repository. Proprietary source materials and the
locally extracted frequency-source dataset are excluded from Git. From this
point onward, completed project changes should be committed and pushed whenever
the remote is available.
