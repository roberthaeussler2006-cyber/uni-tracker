'use client'

import { Week } from '@/lib/types'
import { formatDateRange } from '@/lib/weeks'

interface Props {
  weeks: Week[]
  selectedWeekNumber: number
  onWeekChange: (weekNumber: number) => void
}

export default function WeekSelector({ weeks, selectedWeekNumber, onWeekChange }: Props) {
  const currentWeek = weeks.find((w) => w.week_number === selectedWeekNumber)
  const minWeek = Math.min(...weeks.map((w) => w.week_number))
  const maxWeek = Math.max(...weeks.map((w) => w.week_number))

  return (
    <div className="flex items-center justify-between mb-6">
      <button
        onClick={() => onWeekChange(Math.max(minWeek, selectedWeekNumber - 1))}
        disabled={selectedWeekNumber <= minWeek}
        className="p-2 text-gray-400 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
      >
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
      </button>

      <div className="text-center">
        <div className="text-lg font-semibold text-white">KW {selectedWeekNumber}</div>
        {currentWeek && (
          <div className="text-sm text-gray-400">
            {formatDateRange(currentWeek.start_date, currentWeek.end_date)}
          </div>
        )}
        <div className="text-xs text-gray-500 mt-1">
          Readings for KW {selectedWeekNumber + 1} · Exercises for KW {selectedWeekNumber}
        </div>
      </div>

      <button
        onClick={() => onWeekChange(Math.min(maxWeek, selectedWeekNumber + 1))}
        disabled={selectedWeekNumber >= maxWeek}
        className="p-2 text-gray-400 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
      >
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>
  )
}
