export function getCurrentWeekNumber(): number {
  const now = new Date()
  const startOfYear = new Date(now.getFullYear(), 0, 1)
  const dayOfYear = Math.floor((now.getTime() - startOfYear.getTime()) / 86400000)
  const dayOfWeek = startOfYear.getDay() || 7 // ISO: Monday = 1
  const weekNumber = Math.ceil((dayOfYear + dayOfWeek) / 7)
  // Clamp to our semester range
  return Math.max(9, Math.min(22, weekNumber))
}

export function formatDateRange(startDate: string, endDate: string): string {
  const start = new Date(startDate + 'T00:00:00')
  const end = new Date(endDate + 'T00:00:00')
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  return `${months[start.getMonth()]} ${start.getDate()} \u2013 ${months[end.getMonth()]} ${end.getDate()}`
}

export function daysUntil(dateStr: string): number {
  const target = new Date(dateStr + 'T00:00:00')
  const now = new Date()
  now.setHours(0, 0, 0, 0)
  return Math.ceil((target.getTime() - now.getTime()) / 86400000)
}

// Get the next occurrence of a specific weekday+time from now
// dayOfWeek: 0=Sun, 1=Mon, 2=Tue, ..., 5=Fri, 6=Sat
export function getNextWeekday(dayOfWeek: number, hour: number, minute: number): Date {
  const now = new Date()
  const target = new Date()
  target.setHours(hour, minute, 0, 0)

  // Set to the correct day of this week
  const diff = dayOfWeek - now.getDay()
  target.setDate(now.getDate() + diff)

  // If that's in the past, jump to next week
  if (target <= now) {
    target.setDate(target.getDate() + 7)
  }

  return target
}

// Get the Friday (day 5) date for a given week start date (Monday)
export function getFridayOfWeek(weekStartDate: string): Date {
  const monday = new Date(weekStartDate + 'T10:00:00') // use 10:00 as default exercise time
  monday.setDate(monday.getDate() + 4) // Monday + 4 = Friday
  return monday
}

// Format a countdown from now to a target date
export function formatCountdown(target: Date): { text: string; urgency: 'normal' | 'warning' | 'urgent' } | null {
  const now = new Date()
  const diffMs = target.getTime() - now.getTime()

  if (diffMs <= 0) return null // past

  const totalMinutes = Math.floor(diffMs / 60000)
  const totalHours = Math.floor(totalMinutes / 60)
  const days = Math.floor(totalHours / 24)
  const hours = totalHours % 24

  let text: string
  let urgency: 'normal' | 'warning' | 'urgent'

  if (days > 7) {
    text = `${days}d`
    urgency = 'normal'
  } else if (days >= 1) {
    text = `${days}d ${hours}h`
    urgency = days <= 3 ? 'warning' : 'normal'
  } else {
    const mins = totalMinutes % 60
    text = `${hours}h ${mins}m`
    urgency = 'urgent'
  }

  return { text, urgency }
}
