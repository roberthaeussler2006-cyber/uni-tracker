'use client'

import { useState, useEffect } from 'react'
import { supabase } from '@/lib/supabase'
import { Subject, Week, Task } from '@/lib/types'

interface Props {
  subjects: Subject[]
  weeks: Week[]
}

export default function AnalyticsView({ subjects, weeks }: Props) {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      const { data } = await supabase
        .from('tracker_tasks')
        .select('*')
      if (data) setTasks(data)
      setLoading(false)
    }
    load()
  }, [])

  if (loading) {
    return <div className="text-center text-gray-400 py-12">Loading analytics...</div>
  }

  // Build heatmap data: weeks x subjects
  const heatmapData = weeks.map((week) => ({
    week,
    subjects: subjects.map((subject) => {
      const subjectWeekTasks = tasks.filter(
        (t) => t.week_id === week.id && t.subject_id === subject.id
      )
      const total = subjectWeekTasks.length
      const completed = subjectWeekTasks.filter((t) => t.is_completed).length
      return { subject, total, completed, pct: total > 0 ? completed / total : -1 }
    }),
  }))

  // Overall stats
  const totalTasks = tasks.length
  const completedTasks = tasks.filter((t) => t.is_completed).length
  const overallPct = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 0

  // Per-subject stats
  const subjectStats = subjects.map((subject) => {
    const subjectTasks = tasks.filter((t) => t.subject_id === subject.id)
    const total = subjectTasks.length
    const completed = subjectTasks.filter((t) => t.is_completed).length
    return { subject, total, completed, pct: total > 0 ? Math.round((completed / total) * 100) : 0 }
  })

  function getCellColor(pct: number, color: string): string {
    if (pct < 0) return '#111827' // no tasks
    if (pct === 0) return '#1f2937'
    // Convert hex to RGB and interpolate opacity
    const r = parseInt(color.slice(1, 3), 16)
    const g = parseInt(color.slice(3, 5), 16)
    const b = parseInt(color.slice(5, 7), 16)
    const opacity = 0.2 + pct * 0.8
    return `rgba(${r}, ${g}, ${b}, ${opacity})`
  }

  return (
    <div className="space-y-6">
      {/* Overall Progress */}
      <div className="bg-gray-900 rounded-xl border border-gray-800 p-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-base font-medium text-white">Semester Progress</span>
          <span className="text-base text-gray-400">{overallPct}%</span>
        </div>
        <div className="w-full h-2.5 bg-gray-800 rounded-full">
          <div
            className="h-full bg-indigo-500 rounded-full transition-all duration-500"
            style={{ width: `${overallPct}%` }}
          />
        </div>
        <p className="text-sm text-gray-500 mt-1">{completedTasks} of {totalTasks} tasks completed</p>
      </div>

      {/* Heatmap */}
      <div className="bg-gray-900 rounded-xl border border-gray-800 p-4 overflow-x-auto">
        <h3 className="text-base font-medium text-white mb-4">Completion Heatmap</h3>
        <div className="min-w-[600px]">
          {/* Header row: subject abbreviations */}
          <div className="flex gap-1 mb-1 pl-16">
            {subjects.map((s) => (
              <div key={s.id} className="w-12 text-center">
                <span className="text-xs text-gray-500">{s.short_name}</span>
              </div>
            ))}
          </div>

          {/* Data rows */}
          {heatmapData.map(({ week, subjects: subjectData }) => (
            <div key={week.id} className="flex items-center gap-1 mb-1">
              <span className="text-xs text-gray-500 w-14 text-right pr-2">KW {week.week_number}</span>
              {subjectData.map(({ subject, pct, completed, total }) => (
                <div
                  key={subject.id}
                  className="w-12 h-8 rounded-sm flex items-center justify-center group relative"
                  style={{ backgroundColor: getCellColor(pct, subject.color) }}
                >
                  {total > 0 && (
                    <span className="text-[11px] text-white/60">{completed}/{total}</span>
                  )}
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>

      {/* Per-subject bars */}
      <div className="bg-gray-900 rounded-xl border border-gray-800 p-4">
        <h3 className="text-base font-medium text-white mb-4">Per Subject</h3>
        <div className="space-y-3">
          {subjectStats.map(({ subject, completed, total, pct }) => (
            <div key={subject.id}>
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-2">
                  <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: subject.color }} />
                  <span className="text-sm text-gray-300">{subject.name}</span>
                </div>
                <span className="text-sm text-gray-500">{completed}/{total}</span>
              </div>
              <div className="w-full h-1.5 bg-gray-800 rounded-full">
                <div
                  className="h-full rounded-full transition-all duration-300"
                  style={{ width: `${pct}%`, backgroundColor: subject.color }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
