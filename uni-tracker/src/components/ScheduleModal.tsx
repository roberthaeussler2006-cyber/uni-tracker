'use client'

import { ScheduleEntry } from '@/lib/scheduleData'

interface Props {
  subjectName: string
  subjectShortName: string
  subjectColor: string
  entries: ScheduleEntry[]
  currentWeekNumber: number
  onClose: () => void
}

export default function ScheduleModal({
  subjectName,
  subjectShortName,
  subjectColor,
  entries,
  currentWeekNumber,
  onClose,
}: Props) {
  const isMathTopicList = subjectShortName === 'Math'

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60" onClick={onClose}>
      <div
        className="bg-gray-900 border border-gray-800 rounded-xl w-full max-w-lg mx-4 max-h-[80vh] flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-800">
          <div className="flex items-center gap-2">
            <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: subjectColor }} />
            <h3 className="text-base font-medium text-white">
              {isMathTopicList ? 'Topics' : 'Semester Schedule'}
            </h3>
          </div>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-300 transition-colors"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Schedule List */}
        <div className="overflow-y-auto p-4 space-y-1.5">
          {entries.map((entry, i) => {
            const isCurrentWeek = entry.kw === currentWeekNumber
            const isBreak = String(entry.kw).includes('–')

            return (
              <div
                key={i}
                className={`rounded-lg px-3 py-2.5 border-l-3 ${
                  isBreak ? 'opacity-40' : ''
                }`}
                style={{
                  backgroundColor: isCurrentWeek ? subjectColor + '18' : 'transparent',
                  borderLeftColor: isCurrentWeek ? subjectColor : 'transparent',
                }}
              >
                <div className="flex gap-3">
                  {/* Week number */}
                  <span className={`text-sm font-medium w-10 flex-shrink-0 ${
                    isCurrentWeek ? 'text-white' : 'text-gray-500'
                  }`}>
                    {isMathTopicList ? `${entry.kw}.` : `KW ${entry.kw}`}
                  </span>

                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <p className={`text-sm ${isCurrentWeek ? 'text-white font-medium' : 'text-gray-200'}`}>
                      {entry.topic}
                    </p>
                    {entry.reading && (
                      <p className="text-xs text-gray-400 mt-0.5">
                        📖 {entry.reading}
                      </p>
                    )}
                    {entry.practice && (
                      <p className="text-xs text-gray-400 mt-0.5">
                        📝 {entry.practice}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
