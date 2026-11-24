# Publication figures

Generate the current figures and tables from the repository root with:

```sh
.venv/bin/python scripts/build_publication.py
.venv/bin/python scripts/build_publication.py --check
```

The inputs are the reconciled publication data, the accepted supervised P33 archive and the exact P37 raw brackets. paper/publication_manifest.json pins every input, generator and output hash. No manually typed performance array is allowed.

The earlier gain/scaling PDFs and hardcoded generator at6154b46 are withdrawn; their original bytes remain in Git and the initial recovery hash inventory. The missing scaling_p_success.pdf reference was removed with the unsupported old article, not filled using invented data.
