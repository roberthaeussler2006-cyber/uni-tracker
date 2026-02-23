'use client'

import { useState, useEffect, useCallback, useRef } from 'react'
import { supabase } from '@/lib/supabase'
import { Subject, Week, Task } from '@/lib/types'
import WeekSelector from './WeekSelector'
import ProgressRing from './ProgressRing'
import TaskItem from './TaskItem'
import DailyTaskGrid from './DailyTaskGrid'
import AddTaskModal from './AddTaskModal'
import ScheduleModal from './ScheduleModal'
import { getTaskSubtitle, getFullSchedule, hasSchedule } from '@/lib/scheduleData'

interface Props {
  subjects: Subject[]
  weeks: Week[]
  currentWeek: Week
  selectedWeekNumber: number
  onWeekChange: (weekNumber: number) => void
}

export default function WeeklyView({ subjects, weeks, currentWeek, selectedWeekNumber, onWeekChange }: Props) {
  const [tasks, setTasks] = useState<Task[]>([])
  const [reflectionNotes, setReflectionNotes] = useState(currentWeek.reflection_notes || '')
  const [loading, setLoading] = useState(true)
  const [addModalSubject, setAddModalSubject] = useState<string | null>(null)
  const [scheduleSubject, setScheduleSubject] = useState<Subject | null>(null)
  const generatingRef = useRef<Set<string>>(new Set())

  const loadTasks = useCallback(async () => {
    setLoading(true)
    const { data: existingTasks } = await supabase
      .from('tracker_tasks')
      .select('*')
      .eq('week_id', currentWeek.id)
      .order('sort_order')

    if (existingTasks && existingTasks.length > 0) {
      setTasks(existingTasks)
      setLoading(false)
      return
    }

    // Guard against double-generation (React Strict Mode)
    if (generatingRef.current.has(currentWeek.id)) {
      return
    }
    generatingRef.current.add(currentWeek.id)

    // Auto-generate tasks from templates
    const { data: templates } = await supabase
      .from('tracker_task_templates')
      .select('*')
      .order('sort_order')

    if (!templates || templates.length === 0) {
      generatingRef.current.delete(currentWeek.id)
      setLoading(false)
      return
    }

    const newTasks: Omit<Task, 'id'>[] = []
    let sortOrder = 0

    for (const template of templates) {
      if (template.is_daily) {
        for (let day = 0; day < 7; day++) {
          newTasks.push({
            subject_id: template.subject_id,
            week_id: currentWeek.id,
            template_id: template.id,
            title: template.title,
            is_completed: false,
            is_custom: false,
            day_of_week: day,
            sort_order: sortOrder++,
          })
        }
      } else {
        newTasks.push({
          subject_id: template.subject_id,
          week_id: currentWeek.id,
          template_id: template.id,
          title: template.title,
          is_completed: false,
          is_custom: false,
          day_of_week: null,
          sort_order: sortOrder++,
        })
      }
    }

    const { data: inserted } = await supabase
      .from('tracker_tasks')
      .insert(newTasks)
      .select()

    if (inserted) setTasks(inserted)
    generatingRef.current.delete(currentWeek.id)
    setLoading(false)
  }, [currentWeek.id])

  useEffect(() => {
    loadTasks()
    setReflectionNotes(currentWeek.reflection_notes || '')
  }, [currentWeek.id, loadTasks])

  function handleToggle(taskId: string, completed: boolean) {
    setTasks((prev) =>
      prev.map((t) => (t.id === taskId ? { ...t, is_completed: completed } : t))
    )
  }

  async function handleDeleteTask(taskId: string) {
    setTasks((prev) => prev.filter((t) => t.id !== taskId))
    await supabase.from('tracker_tasks').delete().eq('id', taskId)
  }

  async function handleAddTask(title: string, subjectId: string) {
    const maxSort = Math.max(0, ...tasks.filter((t) => t.subject_id === subjectId).map((t) => t.sort_order))
    const { data } = await supabase
      .from('tracker_tasks')
      .insert({
        subject_id: subjectId,
        week_id: currentWeek.id,
        template_id: null,
        title,
        is_completed: false,
        is_custom: true,
        day_of_week: null,
        sort_order: maxSort + 1,
      })
      .select()
      .single()

    if (data) setTasks((prev) => [...prev, data])
  }

  async function saveReflection(notes: string) {
    setReflectionNotes(notes)
    await supabase
      .from('tracker_weeks')
      .update({ reflection_notes: notes || null })
      .eq('id', currentWeek.id)
  }

  const completedCount = tasks.filter((t) => t.is_completed).length
  const totalCount = tasks.length

  // Group tasks by subject
  const tasksBySubject = subjects.map((subject) => ({
    subject,
    tasks: tasks.filter((t) => t.subject_id === subject.id),
  })).filter((group) => group.tasks.length > 0)

  return (
    <div>
      <WeekSelector
        weeks={weeks}
        selectedWeekNumber={selectedWeekNumber}
        onWeekChange={onWeekChange}
      />

      {/* Weekly Score */}
      <div className="flex items-center gap-3 mb-3 p-3 bg-gray-900 rounded-xl border border-gray-800">
        <ProgressRing completed={completedCount} total={totalCount} size={52} />
        <div>
          <div className="text-sm font-medium text-white">
            {completedCount}/{totalCount} tasks · {totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0}%
          </div>
        </div>
      </div>

      {loading ? (
        <div className="text-center text-gray-400 py-12">Generating tasks...</div>
      ) : (
        <div className="md:columns-2 gap-3 space-y-3">
          {tasksBySubject.map(({ subject, tasks: subjectTasks }) => {
            const regularTasks = subjectTasks.filter((t) => t.day_of_week === null)
            const dailyTasks = subjectTasks.filter((t) => t.day_of_week !== null)

            // Group daily tasks by template
            const dailyGroups = new Map<string, Task[]>()
            dailyTasks.forEach((t) => {
              const key = t.template_id || t.title
              if (!dailyGroups.has(key)) dailyGroups.set(key, [])
              dailyGroups.get(key)!.push(t)
            })

            return (
              <div key={subject.id} className="bg-gray-900 rounded-xl border border-gray-800 p-3 break-inside-avoid">
                <div className="flex items-center justify-between mb-1.5">
                  <div className="flex items-center gap-2">
                    <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: subject.color }} />
                    <span className="text-base font-medium text-white">{subject.name}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    {hasSchedule(subject.short_name) && (
                      <button
                        onClick={() => setScheduleSubject(subject)}
                        className="text-sm text-gray-500 hover:text-gray-300 transition-colors"
                        title="View schedule"
                      >
                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" />
                        </svg>
                      </button>
                    )}
                    <button
                      onClick={() => setAddModalSubject(subject.id)}
                      className="text-sm text-gray-500 hover:text-gray-300 transition-colors"
                    >
                      + add
                    </button>
                  </div>
                </div>

                {regularTasks.map((task) => (
                  <TaskItem
                    key={task.id}
                    task={task}
                    subjectColor={subject.color}
                    subtitle={getTaskSubtitle(subject.short_name, currentWeek.week_number, task.title)}
                    onToggle={handleToggle}
                    onDelete={task.is_custom ? handleDeleteTask : undefined}
                  />
                ))}

                {Array.from(dailyGroups.entries()).map(([key, dayTasks]) => (
                  <DailyTaskGrid
                    key={key}
                    title={dayTasks[0].title}
                    tasks={dayTasks}
                    subjectColor={subject.color}
                    onToggle={handleToggle}
                  />
                ))}
              </div>
            )
          })}
        </div>
      )}

      {/* Weekly Reflection */}
      <div className="mt-3">
        <textarea
          value={reflectionNotes}
          onChange={(e) => setReflectionNotes(e.target.value)}
          onBlur={() => saveReflection(reflectionNotes)}
          placeholder="Weekly reflection notes..."
          rows={2}
          className="w-full px-3 py-2 bg-gray-900 border border-gray-800 rounded-xl text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-gray-700 resize-none"
        />
      </div>

      {addModalSubject && (
        <AddTaskModal
          subjects={subjects}
          defaultSubjectId={addModalSubject}
          onAdd={handleAddTask}
          onClose={() => setAddModalSubject(null)}
        />
      )}

      {scheduleSubject && getFullSchedule(scheduleSubject.short_name) && (
        <ScheduleModal
          subjectName={scheduleSubject.name}
          subjectShortName={scheduleSubject.short_name}
          subjectColor={scheduleSubject.color}
          entries={getFullSchedule(scheduleSubject.short_name)!}
          currentWeekNumber={currentWeek.week_number}
          onClose={() => setScheduleSubject(null)}
        />
      )}
    </div>
  )
}
