# README LaTeX template

Tested on Linux. Requires a LaTeX distribution, e.g. Texlive. This should
already contain pdflatex and bibtex. The official Genes LaTex temaplate (see
 https://www.mdpi.com/authors/latex) is used.

`$REPOROOT` indicates the root directory of the cloned repository.

References in BibTex format can be found at `$REPOROOT/manucsript/references/hackSD-references.bib`

## Tex the manuscript
You have to run pdflatex twice after updatign the references with bibtex.

```
$cd $REPOROOT/manuscript
REPOROOT/manuscript$ pdflatex sd-hack.main.tex
REPOROOT/manuscript$ bibtex sd-hack.main.aux
REPOROOT/manuscript$ pdflatex sd-hack.main.tex
REPOROOT/manuscript$ pdflatex sd-hack.main.tex
```
