#!/usr/bin/env python
"""
exhibits.py -- regenerates Figure 1, Table 1, Figure 3 and Appendix Figure 4
from the verified simulation tables (observational_equivalence.csv,
fixed_observation_budget_validation.csv, finite_sample_validation.csv).

The committed files in exhibits/ are the outputs of this script and of the
project's exhibit pipeline; this script is provided so the four exhibits it
owns can be regenerated when the simulation tables are available at SIM
below.  Reads only; writes only inside exhibits/.  The same sanity gates as
the project's exhibit pipeline are asserted on the inputs.
"""

import os, pathlib
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = pathlib.Path(__file__).resolve().parent
CAR = HERE.parent
# location of the simulation tables; override with the SIM_TABLES environment variable
SIM = pathlib.Path(os.environ.get("SIM_TABLES", CAR / "simulation_tables"))
EX = CAR / "exhibits"
EX.mkdir(parents=True, exist_ok=True)

BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, INK2, INK3 = "#0b0b0b", "#52514e", "#8a8984"
GRID = "#dedcd6"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "font.size": 8.5,
    "axes.labelsize": 8.5,
    "axes.titlesize": 9,
    "axes.titleweight": "bold",
    "axes.edgecolor": INK3,
    "axes.linewidth": 0.6,
    "axes.labelcolor": INK2,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "legend.frameon": False,
    "lines.linewidth": 1.6,
    "figure.dpi": 200,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
    "mathtext.fontset": "dejavuserif",
})


def tidy(ax, ygrid=True):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if ygrid:
        ax.yaxis.grid(True, color=GRID, linewidth=0.5)
        ax.set_axisbelow(True)


def write_table(path, body):
    pathlib.Path(path).write_text(body.rstrip() + "\n")
    print(f"  -> {pathlib.Path(path).relative_to(CAR)}")


def write_fig(fig, stem):
    for ext in ("pdf", "png"):
        fig.savefig(EX / f"{stem}.{ext}")
    plt.close(fig)
    print(f"  -> exhibits/{stem}.pdf")


# ============================================================== load sources
worlds = pd.read_csv(SIM / "observational_equivalence.csv")
budget = pd.read_csv(SIM / "fixed_observation_budget_validation.csv")
finite = pd.read_csv(SIM / "finite_sample_validation.csv")

# ============================================================== sanity gates
assert (budget.auc_C == 0.5).all(), "latent AUC must be exactly 0.5 throughout"
assert budget.average_detection.round(10).nunique() == 1
assert budget.prevalence_F.round(10).nunique() == 1
for _, w in worlds.iterrows():
    assert abs(w.r0 * w.d0 - w.q0) < 1e-12 and abs(w.r1 * w.d1 - w.q1) < 1e-12
    assert abs(w.observed_risk_ratio - w.latent_risk_ratio * w.detection_ratio) < 1e-9, \
        "R_obs = R_lat x M must hold in every column"

# ============================================================ FIGURE 1 diagram
print("Figure 1 -- a finding history is also an observation history")
fig, ax = plt.subplots(figsize=(6.4, 3.3))
ax.set_xlim(0, 100)
ax.set_ylim(-8, 50)
ax.axis("off")

boxes = [
    (2.0, "The condition\nexists", "$C_t = 1$"),
    (26.5, "The audit\nlooks there", "scope, sample,\nprocedures"),
    (51.0, "The audit\ndetects it", "detection, $d$"),
    (75.5, "A finding is\nrecorded", "$F_t = 1$"),
]
W, H, Y = 22.5, 13.0, 28.0
for x, title, sub in boxes:
    ax.add_patch(FancyBboxPatch(
        (x, Y), W, H, boxstyle="round,pad=0,rounding_size=1.4",
        linewidth=0.9, edgecolor=INK3, facecolor="#f4f3ef"))
    ax.text(x + W / 2, Y + H * 0.66, title, ha="center", va="center",
            fontsize=9, color=INK, linespacing=1.25)
    ax.text(x + W / 2, Y + H * 0.22, sub, ha="center", va="center",
            fontsize=7, color=INK3, style="italic", linespacing=1.2)

for x, _, _ in boxes[:-1]:
    ax.add_patch(FancyArrowPatch(
        (x + W + 0.4, Y + H / 2), (x + W + 1.6, Y + H / 2),
        arrowstyle="-|>", mutation_scale=11, linewidth=1.3, color=INK2,
        shrinkA=0, shrinkB=0))

# two feedback routes from this period's record: to next period's scope and
# detection (d), and through corrective action to next period's condition (C)
ax.add_patch(FancyArrowPatch(
    (75.5 + W / 2, Y - 0.4), (26.5 + W / 2, Y - 0.4),
    connectionstyle="arc3,rad=-0.20", arrowstyle="-|>", mutation_scale=12,
    linewidth=1.5, linestyle=(0, (5, 2.5)), color=ORANGE,
    shrinkA=1, shrinkB=1))
ax.text(52.0, 20.5,
        "risk assessment, follow-up, scope\n$\\rightarrow$ next period's detection $d$",
        ha="center", va="top", fontsize=7.2, color=ORANGE, linespacing=1.3)
