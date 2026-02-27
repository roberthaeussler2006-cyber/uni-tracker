'use client'

import { Week } from '@/lib/types'
import { formatDateRange } from '@/lib/weeks'

interface Props {
  weeks: Week[]
  selectedWeekNumber: number
  currentWeekNumber: number
  onWeekChange: (weekNumber: number) => void
  previousWeekNumber: number | null
}

export default function WeekSelector({ weeks, selectedWeekNumber, currentWeekNumber, onWeekChange, previousWeekNumber }: Props) {
  const currentWeek = weeks.find((w) => w.week_number === selectedWeekNumber)
  const prevWeek = previousWeekNumber ? weeks.find((w) => w.week_number === previousWeekNumber) : null
  const minWeek = Math.min(...weeks.map((w) => w.week_number))
  const maxWeek = Math.max(...weeks.map((w) => w.week_number))

  // The "pair" view shows previousWeekNumber & selectedWeekNumber
  // Navigation moves both by 1
  // The actual minimum for the pair: previousWeekNumber must be >= minWeek
  // So selectedWeekNumber must be >= minWeek + 1 (to have a previous)
  const canGoBack = previousWeekNumber ? previousWeekNumber > minWeek : selectedWeekNumber > minWeek
  const canGoForward = selectedWeekNumber < maxWeek

  // Check if we're viewing the current week pair
  const isOnCurrentWeek = selectedWeekNumber === currentWeekNumber || (previousWeekNumber === currentWeekNumber)

  return (
    <div className="mb-3">
      <div className="flex items-center justify-between">
        <button
          onClick={() => onWeekChange(selectedWeekNumber - 1)}
          disabled={!canGoBack}
          className="p-2 text-gray-400 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
        >
          <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
        </button>

        <div className="text-center">
          <div className="flex items-center justify-center gap-2 text-xl font-semibold leading-tight">
            {previousWeekNumber && prevWeek && (
              <>
                <span className={previousWeekNumber === currentWeekNumber ? 'text-blue-400' : 'text-gray-400'}>
                  KW {previousWeekNumber}
                </span>
                <span className="text-gray-600">&</span>
              </>
            )}
            <span className={selectedWeekNumber === currentWeekNumber ? 'text-blue-400' : 'text-white'}>
              KW {selectedWeekNumber}
            </span>
          </div>
          {currentWeek && prevWeek && (
            <div className="text-sm text-gray-500 mt-0.5">
              {formatDateRange(prevWeek.start_date, currentWeek.end_date)}
            </div>
          )}
          {currentWeek && !prevWeek && (
            <div className="text-sm text-gray-500 mt-0.5">
              {formatDateRange(currentWeek.start_date, currentWeek.end_date)}
            </div>
          )}
        </div>

        <button
          onClick={() => onWeekChange(selectedWeekNumber + 1)}
          disabled={!canGoForward}
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
