'use client'

import { useState, useEffect, useCallback } from 'react'
import { supabase } from '@/lib/supabase'
import {
  MACRO_READING_UNITS,
  MACRO_TOTAL_PAGES,
  getMacroExpectedPages,
} from '@/lib/scheduleData'

interface Props {
  selectedWeekNumber: number
}

// Group reading units by KW for the checklist display
const KW_GROUPS = (() => {
  const groups: { kw: number; label: string; units: typeof MACRO_READING_UNITS }[] = []
  const kwLabels: Record<number, string> = {
    8: 'Intro & National Accounts',
    9: 'The Goods Market',
    10: 'Financial Markets',
    11: 'The IS-LM Model',
    12: 'The Labor Market',
    13: 'Inflation & Phillips Curve',
    16: 'The IS-LM-PC Model',
    17: 'Open Economy',
    18: 'International Macro',
    19: 'Growth',
    20: 'Innovation',
  }
  const seen = new Set<number>()
  for (const unit of MACRO_READING_UNITS) {
    if (!seen.has(unit.kw)) {
      seen.add(unit.kw)
      groups.push({
        kw: unit.kw,
        label: kwLabels[unit.kw] || '',
        units: MACRO_READING_UNITS.filter((u) => u.kw === unit.kw),
      })
    }
  }
  return groups
})()

export default function MacroReadingTracker({ selectedWeekNumber }: Props) {
  const [checkedIds, setCheckedIds] = useState<Set<string>>(new Set())
  const [loading, setLoading] = useState(true)
  const [expanded, setExpanded] = useState(false)

  const loadChecked = useCallback(async () => {
    const { data } = await supabase
      .from('tracker_macro_reading')
      .select('chapter_id')

    if (data) {
      setCheckedIds(new Set(data.map((r) => r.chapter_id)))
    }
    setLoading(false)
  }, [])

  useEffect(() => {
    loadChecked()
  }, [loadChecked])

  async function handleToggle(chapterId: string) {
    const newChecked = new Set(checkedIds)

    if (newChecked.has(chapterId)) {
      newChecked.delete(chapterId)
      setCheckedIds(newChecked)
      await supabase
        .from('tracker_macro_reading')
        .delete()
        .eq('chapter_id', chapterId)
    } else {
      newChecked.add(chapterId)
      setCheckedIds(newChecked)
      const { error } = await supabase
        .from('tracker_macro_reading')
        .insert({ chapter_id: chapterId })
      if (error) console.error('Failed to save macro reading:', error)
    }
  }

  // Calculate progress from checked items
  const checkedPages = MACRO_READING_UNITS.reduce(
    (sum, u) => sum + (checkedIds.has(u.id) ? u.pages : 0),
    0
  )
  const checkedCount = checkedIds.size
  const totalUnits = MACRO_READING_UNITS.length
  const progressPercent = MACRO_TOTAL_PAGES > 0
    ? Math.min(100, Math.round((checkedPages / MACRO_TOTAL_PAGES) * 100))
    : 0

  // On-track calculation
  const expectedPages = getMacroExpectedPages(selectedWeekNumber)
  let trackStatus: 'on-track' | 'slightly-behind' | 'behind' | 'ahead' | 'none' = 'none'
  let trackLabel = ''
  let trackColor = ''

  if (checkedCount > 0 && expectedPages) {
    const diff = checkedPages - expectedPages
    const tolerance = MACRO_TOTAL_PAGES * 0.05 // ~16 pages

    if (diff >= tolerance) {
      trackStatus = 'ahead'; trackLabel = 'Ahead'; trackColor = 'text-blue-400'
    } else if (diff >= 0) {
      trackStatus = 'on-track'; trackLabel = 'On track'; trackColor = 'text-emerald-400'
    } else if (diff >= -tolerance * 2) {
      trackStatus = 'slightly-behind'; trackLabel = 'Slightly behind'; trackColor = 'text-yellow-400'
    } else {
      trackStatus = 'behind'; trackLabel = 'Behind'; trackColor = 'text-red-400'
    }
  }

  if (loading) return null

  return (
    <div className="mt-3 pt-3 border-t border-gray-800">
      <div className="flex items-center gap-2 mb-2">
        <svg className="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
        </svg>
        <span className="text-sm font-medium text-gray-300">Reading Progress</span>
        <span className="text-xs text-gray-500 ml-auto">
          {checkedCount}/{totalUnits} chapters
        </span>
      </div>

      {/* Progress bar + stats */}
      <div className="flex items-center gap-3">
        <div className="flex-1 h-2 bg-gray-800 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full transition-all duration-300"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
        <span className="text-xs text-gray-400 whitespace-nowrap">
          ~{checkedPages}p · {progressPercent}%
        </span>
      </div>

      {/* On-track indicator */}
      {trackStatus !== 'none' && (
        <div className="flex items-center gap-1.5 mt-1.5">
          <div className={`w-1.5 h-1.5 rounded-full ${
            trackStatus === 'on-track' || trackStatus === 'ahead' ? 'bg-emerald-400' :
            trackStatus === 'slightly-behind' ? 'bg-yellow-400' : 'bg-red-400'
          }`} />
          <span className={`text-xs font-medium ${trackColor}`}>
            {trackLabel}
          </span>
          {expectedPages && (
            <span className="text-xs text-gray-500">
              (expected: ~{expectedPages}p by KW {selectedWeekNumber})
            </span>
          )}
        </div>
      )}

      {/* Expand/collapse toggle */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-1 mt-2 text-xs text-gray-500 hover:text-gray-300 transition-colors"
      >
        <svg
          className={`w-3 h-3 transition-transform ${expanded ? 'rotate-90' : ''}`}
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
        </svg>
        {expanded ? 'Hide chapters' : 'Show chapters'}
      </button>

      {/* Chapter checklist */}
      {expanded && (
        <div className="mt-2 max-h-[360px] overflow-y-auto space-y-3 pr-1">
          {KW_GROUPS.map((group) => {
            const groupChecked = group.units.filter((u) => checkedIds.has(u.id)).length
            const allChecked = groupChecked === group.units.length

            return (
              <div key={group.kw}>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-[10px] font-medium text-gray-500 uppercase tracking-wider">
                    KW {group.kw}
                  </span>
                  <span className="text-[10px] text-gray-600">{group.label}</span>
                  {allChecked && (
                    <svg className="w-3 h-3 text-emerald-500 ml-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  )}
                </div>
                <div className="space-y-0.5">
                  {group.units.map((unit) => (
                    <label
                      key={unit.id}
                      className="flex items-center gap-2 py-0.5 px-1 rounded hover:bg-gray-800/50 cursor-pointer group"
                    >
                      <input
                        type="checkbox"
                        checked={checkedIds.has(unit.id)}
                        onChange={() => handleToggle(unit.id)}
                        className="w-3.5 h-3.5 rounded border-gray-600 bg-gray-800 text-blue-500 focus:ring-0 focus:ring-offset-0 cursor-pointer"
                      />
                      <span className={`text-xs flex-1 ${
                        checkedIds.has(unit.id) ? 'text-gray-500 line-through' : 'text-gray-300'
                      }`}>
                        {unit.label}
                      </span>
                      <span className="text-[10px] text-gray-600 group-hover:text-gray-500">
                        {unit.pages}p
                      </span>
                    </label>
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
