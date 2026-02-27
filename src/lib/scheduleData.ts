// Week-specific reading and tutorial/exercise info for each subject
// Used to display contextual subtitles on Reading and Practice questions tasks
// Week numbers correspond to Kalenderwoche (KW)

import { Week } from './types'
import { getFridayOfWeek, formatCountdown } from './weeks'

interface WeekReading {
  reading?: string
  practice?: string
}

type SubjectSchedule = Record<number, WeekReading>

// Economics B: Macroeconomics (Blanchard, 7th Global Edition)
// Lectures: Monday 12:15-14:00
// Tutorials: biweekly
// Reading includes sub-sections from later chapters alongside core chapters
const macroSchedule: SubjectSchedule = {
  8: {
    reading: 'Ch 1–2: Introduction & National Accounts (~44p)',
  },
  9: {
    reading: 'Ch 3, 5.1, 14.1–14.2: Goods Market & Expectations (~44p)',
    practice: 'Tutorial 1: Intro & National Accounts (Ch 1–2)',
  },
  10: {
    reading: 'Ch 4, 5.2: Financial Markets (~27p)',
  },
  11: {
    reading: 'Ch 5–6: IS-LM Model (~34p)',
    practice: 'Tutorial 2: Goods & Financial Markets (Ch 3–4, 5.1–5.2, 14.1–14.2)',
  },
  12: {
    reading: 'Ch 7: The Labor Market (~20p)',
  },
  13: {
    reading: 'Ch 8: Phillips Curve & Inflation (~20p)',
    practice: 'Tutorial 3: The IS-LM Model (Ch 5–6)',
  },
  // KW 14-15: Easter break
  16: {
    reading: 'Ch 9: The IS-LM-PC Model (~22p)',
    practice: 'Tutorial 4: Labor Market & Inflation (Ch 7–8)',
  },
  17: {
    reading: 'Ch 17: Goods Market in Open Economy (~20p)',
  },
  18: {
    reading: 'Ch 18.1, 19.2: International Macroeconomics (~12p)',
    practice: 'Tutorial 5: IS-LM-PC Model (Ch 9)',
  },
  19: {
    reading: 'Ch 10–11, 19.5, 20.2, 20.4: Growth (~54p)',
    practice: 'Tutorial 6: Open Economy (Ch 17, 18.1, 19.2)',
  },
  20: {
    reading: 'Ch 12: Technological Progress (~20p)',
    practice: 'Tutorial 7: Growth & Innovation (Ch 10–12, 19.5, 20.2, 20.4)',
  },
  21: {
    reading: 'Exam prep — review',
    practice: 'Tutorial 8: Q&A & Exam Discussion',
  },
}

// Constitutional Law & Public International Law
// Lectures: Tuesday 16:15-18:00, Room 09-010
// Exercises: biweekly Fridays (group 6), 10:15-12:00
// Part 1: Constitutional Law (Prof. Egli) — KW 8-13
// Part 2: Public International Law (Prof. Grover) — KW 16-21
// Textbooks: Egli, Introduction to Swiss Constitutional Law (3rd ed.)
//            Egli, Introduction to Public International Law (3rd ed.)
const lawSchedule: SubjectSchedule = {
  // KW 8 (Law Week 1): not tracked
  9: {
    reading: 'Egli Constitutional Law pp. 24–42: Rechtsstaat, Formal & Substantive Elements (~19p)',
  },
  10: {
    reading: 'Egli Constitutional Law pp. 43–69: Federalism, Three Levels of Government (~27p)',
    practice: 'Exercise: Distribution of Competencies (pp. 43–69)',
  },
  11: {
    reading: 'Egli Constitutional Law pp. 70–116: Democracy, Political Rights, Referendum (~47p)',
  },
  12: {
    reading: 'Egli Constitutional Law pp. 117–128: Fundamental Rights, Restrictions (~12p)',
    practice: 'Exercise: Human Rights (pp. 117–180)',
  },
  13: {
    reading: 'Egli Constitutional Law pp. 129–180: Civil Liberties, Expression, Property (~52p)',
  },
  // KW 14-15: Easter break
  16: {
    reading: 'Egli Public Intl Law pp. 1–19: Intl Legal System, Treaties (~19p)',
    practice: 'Exercise: Law of Treaties (pp. 8–19)',
  },
  17: {
    reading: 'Egli Public Intl Law pp. 20–48: Customary Intl Law, Subjects of PIL (~29p)',
  },
  18: {
    reading: 'Egli Public Intl Law pp. 49–71: UN Charter, Use of Force (~23p)',
    practice: 'Exercise: Law on the Use of Force (pp. 49–71)',
  },
  19: {
    reading: 'Egli Public Intl Law pp. 73–111: Human Rights, Humanitarian & Criminal Law (~39p)',
  },
  20: {
    reading: 'Egli Public Intl Law pp. 113–159: Economic Law, State Responsibility (~47p)',
    practice: 'Exercise: State Responsibility & ICJ (pp. 143–159)',
  },
  21: {
    reading: 'Q&A Session — review',
  },
}

