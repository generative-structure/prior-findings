#!/usr/bin/env python
"""
format_tables.py -- journal formatting for the tables in exhibits/.

Elsevier style puts a short caption above a table and its notes below the
table body. Each table's caption is split into a title (the bold lead
sentence, or the first sentence) and notes, and the notes move below the
tabular inside \\tablenotes{...} (defined in preamble.tex). Idempotent: a
table that already carries \\tablenotes is left alone. Nothing but the
placement of the caption text changes; the script asserts that every number
and every word in the file survives unchanged.
"""
import pathlib, re, sys

EX = pathlib.Path(__file__).resolve().parent.parent / "exhibits"
TABLES = ["ex2_three_worlds.tex", "ex4_multitype.tex", "ex5_sample.tex",
          "ex6_four_state.tex", "ex8_designs.tex", "exB1_budget.tex",
          "exB2_calibration.tex", "exC1_specs.tex", "exC2_zeta.tex"]


def braced(s, start):
    """Return the index just past the brace group opening at s[start]."""
    assert s[start] == "{"
    depth = 0
    for i in range(start, len(s)):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return i + 1
    raise ValueError("unbalanced braces")


def words(t):
    t = re.sub(r"\\(textbf|tablenotes|caption|emph)\b", " ", t)
    return sorted(re.findall(r"[A-Za-z0-9.]+", t))


def split_caption(cap):
    cap = cap.strip()
    if cap.startswith(r"\textbf{"):
        end = braced(cap, len(r"\textbf"))
        return cap[len(r"\textbf{"):end - 1].strip(), cap[end:].strip()
    m = re.match(r"(.+?\.)\s+(.*)", cap, re.S)
    return (m.group(1), m.group(2)) if m else (cap, "")


def fmt(path):
    src = path.read_text()
    if r"\tablenotes{" in src:
        return False
    i = src.index(r"\caption{")
    j = braced(src, i + len(r"\caption"))
    title, notes = split_caption(src[i + len(r"\caption{"):j - 1])
    out = src[:i] + r"\caption{" + title + "}" + src[j:]
    if notes:
        k = out.rindex(r"\end{tabular}") + len(r"\end{tabular}")
        out = out[:k] + "\n\\tablenotes{" + notes + "}" + out[k:]
    assert words(src) == words(out), path.name
    path.write_text(out)
    return True


if __name__ == "__main__":
    for name in TABLES:
        print(("  formatted " if fmt(EX / name) else "  unchanged ") + name)
