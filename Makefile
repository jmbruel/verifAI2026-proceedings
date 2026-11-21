# Makefile for VERIF-AI 2026 LNCS proceedings
#
# llncs.cls lives at the workspace root. pdflatex does not search parent
# directories by default, so the front-matter target sets TEXINPUTS=..:
# to expose the workspace root to pdflatex when it runs inside front-matter/.
#
# Usage:
#   make              -- print this help message
#   make front-matter -- compile the front matter to PDF
#   make proceedings  -- compile the full proceedings to PDF
#   make clean        -- remove all LaTeX build artefacts

.PHONY: help front-matter proceedings clean

## Default target: print usage
help:
	@echo ""
	@echo "VERIF-AI 2026 proceedings build targets:"
	@echo ""
	@echo "  make front-matter   Compile front-matter/front-matter.tex to PDF"
	@echo "  make proceedings    Compile proceedings.tex to PDF"
	@echo "  make clean          Remove all LaTeX build artefacts"
	@echo ""

## Compile the front matter (preface + organization pages)
## TEXINPUTS=..: lets pdflatex find llncs.cls one directory up (workspace root).
## Run twice so cross-references and TOC are resolved.
front-matter:
	cd front-matter && TEXINPUTS=..: pdflatex front-matter.tex
	cd front-matter && TEXINPUTS=..: pdflatex front-matter.tex

## Compile the full proceedings master from the workspace root.
## llncs.cls is at the workspace root, so pdflatex finds it automatically.
## Run twice so cross-references and TOC are resolved.
proceedings:
	pdflatex proceedings.tex
	pdflatex proceedings.tex

## Remove LaTeX build artefacts from the workspace root and from front-matter/.
clean:
	rm -f *.aux *.log *.toc *.out *.synctex.gz proceedings.pdf
	rm -f front-matter/*.aux front-matter/*.log front-matter/*.toc \
	      front-matter/*.out front-matter/*.synctex.gz front-matter/front-matter.pdf