// Business Administration B (2,102)
// Part 1: Business Ethics (Prof. Dr. Michael Festl) — KW 8-10
// Part 2: Financial Management (Dr. Simon Pfister) — KW 11-21
// Textbook (FM): Schäfer, Principles of Financial Management
// English Track: Mon 14:15-16:00
// Exercises: Fridays
// Exam: Written, digital, 180min, closed book. 180pts (45 Ethics + 135 FM)
const busAdminSchedule: SubjectSchedule = {
  // --- Business Ethics (KW 8-10) ---
  8: {
    practice: 'Coaching for Academic Term Paper',
  },
  9: {
    reading: 'Club of Rome: Limits to Growth (Intro) + Williams: Green Giants',
    practice: 'Exercise 1: Case Study South Pole',
  },
  10: {
    reading: 'Friedman: Capitalism & Freedom + Stout: Shareholder Value Myth (Preface, Intro, Ch 4 & 8)',
    practice: 'Exercise 2: Case Study Responsibility',
  },
  // --- Financial Management (KW 11-21) ---
  11: {
    reading: 'Schäfer Ch 1 & 2: Introduction',
  },
  12: {
    reading: 'Schäfer Ch 3 & 4: Statement of Financial Position',
    practice: 'Exercise 1: Intro & Statement of financial position',
  },
  13: {
    reading: 'Schäfer Ch 5 (excl. 5.5) & 6: Profit/Loss & Cash Flows',
    practice: 'Exercise 2: Statement of profit or loss',
  },
  // KW 14-15: Easter break
  16: {
    reading: 'Schäfer Ch 10: Management Accounting',
  },
  17: {
    reading: 'Schäfer Ch 11: Performance Measurement',
    practice: 'Exercise 3: Management accounting',
  },
  18: {
    reading: 'Schäfer Ch 12: Financing',
    practice: 'Exercise 4: Performance measurement',
  },
  // KW 19: St. Gallen Symposium & Dies academicus — no lecture
  20: {
    reading: 'Schäfer Ch 14: Mergers & Acquisitions + Guest Lecture',
    practice: 'Exercise 5: Financing & statement of cash flows',
  },
  21: {
    practice: 'Exercise 6: M&A and wrap up',
  },
  22: {
    reading: 'Optional repetition — review',
  },
}

// Philosophy: Introduction to Philosophical Thinking — Capitalism or Socialism?
// Weekly seminar: Mon 08:15-10:00
// One text (or excerpt) per week, oral exam at end
const philoSchedule: SubjectSchedule = {
  9: {
    reading: 'Smith, Marx & Engels, Fulcher, Newman (excerpts on Capitalism & Socialism)',
  },
  10: {
    reading: 'Friedman – Capitalism and Freedom (1962)',
  },
  11: {
    reading: 'Piketty – Capital in the Twenty-First Century (2014)',
  },
  12: {
    reading: 'Nozick – Anarchy, State, and Utopia (1974)',
  },
  13: {
    reading: 'Van Parijs – Why Surfers Should be Fed (1991)',
  },
  // KW 14-15: Easter break, KW 16: Review (no new reading)
  17: {
    reading: 'Scruton – The Truth in Socialism and Capitalism (2014)',
  },
  18: {
    reading: 'Cohen – Why not Socialism? (2009)',
  },
  19: {
    reading: 'Rand – Atlas Shrugged (1957)',
  },
  20: {
    reading: 'Fisher – Capitalist Realism (2009)',
  },
  // KW 21: Concluding session (no new reading)
}

const scheduleData: Record<string, SubjectSchedule> = {
  Macro: macroSchedule,
  Law: lawSchedule,
  BusAdmin: busAdminSchedule,
  Philo: philoSchedule,
}