ax.add_patch(FancyArrowPatch(
    (75.5 + W / 2 - 4, Y - 0.4), (2.0 + W / 2, Y - 0.4),
    connectionstyle="arc3,rad=-0.60", arrowstyle="-|>", mutation_scale=12,
    linewidth=1.5, linestyle=(0, (2, 2)), color=BLUE,
    shrinkA=1, shrinkB=1))
ax.text(43.0, 2.5,
        "corrective action, if taken $\\rightarrow$ next period's condition $C_t$",
        ha="center", va="top", fontsize=7.2, color=BLUE, linespacing=1.3)
ax.text(92.5, 24.0, "the prior recorded\nfinding $F_{t-1}$ feeds\nback two ways",
        ha="center", va="top", fontsize=7.0, color=INK2, linespacing=1.25)

write_fig(fig, "ex1_diagram")

# ============================================== TABLE 1 three programs
print("Table 1 -- three programs, one record, with q, r, d and M")
Wd = {r.world: r for _, r in worlds.iterrows()}
ORDER = ["P", "O", "R"]
HEAD = {"P": "Persistence", "O": "Follow-up only", "R": "Remediation"}

ex2 = r"""\begin{table}[tbp]
\centering
\caption{\textbf{Three programs that produce exactly the same finding record.}
Read down each column. In all three, a program with no finding last year has a
5~percent chance of a recorded finding this year and a program with a finding
last year has a 20~percent chance, so the observed finding risk ratio
$R_{\mathrm{obs}}$ is 4 in every column. Underneath, the first program's
condition persisted, the second program's condition was no more likely than
before and only the looking changed, and the third program's condition became
\emph{half} as likely while follow-up became eight times as thorough. In each
column the observed ratio is the product of the underlying-condition ratio
$R_{\mathrm{lat}}$ and the follow-up detection multiplier $M$: $4 = 4 \times 1$,
$4 = 1 \times 4$, $4 = 0.5 \times 8$. Exact arithmetic, not simulation.}
\label{tab:worlds}
\small
\begin{tabular}{lccc}
\toprule
& """ + " & ".join(HEAD[w] for w in ORDER) + r""" \\
\midrule
\multicolumn{4}{l}{\emph{Chance the condition is there, $r$\dots}} \\
\quad after a clean year, $r_0$ & """ + " & ".join(f"{Wd[w].r0:.3f}" for w in ORDER) + r""" \\
\quad after a finding year, $r_1$ & """ + " & ".join(f"{Wd[w].r1:.3f}" for w in ORDER) + r""" \\
\addlinespace
\multicolumn{4}{l}{\emph{Chance the audit detects it if it is there, $d$\dots}} \\
\quad after a clean year, $d_0$ & """ + " & ".join(f"{Wd[w].d0:.3f}" for w in ORDER) + r""" \\
\quad after a finding year, $d_1$ & """ + " & ".join(f"{Wd[w].d1:.3f}" for w in ORDER) + r""" \\
\addlinespace
\multicolumn{4}{l}{\emph{What the record shows, $q = r \times d$\dots}} \\
\quad after a clean year, $q_0$ & """ + " & ".join(f"{Wd[w].q0:.2f}" for w in ORDER) + r""" \\
\quad after a finding year, $q_1$ & """ + " & ".join(f"{Wd[w].q1:.2f}" for w in ORDER) + r""" \\
\addlinespace
\textbf{Observed finding risk ratio}, $R_{\mathrm{obs}} = q_1/q_0$ & """ + " & ".join(f"\\textbf{{{Wd[w].observed_risk_ratio:.1f}}}" for w in ORDER) + r""" \\
\textbf{Underlying-condition risk ratio}, $R_{\mathrm{lat}} = r_1/r_0$ & """ + " & ".join(f"\\textbf{{{Wd[w].latent_risk_ratio:.1f}}}" for w in ORDER) + r""" \\
\textbf{Follow-up detection multiplier}, $M = d_1/d_0$ & """ + " & ".join(f"\\textbf{{{Wd[w].detection_ratio:.1f}}}" for w in ORDER) + r""" \\
\bottomrule
\end{tabular}
\end{table}"""
write_table(EX / "ex2_three_worlds.tex", ex2)

# ======================================= FIGURE 2 fixed detection, two panels
print("Figure 2 -- same average detection, stronger targeting (two panels)")
b0, b1 = budget.iloc[0], budget.iloc[-1]
fig, axes = plt.subplots(1, 2, figsize=(5.4, 2.5))

ax = axes[0]
ax.plot(budget.k, budget.auc_F, color=BLUE)
ax.plot(budget.k, budget.auc_C, color=ORANGE, linestyle="--")
ax.text(0.79, b1.auc_F + 0.010, "against the\nrecorded finding",
        ha="right", va="bottom", fontsize=7, color=BLUE, linespacing=1.15)
ax.text(0.79, 0.5 - 0.012, "against the\nunderlying condition",
        ha="right", va="top", fontsize=7, color=ORANGE, linespacing=1.15)
