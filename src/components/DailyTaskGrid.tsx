'use client'

import { Task, DAY_NAMES } from '@/lib/types'
import { supabase } from '@/lib/supabase'

interface Props {
  title: string
  tasks: Task[] // 7 tasks, one per day (Mon-Sun)
  subjectColor: string
  onToggle: (taskId: string, completed: boolean) => void
}

export default function DailyTaskGrid({ title, tasks, subjectColor, onToggle }: Props) {
  const sortedTasks = [...tasks].sort((a, b) => (a.day_of_week ?? 0) - (b.day_of_week ?? 0))
  const completedCount = sortedTasks.filter((t) => t.is_completed).length

  async function handleToggle(task: Task) {
    const newVal = !task.is_completed
    onToggle(task.id, newVal)
    await supabase
      .from('tracker_tasks')
      .update({ is_completed: newVal })
      .eq('id', task.id)
  }

  return (
    <div className="py-1.5">
      <div className="flex items-center gap-2 mb-1">
        <span className={`text-base ${completedCount === 7 ? 'text-gray-500 line-through' : 'text-gray-200'}`}>
          {title}
        </span>
        <span className="text-sm text-gray-500">{completedCount}/7</span>
      </div>
      <div className="flex gap-1.5">
        {sortedTasks.map((task, i) => (
          <button
            key={task.id}
            onClick={() => handleToggle(task)}
            className="flex flex-col items-center gap-0.5"
          >
            <span className="text-xs text-gray-500">{DAY_NAMES[i]}</span>
            <div
              className="w-8 h-8 rounded flex items-center justify-center transition-colors"
              style={{
                backgroundColor: task.is_completed ? subjectColor : '#1f2937',
                border: task.is_completed ? 'none' : '1px solid #374151',
              }}
            >
              {task.is_completed && (
                <svg className="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                </svg>
              )}
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}
