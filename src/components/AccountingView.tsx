'use client'

import { useState } from 'react'

type Section = 'overview' | 'plan' | 'exams' | 'materials'

interface Chapter {
  number: number
  title: string
  bookPages: string
  topics: string[]
  priority: 'high' | 'medium' | 'low'
  examWeight: string
}

interface ExamTopic {
  name: string
  avg: number
  chapters: string
  tip: string
}

const CHAPTERS: Chapter[] = [
  {
    number: 0,
    title: 'Why Financials Matter',
    bookPages: 'pp. 21-49',
    topics: [
      'Introduction to companies & organizations',
      'Four building blocks: assets, liabilities, expenses, revenues',
      'Basics of bookkeeping',
      'History of financials',
      'Accounting software (QuickBooks, Abacus, etc.)',
    ],
    priority: 'low',
    examWeight: 'Not directly tested - background knowledge',
  },
  {
    number: 1,
    title: 'Starting a Small Business and Cash Book',
    bookPages: 'pp. 50-76',
    topics: [
      'Cash Book concept',
      'Cash effect vs. Profit effect',
      'T-Accounts for revenue & expenses',
      'Statement of Profit or Loss',
      'Real company examples (Ryanair, Walmart, Hilti)',
    ],
    priority: 'high',
    examWeight: 'Foundation for everything - must understand first',
  },
  {
    number: 2,
    title: 'Asset Accounts',
    bookPages: 'pp. 77-105',
    topics: [
      'Debit side vs. Credit side of accounts',
      'Full double-entry bookkeeping structure',
      'Year-end bookings & financial statements',
      'Legal obligations for record keeping',
      'Opening and closing entries',
    ],
    priority: 'high',
    examWeight: 'Core concept tested across many topics',
  },
  {
    number: 3,
    title: 'Financing and Statement of Financial Position',
    bookPages: 'pp. 106-134',
    topics: [
      'Financing and investing decisions',
      'Cash-oriented financial ratios (Cash, Quick, Current ratio)',
      'Security-oriented ratios (Equity ratio, LT debt ratio)',
      'Profitability ratios (ROE, ROA, ROS, Gross Profit Margin)',
      'Statement of Financial Position (Balance Sheet)',
    ],
    priority: 'high',
    examWeight: '~6 pts on financial ratios every year',
  },
  {
    number: 4,
    title: 'Sole Proprietorship and Trading Company',
    bookPages: 'pp. 135-158',
    topics: [
      'Private account as sub-account of equity',
      'Owner transactions (salary, payments, withdrawals)',
      'Trading goods: purchasing, selling, inventory correction',
      'Mark-up vs. Margin calculation',
      'Expenses & Sales from trading goods accounts',
    ],
    priority: 'high',
    examWeight: '~14 pts trading + ~3 pts sole proprietorship',
  },
  {
    number: 5,
    title: 'Payment Transactions and Production',
    bookPages: 'pp. 160-181',
    topics: [
      'Cash difference and Petty Cash',
      'Credit card payments (3% commission)',
      'Prepayments (paid to suppliers / received from customers)',
      'Anticipatory Tax in Switzerland',
      'Production company accounts (purchasing, selling, produced goods)',
      'Year-end financial statements for production',
    ],
    priority: 'high',
    examWeight: '~10-11 pts every exam',
  },
  {
    number: 6,
    title: 'Value Adjustments (Depreciation)',
    bookPages: 'pp. 183-202',
    topics: [
      'Straight-line vs. Declining balance depreciation',
      'Direct vs. Indirect depreciation methods',
      'Selling non-current assets (gain/loss)',
      'Loss from receivables (customer payment default)',
      'Debt collection process',
      'Reversal of incorrect entries',
    ],
    priority: 'high',
    examWeight: '~5-9 pts on depreciation & receivables',
  },
  {
    number: 7,
    title: 'Land + Building, Accruals, Provisions',
    bookPages: 'pp. 204-226',
    topics: [
      'Land + building: mixed private & business use',
      'Income and expense accounts for land & building',
      'Discontinue business segment',
      '4 types of accruals (pre/post-paid revenue/expenses)',
      'Provisions: uncertain but likely obligations',
      'Closing of the year with accruals',
    ],
    priority: 'high',
    examWeight: '~6 pts accruals + ~4-5 pts land & building',
  },
  {
    number: 8,
    title: 'Marketable Securities',
    bookPages: 'pp. 227-247',
    topics: [
      'Securities, Financial assets, Investments (3 asset classes)',
      'Market value vs. Purchase value (direct/indirect)',
      'Bonds: nominal value, interest rate, maturity, accrued interest',
      'Shares: market price, nominal value, dividends',
      'Anticipatory tax on dividends (65% shareholder / 35% government)',
      'Year-end valuation (book accrued income + total value change)',
    ],
    priority: 'high',
    examWeight: '~11-13 pts - HIGHEST weighted topic!',
  },
  {
    number: 9,
    title: 'Joint-stock Companies',
    bookPages: 'pp. 248-272',
    topics: [
      'Founding: share capital, non paid-in capital',
      'Increasing shareholders capital',
      'Profit distribution (Art. 671 OR)',
      'Legal reserves: first & second allocation',
      'Base dividend vs. surplus dividend vs. profit sharing bonus',
      'Loss scenarios and recovery',
    ],
    priority: 'medium',
    examWeight: '~5-6 pts every exam',
  },
  {
    number: 10,
    title: 'Valuation Reserves',
    bookPages: 'pp. 273-288',
    topics: [
      'Undervaluing assets / Overvaluing liabilities',
      'Generating valuation reserves (4 methods)',
      'Dissolving valuation reserves (3 methods)',
      'Legal basis in Switzerland',
      'Actual vs. Reported profit',
    ],
    priority: 'medium',
    examWeight: '~4-5 pts every exam',
  },
  {
    number: 11,
    title: 'Multi-year Perspective',
    bookPages: 'pp. 290-300',
    topics: [
      'Multi-year consequences of transactions',
      'Decisions under stable operating business',
      'Make or Buy decisions',
      'CapEx or Leasing',
      'Automation or Customization',
    ],
    priority: 'low',
    examWeight: '~5 pts as board decisions (2025 exam)',
  },
]

