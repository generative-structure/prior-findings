# Follow-Up Is Not Discovery

Manuscript source, exhibits and build for *Follow-Up Is Not Discovery: What a
Record of Prior Audit Findings Can and Cannot Tell You*. The manuscript is
anonymized.

## Build

```bash
make            # prior-findings.pdf (pdflatex + bibtex)
make exhibits   # regenerate the script-owned exhibits from the simulation tables
make check      # undefined references in the last build
```

Requires a TeX distribution with `mathptmx`, `natbib`, `caption`, `booktabs`,
`array`, `amsthm` and the `elsarticle-harv` bibliography style (all in TeX
Live), and Python 3 with `pandas`, `numpy` and `matplotlib` for
`make exhibits`.

## Layout

| Path | Contents |
|---|---|
| `prior-findings.tex`, `preamble.tex`, `sections/` | the manuscript: nine numbered sections, a data-availability statement and Appendices A–C |
| `exhibits/` | every table (`.tex`), figure (`.pdf`) and the numeric macro files `numbers.tex` and `numbers_rev.tex` |
| `refs.bib` | references |
| `scripts/exhibits.py` | regenerates Fig. 1, Tables 1 and 3, Fig. 3, Fig. B.1 and `numbers_rev.tex` from the simulation tables (set `SIM_TABLES` to their directory) |
| `scripts/format_tables.py` | puts each table's notes below its body; changes no word or number (asserted) |

## Numbers and reproducibility

No number in the manuscript is typed by hand. The prose references macros
defined in `exhibits/numbers.tex`, which the project's exhibit pipeline
generates from verified outputs and guards with assertions, and in
`exhibits/numbers_rev.tex`, which `scripts/exhibits.py` generates and checks
against closed forms. The tables in `exhibits/` are generated the same way.
The three-program construction (Table 1) and the fixed-average-detection
construction (Fig. 3, Table B.1) are exact calculations from prespecified
configurations. The finite-sample figure and the multitype table (Table 3) are
Monte Carlo results from a single prespecified configuration with a fixed
seed. Before writing anything, `scripts/exhibits.py` asserts the invariants
those constructions require. For example: the observed risk ratio equals the
underlying ratio times the detection multiplier in every column of Table 1;
the Table 3 cells outside a regime's target set are exactly zero; and the
Brier identities and AUC envelope of Appendix B hold on the whole
fixed-detection grid. Appendix C gives the full simulation specification and
the panel-construction rules.

## Data

All empirical data are public Federal Audit Clearinghouse bulk files
(https://www.fac.gov/data/download/), fiscal years 2016 through 2023, retrieved
in September 2026. No free-text finding narratives, restricted data or
nonpublic records were used. Appendix C of the manuscript describes the
acquisition, the panel construction, every specification, and the
reproduction path. The panel-construction code, the intermediate panel and
the simulation package are deposited separately as described there.

## Citation

Releases of this repository are archived on Zenodo. The concept DOI
[10.5281/zenodo.22906808](https://doi.org/10.5281/zenodo.22906808) always
resolves to the latest version.
