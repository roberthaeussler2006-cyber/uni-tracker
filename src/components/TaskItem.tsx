'use client'

import { Task } from '@/lib/types'
import { supabase } from '@/lib/supabase'

interface Props {
  task: Task
  subjectColor: string
  onToggle: (taskId: string, completed: boolean) => void
  onDelete?: (taskId: string) => void
}

export default function TaskItem({ task, subjectColor, onToggle, onDelete }: Props) {
  async function handleToggle() {
    const newVal = !task.is_completed
    onToggle(task.id, newVal)
    await supabase
      .from('tracker_tasks')
      .update({ is_completed: newVal })
      .eq('id', task.id)
  }

  return (
    <div className="flex items-center gap-3 py-1.5 group">
      <button
        onClick={handleToggle}
        className="flex-shrink-0 w-5 h-5 rounded border-2 flex items-center justify-center transition-colors"
        style={{
          borderColor: task.is_completed ? subjectColor : '#4b5563',
          backgroundColor: task.is_completed ? subjectColor : 'transparent',
        }}
      >
        {task.is_completed && (
          <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
          </svg>
        )}
      </button>

      <span className={`text-sm flex-1 ${task.is_completed ? 'text-gray-500 line-through' : 'text-gray-200'}`}>
        {task.title}
      </span>

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
  )
}
