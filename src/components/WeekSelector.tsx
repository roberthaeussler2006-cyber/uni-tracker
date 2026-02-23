'use client'

import { Week } from '@/lib/types'
import { formatDateRange } from '@/lib/weeks'

interface Props {
  weeks: Week[]
  selectedWeekNumber: number
  currentWeekNumber: number
  onWeekChange: (weekNumber: number) => void
}

export default function WeekSelector({ weeks, selectedWeekNumber, currentWeekNumber, onWeekChange }: Props) {
  const currentWeek = weeks.find((w) => w.week_number === selectedWeekNumber)
  const minWeek = Math.min(...weeks.map((w) => w.week_number))
  const maxWeek = Math.max(...weeks.map((w) => w.week_number))
  const isOnCurrentWeek = selectedWeekNumber === currentWeekNumber
  const isEasterBreak = selectedWeekNumber === 14 || selectedWeekNumber === 15

  return (
    <div className="mb-3">
      <div className="flex items-center justify-between">
        <button
          onClick={() => onWeekChange(Math.max(minWeek, selectedWeekNumber - 1))}
          disabled={selectedWeekNumber <= minWeek}
          className="p-2 text-gray-400 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
        >
          <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
        </button>

        <div className="text-center">
          <div className="text-xl font-semibold text-white leading-tight">
            KW {selectedWeekNumber}
            {isEasterBreak && (
              <span className="text-base text-amber-300 font-normal ml-2">🐣 Easter Break</span>
            )}
            {!isEasterBreak && currentWeek && (
              <span className="text-base text-gray-400 font-normal ml-2">
                {formatDateRange(currentWeek.start_date, currentWeek.end_date)}
              </span>
            )}
          </div>
          {!isEasterBreak && (
            <div className="text-base text-gray-500">
              Readings for KW {selectedWeekNumber + 1} · Exercises for KW {selectedWeekNumber}
            </div>
          )}
        </div>

        <button
          onClick={() => onWeekChange(Math.min(maxWeek, selectedWeekNumber + 1))}
          disabled={selectedWeekNumber >= maxWeek}
          className="p-2 text-gray-400 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
        >
          <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      {!isOnCurrentWeek && (
        <button
          onClick={() => onWeekChange(currentWeekNumber)}
          className="mt-2 w-full py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-base font-medium transition-colors"
        >
          Go to current week (KW {currentWeekNumber})
        </button>
      )}
    </div>
  )
}
