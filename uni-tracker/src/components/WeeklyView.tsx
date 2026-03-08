'use client'

import { Subject, Week } from '@/lib/types'
import WeekSelector from './WeekSelector'
import WeekPanel from './WeekPanel'
import { getCurrentWeekNumber, formatDateRange } from '@/lib/weeks'

interface Props {
  subjects: Subject[]
  weeks: Week[]
  currentWeek: Week
  previousWeek: Week | null
  selectedWeekNumber: number
  onWeekChange: (weekNumber: number) => void
}

export default function WeeklyView({ subjects, weeks, currentWeek, previousWeek, selectedWeekNumber, onWeekChange }: Props) {
  const actualCurrentWeekNumber = getCurrentWeekNumber()

  return (
    <div>
      <WeekSelector
        weeks={weeks}
        selectedWeekNumber={selectedWeekNumber}
        currentWeekNumber={actualCurrentWeekNumber}
        onWeekChange={onWeekChange}
        previousWeekNumber={previousWeek ? selectedWeekNumber - 1 : null}
      />

      {/* Split Week View */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Previous Week (left side) */}
        {previousWeek ? (
          <WeekPanel
            subjects={subjects}
            weeks={weeks}
            week={previousWeek}
            weekNumber={selectedWeekNumber - 1}
            isCurrentWeek={selectedWeekNumber - 1 === actualCurrentWeekNumber}
            label={selectedWeekNumber - 1 === actualCurrentWeekNumber ? 'This Week' : `Previous Week · ${formatDateRange(previousWeek.start_date, previousWeek.end_date)}`}
          />
        ) : (
          <div className="rounded-2xl border-2 border-dashed border-gray-700/30 p-6 flex items-center justify-center">
            <p className="text-sm text-gray-600">No previous week available</p>
          </div>
        )}

        {/* Selected Week (right side) */}
        <WeekPanel
          subjects={subjects}
          weeks={weeks}
          week={currentWeek}
          weekNumber={selectedWeekNumber}
          isCurrentWeek={selectedWeekNumber === actualCurrentWeekNumber}
          label={selectedWeekNumber === actualCurrentWeekNumber ? 'This Week' : `KW ${selectedWeekNumber} · ${formatDateRange(currentWeek.start_date, currentWeek.end_date)}`}
        />
      </div>
    </div>
  )
}
