# HSG Uni Tracker

Personal academic progress tracker for HSG (University of St.Gallen) Assessment Year, Spring Semester 2026.

## How to Run

```bash
cd "/Users/roberthaeussler/Claude Coding/uni tracker/uni-tracker"
npm run dev        # Start dev server at http://localhost:3000
npm run build      # Production build
npm run lint       # ESLint
```

## Tech Stack

- **Framework:** Next.js 16 (App Router) + TypeScript + Tailwind CSS v4
- **Database:** Supabase PostgreSQL (project: `zcbxynnckauxmqdgantp`)
- **Auth:** PIN-based (env var `DASHBOARD_PIN`, cookie session)
- **Deployment:** Vercel

## Supabase

- Project ref: `zcbxynnckauxmqdgantp` (dedicated project, no other apps)
- All tables prefixed `tracker_` with RLS enabled + permissive anon policies
- Tables: `tracker_subjects`, `tracker_task_templates`, `tracker_weeks`, `tracker_tasks`, `tracker_subject_notes`, `tracker_deadlines`, `tracker_settings`

## Project Structure

```
src/
  app/
    layout.tsx          — Root layout (dark mode, Geist font)
    page.tsx            — Main dashboard with 4 tabs
    login/page.tsx      — PIN entry
    api/auth/route.ts   — PIN verification endpoint
  components/
    WeeklyView.tsx      — Weekly task view (default tab)
    SubjectsView.tsx    — Subject cards with completion stats
    AnalyticsView.tsx   — Heatmap + completion analytics
    DeadlinesView.tsx   — Deadline list with countdowns
    AddTaskModal.tsx    — Modal for adding custom tasks
    TaskItem.tsx        — Single task checkbox
    DailyTaskGrid.tsx   — Chinese daily checkboxes (Mon-Sun)
    WeekSelector.tsx    — Week navigation (< KW 9 >)
    ProgressRing.tsx    — Circular progress indicator
  lib/
    supabase.ts         — Supabase client
    types.ts            — TypeScript interfaces
    weeks.ts            — Week calculation utils
    auth.ts             — Cookie/session utils
  middleware.ts          — Auth check on all routes
```

## Semester: Spring 2026 (KW 9-22, Feb 24 - May 31)

Easter break: KW 14-15 (Apr 3-12)
Exam period: May 25 - Jun 12

## Subjects (9 total)

| # | Subject | Short | ECTS | Color | Exam Type | Schedule |
|---|---------|-------|------|-------|-----------|----------|
| 1 | Philosophy: Capitalism or Socialism? | Philo | 2 | #7C3AED (purple) | Oral, analog, closed book, lecture-free period | Tue 9:00-10:30 |
| 2 | Constitutional Law & Public Intl Law | Law | 5.5 | #3B82F6 (blue) | Written, digital, 180min, closed book | Tue 16:15-18:00 (lecture), Fri 10:15-12:00 (exercises group 6) |
| 3 | Chinesisch A1 | Chinese | — | #EF4444 (red) | — | Thu 10:15-12:00 |
| 4 | Economics B: Macroeconomics I | Macro | 5.5 | #10B981 (green) | Written, digital, 180min | Mon 12:15-14:00 |
| 5 | Integrative Project | IP | 4 | #F97316 (orange) | Presentation (50%) + written group paper (50%) | Wed 8:30-10:00 (lecture), Fri (exercises) |
| 6 | Accounting Exam | Accounting | 0 | #EAB308 (yellow) | Written, digital, 180min, closed book | Exam: March 14, 2026 |
| 7 | Academic Training Paper (ATP/WHA) | ATP | — | #14B8A6 (teal) | Group paper + oral exam | Regular work sessions |
| 8 | Mathematics B | Math | 3.5 | #EC4899 (pink) | Written, analog, 120min, closed book | Mon 16:15-18:00 (lecture), Thu 12:15-14:00 (exercises, biweekly) |
| 9 | Business Administration B | BusAdmin | 5.5 | #6366F1 (indigo) | Written, digital, 180min, closed book (180pts: 45 Ethics + 135 FM) | Mon 14:15-16:00 (lecture), Fri (exercises) |

## Task Templates (13 total)

- **Philo:** Reading assignment
- **Law:** Reading, Practice questions
- **Chinese:** Vocab/flashcard review (daily), Character writing practice (daily), Weekly lesson prep
- **Macro:** Reading, Practice questions
- **IP:** Group work session
- **ATP:** Work on paper
- **Math:** Ecoreps exercises
- **BusAdmin:** Weekly reading, Exercises

