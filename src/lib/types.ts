export interface Subject {
  id: string
  name: string
  short_name: string
  color: string
  has_daily_tasks: boolean
  is_milestone_based: boolean
  sort_order: number
  schedule: string | null
}

export interface TaskTemplate {
  id: string
  subject_id: string
  title: string
  is_daily: boolean
  sort_order: number
}

export interface Week {
  id: string
  week_number: number
  start_date: string
  end_date: string
  reflection_notes: string | null
}

export interface Task {
  id: string
  subject_id: string
  week_id: string
  template_id: string | null
  title: string
  is_completed: boolean
  is_custom: boolean
  day_of_week: number | null
  sort_order: number
}

export interface SubjectNote {
  id: string
  subject_id: string
  week_id: string
  content: string | null
  updated_at: string
}

export interface Deadline {
  id: string
  title: string
  date: string
  subject_id: string | null
  description: string | null
  is_milestone: boolean
}

export type TabType = 'weekly' | 'subjects' | 'analytics' | 'deadlines'

export const DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] as const
