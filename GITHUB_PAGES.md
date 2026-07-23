# Publishing the public demo with GitHub Pages

This repository includes `.github/workflows/pages.yml`. It publishes the
contents of the `GermanAnki/` directory whenever `main` is pushed.

## First-time setup

1. Push the repository to GitHub.
2. Open the repository on GitHub.
3. Go to **Settings → Pages**.
4. Under **Build and deployment**, select **GitHub Actions** as the source.
5. Open the **Actions** tab and wait for “Deploy card demo to GitHub Pages” to
   finish.
6. Return to **Settings → Pages** to copy the public URL.
7. Replace the placeholder in `REDDIT_POST.md` with that URL.

For a repository named `GermanAnki` under the account `graybert`, the expected
project-site URL is:

`https://graybert.github.io/GermanAnki/`

After setup, ordinary commits pushed to `main` automatically update the public
site. The source materials directory, extracted reference dataset, local
dependencies, and secrets are excluded from Git.
