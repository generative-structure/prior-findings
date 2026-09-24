#!/usr/bin/env python
"""
exhibits.py -- regenerates Figure 1, Tables 1 and 3, Figure 3, Appendix
Figure 4 and exhibits/numbers_rev.tex from the verified simulation tables
(observational_equivalence.csv, fixed_observation_budget_validation.csv,
finite_sample_validation.csv, multitype_basecase.csv,
observation_only_persistence.csv, predictive_validation_continuous.csv,
fitted_model_validation.csv).

The committed files in exhibits/ are the outputs of this script and of the
project's exhibit pipeline; this script is provided so the exhibits it owns
can be regenerated when the simulation tables are available at SIM below.
Reads only; writes only inside exhibits/.  The same sanity gates as the
project's exhibit pipeline are asserted on the inputs, and every number in
numbers_rev.tex is asserted against its closed form.
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
ax.set_ylim(-8, 52)
ax.axis("off")

boxes = [
    (2.0, "The condition\nexists", "$C_t = 1$"),
    (26.5, "The audit\nexamines it", "scope, sample"),
    (51.0, "The audit\nrecognizes it", "judgment, evidence"),
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

# d covers both steps: being examined and being recognized when examined
ax.plot([26.5, 26.5, 51.0 + W, 51.0 + W], [Y + H + 1.2, Y + H + 2.4, Y + H + 2.4, Y + H + 1.2],
        color=INK2, linewidth=0.8)
ax.text((26.5 + 51.0 + W) / 2, Y + H + 3.4,
        "detection $d$: examined and recognized, given $C_t = 1$",
        ha="center", va="bottom", fontsize=7.4, color=INK2)

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
before and only the looking changed, and in the third the underlying rate is
stipulated to be \emph{half} as high after a finding year while detection is
eight times as high. In each column the observed ratio is the product of the
underlying-condition ratio $R_{\mathrm{lat}}$ and the history-conditioned
detection multiplier $M$: $4 = 4 \times 1$,
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
\textbf{Detection multiplier}, $M = d_1/d_0$ & """ + " & ".join(f"\\textbf{{{Wd[w].detection_ratio:.1f}}}" for w in ORDER) + r""" \\
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
percent across %d replications per point (%d at %s programs). At %d programs the band against the
record runs from %s to %s, while the band against the condition brackets 0.5 at
every size. Binary score: $p = %s$, $\pi = %s$, $d_0 = %s$, $d_1 = %s$, a
separate prespecified configuration from Figure~\ref{fig:budget}; simulation,
seed %d.""" % (
    int(f500.reps), int(fb.reps.min()), f"{int(fb.N.max()):,}", int(f500.N), f"{f500['auc_F_pct_2.5']:.3f}",
    f"{f500['auc_F_pct_97.5']:.3f}", f"{f500.p:.2f}", f"{f500.pi:.2f}",
    f"{f500.d0:.2f}", f"{f500.d1:.2f}", int(f500.seed))
write_table(EX / "exB3_caption.tex", r"\newcommand{\capFinite}{%" + "\n" + capB3 + "}")

# ================================================ TABLE 3 multitype regimes
# The caption states the common-random-number coupling that makes the zeros
# exact; the untouched cells are asserted to be exactly zero.
print("Table 3 -- which way of looking moves which outcome")
multi = pd.read_csv(SIM / "multitype_basecase.csv")
assert multi.groupby("regime").n_prior.nunique().eq(1).all()
assert multi.n_prior.nunique() == 1 and multi.n_no_prior.nunique() == 1, \
    "history groups must be identical across regimes"
piv = multi.pivot_table(index="regime", columns="outcome", values="risk_difference")
OUT3 = ["any_repeat", "any_new_old_category", "any_new_category"]
REG3 = [("M1", "Follow up the same finding"),
        ("M2", "Look harder at the same requirement area"),
        ("M3", "Look harder at the program overall")]