ax.set_ylim(0.43, 0.78)
ax.set_yticks([0.45, 0.55, 0.65, 0.75])
ax.set_xticks([0, 0.4, 0.8])
ax.set_xlabel("retargeting ($k$)")
ax.set_ylabel("AUC")
ax.set_title("A. Ranking power (AUC)", loc="left", color=INK)
tidy(ax)

ax = axes[1]
ax.axhline(0, color=INK3, linewidth=0.6)
ax.plot(budget.k, budget.brier_F - b0.brier_F, color=BLUE)
ax.plot(budget.k, budget.brier_C - b0.brier_C, color=ORANGE, linestyle="--")
ax.text(0.66, 0.0043, "against the\nunderlying condition\n(worse)",
        ha="right", va="bottom", fontsize=7, color=ORANGE, linespacing=1.15)
ax.text(0.80, -0.0044, "against the\nrecorded finding\n(better)",
        ha="right", va="top", fontsize=7, color=BLUE, linespacing=1.15)
ax.set_ylim(-0.0090, 0.0090)
ax.set_yticks([-0.005, 0, 0.005])
ax.set_xticks([0, 0.4, 0.8])
ax.set_xlabel("retargeting ($k$)")
ax.set_ylabel("change in Brier score")
ax.set_title("B. Prediction error (Brier)", loc="left", color=INK)
tidy(ax)

fig.subplots_adjust(wspace=0.45)
write_fig(fig, "ex3_fixed_budget")

cap3 = r"""\textbf{Same average detection, stronger targeting.} Both panels
hold average detection fixed: the average chance of catching an existing
condition stays at %s and the overall recorded finding rate stays at %s at
every point on the horizontal axis. That is a statement about detection, not
about audit hours, staffing or cost. Only the \emph{allocation} of detection
changes, moving toward the programs the score flags, and the score is
statistically independent of where the conditions are. Measured against the
recorded finding, the score improves: AUC rises from %s to %s, and the Brier
score falls from %s to %s. Measured against the underlying condition, the score
is worth nothing at any point on the axis (AUC exactly %s), and its prediction
error \emph{rises}, from %s to %s. Panel B plots both Brier series as the change
from the untargeted starting point. Exact calculation; the grid is in
Appendix~\ref{app:pred}, and the finite-sample version is
Figure~\ref{fig:finite} there. Solid series are measured against the recorded
finding, dashed series against the underlying condition.""" % (
    f"{b0.average_detection:.3f}", f"{b0.prevalence_F:.3f}",
    f"{b0.auc_F:.3f}", f"{b1.auc_F:.3f}",
    f"{b0.brier_F:.4f}", f"{b1.brier_F:.4f}",
    f"{b0.auc_C:.3f}",
    f"{b0.brier_C:.4f}", f"{b1.brier_C:.4f}")
write_table(EX / "ex3_caption.tex", r"\newcommand{\capFixedBudget}{%" + "\n" + cap3 + "}")

# ======================================= APPENDIX FIGURE finite sample
print("Appendix figure -- finite sample")
fig, ax = plt.subplots(figsize=(3.6, 2.5))
fb = finite[finite.scenario == "binary"].sort_values("N")
ax.fill_between(fb.N, fb["auc_F_pct_2.5"], fb["auc_F_pct_97.5"],
                color=BLUE, alpha=0.20, linewidth=0)
ax.plot(fb.N, fb.auc_F_estimate, color=BLUE)
ax.fill_between(fb.N, fb["auc_C_pct_2.5"], fb["auc_C_pct_97.5"],
                color=ORANGE, alpha=0.20, linewidth=0)
ax.plot(fb.N, fb.auc_C_estimate, color=ORANGE, linestyle="--")
ax.set_xscale("log")
ax.set_xlim(420, 80000)
ax.set_ylim(0.40, 0.95)
ax.set_yticks([0.4, 0.6, 0.8])
ax.set_xlabel("programs in the portfolio")
ax.set_ylabel("AUC")
ax.text(520, 0.935, "against the\nrecorded finding", fontsize=7, color=BLUE,
        va="top", linespacing=1.15)
ax.text(520, 0.425, "against the\nunderlying condition", fontsize=7,
        color=ORANGE, va="bottom", linespacing=1.15)
tidy(ax)
write_fig(fig, "exB3_finite")

f500 = fb[fb.N == 500].iloc[0]
capB3 = r"""\textbf{Not a large-sample artifact.} Sampling distributions of the
AUC of a score with no information about the underlying condition, measured
against the recorded finding (solid) and against the condition (dashed), at
portfolio sizes an audit organization actually has. Bands are the middle 95
percent across %d replications per point. At %d programs the band against the
record runs from %s to %s, while the band against the condition brackets 0.5 at
every size. A separate prespecified configuration from Figure~\ref{fig:budget};
simulation, seed %d.""" % (
    int(f500.reps), int(f500.N), f"{f500['auc_F_pct_2.5']:.3f}",
    f"{f500['auc_F_pct_97.5']:.3f}", int(f500.seed))
write_table(EX / "exB3_caption.tex", r"\newcommand{\capFinite}{%" + "\n" + capB3 + "}")
print("done")