// ─── Full semester schedule data for the Schedule Modal ───

export interface ScheduleEntry {
  kw: number | string
  topic: string
  reading?: string
  practice?: string
}

const macroFullSchedule: ScheduleEntry[] = [
  { kw: 8, topic: 'Introduction & National Accounts', reading: 'Ch 1–2' },
  { kw: 9, topic: 'The Goods Market', reading: 'Ch 3, 5.1, 14.1–14.2', practice: 'Tutorial 1' },
  { kw: 10, topic: 'Financial Markets', reading: 'Ch 4, 5.2' },
  { kw: 11, topic: 'The IS-LM Model', reading: 'Ch 5–6', practice: 'Tutorial 2' },
  { kw: 12, topic: 'The Labor Market', reading: 'Ch 7' },
  { kw: 13, topic: 'Inflation & Phillips Curve', reading: 'Ch 8', practice: 'Tutorial 3' },
  { kw: '14–15', topic: 'Easter Break' },
  { kw: 16, topic: 'The IS-LM-PC Model', reading: 'Ch 9', practice: 'Tutorial 4' },
  { kw: 17, topic: 'Goods Market in Open Economy', reading: 'Ch 17' },
  { kw: 18, topic: 'International Macroeconomics', reading: 'Ch 18.1, 19.2', practice: 'Tutorial 5' },
  { kw: 19, topic: 'Growth', reading: 'Ch 10–11, 19.5, 20.2, 20.4', practice: 'Tutorial 6' },
  { kw: 20, topic: 'Innovation', reading: 'Ch 12', practice: 'Tutorial 7' },
  { kw: 21, topic: 'Q&A / Exam Prep', practice: 'Tutorial 8' },
]

const lawFullSchedule: ScheduleEntry[] = [
  { kw: 8, topic: 'Introduction & Structural Principles', reading: 'pp. 1–23' },
  { kw: 9, topic: 'Rechtsstaat', reading: 'pp. 24–42' },
  { kw: 10, topic: 'Federalism', reading: 'pp. 43–69', practice: 'Exercise: Competencies' },
  { kw: 11, topic: 'Democracy & Political Rights', reading: 'pp. 70–116' },
  { kw: 12, topic: 'Fundamental Rights', reading: 'pp. 117–128', practice: 'Exercise: Human Rights' },
  { kw: 13, topic: 'Civil Liberties & Property', reading: 'pp. 129–180' },
  { kw: '14–15', topic: 'Easter Break' },
  { kw: 16, topic: 'Intl Legal System & Treaties', reading: 'PIL pp. 1–19', practice: 'Exercise: Treaties' },
  { kw: 17, topic: 'Customary Intl Law', reading: 'PIL pp. 20–48' },
  { kw: 18, topic: 'UN Charter & Use of Force', reading: 'PIL pp. 49–71', practice: 'Exercise: Use of Force' },
  { kw: 19, topic: 'Human Rights & Humanitarian Law', reading: 'PIL pp. 73–111' },
  { kw: 20, topic: 'Economic Law & State Responsibility', reading: 'PIL pp. 113–159', practice: 'Exercise: State Responsibility' },
  { kw: 21, topic: 'Q&A Session' },
]

const busAdminFullSchedule: ScheduleEntry[] = [
  { kw: 8, topic: 'Virtue Ethics, Deontology, Utilitarianism', practice: 'Coaching: Term Paper' },
  { kw: 9, topic: 'Sustainability', reading: 'Club of Rome + Green Giants', practice: 'Ex 1: South Pole' },
  { kw: 10, topic: 'Responsibility', reading: 'Friedman + Stout', practice: 'Ex 2: Responsibility' },
  { kw: 11, topic: 'FM: Introduction', reading: 'Schäfer Ch 1 & 2' },
  { kw: 12, topic: 'FM: Financial Position', reading: 'Schäfer Ch 3 & 4', practice: 'Ex 1: Financial Position' },
  { kw: 13, topic: 'FM: Profit/Loss & Cash Flows', reading: 'Schäfer Ch 5 (excl 5.5) & 6', practice: 'Ex 2: Profit or Loss' },
  { kw: '14–15', topic: 'Easter Break' },
  { kw: 16, topic: 'FM: Management Accounting', reading: 'Schäfer Ch 10' },
  { kw: 17, topic: 'FM: Performance Measurement', reading: 'Schäfer Ch 11', practice: 'Ex 3: Mgmt Accounting' },
  { kw: 18, topic: 'FM: Financing', reading: 'Schäfer Ch 12', practice: 'Ex 4: Performance' },
  { kw: 19, topic: 'St. Gallen Symposium (no lecture)' },
  { kw: 20, topic: 'FM: M&A + Guest Lecture', reading: 'Schäfer Ch 14', practice: 'Ex 5: Financing & Cash Flows' },
  { kw: 21, topic: '—', practice: 'Ex 6: M&A and Wrap Up' },
  { kw: 22, topic: 'Optional Repetition' },
]

