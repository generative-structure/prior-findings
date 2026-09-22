# Follow-Up Is Not Discovery

Manuscript source, exhibits and build for *Follow-Up Is Not Discovery: What a
Record of Prior Audit Findings Can and Cannot Tell You*. The manuscript is
anonymized.

## Build

```bash
make            # prior-findings.pdf (pdflatex + bibtex)
make check      # undefined references in the last build
```

Requires a TeX distribution with `mathptmx`, `natbib`, `booktabs`, `endfloat`
and `amsthm`.

## Layout

| Path | Contents |
|---|---|
| `prior-findings.tex`, `sections/` | the manuscript: nine main-text sections and three appendices |
| `exhibits/` | every table (`.tex`), figure (`.pdf`, `.png`) and the numeric macro file `numbers.tex` |
| `refs.bib` | references |
| `scripts/exhibits.py` | regenerates Figure 1, Table 1, Figure 3 and Appendix Figure 4 from the simulation tables |
| `MATH_AUDITOR_CROSSWALK.md` | every main-text equation with its symbols, plain-language reading, numerical example and audit implication |
| `CLAIM_EVIDENCE_MAP.md` | every substantive claim mapped to a proposition, exact construction, empirical table, simulation result, regulatory source or citation |

## Numbers and reproducibility

No number in the manuscript is typed by hand. The prose references macros
defined in `exhibits/numbers.tex`, which the project's exhibit pipeline
generates from verified outputs and guards with assertions; the tables in
`exhibits/` are generated the same way. The three-program construction (Table
1) and the fixed-average-detection construction (Figure 3, Appendix Table 4)
are exact calculations from prespecified configurations; the finite-sample
figure and the multitype table are Monte Carlo results from a single
prespecified configuration with a fixed seed. `scripts/exhibits.py` asserts
the invariants those constructions require (for example that the observed risk
ratio equals the underlying ratio times the detection multiplier in every
column of Table 1) before writing anything.

## Data

All empirical data are public Federal Audit Clearinghouse bulk files
(https://www.fac.gov/data/download/), fiscal years 2016 through 2023, retrieved
in September 2026. No free-text finding narratives, restricted data or
nonpublic records were used. Appendix C of the manuscript describes the
acquisition, the panel construction, every specification, and the
reproduction path. The panel-construction code, the intermediate panel and
the simulation package are deposited separately as described there.

## Citation

A release of this repository is archived on Zenodo; the DOI will be added here
when the release is made.