const EXAM_TOPICS: ExamTopic[] = [
  { name: 'Trading company', avg: 14, chapters: 'Ch 4', tip: 'Practice booking entries for purchases, sales, returns, discounts, inventory corrections' },
  { name: 'Marketable securities', avg: 12, chapters: 'Ch 8', tip: 'Master bonds + shares valuation, anticipatory tax (65/35 split), year-end bookings' },
  { name: 'Payment & production', avg: 11, chapters: 'Ch 5', tip: 'Credit card commissions, prepayments, production accounts (purchasing/selling/produced)' },
  { name: 'Depreciation & receivables', avg: 7, chapters: 'Ch 6', tip: 'Straight-line vs. declining balance, direct vs. indirect, debt collection process' },
  { name: 'Interpretation of booking entries', avg: 7, chapters: 'Ch 1-8', tip: 'Given a booking entry, explain what happened - requires understanding ALL account types' },
  { name: 'Financial ratios', avg: 6, chapters: 'Ch 3', tip: 'Memorize formulas: Cash/Quick/Current ratio, Equity ratio, ROE, ROA, ROS, Gross Profit Margin' },
  { name: 'Accruals & provisions', avg: 6, chapters: 'Ch 7', tip: 'Know 4 accrual types, Dec 31 booking + Jan 1 reversal, provisions vs. accruals distinction' },
  { name: 'P&L in reporting format', avg: 6, chapters: 'Ch 2-3', tip: 'Know the format: Revenue > Gross Income > EBITDA > EBIT > EBT > Profit of period' },
  { name: 'Joint-stock company', avg: 5, chapters: 'Ch 9', tip: 'Art. 671 OR profit distribution, legal reserves (5% to 20%), base/surplus dividend' },
  { name: 'Land & building', avg: 5, chapters: 'Ch 7', tip: 'Mixed use bookings, income/expense accounts for L&B, lease of own premises' },
  { name: 'Valuation reserves', avg: 4, chapters: 'Ch 10', tip: 'Generate by undervaluing assets/overvaluing liabilities, dissolve through devaluation/outflow' },
  { name: 'Profit & cash effect', avg: 4, chapters: 'Ch 1', tip: 'For each transaction: does it affect cash? does it affect profit? Both? Neither?' },
  { name: 'Inventory changes', avg: 4, chapters: 'Ch 4-5', tip: 'Increase = decrease expenses, decrease = increase expenses (year-end only)' },
  { name: 'Sole proprietorship', avg: 4, chapters: 'Ch 4', tip: 'Private account, owner withdrawals/claims, disclosed as equity in closing' },
  { name: 'Miscellaneous', avg: 6, chapters: 'All', tip: 'Various smaller questions across all topics' },
  { name: 'Board decisions', avg: 5, chapters: 'Ch 11', tip: 'Compare multi-year financial plans, analyze ratios, recommend investment strategy' },
]