const mathFullSchedule: ScheduleEntry[] = [
  { kw: 1, topic: 'Integrals' },
  { kw: 2, topic: 'Applications of Integral Calculus' },
  { kw: 3, topic: 'Matrices and Determinants' },
  { kw: 4, topic: 'Vectors' },
  { kw: 5, topic: 'Systems of Linear Equations' },
  { kw: 6, topic: 'Eigenvalues and Eigenvectors' },
  { kw: 7, topic: 'Difference Equations' },
  { kw: 8, topic: 'Applications of Linear Algebra' },
]

const philoFullSchedule: ScheduleEntry[] = [
  { kw: 8, topic: 'Introductions & Overview' },
  { kw: 9, topic: 'Capitalism & Socialism: Terminology', reading: 'Smith, Marx & Engels, Fulcher, Newman' },
  { kw: 10, topic: 'Capitalism and Freedom', reading: 'Friedman (1962)' },
  { kw: 11, topic: 'Capital in the Twenty-First Century', reading: 'Piketty (2014)' },
  { kw: 12, topic: 'Anarchy, State, and Utopia', reading: 'Nozick (1974)' },
  { kw: 13, topic: 'Why Surfers Should be Fed', reading: 'Van Parijs (1991)' },
  { kw: '14–15', topic: 'Easter Break' },
  { kw: 16, topic: 'Review First Half / Oral Exam Info' },
  { kw: 17, topic: 'The Truth in Socialism and Capitalism', reading: 'Scruton (2014)' },
  { kw: 18, topic: 'Why not Socialism?', reading: 'Cohen (2009)' },
  { kw: 19, topic: 'Atlas Shrugged', reading: 'Rand (1957)' },
  { kw: 20, topic: 'Capitalist Realism', reading: 'Fisher (2009)' },
  { kw: 21, topic: 'Concluding Session' },
]

const fullScheduleData: Record<string, ScheduleEntry[]> = {
  Macro: macroFullSchedule,
  Law: lawFullSchedule,
  BusAdmin: busAdminFullSchedule,
  Philo: philoFullSchedule,
  Math: mathFullSchedule,
}

export function getFullSchedule(subjectShortName: string): ScheduleEntry[] | null {
  return fullScheduleData[subjectShortName] || null
}

export function hasSchedule(subjectShortName: string): boolean {
  return subjectShortName in fullScheduleData
}

// ─── Schedule screenshot images ───

const scheduleImages: Record<string, string[]> = {
  Macro: ['/schedules/econ.png'],
  Law: ['/schedules/law-1.png', '/schedules/law-2.png', '/schedules/law-exercises-1.png', '/schedules/law-exercises-2.png'],
  BusAdmin: ['/schedules/ba.png'],
}

export function getScheduleImages(subjectShortName: string): string[] | null {
  return scheduleImages[subjectShortName] || null
}

export function getTaskSubtitle(
  subjectShortName: string,
  weekNumber: number,
  taskTitle: string
): string | null {
  const schedule = scheduleData[subjectShortName]
  if (!schedule) return null

  const titleLower = taskTitle.toLowerCase()

  // Readings are done this week for NEXT week's lecture
  if (titleLower.includes('reading')) {
    const nextWeekInfo = schedule[weekNumber + 1]
    return nextWeekInfo?.reading || null
  }

  // Practice/exercises are for THIS week's tutorial/exercise
  if (titleLower.includes('practice') || titleLower.includes('exercise')) {
    const weekInfo = schedule[weekNumber]
    return weekInfo?.practice || null
  }

  return null
}

// ─── Math B Sub-chapters (for progress tracking) ───

export interface MathSubchapter {
  id: string       // e.g. "1.1", "3.5"
  title: string    // short descriptive title
  chapter: number  // main chapter number (1-8)
}

