'use client'

import { useState, useEffect } from 'react'
import { supabase } from '@/lib/supabase'
import { Subject, Deadline } from '@/lib/types'
import { daysUntil } from '@/lib/weeks'

interface Props {
  subjects: Subject[]
}

export default function DeadlinesView({ subjects }: Props) {
  const [deadlines, setDeadlines] = useState<Deadline[]>([])
  const [loading, setLoading] = useState(true)
  const [showAdd, setShowAdd] = useState(false)
  const [newTitle, setNewTitle] = useState('')
  const [newDate, setNewDate] = useState('')
  const [newSubject, setNewSubject] = useState('')
  const [newDescription, setNewDescription] = useState('')

  useEffect(() => {
    async function load() {
      const { data } = await supabase
        .from('tracker_deadlines')
        .select('*')
        .order('date')
      if (data) setDeadlines(data)
      setLoading(false)
    }
    load()
  }, [])

  async function addDeadline(e: React.FormEvent) {
    e.preventDefault()
    if (!newTitle.trim() || !newDate) return

    const { data } = await supabase
      .from('tracker_deadlines')
      .insert({
        title: newTitle.trim(),
        date: newDate,
        subject_id: newSubject || null,
        description: newDescription.trim() || null,
        is_milestone: false,
      })
      .select()
      .single()

    if (data) {
      setDeadlines((prev) => [...prev, data].sort((a, b) => a.date.localeCompare(b.date)))
      setNewTitle('')
      setNewDate('')
      setNewSubject('')
      setNewDescription('')
      setShowAdd(false)
    }
  }

  async function deleteDeadline(id: string) {
    setDeadlines((prev) => prev.filter((d) => d.id !== id))
    await supabase.from('tracker_deadlines').delete().eq('id', id)
  }

  function getSubjectColor(subjectId: string | null): string {
    if (!subjectId) return '#6b7280'
    return subjects.find((s) => s.id === subjectId)?.color || '#6b7280'
  }

  function getSubjectName(subjectId: string | null): string {
    if (!subjectId) return 'General'
    return subjects.find((s) => s.id === subjectId)?.short_name || 'General'
  }

  if (loading) {
    return <div className="text-center text-gray-400 py-12">Loading deadlines...</div>
  }

  const upcoming = deadlines.filter((d) => daysUntil(d.date) >= 0)
  const past = deadlines.filter((d) => daysUntil(d.date) < 0)

  // Find the furthest deadline for countdown bar scaling
  const maxDays = Math.max(1, ...upcoming.map((d) => daysUntil(d.date)))

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-sm font-medium text-gray-400">Upcoming</h2>
        <button
          onClick={() => setShowAdd(!showAdd)}
          className="text-xs text-gray-500 hover:text-gray-300 transition-colors"
        >
          {showAdd ? 'Cancel' : '+ Add deadline'}
        </button>
      </div>

      {showAdd && (
        <form onSubmit={addDeadline} className="bg-gray-900 rounded-xl border border-gray-800 p-4 space-y-3">
          <input
            type="text"
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            placeholder="Deadline title"
            autoFocus
            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-sm text-white placeholder-gray-500 focus:outline-none focus:border-gray-600"
          />
          <div className="flex gap-2">
            <input
              type="date"
              value={newDate}
              onChange={(e) => setNewDate(e.target.value)}
              className="flex-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-sm text-white focus:outline-none focus:border-gray-600"
            />
            <select
              value={newSubject}
              onChange={(e) => setNewSubject(e.target.value)}
              className="flex-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-sm text-white focus:outline-none focus:border-gray-600"
            >
              <option value="">General</option>
              {subjects.map((s) => (
                <option key={s.id} value={s.id}>{s.name}</option>
              ))}
            </select>
          </div>
          <input
            type="text"
            value={newDescription}
            onChange={(e) => setNewDescription(e.target.value)}
            placeholder="Description (optional)"
            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-sm text-white placeholder-gray-500 focus:outline-none focus:border-gray-600"
          />
          <button
            type="submit"
            disabled={!newTitle.trim() || !newDate}
            className="w-full py-2 text-sm text-white bg-indigo-600 hover:bg-indigo-500 rounded-lg disabled:opacity-50 transition-colors"
          >
            Add Deadline
          </button>
        </form>
      )}

      {upcoming.length === 0 ? (
        <div className="text-center text-gray-500 py-8 text-sm">No upcoming deadlines</div>
      ) : (
        upcoming.map((deadline) => {
          const days = daysUntil(deadline.date)
          const color = getSubjectColor(deadline.subject_id)
          const barWidth = Math.max(5, ((maxDays - days) / maxDays) * 100)

          return (
            <div key={deadline.id} className="bg-gray-900 rounded-xl border border-gray-800 p-4 group">
              <div className="flex items-start justify-between mb-2">
                <div>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: color }} />
                    <span className="text-sm font-medium text-white">{deadline.title}</span>
                  </div>
                  <div className="flex items-center gap-2 mt-0.5 ml-4">
                    <span className="text-xs text-gray-500">{getSubjectName(deadline.subject_id)}</span>
                    <span className="text-xs text-gray-600">·</span>
                    <span className="text-xs text-gray-500">{deadline.date}</span>
                  </div>
                  {deadline.description && (
                    <p className="text-xs text-gray-500 mt-1 ml-4">{deadline.description}</p>
                  )}
                </div>
                <div className="flex items-center gap-2">
                  <div className="text-right">
                    <span className={`text-lg font-bold ${days <= 3 ? 'text-red-400' : days <= 7 ? 'text-yellow-400' : 'text-white'}`}>
                      {days}
                    </span>
                    <span className="text-xs text-gray-500 ml-1">days</span>
                  </div>
                  <button
                    onClick={() => deleteDeadline(deadline.id)}
                    className="opacity-0 group-hover:opacity-100 text-gray-500 hover:text-red-400 transition-all p-1"
                  >
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>

              {/* Countdown bar */}
              <div className="w-full h-1 bg-gray-800 rounded-full mt-2">
                <div
                  className="h-full rounded-full transition-all"
                  style={{ width: `${barWidth}%`, backgroundColor: color }}
                />
              </div>
            </div>
          )
        })
      )}

      {past.length > 0 && (
        <>
          <h2 className="text-sm font-medium text-gray-500 mt-8 mb-2">Past</h2>
          {past.map((deadline) => (
            <div key={deadline.id} className="bg-gray-900/50 rounded-xl border border-gray-800/50 p-4 opacity-50">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: getSubjectColor(deadline.subject_id) }} />
                <span className="text-sm text-gray-400 line-through">{deadline.title}</span>
                <span className="text-xs text-gray-600 ml-auto">{deadline.date}</span>
              </div>
            </div>
          ))}
        </>
      )}
    </div>
  )
}
