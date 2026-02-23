'use client'

import { useState, useEffect, useCallback, useRef } from 'react'
import { supabase } from '@/lib/supabase'
import { Week } from '@/lib/types'
import {
  getLawExpectedPace,
  getLawCumulativePages,
  LAW_TOTAL_PAGES,
  LAW_CL_TOTAL,
  LAW_PIL_TOTAL,
  getMacroExpectedPages,
  MACRO_TOTAL_PAGES,
  getFmExpectedPage,
  FM_TOTAL_PAGES,
} from '@/lib/scheduleData'

type SubjectType = 'Law' | 'Macro' | 'BusAdmin'

interface Props {
  subject: SubjectType
  currentWeek: Week
  selectedWeekNumber: number
}

export default function ReadingProgressTracker({ subject, currentWeek, selectedWeekNumber }: Props) {
  const [currentPage, setCurrentPage] = useState(0)
  const [inputValue, setInputValue] = useState('')
  const [book, setBook] = useState<'constitutional' | 'pil'>('constitutional')
  const [saving, setSaving] = useState(false)
  const saveTimer = useRef<ReturnType<typeof setTimeout> | null>(null)
  const isLaw = subject === 'Law'
  const isFm = subject === 'BusAdmin'

  const loadProgress = useCallback(async () => {
    const { data } = await supabase
      .from('tracker_reading_progress')
      .select('current_page, book')
      .eq('week_id', currentWeek.id)
      .eq('subject', subject)
      .single()

    if (data) {
      setCurrentPage(data.current_page)
      setInputValue(data.current_page > 0 ? String(data.current_page) : '')
      if (isLaw && data.book) setBook(data.book as 'constitutional' | 'pil')
    } else {
      setCurrentPage(0)
      setInputValue('')
    }
  }, [currentWeek.id, subject, isLaw])

  useEffect(() => {
    loadProgress()
  }, [loadProgress])

  function save(page: number, selectedBook: string) {
    if (saveTimer.current) clearTimeout(saveTimer.current)
    saveTimer.current = setTimeout(async () => {
      setSaving(true)
      const record: Record<string, unknown> = {
        week_id: currentWeek.id,
        subject,
        current_page: page,
      }
      if (isLaw) record.book = selectedBook

      const { error } = await supabase
        .from('tracker_reading_progress')
        .upsert(record, { onConflict: 'week_id,subject' })

      if (error) console.error('Failed to save reading progress:', error)
      setSaving(false)
    }, 500)
  }

  // Get max page for current context
  function getMaxPage(): number {
    if (isLaw) return book === 'constitutional' ? LAW_CL_TOTAL : LAW_PIL_TOTAL
    if (isFm) return FM_TOTAL_PAGES
    return MACRO_TOTAL_PAGES // Macro: cumulative pages read
  }

  function handlePageChange(value: string) {
    setInputValue(value)
    const page = parseInt(value) || 0
    const clamped = Math.min(Math.max(0, page), getMaxPage())
    setCurrentPage(clamped)
    save(clamped, book)
  }

  function handleBookChange(newBook: 'constitutional' | 'pil') {
    if (newBook === book) return
    setBook(newBook)
    setCurrentPage(0)
    setInputValue('')
    save(0, newBook)
  }

  // Calculate progress
  function getTotalPages(): number {
    if (isLaw) return LAW_TOTAL_PAGES
    if (isFm) return FM_TOTAL_PAGES
    return MACRO_TOTAL_PAGES
  }

  const totalPages = getTotalPages()
  const cumulativePages = isLaw ? getLawCumulativePages(book, currentPage) : currentPage
  const progressPercent = totalPages > 0 ? Math.min(100, Math.round((cumulativePages / totalPages) * 100)) : 0

  // On-track calculation
  let trackStatus: 'on-track' | 'slightly-behind' | 'behind' | 'ahead' | 'none' = 'none'
  let trackLabel = ''
  let trackColor = ''
  let expectedDisplay = ''

  if (currentPage > 0) {
    let expectedCumulative = 0

    if (isLaw) {
      const expected = getLawExpectedPace(selectedWeekNumber)
      if (expected) {
        expectedCumulative = getLawCumulativePages(expected.book, expected.page)
        expectedDisplay = `p.${expected.page} ${expected.book === 'constitutional' ? 'CL' : 'PIL'}`
      }
    } else if (isFm) {
      const expectedPage = getFmExpectedPage(selectedWeekNumber)
      if (expectedPage) {
        expectedCumulative = expectedPage
        expectedDisplay = `p.${expectedPage}`
      }
    } else {
      const expectedPages = getMacroExpectedPages(selectedWeekNumber)
      if (expectedPages) {
        expectedCumulative = expectedPages
        expectedDisplay = `${expectedPages}p`
      }
    }

    if (expectedCumulative > 0) {
      const diff = cumulativePages - expectedCumulative
      const tolerance = totalPages * 0.05

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
  }

  const maxPage = getMaxPage()
  const placeholder = subject === 'Macro' ? 'Pages read...' : 'Current page...'
  const label = isFm ? 'FM Reading Progress' : 'Reading Progress'

  return (
    <div className="mt-3 pt-3 border-t border-gray-800">
      <div className="flex items-center gap-2 mb-2">
        <svg className="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
        </svg>
        <span className="text-sm font-medium text-gray-300">{label}</span>
        {saving && <span className="text-xs text-gray-500">Saving...</span>}
      </div>

      {/* Law book toggle */}
      {isLaw && (
        <div className="flex gap-1 mb-2">
          <button
            onClick={() => handleBookChange('constitutional')}
            className={`flex-1 px-2 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              book === 'constitutional'
                ? 'bg-blue-600/30 text-blue-300 border border-blue-500/50'
                : 'bg-gray-800 text-gray-500 border border-gray-700 hover:text-gray-400'
            }`}
          >
            Constitutional Law
          </button>
          <button
            onClick={() => handleBookChange('pil')}
            className={`flex-1 px-2 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              book === 'pil'
                ? 'bg-blue-600/30 text-blue-300 border border-blue-500/50'
                : 'bg-gray-800 text-gray-500 border border-gray-700 hover:text-gray-400'
            }`}
          >
            Public Intl Law
          </button>
        </div>
      )}

      {/* Page input */}
      <div className="flex items-center gap-2 mb-2">
        <input
          type="number"
          min={0}
          max={maxPage}
          value={inputValue}
          onChange={(e) => handlePageChange(e.target.value)}
          placeholder={placeholder}
          className="flex-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-sm text-gray-200 focus:outline-none focus:border-gray-600 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
        />
        <span className="text-xs text-gray-500 whitespace-nowrap">
          / {maxPage}
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
          {progressPercent}%
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
          {expectedDisplay && (
            <span className="text-xs text-gray-500">
              (expected: {expectedDisplay} by KW {selectedWeekNumber})
            </span>
          )}
        </div>
      )}
    </div>
  )
}