export const MATH_SUBCHAPTERS: MathSubchapter[] = [
  // Chapter 1: Integrals (10 sub-chapters)
  { id: '1.1', title: 'Antiderivatives', chapter: 1 },
  { id: '1.2', title: 'Rules of integration', chapter: 1 },
  { id: '1.3', title: 'Substitution method', chapter: 1 },
  { id: '1.4', title: 'Integration by parts', chapter: 1 },
  { id: '1.5', title: 'Partial fractions', chapter: 1 },
  { id: '1.6', title: 'Definite integral', chapter: 1 },
  { id: '1.7', title: 'Fundamental theorem of calculus', chapter: 1 },
  { id: '1.8', title: 'Improper integrals', chapter: 1 },
  { id: '1.9', title: 'Numerical integration', chapter: 1 },
  { id: '1.10', title: 'Applications of integrals', chapter: 1 },

  // Chapter 2: Applications of Integral Calculus (2 sub-chapters)
  { id: '2.1', title: 'Area between curves', chapter: 2 },
  { id: '2.2', title: 'Economic applications', chapter: 2 },

  // Chapter 3: Matrices and Determinants (8 sub-chapters)
  { id: '3.1', title: 'Matrix basics', chapter: 3 },
  { id: '3.2', title: 'Matrix operations', chapter: 3 },
  { id: '3.3', title: 'Matrix multiplication', chapter: 3 },
  { id: '3.4', title: 'Transpose and special matrices', chapter: 3 },
  { id: '3.5', title: 'Inverse matrix', chapter: 3 },
  { id: '3.6', title: 'Determinants', chapter: 3 },
  { id: '3.7', title: 'Properties of determinants', chapter: 3 },
  { id: '3.8', title: 'Cramer\'s rule', chapter: 3 },

  // Chapter 4: Vectors (7 sub-chapters)
  { id: '4.1', title: 'Vector basics', chapter: 4 },
  { id: '4.2', title: 'Vector operations', chapter: 4 },
  { id: '4.3', title: 'Linear combinations', chapter: 4 },
  { id: '4.4', title: 'Scalar product', chapter: 4 },
  { id: '4.5', title: 'Cross product', chapter: 4 },
  { id: '4.6', title: 'Lines and planes', chapter: 4 },
  { id: '4.7', title: 'Distance calculations', chapter: 4 },

  // Chapter 5: Systems of Linear Equations (7 sub-chapters)
  { id: '5.1', title: 'Introduction to linear systems', chapter: 5 },
  { id: '5.2', title: 'Gaussian elimination', chapter: 5 },
  { id: '5.3', title: 'Solution sets', chapter: 5 },
  { id: '5.4', title: 'Homogeneous systems', chapter: 5 },
  { id: '5.5', title: 'Matrix rank', chapter: 5 },
  { id: '5.6', title: 'Applications', chapter: 5 },
  { id: '5.7', title: 'Leontief model', chapter: 5 },

  // Chapter 6: Eigenvalues and Eigenvectors (3 sub-chapters)
  { id: '6.1', title: 'Definition and computation', chapter: 6 },
  { id: '6.2', title: 'Diagonalization', chapter: 6 },
  { id: '6.3', title: 'Applications', chapter: 6 },

  // Chapter 7: Difference Equations (4 sub-chapters)
  { id: '7.1', title: 'First-order difference equations', chapter: 7 },
  { id: '7.2', title: 'Second-order difference equations', chapter: 7 },
  { id: '7.3', title: 'Stability analysis', chapter: 7 },
  { id: '7.4', title: 'Applications', chapter: 7 },

  // Chapter 8: Applications of Linear Algebra (2 sub-chapters)
  { id: '8.1', title: 'Markov chains', chapter: 8 },
  { id: '8.2', title: 'Input-output analysis', chapter: 8 },
]

