'use client'

import { useState, useEffect } from 'react'
import { supabase } from '@/lib/supabase'
import { Subject, Week, TabType } from '@/lib/types'
import { getCurrentWeekNumber } from '@/lib/weeks'
import WeeklyView from '@/components/WeeklyView'
import SubjectsView from '@/components/SubjectsView'
import AnalyticsView from '@/components/AnalyticsView'
import DeadlinesView from '@/components/DeadlinesView'
import Chatbot from '@/components/Chatbot'

const TABS: { key: TabType; label: string }[] = [
  { key: 'weekly', label: 'Weekly' },
  { key: 'subjects', label: 'Subjects' },
  { key: 'analytics', label: 'Analytics' },
  { key: 'deadlines', label: 'Deadlines' },
]

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState<TabType>('weekly')
  const [subjects, setSubjects] = useState<Subject[]>([])
  const [weeks, setWeeks] = useState<Week[]>([])
  const [currentWeek, setCurrentWeek] = useState<Week | null>(null)
  const [selectedWeekNumber, setSelectedWeekNumber] = useState(getCurrentWeekNumber())
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      const [subjectsRes, weeksRes] = await Promise.all([
        supabase.from('tracker_subjects').select('*').order('sort_order'),
        supabase.from('tracker_weeks').select('*').order('week_number'),
      ])
      if (subjectsRes.data) setSubjects(subjectsRes.data)
      if (weeksRes.data) {
        setWeeks(weeksRes.data)
        const week = weeksRes.data.find((w: Week) => w.week_number === selectedWeekNumber)
        setCurrentWeek(week || weeksRes.data[0])
      }
      setLoading(false)
    }
    load()
  }, [])

  useEffect(() => {
    const week = weeks.find((w) => w.week_number === selectedWeekNumber)
    if (week) setCurrentWeek(week)
  }, [selectedWeekNumber, weeks])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <div className="text-gray-400">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-950">
      <header className="sticky top-0 z-50 bg-gray-950/80 backdrop-blur-sm border-b border-gray-800">
        <div className="max-w-5xl mx-auto px-4">
          <div className="flex items-center justify-between h-14">
            <span className="text-base font-medium text-gray-400">HSG Tracker</span>
            <span className="text-sm text-gray-500">KW {selectedWeekNumber}</span>
          </div>
          <nav className="flex gap-1 pb-2">
            {TABS.map((tab) => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                className={`px-4 py-1.5 rounded-md text-base font-medium transition-colors ${
                  activeTab === tab.key
                    ? 'bg-gray-800 text-white'
                    : 'text-gray-400 hover:text-gray-200 hover:bg-gray-900'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-6">
        {activeTab === 'weekly' && currentWeek && (
          <WeeklyView
            subjects={subjects}
            weeks={weeks}
            currentWeek={currentWeek}
            selectedWeekNumber={selectedWeekNumber}
            onWeekChange={setSelectedWeekNumber}
          />
        )}
        {activeTab === 'subjects' && currentWeek && (
          <SubjectsView subjects={subjects} weeks={weeks} currentWeek={currentWeek} />
        )}
        {activeTab === 'analytics' && (
          <AnalyticsView subjects={subjects} weeks={weeks} />
        )}
        {activeTab === 'deadlines' && (
          <DeadlinesView subjects={subjects} />
        )}
      </main>

      <Chatbot />
    </div>
  )
}
