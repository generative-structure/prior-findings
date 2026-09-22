# CLAIM_EVIDENCE_MAP.md

Every substantive claim in the main text of `prior-findings.tex`, mapped
to its evidence. Row ids in parentheses refer to the project's internal claim map, which is
not part of this repository. Evidence types:
**P** formal proposition (Appendix A/B), **X** exact construction, **F** FAC
table, **S** simulation result, **R** regulatory source, **L** literature.

Source tokens: `SIM/` = the simulation tables; `FAC/` = the Federal Audit
Clearinghouse panel outputs. Both are project files outside this repository;
the committed exhibits are the verified outputs derived from them.

| id | claim | § | evidence type | source |
|---|---|---|---|---|
| K01 (C01) | Verification bias, imperfect detection, endogenous inspection and selective labels are established problems; audit research uses prior findings to measure risk and to set verification, and the most directly related finding studies document recurrence and predictive association and recognize condition-plus-detection but do not separately identify the latent-risk and observation components; this paper derives what remains identified and how design recovers the rest | 1 | L | ransohoff1978, begg1983, mackenzie2002, heckman1978, lakkaraju2017; keating2005, petrovits2011, rice2012, waymire2018 |
| K02 (C02) | `P(F_t=1\|f) = P(C_t=1\|f) × P(F_t=1\|C_t=1,f)`; `q_f = r_f d_f` | 1 | P | Prop. A.1 |
| K03 | Dropping no-false-positives weakens identification | 1, A | P (remark) | App. A remark after A.4; App. B false-positive check (`SIM/false_positive_sensitivity.csv`) |
| K04 (C05) | Persistence, follow-up-only and remediation worlds give the same record (0.05, 0.20) | 2, Table 1 | X | `SIM/observational_equivalence.csv`; asserted `q = r d` and `R_obs = R_lat M` in `scripts/s2_car_exhibits.py` |
| K05 | `R_obs = R_lat × M`; 4 = 4×1 = 1×4 = 0.5×8 | 2 | P + X | Prop. A.1; Table 1 rows |
| K06 (C06) | Remediation reversal iff `M > r0/r1` | 2 | P + X | Prop. A.4; Table 1 Remediation column (2 vs 8) |
| K07 (C03) | `r_f ≥ q_f`; `R_lat ∈ [q1, 1/q0]`, sharp; [0.20, 20] at Table 1 values | 3 | P + X | Prop. A.1, A.2 |
| K08 (C04) | Under `d1 ≥ d0`: `R_lat ≤ R_obs`; `R_obs < 1 ⇒ R_lat < 1` | 3 | P | Prop. A.3 |
| K09 (C04) | `1 ≤ M ≤ M̄ ⇒ R_lat ≥ R_obs/M̄`; 4/2 = 2; 3/1.5 = 2 | 3, 8 | P + arithmetic | Prop. A.3(ii) |
| K10 | Monotone detection is consistent with a follow-up regime but remains a substantive assumption about how follow-up affects detection of an existing condition; may hold for some condition types and not others | 3 | R (direction) + stated assumption | 2 CFR 200.514(e); failure cases stated in text |
| K11 (C07) | More history does not identify the unrestricted model | 3 | P | Prop. A.5 |
| K12 (C08) | Restricted latent-state models can be identified; identification comes from restrictions | 3 | L + P remark | allman2009; App. A remark |
| K13 | Single Audit definitions: major program, Type A/B, low-risk criteria, Compliance Supplement, follow-up rule | 4 | R | 2 CFR 200.518(b),(c)(1); 200.519(b)(2); 200.514(e) |
| K14 | Not every prior finding disqualifies low-risk Type A status | 4 fn | R | 2 CFR 200.518(c)(1) |
| K15 | Findings left uncorrected are a documented problem | 4 | L | gao2002 |
| K16 (C29) | Sample A holds the major-program-selection channel fixed, not audit intensity or condition-specific observation | 4, C | R + method | 2 CFR 200.514(e); `FAC_PANEL_CONTRACT.md` §6 |
| K17 | Prior literature: findings recur; auditee characteristics predict control problems; reported finding = condition × detection | 5 | L | keating2005, petrovits2011, waymire2018, gao2002, gao2024, waddell2023 |
| K18 (C30) | Panel 2,387,511; resolved 1,600,898; Sample A 206,926 (39,067 / 167,859); 45,952 auditees | 5, Table 6 | F | `FAC/fac_panel_exclusion_flow.csv`, `fac_history_state_taxonomy.csv` |
| K19 (C30) | Missing-prior program-years (366,506; 15.35%) excluded, finding rate 3.3% vs 2.1% | 5 | F | `FAC/fac_history_state_taxonomy.csv` |
| K20 (C24) | Any finding: 0.0766 vs 0.5783; Δ +0.5017 [0.4927, 0.5104]; RR 7.55 | 5, Table 2 | F | `FAC/fac_four_state_bootstrap.csv` |
| K21 (C22, C25) | `Δ_any = Δ_R + Δ_N + Δ_B`: 0.5017 = 0.3073 + 0.0456 + 0.1488, all intervals exclude zero | 5 | P (identity) + F | `FAC/fac_four_state_adjacent.csv`; identity asserted in `s1_exhibits.py` |
| K22 (C26, C27) | Any new = N + B: +0.1945 [0.1870, 0.2021], 0.0751 → 0.2696, RR 3.59; new-only RR 1.61; factor 2.23 definitional | 5 | F | same |
| K23 | Mixed periods arise from thorough repeat follow-up or multiple deficiencies; not separated | 5 | interpretation | stated as unidentified |
| K24 (C23) | Counts: +1.0683 = +0.7441 + +0.3243 | 5 | F | `FAC/fac_count_decomposition.csv` (additivity 0.00000) |
| K25 (C34) | FAC associations do not identify the mechanism (six candidates listed) | 5 | nonclaim | stated; Prop. A.5 |
| K26 (C31) | Recurrence share 61.2–90.9 percent (ζ = 0 to 1); mixed periods 25.9%; swing 29.7 | 5, Fig. 2, Table 8 | F | `FAC/fac_mixed_case_attribution_sensitivity.csv`, `fac_909_reconstruction.json` |
| K27 (C21) | Two-area opportunity arithmetic 0.36 vs 0.20; twelve-area null RR 0.72 | 5 | X + S | arithmetic; `SIM/multitype_basecase.csv` regime M0 |
| K28 (C32) | No first-in-area denominator in FAC; comparison not made | 5, C | data limitation | Compliance Supplement external; `FAC_EMPIRICAL_ADJUDICATION.md` §6 |
| K29 (C28) | Stable provenance: any 0.4885, any-new 0.1949 (n 167,017) | 5, Table 7 | F | `FAC/fac_four_state_stable_provenance.csv` |
| K30 (C28) | Validated link: R-only 0.2994, B 0.1454, any-new 0.1945, fifth state 0.0079; link resolves 61.0% | 5, C, Table 7 | F | `FAC/fac_four_state_adjacent.csv`; `exhibits/data/fac_validated_link_resolution.csv`, `fac_validated_link_fifth_state.csv` |
| K31 | Three-year history: n 94,360; any 0.3674; any-new 0.1716 | 5, Table 7 | F | `FAC/fac_four_state_cumulative.csv` |
| K32 (C19) | Condition-specific follow-up moves only repeats (+0.0394, 0, 0); category-level (+0.0279, +0.0454, 0); generalized (+0.0223, +0.0366, +0.1388) | 6, Table 3 | S | `SIM/multitype_basecase.csv`; common random numbers |
| K33 (C20) | Stable heterogeneity moves new-area findings (RR 1.02) but not as far as generalized scrutiny (2.06) at prespecified parameters | 6, A | S | `SIM/multitype_frailty.csv` |
| K34 | Table 3 narrows explanations, does not identify the mechanism; FAC pattern consistent with rows 2–3 and with worse programs | 6 | interpretation | Table 2 + Table 3 |
| K35 | Score-driven allocation loop is documented elsewhere | 7 | L | ensign2018, lum2016, lakkaraju2017, kleinberg2018 |
| K36 (C16) | Fixed average detection 0.40, prevalence 0.08: AUC vs F 0.500 → 0.704, AUC vs C 0.500 throughout; Brier vs F 0.0736 → 0.0688, vs C 0.1744 → 0.1792 | 7, Fig. 3, Table 4 | X | `SIM/fixed_observation_budget_validation.csv` (21 exact rows; invariances asserted) |
| K37 (C15) | Perfect calibration for F with flat C; 94-fold span | 7, B, Table 5 | P + S | Prop. B.2; `SIM/predictive_calibration_deciles.csv` |
| K38 (C18) | Pattern present at N = 500: AUC-F [0.629, 0.852], AUC-C brackets 0.5 | 7 (pointer), B, Fig. 4 | S | `SIM/finite_sample_validation.csv` |
| K39 (C17) | Fitted learner inherits the property (AUC-F 0.8328 vs 0.8332; AUC-C 0.4996) | 7 (pointer), B | S | `SIM/fitted_model_validation.csv` |
| K40 | Train/test split does not detect the problem | 7 | argument | same process, same targeting policy |
| K41 | M is `d1/d0`, not effort, hours, sample size, coverage or procedure counts; M is target-specific (defined for a condition, finding class or procedure) | 8 | definition | Section 2 definition; Section 8 opening |
| K42 | Reference observation under a common measurement rule: sample representative within each history group (may be stratified on history), same rule, common sensitivity, no effect on the condition, negligible false positives ⇒ `q_ref_1/q_ref_0 = R_lat`, `M = R_obs/R_lat`; same nominal procedure does not guarantee common sensitivity | 8, Table 4 | P + L | Prop. A.6; slemrod2019, levine2012 |
| K43 | High-sensitivity reference procedures anchor r and give `d = q/r`; exhaustive coverage removes sampling uncertainty but does not make detection perfect; anchor rests on sensitivity for the target condition | 8 | P (A.1) + stated qualification | — |
| K44 | Independent reference adjudication of a representative or weighted sample within each history group estimates d0, d1 only when the reference is accurate enough; an imperfect reference needs its own error process addressed; blind re-performance of the same work is not ground truth | 8 | L + argument | degroot2011 |
| K45 | Two procedures identify catch rates and missed conditions under conditional independence of failures and stable sensitivity within the stratum | 8 | P + L | Prop. A.7; mackenzie2002 |
| K46 | Quasi-random attention changes identify relative detection effects or tighten bounds only if they do not alter or select on the condition (exclusion restriction); absolute prevalence needs a sensitivity anchor | 8 | argument | stated restriction; levine2012 as example design |
| K47 | Procedure inputs support M̄ only through an explicit model; `M ≤ 1.5, R_obs = 3 ⇒ R_lat ≥ 2`, range [2, 3] with monotone detection | 8 | P (A.3) + arithmetic | — |
| K48 (C13) | Lagged-finding AUC bounded by (1+p)/2 in the observation-only model | B | P | App. B labeling trap; `SIM/predictive_validation_binary.csv` |
| K49 (C10, C11) | Observation-only dynamics: Markov record, `ρ_1 ≤ p`; RR 20 with ρ 0.095 | A | P + S | Prop. A.8; `SIM/observation_only_persistence.csv` |
| K50 (C33) | Horizons beyond t+1 not interpreted: attrition 34.8% / 53.5%; repeat rate 0.4661 → 0.3004 | C | F | `exhibits/data/fac_h2_eligibility.csv`; `FAC/p2/temporal_horizon_results.csv` |
| K51 | Category overlap among programs with findings twice: 86.4% share a category; Jaccard 0.664 | C | F | `exhibits/data/fac_category_overlap_source.csv` |

Nonclaims carried forward from the project map and honored in the text: no
latent-condition interpretation of FAC transitions (C34); no headline
recurrence share (C31); no first-in-area hazard (C32); no horizon results in
the main text (C33); no priority claim for any construction; no claim that
observation feedback dominates.
| K52 | Prior findings may contain information about discovery (persistent broad susceptibility; one weakness affecting several condition types); the record alone does not identify how much of that relationship reflects conditions and how much the observation process | 1, 6, 9 | interpretation + P | Prop. A.5; App. A frailty remark (`SIM/multitype_frailty.csv`) |
| K53 | Six designs summarized with what each supplies and its critical assumption; designs are not ranked | 8, Table 4 | summary of K42–K47 | `exhibits/ex8_designs.tex` (no numbers; summary table) |
