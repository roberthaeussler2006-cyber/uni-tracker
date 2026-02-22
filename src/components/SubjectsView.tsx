'use client'

import { useState, useEffect } from 'react'
import { supabase } from '@/lib/supabase'
import { Subject, Week, Task, SubjectNote } from '@/lib/types'

interface Props {
  subjects: Subject[]
  weeks: Week[]
  currentWeek: Week
}

export default function SubjectsView({ subjects, weeks, currentWeek }: Props) {
  const [tasks, setTasks] = useState<Task[]>([])
  const [notes, setNotes] = useState<Record<string, string>>({})
  const [expandedSubject, setExpandedSubject] = useState<string | null>(null)
  const [allTasks, setAllTasks] = useState<Task[]>([])

  useEffect(() => {
    async function load() {
      const [tasksRes, notesRes] = await Promise.all([
        supabase.from('tracker_tasks').select('*').eq('week_id', currentWeek.id),
        supabase.from('tracker_subject_notes').select('*').eq('week_id', currentWeek.id),
      ])
      if (tasksRes.data) setTasks(tasksRes.data)
      if (notesRes.data) {
        const noteMap: Record<string, string> = {}
        notesRes.data.forEach((n: SubjectNote) => {
          noteMap[n.subject_id] = n.content || ''
        })
        setNotes(noteMap)
      }
    }
    load()
  }, [currentWeek.id])

  async function loadAllTasks() {
    const { data } = await supabase
      .from('tracker_tasks')
      .select('*')
      .order('sort_order')
    if (data) setAllTasks(data)
  }

  useEffect(() => {
    if (expandedSubject) loadAllTasks()
  }, [expandedSubject])

  async function saveNote(subjectId: string, content: string) {
    setNotes((prev) => ({ ...prev, [subjectId]: content }))
    await supabase
      .from('tracker_subject_notes')
      .upsert(
        { subject_id: subjectId, week_id: currentWeek.id, content: content || null, updated_at: new Date().toISOString() },
        { onConflict: 'subject_id,week_id' }
      )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {subjects.map((subject) => {
        const subjectTasks = tasks.filter((t) => t.subject_id === subject.id)
        const completed = subjectTasks.filter((t) => t.is_completed).length
        const total = subjectTasks.length
        const isExpanded = expandedSubject === subject.id

        return (
          <div key={subject.id} className="bg-gray-900 rounded-xl border border-gray-800 overflow-hidden">
            {/* Color bar */}
            <div className="h-1" style={{ backgroundColor: subject.color }} />

            <div className="p-4">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className="text-base font-medium text-white">{subject.name}</span>
                </div>
                <span className="text-sm text-gray-400">
                  {total > 0 ? `${completed}/${total}` : 'No tasks'}
                </span>
              </div>

              {/* Progress bar */}
              {total > 0 && (
                <div className="w-full h-1.5 bg-gray-800 rounded-full mb-3">
                  <div
                    className="h-full rounded-full transition-all duration-300"
                    style={{
                      width: `${(completed / total) * 100}%`,
                      backgroundColor: subject.color,
                    }}
                  />
                </div>
              )}

              {/* Schedule */}
              {subject.schedule && (
                <p className="text-sm text-gray-500 mb-2">{subject.schedule}</p>
              )}

              {/* Note */}
              <textarea
                value={notes[subject.id] || ''}
                onChange={(e) => setNotes((prev) => ({ ...prev, [subject.id]: e.target.value }))}
                onBlur={() => saveNote(subject.id, notes[subject.id] || '')}
                placeholder="Notes for this week..."
                rows={2}
                className="w-full px-3 py-2 bg-gray-800 border border-gray-700/50 rounded-lg text-sm text-gray-300 placeholder-gray-600 focus:outline-none focus:border-gray-600 resize-none"
              />

              {/* Expand / collapse for history */}
              <button
                onClick={() => setExpandedSubject(isExpanded ? null : subject.id)}
                className="mt-2 text-sm text-gray-500 hover:text-gray-300 transition-colors"
              >
                {isExpanded ? 'Hide history' : 'Show history'}
              </button>

              {isExpanded && (
                <div className="mt-3 space-y-2 border-t border-gray-800 pt-3">
                  {weeks.map((week) => {
                    const weekTasks = allTasks.filter(
                      (t) => t.subject_id === subject.id && t.week_id === week.id
                    )
                    if (weekTasks.length === 0) return null
                    const weekCompleted = weekTasks.filter((t) => t.is_completed).length
                    const weekTotal = weekTasks.length
                    const pct = Math.round((weekCompleted / weekTotal) * 100)

                    return (
                      <div key={week.id} className="flex items-center gap-2">
                        <span className="text-sm text-gray-500 w-12">KW {week.week_number}</span>
                        <div className="flex-1 h-1.5 bg-gray-800 rounded-full">
                          <div
                            className="h-full rounded-full"
                            style={{
                              width: `${pct}%`,
                              backgroundColor: subject.color,
                              opacity: pct > 0 ? 1 : 0.2,
                            }}
                          />
                        </div>
                        <span className="text-sm text-gray-500 w-14 text-right">{weekCompleted}/{weekTotal}</span>
                      </div>
                    )
                  })}
                </div>
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
}
