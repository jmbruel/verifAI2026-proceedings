# Makefile for VERIF-AI 2026 LNCS proceedings
#
# llncs.cls lives at the workspace root. pdflatex does not search parent
# directories by default, so TEXINPUTS exposes the workspace root when
# compiling inside front-matter/ (..) or papers/<folder>/ (../..).
#
# Usage:
#   make                               -- print this help message
#   make front-matter                  -- compile front-matter/front-matter.tex to PDF
#   make paper DIR=papers/p1992        -- compile one LaTeX paper independently (optional MAIN=foo.tex)
#   make papers                        -- compile all LaTeX papers found under papers/*/
#   make proceedings                   -- assemble proceedings.pdf via pdfpages
#   make clean                         -- remove root and front-matter LaTeX build artefacts
#   make clean-papers                  -- remove LaTeX build artefacts inside papers/*/

PDFLATEX := pdflatex -interaction=nonstopmode -halt-on-error

.PHONY: help front-matter paper papers proceedings clean clean-papers

## Default target: print usage
help:
	@echo ""
	@echo "VERIF-AI 2026 proceedings build targets:"
	@echo ""
	@echo "  make front-matter              Compile front-matter/front-matter.tex to PDF"
	@echo "  make paper DIR=papers/p<id>    Compile one LaTeX paper inside its folder (optional MAIN=file.tex)"
	@echo "  make papers                    Compile every LaTeX paper folder under papers/*/"
	@echo "  make proceedings               Assemble proceedings.pdf (front matter + pdfpages)"
	@echo "  make clean                     Remove root and front-matter LaTeX build artefacts"
	@echo "  make clean-papers              Remove LaTeX build artefacts inside papers/*/"
	@echo ""

## Compile the front matter (preface + organization pages)
## Run twice so running heads and cross-references are resolved.
front-matter:
	cd front-matter && TEXINPUTS=..: $(PDFLATEX) front-matter.tex
	cd front-matter && TEXINPUTS=..: $(PDFLATEX) front-matter.tex

## Compile a single LaTeX paper independently inside its own folder.
## Auto-detects the main .tex (at top level or inside subfolders like source/, src/, etc.,
## skipping standalone figure files) if MAIN is omitted.
## Runs bibtex automatically if the .aux file references a .bib database and no .bbl exists.
paper:
	@if [ -z "$(DIR)" ] || [ ! -d "$(DIR)" ]; then \
		echo "Usage: make paper DIR=papers/p<submission-id> [MAIN=relative/path.tex]"; \
		exit 1; \
	fi
	@set -e; \
	main="$(MAIN)"; \
	if [ -z "$$main" ]; then \
		main=$$(python3 -c 'import os, re, sys; root=sys.argv[1]; cands=[]; \
			[cands.append(os.path.relpath(os.path.join(dp,fn), root)) \
			 for dp,_,fns in os.walk(root) for fn in sorted(fns) \
			 if fn.endswith(".tex") and "\\begin{document}" in open(os.path.join(dp,fn), errors="ignore").read() \
			 and not re.search(r"\\documentclass(?:\[[^\]]*\])?\{standalone\}", open(os.path.join(dp,fn), errors="ignore").read())]; \
			cands.sort(key=lambda p: (p.count(os.sep), 0 if os.path.basename(p)=="main.tex" else 1, p)); \
			print(cands[0] if cands else "")' "$(DIR)"); \
	fi; \
	if [ -z "$$main" ]; then \
		echo "[SKIP] $(DIR): no LaTeX main file with \\begin{document} found (Word paper or empty?)"; \
		exit 0; \
	fi; \
	srcdir="$(DIR)/$$(dirname "$$main")"; \
	texfile="$$(basename "$$main")"; \
	base="$${texfile%.tex}"; \
	echo "==> Compiling $(DIR)/$$main"; \
	cd "$$srcdir"; \
	TEXINPUTS="$(CURDIR):" $(PDFLATEX) "$$texfile"; \
	if grep -q '\\bibdata' "$$base.aux" 2>/dev/null && [ ! -f "$$base.bbl" ]; then \
		bibtex "$$base" || true; \
		TEXINPUTS="$(CURDIR):" $(PDFLATEX) "$$texfile"; \
	fi; \
	TEXINPUTS="$(CURDIR):" $(PDFLATEX) "$$texfile"; \
	echo "[OK] $(DIR)/$$(dirname "$$main")/$$base.pdf"

## Compile all LaTeX papers present in papers/*/ independently and report summary.
papers:
	@failed=""; count=0; \
	for d in papers/*/; do \
		[ -d "$$d" ] || continue; \
		count=$$((count + 1)); \
		if ! $(MAKE) --no-print-directory paper DIR="$${d%/}"; then \
			failed="$$failed $$d"; \
		fi; \
	done; \
	if [ "$$count" -eq 0 ]; then \
		echo "No paper directories found under papers/."; \
	elif [ -n "$$failed" ]; then \
		echo ""; \
		echo "[FAIL] Compilation failed for:$$failed"; \
		exit 1; \
	else \
		echo ""; \
		echo "[OK] Processed $$count paper folder(s)."; \
	fi

## Assemble the full proceedings preview PDF from the workspace root.
## Run twice so the Table of Contents and PDF bookmarks are resolved.
proceedings:
	$(PDFLATEX) proceedings.tex
	$(PDFLATEX) proceedings.tex

## Remove LaTeX build artefacts from the workspace root and from front-matter/.
clean:
	rm -f *.aux *.log *.toc *.out *.blg *.fls *.fdb_latexmk *.synctex.gz proceedings.pdf
	rm -f front-matter/*.aux front-matter/*.log front-matter/*.toc \
	      front-matter/*.out front-matter/*.blg front-matter/*.fls \
	      front-matter/*.fdb_latexmk front-matter/*.synctex.gz front-matter/front-matter.pdf

## Remove LaTeX build artefacts inside papers/*/ (preserves .tex, .bib, .bbl, figures, and PDFs).
clean-papers:
	find papers -mindepth 2 -type f \( \
		-name '*.aux' -o -name '*.log' -o -name '*.toc' -o -name '*.out' \
		-o -name '*.blg' -o -name '*.fls' -o -name '*.fdb_latexmk' -o -name '*.synctex.gz' \
	\) -delete
