# Local card reviewer

From the repository directory, run:

```powershell
python tools/serve_viewer.py
```

Then open `http://localhost:4173/viewer/`. The viewer loads both canonical
frequency-batch JSONL files directly, so rebuilding a batch updates the review
site after a refresh. Frequency rank remains available in the review controls
and canonical metadata, but it is not displayed on the card itself.