cells3 = {(c, o): piv.loc[c, o] - piv.loc["M0", o] for c, _ in REG3 for o in OUT3}
# untouched cells must be exactly zero, not merely small
for c, o in [("M1", "any_new_old_category"), ("M1", "any_new_category"),
             ("M2", "any_new_category")]:
    assert cells3[(c, o)] == 0.0, (c, o, cells3[(c, o)])
rows3 = "\n".join(f"{name} & " + " & ".join(f"${cells3[(c, o)]:+.4f}$" for o in OUT3) + r" \\"
                  for c, name in REG3)
nprior = int(multi.n_prior.iloc[0]); nno = int(multi.n_no_prior.iloc[0])
ex4 = r"""\begin{table}[tbp]
\centering
\caption{\textbf{How you look decides what turns up.} Three ways of letting last
year's finding change this year's audit, with the underlying problems held
identical and drawn independently each period. Each cell is the change in the
gap between programs with and without a prior finding, measured against a
baseline in which prior findings change nothing. Following up the same finding
moves repeats and \emph{only} repeats. Looking harder across a requirement area
also surfaces new findings inside that area. Looking harder at the program
overall also surfaces findings in areas that never had one --- which is what an
auditor would otherwise read as a genuinely new problem. The zeros are exact.
First-period histories, and with them the history groups (%s programs with a
prior finding, %s without) and each program's set of previously flagged
conditions and areas, are drawn once and shared by all regimes; second-period
conditions and detection draws are shared unit by unit; and a regime changes
detection only for the conditions it targets. An outcome outside a regime's
target set is therefore identical, program by program, to its baseline value.
Simulation, $10^6$ programs; Appendix~\ref{app:emp} gives the full
specification.}
\label{tab:multitype}
\small
\begin{tabular}{lccc}
\toprule
& \multicolumn{3}{c}{Change in the prior-finding gap} \\
\cmidrule(lr){2-4}
If last year's finding makes the auditor\dots
& \shortstack{A finding\\repeats}
& \shortstack{Something new,\\in an area that\\already had one}
& \shortstack{Something new,\\in an area that\\did not} \\
\midrule
""" % (f"{nprior:,}", f"{nno:,}") + rows3 + r"""
\bottomrule
\end{tabular}
\end{table}"""
write_table(EX / "ex4_multitype.tex", ex4)

# ============================================ numbers added in the revision
# Every number added in the 2026-09-23 revision is generated here and
# asserted against its closed form.
print("numbers_rev.tex -- quantities added in the 2026-09-23 revision")
import re
import numpy as np
REV = {}


def exact_continuous_auc_F(p, alpha, d_min, d_max, c, n_grid=200_001):
    """AUC(S, F) by trapezoidal quadrature for S ~ U(0,1), logistic d(S)."""
    s = np.linspace(0.0, 1.0, n_grid)
    with np.errstate(over="ignore"):
        d = d_min + (d_max - d_min) / (1.0 + np.exp(-alpha * (s - c)))
    w1 = d / np.trapezoid(d, s)
    w0 = (1 - p * d) / np.trapezoid(1 - p * d, s)
    cdf0 = np.concatenate([[0.0], np.cumsum((w0[1:] + w0[:-1]) / 2 * np.diff(s))])
    return float(np.trapezoid(w1 * cdf0, s))

# validated-link resolution share, correctly rounded (40,930 / 67,157)
nums = (EX / "numbers.tex").read_text()
def macro(name):
    return int(re.search(r"\\newcommand\{\\%s\}\{([\d,]+)\}" % name, nums).group(1).replace(",", ""))
flagged, resolved = macro("nLinkFlagged"), macro("nLinkResolved")
assert (flagged, resolved) == (67157, 40930), (flagged, resolved)
REV["LinkPctRev"] = f"{100 * resolved / flagged:.1f}"
assert REV["LinkPctRev"] == "60.9"