// Expected sub-chapter to reach by each KW (semester weeks KW 9-22, Easter break KW 14-15)
// ~3.6 sub-chapters per teaching week across 12 teaching weeks
const mathExpectedPace: Record<number, string> = {
  9: '1.4',    // Week 1: 4 sub-chapters
  10: '1.8',   // Week 2: 4 sub-chapters
  11: '2.2',   // Week 3: finish Ch 1, all of Ch 2
  12: '3.4',   // Week 4: into Ch 3
  13: '3.8',   // Week 5: finish Ch 3
  // 14-15: Easter break
  16: '4.4',   // Week 6: into Ch 4
  17: '4.7',   // Week 7: finish Ch 4
  18: '5.4',   // Week 8: into Ch 5
  19: '5.7',   // Week 9: finish Ch 5
  20: '6.3',   // Week 10: all of Ch 6
  21: '7.4',   // Week 11: all of Ch 7
  22: '8.2',   // Week 12: all of Ch 8 — done
}

export function getMathExpectedSubchapter(weekNumber: number): string | null {
  // During Easter break, use KW 13 expectation
  if (weekNumber === 14 || weekNumber === 15) return mathExpectedPace[13] || null
  return mathExpectedPace[weekNumber] || null
}

export function getMathSubchapterIndex(subchapterId: string): number {
  return MATH_SUBCHAPTERS.findIndex((sc) => sc.id === subchapterId)
}

// ─── Law reading progress tracking ───

export interface LawExpectedPace {
  book: 'constitutional' | 'pil'
  page: number
}

// Expected page in the respective textbook by each KW
// Constitutional Law: Egli, Introduction to Swiss Constitutional Law (3rd ed.) — pp. 24–180
// Public International Law: Egli, Introduction to Public International Law (3rd ed.) — pp. 1–159
// Expected cumulative page by end of each week.
// Readings done in KW N prepare for KW N+1's lecture,
// so by end of KW N you should have finished schedule[N+1]'s reading.
const lawExpectedPace: Record<number, LawExpectedPace> = {
  9:  { book: 'constitutional', page: 69 },   // read pp.43-69 for KW 10
  10: { book: 'constitutional', page: 116 },  // read pp.70-116 for KW 11
  11: { book: 'constitutional', page: 128 },  // read pp.117-128 for KW 12
  12: { book: 'constitutional', page: 180 },  // read pp.129-180 for KW 13
  13: { book: 'constitutional', page: 180 },  // no new CL reading (Easter ahead)
  // 14-15: Easter break
  15: { book: 'pil', page: 19 },              // read PIL pp.1-19 for KW 16
  16: { book: 'pil', page: 48 },              // read PIL pp.20-48 for KW 17
  17: { book: 'pil', page: 71 },              // read PIL pp.49-71 for KW 18
  18: { book: 'pil', page: 111 },             // read PIL pp.73-111 for KW 19
  19: { book: 'pil', page: 159 },             // read PIL pp.113-159 for KW 20
  20: { book: 'pil', page: 159 },             // review
  21: { book: 'pil', page: 159 },             // review
}

export const LAW_CL_TOTAL = 180  // Constitutional Law max page
export const LAW_PIL_TOTAL = 159 // Public International Law max page
export const LAW_TOTAL_PAGES = LAW_CL_TOTAL + LAW_PIL_TOTAL // 339

export function getLawExpectedPace(weekNumber: number): LawExpectedPace | null {
  if (weekNumber === 14) return lawExpectedPace[13] || null
  return lawExpectedPace[weekNumber] || null
}

export function getLawCumulativePages(book: 'constitutional' | 'pil', page: number): number {
  return book === 'constitutional' ? page : LAW_CL_TOTAL + page
}

// ─── Macro (Economics B) reading progress tracking ───

// All assigned reading units with page counts — for chapter checklist tracker
export interface MacroReadingUnit {
  id: string       // unique identifier e.g. "ch3", "ch5.1"
  label: string    // display label
  pages: number    // estimated page count
  kw: number       // lecture week this is assigned for
}