const MATERIALS = [
  { name: 'Textbook', file: 'FinancialAccounting_Book_2025_partsAll.pdf', type: 'book', desc: 'Full course textbook (315 pages, 12 chapters) by Dr. Simon Pfister' },
  { name: 'Lecture Summary', file: 'FinancialAccounting11 Summary.pdf', type: 'summary', desc: 'Lecture 11 recap slides - great overview of all topics' },
  { name: 'Exam Info Sheet 2025', file: '2025_June_InfoSheets.pdf', type: 'info', desc: 'Chart of accounts, P&L format, support material given during exam' },
  { name: 'Past Paper: June 2023', file: '2023 June.pdf', type: 'exam', desc: 'Full exam paper (24 pages, 100 points, 3 hours)' },
  { name: 'Solution: June 2023', file: '2023 June_solution.pdf', type: 'solution', desc: 'Official solution for June 2023 exam' },
  { name: 'Past Paper: June 2024', file: '2024 June (1).pdf', type: 'exam', desc: 'Full exam paper (24 pages, 100 points, 3 hours)' },
  { name: 'Solution: June 2024', file: '2024 June_solution.pdf', type: 'solution', desc: 'Official solution for June 2024 exam' },
  { name: 'Solution: Jan 2025', file: '2025_January_Solution.pdf', type: 'solution', desc: 'Official solution for January 2025 exam' },
]

