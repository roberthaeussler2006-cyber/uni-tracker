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

const scheduleData: Record<string, SubjectSchedule> = {
  Macro: macroSchedule,
  Law: lawSchedule,
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
