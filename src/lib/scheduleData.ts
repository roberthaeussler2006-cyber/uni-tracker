// Week-specific reading and tutorial/exercise info for each subject
// Used to display contextual subtitles on Reading and Practice questions tasks
// Week numbers correspond to Kalenderwoche (KW)

interface WeekReading {
  reading?: string
  practice?: string
}

type SubjectSchedule = Record<number, WeekReading>

// Economics B: Macroeconomics (Blanchard, 7th Global Edition)
// Lectures: Monday 12:15-14:00
// Tutorials: biweekly
// Reading approach: full chapters (no sub-section jumping), extensions folded into lighter weeks
const macroSchedule: SubjectSchedule = {
  // KW 8 not tracked (before semester)
  9: {
    reading: 'Ch 3: The Goods Market (~20p)',
    practice: 'Tutorial 1: Intro & National Accounts (Ch 1, 2)',
  },
  10: {
    reading: 'Ch 4: Financial Markets I + Ch 14.1–14.2: Expectations (~37p)',
  },
  11: {
    reading: 'Ch 5–6: IS-LM Model + Extended IS-LM (~45p)',
    practice: 'Tutorial 2: Goods Market & Financial Markets',
  },
  12: {
    reading: 'Ch 7: The Labor Market (~20p)',
  },
  13: {
    reading: 'Ch 8: Phillips Curve & Inflation (~20p)',
    practice: 'Tutorial 3: The IS-LM Model',
  },
  // KW 14-15: Easter break
  16: {
    reading: 'Ch 9: The IS-LM-PC Model (~19p)',
    practice: 'Tutorial 4: Labor Market & Inflation',
  },
  17: {
    reading: 'Ch 17–18: Openness & Goods Market in Open Economy (~42p)',
  },
  18: {
    reading: 'Ch 19: Output, Interest Rate & Exchange Rate (~20p)',
    practice: 'Tutorial 5: IS-LM-PC Model',
  },
  19: {
    reading: 'Ch 10–11: Facts of Growth & Saving/Capital (~42p)',
    practice: 'Tutorial 6: Open Economy & Intl Macro',
  },
  20: {
    reading: 'Ch 12: Technological Progress + Ch 20.2, 20.4 (~32p)',
    practice: 'Tutorial 7: Growth & Innovation',
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

const scheduleData: Record<string, SubjectSchedule> = {
  Macro: macroSchedule,
  Law: lawSchedule,
  BusAdmin: busAdminSchedule,
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
  { kw: 9, topic: 'The Goods Market', reading: 'Ch 3', practice: 'Tutorial 1' },
  { kw: 10, topic: 'Financial Markets', reading: 'Ch 4 + Ch 14.1–14.2' },
  { kw: 11, topic: 'The IS-LM Model', reading: 'Ch 5–6', practice: 'Tutorial 2' },
  { kw: 12, topic: 'The Labor Market', reading: 'Ch 7' },
  { kw: 13, topic: 'Inflation & Phillips Curve', reading: 'Ch 8', practice: 'Tutorial 3' },
  { kw: '14–15', topic: 'Easter Break' },
  { kw: 16, topic: 'The IS-LM-PC Model', reading: 'Ch 9', practice: 'Tutorial 4' },
  { kw: 17, topic: 'Open Economy', reading: 'Ch 17–18' },
  { kw: 18, topic: 'International Macro', reading: 'Ch 19', practice: 'Tutorial 5' },
  { kw: 19, topic: 'Growth', reading: 'Ch 10–11', practice: 'Tutorial 6' },
  { kw: 20, topic: 'Innovation', reading: 'Ch 12 + Ch 20.2, 20.4', practice: 'Tutorial 7' },
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

const fullScheduleData: Record<string, ScheduleEntry[]> = {
  Macro: macroFullSchedule,
  Law: lawFullSchedule,
  BusAdmin: busAdminFullSchedule,
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
