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
| 9 | Business Administration | BusAdmin | — | #6366F1 (indigo) | — | Mon 14:15-16:00 (lecture), Fri (exercises) |

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

## Macroeconomics Lecture Topics

Introduction & National-Income Accounts, The Goods Market, Financial Markets, The IS-LM Model, The Labour Market, Inflation, Economies in the Medium Run, Openness in Goods and Financial Markets, Economic Policy in the Open Economy, Long-term Growth, Innovation, Summary

Textbook: Olivier Blanchard, Macroeconomics (global edition), Pearson, 7th/8th/9th edition

## Law Course Structure

- Part 1 (before break): Constitutional Law (Prof. Patricia Egli) — Rechtsstaat, federalism, democracy, social justice, fundamental rights
- Part 2 (after break): Public International Law (Prof. Leena Grover) — UN system, human rights, humanitarian law, criminal law, environmental law, economic law
- Exercises: group 6, every other week
- Independent studies: every other week on Canvas

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
- `Introduction to financial management.pdf` — Finance textbook
- `HSGCalendar (2).ics` — HSG calendar
- `ble.ics` — Additional calendar
