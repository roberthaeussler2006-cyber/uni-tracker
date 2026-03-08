'use client'

import { useState, useEffect, useCallback, useRef } from 'react'
import { supabase } from '@/lib/supabase'
import { Subject, Week, Task } from '@/lib/types'
import ProgressRing from './ProgressRing'
import TaskItem from './TaskItem'
import DailyTaskGrid from './DailyTaskGrid'
import AddTaskModal from './AddTaskModal'
import ScheduleModal from './ScheduleModal'
import ScheduleImageModal from './ScheduleImageModal'
import MathProgressTracker from './MathProgressTracker'
import ReadingProgressTracker from './ReadingProgressTracker'
import MacroReadingTracker from './MacroReadingTracker'
import { getTaskSubtitle, getTaskCountdown, getFullSchedule, hasSchedule, getScheduleImages } from '@/lib/scheduleData'

interface Props {
  subjects: Subject[]
  weeks: Week[]
  week: Week
  weekNumber: number
  isCurrentWeek: boolean
  label: string
}

export default function WeekPanel({ subjects, weeks, week, weekNumber, isCurrentWeek, label }: Props) {
  const [tasks, setTasks] = useState<Task[]>([])
  const [reflectionNotes, setReflectionNotes] = useState(week.reflection_notes || '')
  const [loading, setLoading] = useState(true)
  const [addModalSubject, setAddModalSubject] = useState<string | null>(null)
  const [scheduleSubject, setScheduleSubject] = useState<Subject | null>(null)
  const [imageSubject, setImageSubject] = useState<Subject | null>(null)
  const generatingRef = useRef<Set<string>>(new Set())

  const loadTasks = useCallback(async () => {
    setLoading(true)
    const { data: existingTasks } = await supabase
      .from('tracker_tasks')
      .select('*')
      .eq('week_id', week.id)
      .order('sort_order')

    if (existingTasks && existingTasks.length > 0) {
      setTasks(existingTasks)
      setLoading(false)
      return
    }

    if (generatingRef.current.has(week.id)) {
      return
    }
    generatingRef.current.add(week.id)

    const { data: templates } = await supabase
      .from('tracker_task_templates')
      .select('*')
      .order('sort_order')

    if (!templates || templates.length === 0) {
      generatingRef.current.delete(week.id)
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
            week_id: week.id,
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
          week_id: week.id,
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
    generatingRef.current.delete(week.id)
    setLoading(false)
  }, [week.id])

  useEffect(() => {
    loadTasks()
    setReflectionNotes(week.reflection_notes || '')
  }, [week.id, loadTasks])

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
        week_id: week.id,
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
      .eq('id', week.id)
  }

  const DAILY_WEIGHT = 1 / 7
  const completedCount = tasks.reduce((sum, t) => {
    if (!t.is_completed) return sum
    return sum + (t.day_of_week !== null ? DAILY_WEIGHT : 1)
  }, 0)
  const totalCount = tasks.reduce((sum, t) => {
    return sum + (t.day_of_week !== null ? DAILY_WEIGHT : 1)
  }, 0)

  const tasksBySubject = subjects.map((subject) => ({
    subject,
    tasks: tasks.filter((t) => t.subject_id === subject.id),
  })).filter((group) => group.tasks.length > 0)

  const isEasterBreak = weekNumber === 14 || weekNumber === 15

  return (
    <div className={`rounded-2xl border-2 p-3 ${
      isCurrentWeek
        ? 'border-blue-500/60 bg-blue-950/10'
        : 'border-gray-700/50 bg-gray-950/50'
    }`}>
      {/* Week Panel Header */}
      <div className="flex items-center gap-2 mb-3">
        <div className={`px-3 py-1 rounded-lg text-sm font-semibold ${
          isCurrentWeek
            ? 'bg-blue-600 text-white'
            : 'bg-gray-700 text-gray-300'
        }`}>
          KW {weekNumber}
        </div>
        <span className={`text-sm font-medium ${
          isCurrentWeek ? 'text-blue-400' : 'text-gray-500'
        }`}>
          {label}
        </span>
        {isCurrentWeek && (
          <span className="ml-auto flex items-center gap-1.5 text-xs text-blue-400 font-medium">
            <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
            Current
          </span>
        )}
      </div>

      {/* Easter Break Banner */}
      {isEasterBreak && (
        <div className="mb-3 p-3 bg-amber-900/20 border border-amber-800/40 rounded-xl text-center">
          <span className="text-xl">🐣</span>
          <p className="text-base font-medium text-amber-200 mt-1">Easter Break</p>
          <p className="text-sm text-amber-300/70">No lectures or exercises</p>
        </div>
      )}

      {/* Weekly Score */}
      <div className="flex items-center gap-3 mb-3 p-3 bg-gray-900 rounded-xl border border-gray-800">
        <ProgressRing completed={Math.round(completedCount)} total={Math.round(totalCount)} size={48} />
        <div>
          <div className="text-sm font-medium text-white">
            {Math.round(completedCount * 10) / 10}/{Math.round(totalCount)} tasks · {totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0}%
          </div>
        </div>
      </div>

      {loading ? (
        <div className="text-center text-gray-400 py-8 text-sm">Generating tasks...</div>
      ) : (
        <div className="space-y-3">
          {tasksBySubject.map(({ subject, tasks: subjectTasks }) => {
            const regularTasks = subjectTasks.filter((t) => t.day_of_week === null)
            const dailyTasks = subjectTasks.filter((t) => t.day_of_week !== null)

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
                    <span className="text-base font-medium text-white">{subject.short_name}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    {getScheduleImages(subject.short_name) && (
                      <button
                        onClick={() => setImageSubject(subject)}
                        className="text-gray-500 hover:text-gray-300 transition-colors"
                        title="View original schedule"
                      >
                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909M3.75 21h16.5A2.25 2.25 0 0022.5 18.75V5.25A2.25 2.25 0 0020.25 3H3.75A2.25 2.25 0 001.5 5.25v13.5A2.25 2.25 0 003.75 21z" />
                        </svg>
                      </button>
                    )}
                    {hasSchedule(subject.short_name) && (
                      <button
                        onClick={() => setScheduleSubject(subject)}
                        className="text-gray-500 hover:text-gray-300 transition-colors"
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
                      +
                    </button>
                  </div>
                </div>

                {regularTasks.map((task) => (
                  <TaskItem
                    key={task.id}
                    task={task}
                    subjectColor={subject.color}
                    subtitle={getTaskSubtitle(subject.short_name, week.week_number, task.title)}
                    countdown={getTaskCountdown(subject.short_name, task.title, weeks, week.week_number)}
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

                {subject.short_name === 'Math' && (
                  <MathProgressTracker
                    currentWeek={week}
                    selectedWeekNumber={weekNumber}
                  />
                )}
                {subject.short_name === 'Law' && (
                  <ReadingProgressTracker
                    subject="Law"
                    currentWeek={week}
                    selectedWeekNumber={weekNumber}
                  />
                )}
                {subject.short_name === 'Macro' && (
                  <MacroReadingTracker
                    selectedWeekNumber={weekNumber}
                  />
                )}
                {subject.short_name === 'BusAdmin' && weekNumber >= 10 && (
                  <ReadingProgressTracker
                    subject="BusAdmin"
                    currentWeek={week}
                    selectedWeekNumber={weekNumber}
                  />
                )}
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
          placeholder="Weekly reflection..."
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
          currentWeekNumber={week.week_number}
          onClose={() => setScheduleSubject(null)}
        />
      )}

      {imageSubject && getScheduleImages(imageSubject.short_name) && (
        <ScheduleImageModal
          subjectColor={imageSubject.color}
          images={getScheduleImages(imageSubject.short_name)!}
          onClose={() => setImageSubject(null)}
        />
      )}
    </div>
  )
}