export const MACRO_READING_UNITS: MacroReadingUnit[] = [
  // KW 8: Introduction & National Accounts
  { id: 'ch1', label: 'Ch 1', pages: 18, kw: 8 },
  { id: 'ch2', label: 'Ch 2', pages: 26, kw: 8 },
  // KW 9: The Goods Market
  { id: 'ch3', label: 'Ch 3', pages: 20, kw: 9 },
  { id: 'ch5.1', label: 'Ch 5.1', pages: 9, kw: 9 },
  { id: 'ch14.1-2', label: 'Ch 14.1–14.2', pages: 15, kw: 9 },
  // KW 10: Financial Markets
  { id: 'ch4', label: 'Ch 4', pages: 22, kw: 10 },
  { id: 'ch5.2', label: 'Ch 5.2', pages: 5, kw: 10 },
  // KW 11: The IS-LM Model
  { id: 'ch5.3+', label: 'Ch 5.3+', pages: 8, kw: 11 },
  { id: 'ch6', label: 'Ch 6', pages: 26, kw: 11 },
  // KW 12: The Labor Market
  { id: 'ch7', label: 'Ch 7', pages: 20, kw: 12 },
  // KW 13: Inflation & Phillips Curve
  { id: 'ch8', label: 'Ch 8', pages: 20, kw: 13 },
  // KW 16: The IS-LM-PC Model
  { id: 'ch9', label: 'Ch 9', pages: 22, kw: 16 },
  // KW 17: Open Economy
  { id: 'ch17', label: 'Ch 17', pages: 20, kw: 17 },
  // KW 18: International Macroeconomics
  { id: 'ch18.1', label: 'Ch 18.1', pages: 8, kw: 18 },
  { id: 'ch19.2', label: 'Ch 19.2', pages: 4, kw: 18 },
  // KW 19: Growth
  { id: 'ch10', label: 'Ch 10', pages: 18, kw: 19 },
  { id: 'ch11', label: 'Ch 11', pages: 24, kw: 19 },
  { id: 'ch19.5', label: 'Ch 19.5', pages: 4, kw: 19 },
  { id: 'ch20.2', label: 'Ch 20.2', pages: 4, kw: 19 },
  { id: 'ch20.4', label: 'Ch 20.4', pages: 4, kw: 19 },
  // KW 20: Innovation
  { id: 'ch12', label: 'Ch 12', pages: 20, kw: 20 },
]

// Cumulative pages of assigned reading by each KW
// Blanchard, Macroeconomics (7th Global Edition) — ~317 total assigned pages
// Includes full Ch 1–12, 17 plus sub-sections of Ch 14, 18, 19, 20
// Expected cumulative pages by end of each week.
// Readings done in KW N prepare for KW N+1's lecture.
const macroExpectedPace: Record<number, number> = {
  8:  88,    // Ch 1-2 (for KW 8) + Ch 3, 5.1, 14.1-14.2 (for KW 9)
  9:  115,   // + Ch 4 (22p) + Ch 5.2 (5p) for KW 10
  10: 149,   // + Ch 5.3+ (8p) + Ch 6 (26p) for KW 11
  11: 169,   // + Ch 7 (20p) for KW 12
  12: 189,   // + Ch 8 (20p) for KW 13
  13: 189,   // no new reading (Easter ahead)
  // 14: Easter
  15: 211,   // + Ch 9 (22p) for KW 16
  16: 231,   // + Ch 17 (20p) for KW 17
  17: 243,   // + Ch 18.1 (8p) + Ch 19.2 (4p) for KW 18
  18: 297,   // + Ch 10-11, 19.5, 20.2, 20.4 (54p) for KW 19
  19: 317,   // + Ch 12 (20p) for KW 20
  20: 317,   // review
  21: 317,   // review
}

export const MACRO_TOTAL_PAGES = 317

export function getMacroExpectedPages(weekNumber: number): number | null {
  if (weekNumber === 14) return macroExpectedPace[13] || null
  return macroExpectedPace[weekNumber] || null
}

// ─── Financial Management (BusAdmin) reading progress tracking ───

// Schäfer, Principles of Financial Management
// Assigned chapters: 1, 2, 3, 4, 5 (excl 5.5), 6, 10, 11, 12, 14
// Chapters 7–9 and 13 are skipped; reading is forward with small jumps
// FM part starts KW 11 (KW 8-10 is Business Ethics, no textbook tracking)
// Expected cumulative pages by end of each week.
// Readings done in KW N prepare for KW N+1's lecture.
const fmExpectedPace: Record<number, number> = {
  10: 25,    // read Ch 1&2 for KW 11
  11: 125,   // read Ch 3&4 for KW 12
  12: 162,   // read Ch 5&6 for KW 13
  13: 162,   // no new reading (Easter ahead)
  // 14: Easter
  15: 228,   // read Ch 10 for KW 16
  16: 268,   // read Ch 11 for KW 17
  17: 290,   // read Ch 12 for KW 18
  18: 290,   // no reading (KW 19 = Symposium)
  19: 343,   // read Ch 14 for KW 20
  20: 343,   // review
  21: 343,   // review
  22: 343,   // review
}