## Key Deadlines

| Date | Deadline | Subject |
|------|----------|---------|
| Feb 27 | IP Stammteamblatt Upload | IP |
| Mar 11 | IP Coaching Documents 1 | IP |
| Mar 14 | Accounting Exam | Accounting |
| Mar 18 | IP Coaching Documents 2 | IP |
| Apr 02 | IP/ATP Written Group Paper | ATP |
| Apr 03 | Easter Break Start | — |
| Apr 10 | IP/ATP Peer Feedback | ATP |
| Apr 12 | IP/ATP Oral Exam Submission | ATP |
| May 25 | Exam Period Start | — |
| Jun 12 | Exam Period End | — |

## Philosophy Schedule (weekly readings)

| Week | Topic | Reading |
|------|-------|---------|
| KW 9 (Feb 24) | Capitalism and Socialism, terminology | Smith, Marx & Engels, Fulcher, Newman |
| KW 10 (Mar 3) | Friedman - Capitalism and Freedom (1962) | test Capitalism 1 |
| KW 11 (Mar 10) | Piketty - Capital in the 21st Century (2014) | test Socialism 1 |
| KW 12 (Mar 17) | Nozick - Anarchy, State, and Utopia (1974) | test Capitalism 2 |
| KW 13 (Mar 24) | Van Parijs - Why Surfers Should be Fed (1991) | test Socialism 2 |
| KW 14 | Break | — |
| KW 15 (Apr 7) | Review first half + oral exam discussion | — |
| KW 16 (Apr 14) | Scruton - The Truth in Socialism and Capitalism (2014) | test Capitalism 3 |
| KW 17 (Apr 21) | Cohen - Why not Socialism? (2009) | test Capitalism 3 |
| KW 18 (Apr 28) | Rand - Atlas Shrugged (1957) | test Capitalism 4 |
| KW 19 (May 5) | Fisher - Capitalist Realism (2009) | test Socialism 4 |
| KW 20 (May 12) | Concluding session, reflections | — |

## Integrative Project Schedule

- SW 1 (KW 8): Lecture 1, Exercise 1
- SW 2 (KW 9): Lecture 2 (Plenary Discussion), Group Formation, Stammteamblatt upload by Friday
- SW 3 (KW 10): Lecture 3 (Guest Lecture - Kevin Fleck, CFO Flughafen Zurich AG)
- SW 4 (KW 11): Exercise 2 / Coaching Session 1 (docs due Wed Mar 11)
- SW 5 (KW 12): Exercise 3 / Coaching Session 2 (docs due Wed Mar 18)
- SW 6 (KW 13): —
- SW 7 (KW 14): Group paper deadline Thu Apr 2
- KW 15: Break
- SW 9-13 (KW 16-20): Oral Group Examinations (Mon 8am-12pm)

## Math B Topics

1. Integrals
2. Applications of Integral Calculus
3. Matrices and Determinants
4. Vectors
5. Systems of Linear Equations
6. Eigenvalues and Eigenvectors
7. Difference Equations
8. Applications of Linear Algebra

## Economics B (Macroeconomics) — Full Schedule

Textbook: Olivier Blanchard, Macroeconomics (7th Global Edition), Pearson — 581 pages
Lectures: Monday 12:15-14:00 | Tutorials: biweekly

Reading approach: full chapters (no sub-section jumping). Extensions (Ch 14, 20) folded into lighter weeks.
Total course reading: ~297 pages | Average: ~30p/week

### Weekly Reading Plan

| KW | Lecture Topic | Reading (before Mon lecture) | ~Pages |
|----|-------------|----------------------------|--------|
| 8 | Introduction & National Accounts | Ch 1, 2 | 46p |
| 9 | The Goods Market | Ch 3 | 20p |
| 10 | Financial Markets | Ch 4 + Ch 14.1–14.2 (Expectations) | 37p |
| 11 | The IS-LM Model | Ch 5 + 6 | 45p |
| 12 | The Labor Market | Ch 7 | 20p |
| 13 | Inflation | Ch 8 | 20p |
| 14-15 | **BREAK** | — | — |
| 16 | The IS-LM-PC Model | Ch 9 | 19p |
| 17 | Open Economy | Ch 17 + 18 | 42p |
| 18 | International Macroeconomics | Ch 19 | 20p |
| 19 | Growth | Ch 10 + 11 | 42p |
| 20 | Innovation | Ch 12 + Ch 20.2, 20.4 | 32p |
| 21 | Q&A | Review | — |

