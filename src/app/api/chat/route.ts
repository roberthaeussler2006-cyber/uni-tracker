import { NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || ''
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''

async function getTrackerContext() {
  if (!supabaseUrl || !supabaseAnonKey) {
    return 'No database connection available.'
  }

  const supabase = createClient(supabaseUrl, supabaseAnonKey)

  const [subjectsRes, deadlinesRes, weeksRes, tasksRes] = await Promise.all([
    supabase.from('tracker_subjects').select('id, name, short_name, schedule').order('sort_order'),
    supabase.from('tracker_deadlines').select('*, tracker_subjects(name, short_name)').order('date'),
    supabase.from('tracker_weeks').select('*').order('week_number'),
    supabase.from('tracker_tasks').select('*, tracker_subjects(name, short_name)').order('created_at', { ascending: false }).limit(100),
  ])

  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const todayStr = today.toISOString().split('T')[0]

  const subjects = subjectsRes.data || []
  const deadlines = deadlinesRes.data || []
  const weeks = weeksRes.data || []
  const tasks = tasksRes.data || []

  const upcomingDeadlines = deadlines.filter((d: { date: string }) => d.date >= todayStr)
  const pastDeadlines = deadlines.filter((d: { date: string }) => d.date < todayStr)

  // Calculate days until each deadline
  const deadlinesWithDays = upcomingDeadlines.map((d: { date: string; title: string; description: string | null; is_milestone: boolean; tracker_subjects: { name: string; short_name: string } | null }) => {
    const target = new Date(d.date + 'T00:00:00')
    const days = Math.ceil((target.getTime() - today.getTime()) / 86400000)
    return {
      title: d.title,
      date: d.date,
      days_until: days,
      description: d.description,
      is_milestone: d.is_milestone,
      subject: d.tracker_subjects?.name || 'General',
    }
  })

  // Task completion stats
  const completedTasks = tasks.filter((t: { is_completed: boolean }) => t.is_completed).length
  const totalTasks = tasks.length

  return `TODAY'S DATE: ${todayStr}

SUBJECTS:
${subjects.map((s: { name: string; short_name: string; schedule: string | null }) => `- ${s.name} (${s.short_name})${s.schedule ? ` — Schedule: ${s.schedule}` : ''}`).join('\n')}

UPCOMING DEADLINES (${upcomingDeadlines.length}):
${deadlinesWithDays.length > 0 ? deadlinesWithDays.map((d: { title: string; subject: string; date: string; days_until: number; description: string | null; is_milestone: boolean }) =>
    `- ${d.title} [${d.subject}] — ${d.date} (${d.days_until} days away)${d.description ? ` — ${d.description}` : ''}${d.is_milestone ? ' [MILESTONE]' : ''}`
  ).join('\n') : 'No upcoming deadlines.'}

PAST DEADLINES (${pastDeadlines.length}):
${pastDeadlines.length > 0 ? pastDeadlines.map((d: { title: string; date: string; tracker_subjects: { name: string } | null }) =>
    `- ${d.title} [${d.tracker_subjects?.name || 'General'}] — ${d.date}`
  ).join('\n') : 'None.'}

SEMESTER WEEKS:
${weeks.map((w: { week_number: number; start_date: string; end_date: string }) => `- Week ${w.week_number}: ${w.start_date} to ${w.end_date}`).join('\n')}

TASK COMPLETION: ${completedTasks}/${totalTasks} tasks completed`
}

export async function POST(request: Request) {
  try {
    const { messages } = await request.json()

    if (!messages || !Array.isArray(messages)) {
      return NextResponse.json({ error: 'Messages required' }, { status: 400 })
    }

    const context = await getTrackerContext()

    const systemMessage = {
      role: 'system',
      content: `You are a helpful university study assistant for an HSG (University of St. Gallen) student. You have access to their tracker data including deadlines, subjects, tasks, and schedule.

Answer questions about their deadlines, upcoming tasks, study schedule, and provide helpful study advice. Be concise, friendly, and direct. Use the data below to give accurate answers.

When discussing deadlines, always mention how many days away they are. If a deadline is within 3 days, emphasize urgency. Group related information logically.

${context}`
    }

    const apiMessages = [systemMessage, ...messages]

    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.OPENROUTER_API_KEY}`,
      },
      body: JSON.stringify({
        model: 'moonshotai/kimi-k2',
        messages: apiMessages,
        max_tokens: 1024,
        temperature: 0.7,
      }),
    })

    if (!response.ok) {
      const error = await response.text()
      console.error('OpenRouter error:', error)
      return NextResponse.json({ error: 'AI service error' }, { status: 502 })
    }

    const data = await response.json()
    const reply = data.choices?.[0]?.message?.content || 'Sorry, I could not generate a response.'

    return NextResponse.json({ message: reply })
  } catch (error) {
    console.error('Chat API error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}
