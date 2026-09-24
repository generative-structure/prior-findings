# Build for "Follow-Up Is Not Discovery".
#
#   make            compile prior-findings.pdf
#   make exhibits   regenerate the script-owned exhibits and numbers_rev.tex,
#                   then apply the journal table format (needs the simulation
#                   tables; see scripts/exhibits.py)
#   make check      undefined references / citations in the last build
#   make clean      remove LaTeX intermediates
#
# Every number in the prose is a macro in exhibits/numbers.tex or
# exhibits/numbers_rev.tex; nothing is typed by hand.

DOC := prior-findings
SECTIONS := $(wildcard sections/*.tex)

.PHONY: all pdf exhibits check clean

all: pdf

$(DOC).pdf: $(DOC).tex preamble.tex refs.bib $(SECTIONS) $(wildcard exhibits/*)
	pdflatex -interaction=nonstopmode -halt-on-error $(DOC).tex
	bibtex $(DOC)
	pdflatex -interaction=nonstopmode -halt-on-error $(DOC).tex
	pdflatex -interaction=nonstopmode -halt-on-error $(DOC).tex

pdf: $(DOC).pdf

exhibits:
	python3 scripts/exhibits.py
	python3 scripts/format_tables.py

check:
	@! grep -E "undefined|Undefined" $(DOC).log && echo "no undefined references" || echo "undefined references found"

clean:
	rm -f $(DOC).aux $(DOC).log $(DOC).bbl $(DOC).blg $(DOC).out $(DOC).toc $(DOC).pdf