### Tutorials

| KW | # | Topics Covered |
|----|---|----------------|
| 9 | 1 | Intro & National Accounts |
| 11 | 2 | Goods Market & Financial Markets |
| 13 | 3 | The IS-LM Model |
| 16 | 4 | Labor Market & Inflation |
| 18 | 5 | IS-LM-PC Model |
| 19 | 6 | Open Economy & Intl Macro |
| 20 | 7 | Growth & Innovation |
| 21 | 8 | Q&A & Exam Discussion |

## Law — Full Agenda (Swiss Constitutional Law & Public International Law)

Lectures: Tuesday 16:15-18:00, Room 09-010
Exercises: biweekly Fridays, Group 6, 10:15-12:00

### Part 1: Constitutional Law (Prof. Dr. Patricia Egli)

| Law Wk | KW | Date | Reading (Egli, Swiss Constitutional Law, 3rd ed.) | Topics |
|--------|-----|------|-----|--------|
| 1 | 8 | 17/02 | pp. 1–23 | Introduction, Sources of Constitutional Law, Structural Principles |
| 2 | 9 | 24/02 | pp. 24–42 | Rechtsstaat, Formal & Substantive Elements, Legal Enactments |
| 3 | 10 | 03/03 | pp. 43–69 | Federalism, Three Levels of Government, Distribution of Competences |
| 4 | 11 | 10/03 | pp. 70–116 | Democracy, Political Rights, Popular Initiative & Referendum |
| 5 | 12 | 17/03 | pp. 117–128 | Fundamental Rights, Categories, Restrictions |
| 6 | 13 | 24/03 | pp. 129–180 | Civil Liberties, Freedom of Expression, Property, Economic Freedom |

**Guest Lecture (Week 5):** Wed 18/03/2026, 16:15-19:00, Room 02-001
- Dr. Martin Kayser (Judge, ret.) & Prof. Yossi Nehushtan (Keele University, UK)
- "Government by Consent: The Swiss Political System in Comparative Perspective"

### Part 2: Public International Law (Prof. Dr. Leena Grover)

| Law Wk | KW | Date | Reading (Egli, Public Intl Law, 3rd ed.) | Topics |
|--------|-----|------|-----|--------|
| 9 | 16 | 14/04 | pp. 1–19 | Intl Legal System, Sources: Treaties |
| 10 | 17 | 21/04 | pp. 20–48 | Customary Intl Law, Monism/Dualism, Subjects of PIL |
| 11 | 18 | 28/04 | pp. 49–71 | UN Charter & Organs, Use of Force |
| 12 | 19 | 05/05 | pp. 73–111 | Human Rights Law, Humanitarian Law, Criminal Law |
| 13 | 20 | 12/05 | pp. 113–159 | Economic Law, Environmental Law, State Responsibility |
| 14 | 21 | 19/05 | — | Q&A Session |

### Exercises (Fridays, biweekly)

**Part 1: Constitutional Law**

| Law Wk | KW | Date | Reading | Topic |
|--------|-----|------|---------|-------|
| 1 | 8 | 20/02 | pp. 1–23 | Sources & Interpretation of Constitutional Law |
| 3 | 10 | 06/03 | pp. 43–69 | Distribution of Competencies |
| 5 | 12 | 20/03 | pp. 117–180 | Human Rights |

**Part 2: Public International Law**

| Law Wk | KW | Date | Reading (PIL) | Topic |
|--------|-----|------|---------------|-------|
| 9 | 16 | 17/04 | pp. 8–19 | Law of Treaties |
| 11 | 18 | 01/05 | pp. 49–71 | Law on the Use of Force |
| 13 | 20 | 15/05 | pp. 143–159 | State Responsibility & ICJ |

## Business Administration B (2,102) — Full Schedule

5.5 ECTS | Exam: Written, digital, 180min, closed book | 180pts (45 Ethics + 135 FM)
Supplementary aids: Private laptop (compulsory, no tablets), mains adapter, LockDown Browser
English Track: Mon 14:15-16:00 | Exercises: Fridays

### Part 1: Business Ethics (Prof. Dr. Michael Festl) — KW 8-10