export const FM_TOTAL_PAGES = 343 // End of Ch 14 content

export function getFmExpectedPage(weekNumber: number): number | null {
  if (weekNumber === 14) return fmExpectedPace[13] || null
  return fmExpectedPace[weekNumber] || null
}

// ─── Countdown target logic ───

// Lecture/seminar times (dayOfWeek: 0=Sun, 1=Mon, ..., 5=Fri)
const MACRO_LECTURE = { day: 1, hour: 12, minute: 15 } // Monday 12:15
const LAW_LECTURE = { day: 2, hour: 16, minute: 15 }   // Tuesday 16:15
const PHILO_SEMINAR = { day: 2, hour: 8, minute: 15 }  // Tuesday 08:15

// Extract week numbers that have exercise/practice sessions
function getExerciseWeekNumbers(subjectShortName: string): number[] {
  const schedule = scheduleData[subjectShortName]
  if (!schedule) return []
  return Object.entries(schedule)
    .filter(([, info]) => info.practice)
    .map(([kw]) => Number(kw))
}

// Get the exercise date relevant to a specific viewed week
// If this week has an exercise → that exercise. Otherwise → next exercise after this week.
// If all exercises are past → most recent one (will show overdue).
function getExerciseDateForWeek(subjectShortName: string, weekNumber: number, weeks: Week[]): Date | null {
  const exerciseKWs = getExerciseWeekNumbers(subjectShortName)
  if (exerciseKWs.length === 0) return null

  // If this week has an exercise, use it
  if (exerciseKWs.includes(weekNumber)) {
    const week = weeks.find((w) => w.week_number === weekNumber)
    if (week) return getFridayOfWeek(week.start_date)
  }

  // Find the next exercise after this week
  const futureKWs = exerciseKWs.filter((kw) => kw > weekNumber).sort((a, b) => a - b)
  if (futureKWs.length > 0) {
    const week = weeks.find((w) => w.week_number === futureKWs[0])
    if (week) return getFridayOfWeek(week.start_date)
  }

  // All exercises are past — use the most recent one
  const pastKWs = exerciseKWs.filter((kw) => kw <= weekNumber).sort((a, b) => b - a)
  if (pastKWs.length > 0) {
    const week = weeks.find((w) => w.week_number === pastKWs[0])
    if (week) return getFridayOfWeek(week.start_date)
  }

  return null
}

// Compute the specific lecture date from a week's start_date (Monday)
function getLectureDateForWeek(weekStartDate: string, lecture: { day: number; hour: number; minute: number }): Date {
  const date = new Date(weekStartDate + 'T00:00:00')
  date.setDate(date.getDate() + (lecture.day - 1)) // day 1=Mon→+0, day 2=Tue→+1
  date.setHours(lecture.hour, lecture.minute, 0, 0)
  return date
}

// Get countdown info for a task (supports both countdown and overdue)
// weekNumber makes it week-aware: reading in KW N targets KW N+1's lecture
export function getTaskCountdown(
  subjectShortName: string,
  taskTitle: string,
  weeks: Week[],
  weekNumber: number
): { text: string; urgency: 'normal' | 'warning' | 'urgent' | 'overdue' } | null {
  if (subjectShortName !== 'Macro' && subjectShortName !== 'Law' && subjectShortName !== 'Philo') return null

  const titleLower = taskTitle.toLowerCase()
  const isReading = titleLower.includes('reading')
  const isExercise = titleLower.includes('practice') || titleLower.includes('exercise group') || titleLower.includes('notes sheet') || titleLower.includes('notes based')

  if (!isReading && !isExercise) return null

  let target: Date | null = null

  if (isReading) {
    // Reading done in KW N prepares for KW N+1's lecture/seminar
    const targetWeek = weeks.find((w) => w.week_number === weekNumber + 1)
    if (!targetWeek) return null
    const lecture = subjectShortName === 'Macro' ? MACRO_LECTURE
      : subjectShortName === 'Philo' ? PHILO_SEMINAR
      : LAW_LECTURE
    target = getLectureDateForWeek(targetWeek.start_date, lecture)
  } else {
    // Exercise: find the exercise for this week or the next one (Philo has no exercises)
    if (subjectShortName === 'Philo') return null
    target = getExerciseDateForWeek(subjectShortName, weekNumber, weeks)
  }

  if (!target) return null
  return formatCountdown(target)
}