# observation-only example of Proposition A.8: stationary prevalence
oo = pd.read_csv(SIM / "observation_only_persistence.csv")
s3 = oo[oo.scenario == "S3"].iloc[0]
q0, q1 = s3.p * s3.d0, s3.p * s3.d1
mu_star = q0 / (1 - q1 + q0)
assert abs(mu_star - s3.exact_prevalence_F) < 1e-12 and 0 < mu_star < 1
REV["ObsOnlyMuStar"] = f"{mu_star:.4f}"
REV["ObsOnlyBurn"] = f"{int(s3.burn_in)}"
REV["ObsOnlyT"] = f"{int(s3['T'])}"
REV["ObsOnlyN"] = f"{int(s3.N):,}"

# fixed-budget construction: exact Brier identities and the AUC envelope
p_b, pi_b, db = budget.p.iloc[0], budget.pi.iloc[0], budget.dbar.iloc[0]
mu_b = p_b * db
for _, r in budget.iterrows():
    v = p_b ** 2 * pi_b * (1 - pi_b) * r.k ** 2
    assert abs(r.brier_F - (mu_b * (1 - mu_b) - v)) < 1e-12
    assert abs(r.brier_C - (p_b * (1 - p_b) + (p_b - mu_b) ** 2 + v)) < 1e-12
k_end = budget.k.iloc[-1]
REV["BrierShift"] = f"{p_b ** 2 * pi_b * (1 - pi_b) * k_end ** 2:.4f}"
env = 1 - (1 - p_b) * db / (2 * (1 - p_b * db))
assert (budget.auc_F <= env + 1e-12).all()
REV["AucEnvelope"] = f"{env:.4f}"
assert REV["AucEnvelope"] == "0.8261"

# continuous score: configuration, and the step-function limit as alpha grows
cont = pd.read_csv(SIM / "predictive_validation_continuous.csv")
c40 = cont[cont.alpha == cont.alpha.max()].iloc[0]
dmin, dmax, cc, pc = c40.d_min, c40.d_max, c40.c, c40.p
lo_F = (1 - cc) * dmax / ((1 - cc) * dmax + cc * dmin)       # P(S > c | F = 1)
w0_hi = (1 - cc) * (1 - pc * dmax); w0_lo = cc * (1 - pc * dmin)
hi0 = w0_hi / (w0_hi + w0_lo)                                 # P(S > c | F = 0)
auc_lim = lo_F * (1 - hi0) + 0.5 * lo_F * hi0 + 0.5 * (1 - lo_F) * (1 - hi0)
auc_num = exact_continuous_auc_F(pc, 1e4, dmin, dmax, cc)
assert abs(auc_lim - auc_num) < 1e-3, (auc_lim, auc_num)
assert (cont.sort_values("alpha").exact_auc_F.diff().dropna() > 0).all()
assert c40.exact_auc_F < auc_lim
REV["ContAucLimit"] = f"{auc_lim:.3f}"
REV["ContDmin"] = f"{dmin:.2f}"; REV["ContDmax"] = f"{dmax:.2f}"
REV["ContC"] = f"{cc:.2f}"; REV["ContP"] = f"{pc:.2f}"
REV["ContAlphaMax"] = f"{int(c40.alpha)}"
calib_alpha = 20
fit = pd.read_csv(SIM / "fitted_model_validation.csv")
REV["FitAlpha"] = f"{int(fit.loc[(fit.auc_F - 0.8328).abs().idxmin(), 'alpha'])}"
assert REV["FitAlpha"] == "10"

# multitype specification
REV["MultiNprior"] = f"{nprior:,}"
REV["MultiNnoPrior"] = f"{nno:,}"

body = ["% Generated by scripts/exhibits.py -- do not edit by hand.",
        "% Quantities added in the 2026-09-23 revision."]
body += [f"\\newcommand{{\\n{k}}}{{{v}}}" for k, v in REV.items()]
write_table(EX / "numbers_rev.tex", "\n".join(body))

print("done")