| KW | # | Topic | Reading (before lecture) |
|----|---|-------|------------------------|
| 8 | 1 | Basics: Virtue Ethics, Deontology, Utilitarianism | — |
| 9 | 2 | Sustainability | Club of Rome: Limits to Growth (Intro) + Williams: Green Giants |
| 10 | 3 | Responsibility | Friedman: Capitalism & Freedom + Stout: Shareholder Value Myth |

### Part 2: Financial Management (Dr. Simon Pfister) — KW 11-21

Textbook: Schäfer, Principles of Financial Management: A Practice-oriented Introduction

| KW | # | Topic | Reading (before lecture) |
|----|---|-------|------------------------|
| 11 | 4 | Introduction | Schäfer Ch 1 & 2 |
| 12 | 5 | Statement of financial position | Schäfer Ch 3 & 4 |
| 13 | 6 | Statement of profit or loss & cash flows | Schäfer Ch 5 (excl. 5.5) & 6 |
| 14-15 | — | **BREAK** | — |
| 16 | 7 | Management accounting | Schäfer Ch 10 |
| 17 | 8 | Performance Measurement | Schäfer Ch 11 |
| 18 | 9 | Financing | Schäfer Ch 12 |
| 19 | — | St. Gallen Symposium & Dies academicus | — |
| 20 | 10 | Mergers & Acquisitions + Guest Lecture | Schäfer Ch 14 |
| 21 | — | — | — |
| 22 | — | Optional Repetition | — |

### Exercises (Fridays)

**Business Ethics:**

| KW | Exercise |
|----|----------|
| 8 | Coaching for Academic Term Paper |
| 9 | Exercise 1: Case Study South Pole |
| 10 | Exercise 2: Case Study Responsibility |

**Financial Management:**

| KW | Exercise |
|----|----------|
| 12 | Exercise 1: Intro & Statement of financial position |
| 13 | Exercise 2: Statement of profit or loss |
| 17 | Exercise 3: Management accounting |
| 18 | Exercise 4: Performance measurement |
| 20 | Exercise 5: Financing & statement of cash flows |
| 21 | Exercise 6: M&A and wrap up |

## Context Files

Reference documents are stored in the parent directory (`../`):
- `philo.pdf` — Philosophy fact sheet
- `law.pdf` — Law fact sheet (same as `Course fact sheet.pdf`)
- `macro.pdf` — Macroeconomics fact sheet
- `math.pdf` — Mathematics B fact sheet
- `ip.pdf` — Integrative Project course fact sheet
- `accounting.pdf` — Accounting fact sheet
- `Fact sheet Integrative Project SpS26 (3).pdf` — Detailed IP exam rules (9 pages)
- `IP26_Schedule (1).pdf` — IP semester schedule
- `Case Study Flughafen Zurich AG (1).pdf` — IP case study
- `Integrative Project Lecture Slides.pdf` — IP lecture slides
- `Chinesisch A1 Schriftzeichenliste (1).pdf` — Chinese character list
- `Chinesisch A1 Vokabeln (3).xlsx` — Chinese vocabulary
- `Chinesisch_A1_Lernkarten.html` — Chinese flashcards app
- `Chinesisch_A1_Pinyin_Trainer.html` — Chinese pinyin trainer app
- `international law.pdf` — International law textbook
- `Macroeconomics 7th.pdf` — Blanchard textbook
- `Introduction to financial management.pdf` — Schäfer FM textbook
- `2,102_CourseandExaminationFactSheet.pdf` — Business Administration B fact sheet
- `HSGCalendar (2).ics` — HSG calendar
- `ble.ics` — Additional calendar

## PDF Notes Generation

When generating PDF study notes:

- **Always use proper mathematical notation** for ALL formulas, equations, and mathematical expressions. Never leave formulas as plain text (e.g., never write `M^d = $Y * L(i)` or `1/(1-c1)` in plain text).
- Use the `render_latex()` function and `formula_block()` method to render LaTeX formulas as images embedded in the PDF.
- Variable definitions (e.g., M^d = demand for money) should also be rendered as formula blocks, not plain text bullets.
- When a formula appears inline in a bullet point, split it: put the description in the bullet and the formula in a `formula_block()` call below it.
- Use `fontsize=12` for summary/reference formulas and `fontsize=14` (default) for main content formulas.
- The PDF generation script is at `notes/econ/generate_pdfs.py`.
