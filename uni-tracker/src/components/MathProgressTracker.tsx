'use client'

import { useState, useEffect, useCallback } from 'react'
import { supabase } from '@/lib/supabase'
import { Week } from '@/lib/types'
import {
  MATH_SUBCHAPTERS,
  getMathExpectedSubchapter,
  getMathSubchapterIndex,
} from '@/lib/scheduleData'

interface Props {
  currentWeek: Week
  selectedWeekNumber: number
}

export default function MathProgressTracker({ currentWeek, selectedWeekNumber }: Props) {
  const [selectedSubchapter, setSelectedSubchapter] = useState<string | null>(null)
  const [saving, setSaving] = useState(false)

  const loadProgress = useCallback(async () => {
    const { data } = await supabase
      .from('tracker_math_progress')
      .select('sub_chapter')
      .eq('week_id', currentWeek.id)
      .single()

    if (data) {
      setSelectedSubchapter(data.sub_chapter)
    } else {
      setSelectedSubchapter(null)
    }
  }, [currentWeek.id])

  useEffect(() => {
    loadProgress()
  }, [loadProgress])

  async function handleChange(subchapterId: string) {
    const value = subchapterId === '' ? null : subchapterId
    setSelectedSubchapter(value)

    if (!value) {
      // Delete the record if cleared
      await supabase
        .from('tracker_math_progress')
        .delete()
        .eq('week_id', currentWeek.id)
      return
    }

    setSaving(true)
    // Upsert: insert or update on conflict (week_id is unique)
    const { error } = await supabase
      .from('tracker_math_progress')
      .upsert(
        { week_id: currentWeek.id, sub_chapter: value },
        { onConflict: 'week_id' }
      )
    if (error) console.error('Failed to save math progress:', error)
    setSaving(false)
  }

  // Calculate progress
  const totalSubchapters = MATH_SUBCHAPTERS.length
  const currentIndex = selectedSubchapter ? getMathSubchapterIndex(selectedSubchapter) : -1
  const completedCount = currentIndex >= 0 ? currentIndex + 1 : 0
  const progressPercent = Math.round((completedCount / totalSubchapters) * 100)

  // On-track calculation
  const expectedId = getMathExpectedSubchapter(selectedWeekNumber)
  const expectedIndex = expectedId ? getMathSubchapterIndex(expectedId) : -1
  const expectedCount = expectedIndex >= 0 ? expectedIndex + 1 : 0

  let trackStatus: 'on-track' | 'slightly-behind' | 'behind' | 'ahead' | 'none' = 'none'
  let trackLabel = ''
  let trackColor = ''

  if (selectedSubchapter && expectedId) {
    const diff = completedCount - expectedCount
    if (diff >= 2) {
      trackStatus = 'ahead'
      trackLabel = 'Ahead'
      trackColor = 'text-blue-400'
    } else if (diff >= 0) {
      trackStatus = 'on-track'
      trackLabel = 'On track'
      trackColor = 'text-emerald-400'
    } else if (diff >= -3) {
      trackStatus = 'slightly-behind'
      trackLabel = 'Slightly behind'
      trackColor = 'text-yellow-400'
    } else {
      trackStatus = 'behind'
      trackLabel = 'Behind'
      trackColor = 'text-red-400'
    }
  }

  // Group sub-chapters by chapter for the dropdown
  const chapters = Array.from(new Set(MATH_SUBCHAPTERS.map((sc) => sc.chapter)))

  const chapterNames: Record<number, string> = {
    1: 'Integrals',
    2: 'Applications of Integral Calculus',
    3: 'Matrices and Determinants',
    4: 'Vectors',
    5: 'Systems of Linear Equations',
    6: 'Eigenvalues and Eigenvectors',
    7: 'Difference Equations',
    8: 'Applications of Linear Algebra',
  }

  return (
    <div className="mt-3 pt-3 border-t border-gray-800">
      <div className="flex items-center gap-2 mb-2">
        <svg className="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
        </svg>
        <span className="text-sm font-medium text-gray-300">Progress Tracker</span>
        {saving && <span className="text-xs text-gray-500">Saving...</span>}
      </div>

      {/* Dropdown */}
      <select
        value={selectedSubchapter || ''}
        onChange={(e) => handleChange(e.target.value)}
        className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-sm text-gray-200 focus:outline-none focus:border-gray-600 appearance-none cursor-pointer mb-2"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%239ca3af'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E")`,
          backgroundRepeat: 'no-repeat',
          backgroundPosition: 'right 0.5rem center',
          backgroundSize: '1.25rem',
        }}
      >
        <option value="">Select sub-chapter reached...</option>
        {chapters.map((ch) => (
          <optgroup key={ch} label={`Ch ${ch}: ${chapterNames[ch]}`}>
            {MATH_SUBCHAPTERS.filter((sc) => sc.chapter === ch).map((sc) => (
              <option key={sc.id} value={sc.id}>
                {sc.id} — {sc.title}
              </option>
            ))}
          </optgroup>
        ))}
      </select>

      {/* Progress bar + stats */}
      <div className="flex items-center gap-3">
        <div className="flex-1 h-2 bg-gray-800 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full transition-all duration-300"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
        <span className="text-xs text-gray-400 whitespace-nowrap">
          {completedCount}/{totalSubchapters} · {progressPercent}%
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
          {expectedId && (
            <span className="text-xs text-gray-500">
              (expected: {expectedId} by KW {selectedWeekNumber})
            </span>
          )}
        </div>
      )}
    </div>
  )
}