const STUDY_PHASES = [
  {
    phase: 1,
    title: 'Foundations (Start here)',
    duration: '3-4 days',
    chapters: [1, 2],
    description: 'Understand what accounting IS. Learn: Cash Book, T-Accounts, debit vs. credit, double-entry bookkeeping, opening/closing entries. This is the language of accounting - nothing else makes sense without it.',
    actions: [
      'Read Chapter 1 carefully - follow Tom\'s business story',
      'Practice drawing T-accounts and making booking entries',
      'Understand: every transaction has TWO sides (debit + credit)',
      'Do ALL exercises in Chapter 1 and 2',
    ],
  },
  {
    phase: 2,
    title: 'Financial Statements & Ratios',
    duration: '2-3 days',
    chapters: [3],
    description: 'Learn the two key statements: Statement of Financial Position (Balance Sheet) and Statement of Profit or Loss (P&L). Master the financial ratios - they appear every exam.',
    actions: [
      'Memorize the P&L reporting format (Revenue > Gross Income > EBITDA > EBIT > EBT > Profit)',
      'Learn ALL ratio formulas: Cash, Quick, Current, Equity, ROE, ROA, ROS, Gross Profit Margin',
      'Practice calculating ratios from real company examples (H&M, Julius Baer)',
    ],
  },
  {
    phase: 3,
    title: 'Trading & Sole Proprietorship',
    duration: '3-4 days',
    chapters: [4],
    description: 'Trading company is worth ~14 points on every exam - the MOST valuable chapter. Learn purchasing, selling, inventory, mark-up vs. margin.',
    actions: [
      'Master: Expenses for trading goods / Sales from trading goods accounts',
      'Learn returns, trade discounts, quantity discounts, transport costs',
      'Practice inventory corrections (increase vs. decrease)',
      'Understand mark-up vs. margin calculation',
      'Learn sole proprietorship: private account, owner income',
    ],
  },
  {
    phase: 4,
    title: 'Payments & Production',
    duration: '2-3 days',
    chapters: [5],
    description: 'Worth ~10-11 points. Credit card payments, prepayments, and production company specifics.',
    actions: [
      'Credit card: 3% commission = financial expense, learn the two-step booking',
      'Prepayments: liability (from customers) vs. asset (to suppliers)',
      'Production: purchasing side, selling side, produced goods in stock',
      'Understand changes in inventory for semi-finished/finished goods',
    ],
  },
  {
    phase: 5,
    title: 'Depreciation & Value Adjustments',
    duration: '2-3 days',
    chapters: [6],
    description: 'Worth ~5-9 points. How assets lose value over time, and dealing with customers who don\'t pay.',
    actions: [
      'Compare straight-line vs. declining balance depreciation',
      'Compare direct (reduce asset) vs. indirect (VA account) methods',
      'Practice selling old assets at gain/loss',
      'Learn the debt collection process and booking entries',
      'Practice reversal of incorrect entries',
    ],
  },
  {
    phase: 6,
    title: 'Land & Building, Accruals, Provisions',
    duration: '2-3 days',
    chapters: [7],
    description: 'Worth ~10 points combined. Accruals are tricky but important.',
    actions: [
      'Learn 4 accrual types: pre-paid revenue, post-paid revenue, pre-paid expense, post-paid expense',
      'Practice Dec 31 accrual booking + Jan 1 reversal',
      'Land & building: mixed use, income/expense accounts',
      'Provisions: uncertain obligation, booking to provisions account',
    ],
  },
  {
    phase: 7,
    title: 'Marketable Securities',
    duration: '3-4 days',
    chapters: [8],
    description: 'Worth ~11-13 points - second HIGHEST weighted topic! Bonds and shares require detailed understanding.',
    actions: [
      'Bonds: nominal value, current value, interest rate, maturity date, accrued interest',
      'Shares: market price, nominal value, dividend calculation',
      'Anticipatory tax: 65% to shareholder, 35% to government',
      'Year-end: book accrued income + total change in value',
      'Purchase value vs. market value methods',
      'Do EVERY exercise in Chapter 8',
    ],
  },
  {
    phase: 8,
    title: 'Joint-stock & Valuation Reserves',
    duration: '2-3 days',
    chapters: [9, 10],
    description: 'Worth ~10 points combined. Joint-stock profit distribution follows specific Swiss legal rules.',
    actions: [
      'Memorize Art. 671 OR (general reserve rules)',
      'Practice: founding entries, capital increase, profit distribution',
      'First allocation (5% until reserve = 20% of share capital)',
      'Second allocation (10% of surplus dividend)',
      'Valuation reserves: generate and dissolve methods',
    ],
  },
  {
    phase: 9,
    title: 'Exam Practice',
    duration: '4-5 days',
    chapters: [11],
    description: 'The most important phase. Do full past papers under timed conditions.',
    actions: [
      'Read Chapter 11 for multi-year perspective',
      'Do June 2023 exam (3 hours timed) then check solution',
      'Do June 2024 exam (3 hours timed) then check solution',
      'Review January 2025 solution to see what was tested',
      'Re-do any sections where you scored poorly',
      'Focus on your weakest topics from the exam analysis',
    ],
  },
]

