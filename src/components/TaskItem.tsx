'use client'

import { Task } from '@/lib/types'
import { supabase } from '@/lib/supabase'

interface Props {
  task: Task
  subjectColor: string
  subtitle?: string | null
  countdown?: { text: string; urgency: 'normal' | 'warning' | 'urgent' } | null
  onToggle: (taskId: string, completed: boolean) => void
  onDelete?: (taskId: string) => void
}

export default function TaskItem({ task, subjectColor, subtitle, countdown, onToggle, onDelete }: Props) {
  async function handleToggle() {
    const newVal = !task.is_completed
    onToggle(task.id, newVal)
    await supabase
      .from('tracker_tasks')
      .update({ is_completed: newVal })
      .eq('id', task.id)
  }

  return (
    <div className="py-2 group">
      <div className="flex items-center gap-3">
        <button
          onClick={handleToggle}
          className="flex-shrink-0 w-7 h-7 rounded border-2 flex items-center justify-center transition-colors"
          style={{
            borderColor: task.is_completed ? subjectColor : '#4b5563',
            backgroundColor: task.is_completed ? subjectColor : 'transparent',
          }}
        >
          {task.is_completed && (
            <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
            </svg>
          )}
        </button>

        <div className="flex-1 min-w-0 flex items-center gap-2">
          <span className={`text-lg ${task.is_completed ? 'text-gray-500 line-through' : 'text-gray-200'}`}>
            {task.title}
          </span>
          {countdown && !task.is_completed && (
            <span className={`text-xs font-medium px-1.5 py-0.5 rounded ${
              countdown.urgency === 'urgent'
                ? 'bg-red-900/40 text-red-400'
                : countdown.urgency === 'warning'
                  ? 'bg-yellow-900/40 text-yellow-400'
                  : 'bg-gray-800 text-gray-400'
            }`}>
              {countdown.text}
            </span>
          )}
        </div>

        {task.is_custom && onDelete && (
          <button
            onClick={() => onDelete(task.id)}
            className="opacity-0 group-hover:opacity-100 text-gray-500 hover:text-red-400 transition-all"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>

      {subtitle && (
        <div
          className={`ml-9 mt-1.5 rounded-lg px-3 py-2 border-l-3 ${task.is_completed ? 'opacity-40' : ''}`}
          style={{
            backgroundColor: subjectColor + '12',
            borderLeftColor: subjectColor,
          }}
        >
          <span className={`text-base ${task.is_completed ? 'text-gray-400' : 'text-gray-200'}`}>
            {subtitle}
          </span>
        </div>
      )}
    </div>
  )
}
