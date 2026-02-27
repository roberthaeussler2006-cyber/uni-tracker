# Uni Tracker - Claude Code Instructions

## PDF Notes Generation

When generating PDF study notes:

- **Always use proper mathematical notation** for ALL formulas, equations, and mathematical expressions. Never leave formulas as plain text (e.g., never write `M^d = $Y * L(i)` or `1/(1-c1)` in plain text).
- Use the `render_latex()` function and `formula_block()` method to render LaTeX formulas as images embedded in the PDF.
- Variable definitions (e.g., M^d = demand for money) should also be rendered as formula blocks, not plain text bullets.
- When a formula appears inline in a bullet point, split it: put the description in the bullet and the formula in a `formula_block()` call below it.
- Use `fontsize=12` for summary/reference formulas and `fontsize=14` (default) for main content formulas.
- The PDF generation script is at `notes/econ/generate_pdfs.py`.

## Project Structure

- `notes/` — Subject folders (`econ/`, `law/`, `ba/`) containing generated PDF notes
- `reference/` — Source materials (textbooks, fact sheets, calendars, etc.)