export default function AccountingView() {
  const [activeSection, setActiveSection] = useState<Section>('overview')
  const [expandedChapter, setExpandedChapter] = useState<number | null>(null)
  const [expandedPhase, setExpandedPhase] = useState<number | null>(0)

  const sections: { key: Section; label: string }[] = [
    { key: 'overview', label: 'Chapters' },
    { key: 'plan', label: 'Study Plan' },
    { key: 'exams', label: 'Exam Analysis' },
    { key: 'materials', label: 'Materials' },
  ]

  const priorityColor = (p: string) => {
    if (p === 'high') return 'text-red-400'
    if (p === 'medium') return 'text-yellow-400'
    return 'text-gray-500'
  }

  const priorityBg = (p: string) => {
    if (p === 'high') return 'bg-red-500/10 border-red-500/30'
    if (p === 'medium') return 'bg-yellow-500/10 border-yellow-500/30'
    return 'bg-gray-500/10 border-gray-500/30'
  }

  const typeIcon = (type: string) => {
    if (type === 'book') return 'bg-blue-500/20 text-blue-400'
    if (type === 'summary') return 'bg-purple-500/20 text-purple-400'
    if (type === 'info') return 'bg-green-500/20 text-green-400'
    if (type === 'exam') return 'bg-orange-500/20 text-orange-400'
    return 'bg-emerald-500/20 text-emerald-400'
  }

  const totalExamPts = EXAM_TOPICS.reduce((s, t) => s + t.avg, 0)

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center gap-3">
        <div className="w-1.5 h-8 rounded-full bg-green-500" />
        <div>
          <h2 className="text-lg font-semibold text-white">Financial Accounting</h2>
          <p className="text-sm text-gray-400">Dr. Simon Pfister &middot; HSG &middot; 12 Chapters &middot; 3h Exam</p>
        </div>
      </div>

      {/* Sub-navigation */}
      <div className="flex gap-1 bg-gray-900 rounded-lg p-1">
        {sections.map((s) => (
          <button
            key={s.key}
            onClick={() => setActiveSection(s.key)}
            className={`flex-1 px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
              activeSection === s.key
                ? 'bg-gray-800 text-white'
                : 'text-gray-400 hover:text-gray-200'
            }`}
          >
            {s.label}
          </button>
        ))}
      </div>

      {/* CHAPTERS OVERVIEW */}
      {activeSection === 'overview' && (
        <div className="space-y-2">
          <p className="text-sm text-gray-400">
            All 12 chapters from the textbook. Click to expand topics. Priority based on exam weight analysis.
          </p>
          {CHAPTERS.map((ch) => (
            <div
              key={ch.number}
              className={`border rounded-lg overflow-hidden ${
                expandedChapter === ch.number ? 'border-gray-700' : 'border-gray-800'
              }`}
            >
              <button
                onClick={() => setExpandedChapter(expandedChapter === ch.number ? null : ch.number)}
                className="w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-gray-900/50 transition-colors"
              >
                <span className="text-sm font-mono text-gray-500 w-6">
                  {ch.number}
                </span>
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-white truncate">{ch.title}</div>
                  <div className="text-xs text-gray-500">{ch.bookPages}</div>
                </div>
                <span className={`text-xs px-2 py-0.5 rounded-full border ${priorityBg(ch.priority)}`}>
                  <span className={priorityColor(ch.priority)}>
                    {ch.priority}
                  </span>
                </span>
                <svg
                  className={`w-4 h-4 text-gray-500 transition-transform ${
                    expandedChapter === ch.number ? 'rotate-180' : ''
                  }`}
                  fill="none" viewBox="0 0 24 24" stroke="currentColor"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              {expandedChapter === ch.number && (
                <div className="px-4 pb-3 border-t border-gray-800">
                  <div className="text-xs text-gray-500 mt-2 mb-1">Exam weight: {ch.examWeight}</div>
                  <ul className="space-y-1">
                    {ch.topics.map((topic, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-gray-300">
                        <span className="text-gray-600 mt-0.5">-</span>
                        {topic}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* STUDY PLAN */}
      {activeSection === 'plan' && (
        <div className="space-y-3">
          <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-3">
            <div className="text-sm font-medium text-green-400">Beginner study guide</div>
            <div className="text-xs text-green-300/70 mt-1">
              You&apos;ve never done accounting before. This plan goes from zero to exam-ready in ~25-30 days.
              Follow the phases in order - each builds on the previous one.
            </div>
          </div>

          {STUDY_PHASES.map((phase, idx) => (
            <div
              key={phase.phase}
              className={`border rounded-lg overflow-hidden ${
                expandedPhase === idx ? 'border-gray-700' : 'border-gray-800'
              }`}
            >
              <button
                onClick={() => setExpandedPhase(expandedPhase === idx ? null : idx)}
                className="w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-gray-900/50 transition-colors"
              >
                <div className="flex items-center justify-center w-7 h-7 rounded-full bg-green-500/20 text-green-400 text-xs font-bold shrink-0">
                  {phase.phase}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-white">{phase.title}</div>
                  <div className="text-xs text-gray-500">
                    Ch {phase.chapters.join(', ')} &middot; {phase.duration}
                  </div>
                </div>
                <svg
                  className={`w-4 h-4 text-gray-500 transition-transform ${
                    expandedPhase === idx ? 'rotate-180' : ''
                  }`}
                  fill="none" viewBox="0 0 24 24" stroke="currentColor"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              {expandedPhase === idx && (
                <div className="px-4 pb-3 border-t border-gray-800">
                  <p className="text-sm text-gray-400 mt-2 mb-2">{phase.description}</p>
                  <div className="text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">What to do</div>
                  <ul className="space-y-1">
                    {phase.actions.map((action, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-gray-300">
                        <span className="text-green-500 mt-0.5 shrink-0">&#10003;</span>
                        {action}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}

          <div className="bg-gray-900 border border-gray-800 rounded-lg p-3">
            <div className="text-sm font-medium text-gray-300">Key tips for a complete beginner</div>
            <ul className="mt-2 space-y-1 text-sm text-gray-400">
              <li>- Every booking entry has a DEBIT (left) and CREDIT (right) side - amounts must match</li>
              <li>- Assets increase on debit, decrease on credit. Liabilities are the opposite</li>
              <li>- Expenses increase on debit (like assets). Revenue increases on credit (like liabilities)</li>
              <li>- The exam gives you a chart of accounts - use account NAMES not numbers</li>
              <li>- Practice past papers under timed conditions (3 hours, 100 points)</li>
              <li>- The info sheet provided during exam has all formulas and account structures</li>
            </ul>
          </div>
        </div>
      )}

      {/* EXAM ANALYSIS */}
      {activeSection === 'exams' && (
        <div className="space-y-3">
          <p className="text-sm text-gray-400">
            Point distribution averaged across June 2023, June 2024, and June 2025 exams. Total: {totalExamPts} pts.
          </p>

          {/* Bar chart */}
          <div className="space-y-1.5">
            {EXAM_TOPICS.sort((a, b) => b.avg - a.avg).map((topic) => {
              const pct = (topic.avg / 14) * 100
              return (
                <div key={topic.name} className="group">
                  <div className="flex items-center gap-2">
                    <div className="w-40 text-xs text-gray-400 truncate shrink-0">{topic.name}</div>
                    <div className="flex-1 h-5 bg-gray-800 rounded overflow-hidden">
                      <div
                        className="h-full rounded transition-all"
                        style={{
                          width: `${Math.min(pct, 100)}%`,
                          backgroundColor: topic.avg >= 10 ? '#ef4444' : topic.avg >= 6 ? '#eab308' : '#6b7280',
                        }}
                      />
                    </div>
                    <span className="text-xs text-gray-400 w-8 text-right font-mono">{topic.avg}</span>
                  </div>
                  <div className="text-xs text-gray-500 ml-42 pl-42 hidden group-hover:block ml-[168px] mt-0.5">
                    {topic.chapters} &middot; {topic.tip}
                  </div>
                </div>
              )
            })}
          </div>

          {/* Detail cards */}
          <div className="text-xs font-medium text-gray-500 mt-4 uppercase tracking-wide">Topic details & study tips</div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {EXAM_TOPICS.sort((a, b) => b.avg - a.avg).map((topic) => (
              <div key={topic.name} className="bg-gray-900 border border-gray-800 rounded-lg p-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-white">{topic.name}</span>
                  <span className={`text-xs font-mono px-1.5 py-0.5 rounded ${
                    topic.avg >= 10 ? 'bg-red-500/20 text-red-400' :
                    topic.avg >= 6 ? 'bg-yellow-500/20 text-yellow-400' :
                    'bg-gray-700 text-gray-400'
                  }`}>
                    ~{topic.avg} pts
                  </span>
                </div>
                <div className="text-xs text-gray-500 mt-0.5">{topic.chapters}</div>
                <div className="text-xs text-gray-400 mt-1">{topic.tip}</div>
              </div>
            ))}
          </div>

          {/* Past papers table */}
          <div className="text-xs font-medium text-gray-500 mt-4 uppercase tracking-wide">Past paper comparison</div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-gray-500 text-xs border-b border-gray-800">
                  <th className="text-left py-2 pr-3">Topic</th>
                  <th className="text-center py-2 px-2">Jun 23</th>
                  <th className="text-center py-2 px-2">Jun 24</th>
                  <th className="text-center py-2 px-2">Jun 25</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { name: 'Trading company', y23: 14, y24: 13, y25: 14 },
                  { name: 'Marketable securities', y23: 11, y24: 13, y25: 13 },
                  { name: 'Payment & production', y23: 11, y24: 11, y25: 10 },
                  { name: 'Depreciation & receivables', y23: 5, y24: 8, y25: 9 },
                  { name: 'Interpretation of entries', y23: 8, y24: 8, y25: 4 },
                  { name: 'Financial ratios', y23: 6, y24: 0, y25: 6 },
                  { name: 'Accruals & provisions', y23: 5, y24: 6, y25: 6 },
                  { name: 'P&L reporting format', y23: 4, y24: 11, y25: 4 },
                  { name: 'Joint-stock company', y23: 6, y24: 5, y25: 5 },
                  { name: 'Land & building', y23: 5, y24: 5, y25: 4 },
                  { name: 'Valuation reserves', y23: 5, y24: 4, y25: 4 },
                  { name: 'Profit & cash effect', y23: 4, y24: 4, y25: 4 },
                  { name: 'Inventory changes', y23: 4, y24: 4, y25: 4 },
                  { name: 'Sole proprietorship', y23: 5, y24: 3, y25: 3 },
                  { name: 'Miscellaneous', y23: 7, y24: 5, y25: 5 },
                  { name: 'Board decisions', y23: 0, y24: 0, y25: 5 },
                ].map((row) => (
                  <tr key={row.name} className="border-b border-gray-800/50">
                    <td className="py-1.5 pr-3 text-gray-300 text-xs">{row.name}</td>
                    <td className="text-center py-1.5 px-2 text-xs text-gray-400">{row.y23 || '-'}</td>
                    <td className="text-center py-1.5 px-2 text-xs text-gray-400">{row.y24 || '-'}</td>
                    <td className="text-center py-1.5 px-2 text-xs text-gray-400">{row.y25 || '-'}</td>
                  </tr>
                ))}
                <tr className="font-medium">
                  <td className="py-1.5 pr-3 text-white text-xs">Total</td>
                  <td className="text-center py-1.5 px-2 text-xs text-white">100</td>
                  <td className="text-center py-1.5 px-2 text-xs text-white">100</td>
                  <td className="text-center py-1.5 px-2 text-xs text-white">100</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* MATERIALS */}
      {activeSection === 'materials' && (
        <div className="space-y-3">
          <p className="text-sm text-gray-400">
            All files in your accounting folder. 8 PDFs covering the textbook, summaries, past papers, and solutions.
          </p>
          {MATERIALS.map((mat) => (
            <div key={mat.file} className="flex items-start gap-3 bg-gray-900 border border-gray-800 rounded-lg p-3">
              <div className={`px-2 py-1 rounded text-xs font-medium shrink-0 ${typeIcon(mat.type)}`}>
                {mat.type === 'book' ? 'BOOK' :
                 mat.type === 'summary' ? 'SLIDES' :
                 mat.type === 'info' ? 'INFO' :
                 mat.type === 'exam' ? 'EXAM' : 'SOLN'}
              </div>
              <div className="min-w-0">
                <div className="text-sm font-medium text-white">{mat.name}</div>
                <div className="text-xs text-gray-500 truncate">{mat.file}</div>
                <div className="text-xs text-gray-400 mt-0.5">{mat.desc}</div>
              </div>
            </div>
          ))}

          <div className="bg-gray-900 border border-gray-800 rounded-lg p-3 mt-4">
            <div className="text-sm font-medium text-gray-300">Recommended reading order</div>
            <ol className="mt-2 space-y-1 text-sm text-gray-400 list-decimal list-inside">
              <li>Lecture Summary (quick overview of all 11 topic areas)</li>
              <li>Textbook chapters 1-8 (core exam content)</li>
              <li>Textbook chapters 9-10 (secondary exam content)</li>
              <li>Exam Info Sheet 2025 (understand what you get during the exam)</li>
              <li>Past Paper June 2023 + Solution (first practice run)</li>
              <li>Past Paper June 2024 + Solution (second practice run)</li>
              <li>January 2025 Solution (review what was recently tested)</li>
            </ol>
          </div>
        </div>
      )}
    </div>
  )
}
