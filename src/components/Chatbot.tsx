'use client'

import { useState, useRef, useEffect, useMemo } from 'react'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

function renderMarkdown(text: string) {
  const lines = text.split('\n')
  const elements: React.ReactNode[] = []
  let listItems: React.ReactNode[] = []
  let listType: 'ul' | 'ol' | null = null
  let key = 0

  function flushList() {
    if (listItems.length > 0 && listType) {
      if (listType === 'ul') {
        elements.push(<ul key={key++} className="list-disc list-inside space-y-0.5 my-1">{listItems}</ul>)
      } else {
        elements.push(<ol key={key++} className="list-decimal list-inside space-y-0.5 my-1">{listItems}</ol>)
      }
      listItems = []
      listType = null
    }
  }

  function formatInline(str: string): React.ReactNode {
    // Bold: **text**
    const parts: React.ReactNode[] = []
    let remaining = str
    let inlineKey = 0
    while (remaining.length > 0) {
      const boldMatch = remaining.match(/\*\*(.+?)\*\*/)
      if (boldMatch && boldMatch.index !== undefined) {
        if (boldMatch.index > 0) {
          parts.push(remaining.slice(0, boldMatch.index))
        }
        parts.push(<strong key={inlineKey++} className="font-semibold text-white">{boldMatch[1]}</strong>)
        remaining = remaining.slice(boldMatch.index + boldMatch[0].length)
      } else {
        parts.push(remaining)
        break
      }
    }
    return parts.length === 1 ? parts[0] : <>{parts}</>
  }

  for (const line of lines) {
    const trimmed = line.trim()

    // Empty line
    if (trimmed === '') {
      flushList()
      elements.push(<div key={key++} className="h-2" />)
      continue
    }

    // Unordered list: - item or • item or → item
    const ulMatch = trimmed.match(/^[-•→]\s+(.+)/)
    if (ulMatch) {
      if (listType !== 'ul') flushList()
      listType = 'ul'
      listItems.push(<li key={key++} className="text-gray-300">{formatInline(ulMatch[1])}</li>)
      continue
    }

    // Ordered list: 1. item
    const olMatch = trimmed.match(/^(\d+)[.)]\s+(.+)/)
    if (olMatch) {
      if (listType !== 'ol') flushList()
      listType = 'ol'
      listItems.push(<li key={key++} className="text-gray-300">{formatInline(olMatch[2])}</li>)
      continue
    }

    // Indented sub-items (→ or spaces + -)
    const subMatch = trimmed.match(/^\s{2,}[→\-•]\s*(.+)/)
    if (subMatch && listType) {
      listItems.push(<li key={key++} className="text-gray-400 ml-4 text-xs">{formatInline(subMatch[1])}</li>)
      continue
    }

    // Regular paragraph
    flushList()
    elements.push(<p key={key++} className="my-0.5">{formatInline(trimmed)}</p>)
  }

  flushList()
  return elements
}

function FormattedMessage({ content, isUser }: { content: string; isUser: boolean }) {
  const rendered = useMemo(() => isUser ? null : renderMarkdown(content), [content, isUser])

  if (isUser) {
    return <>{content}</>
  }

  return <div className="space-y-0">{rendered}</div>
}

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus()
    }
  }, [isOpen])

  async function sendMessage(e: React.FormEvent) {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage: Message = { role: 'user', content: input.trim() }
    const newMessages = [...messages, userMessage]
    setMessages(newMessages)
    setInput('')
    setLoading(true)

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: newMessages }),
      })

      const data = await res.json()

      if (data.error) {
        setMessages([...newMessages, { role: 'assistant', content: 'Sorry, something went wrong. Try again.' }])
      } else {
        setMessages([...newMessages, { role: 'assistant', content: data.message }])
      }
    } catch {
      setMessages([...newMessages, { role: 'assistant', content: 'Connection error. Please try again.' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      {/* Floating button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 z-50 w-14 h-14 bg-indigo-600 hover:bg-indigo-500 text-white rounded-full shadow-lg shadow-indigo-500/25 flex items-center justify-center transition-all hover:scale-105 active:scale-95"
      >
        {isOpen ? (
          <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        ) : (
          <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        )}
      </button>

      {/* Chat panel */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 z-50 w-[360px] max-h-[500px] bg-gray-900 border border-gray-800 rounded-2xl shadow-2xl shadow-black/50 flex flex-col overflow-hidden">
          {/* Header */}
          <div className="px-4 py-3 border-b border-gray-800 flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-indigo-600/20 flex items-center justify-center">
              <svg className="w-4 h-4 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <div>
              <div className="text-sm font-medium text-white">Study Assistant</div>
              <div className="text-xs text-gray-500">Ask about deadlines, tasks & schedule</div>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-4 py-3 space-y-3 min-h-[300px] max-h-[350px]">
            {messages.length === 0 && (
              <div className="text-center py-8">
                <div className="text-gray-500 text-sm mb-3">Ask me anything about your studies</div>
                <div className="space-y-2">
                  {['What deadlines are coming up?', 'What should I focus on this week?', 'Summarize my schedule'].map((q) => (
                    <button
                      key={q}
                      onClick={() => {
                        setInput(q)
                        setTimeout(() => {
                          const form = document.getElementById('chat-form') as HTMLFormElement
                          form?.requestSubmit()
                        }, 50)
                      }}
                      className="block w-full text-left px-3 py-2 text-xs text-gray-400 bg-gray-800/50 hover:bg-gray-800 rounded-lg transition-colors"
                    >
                      {q}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {messages.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div
                  className={`max-w-[85%] px-3 py-2 rounded-xl text-sm ${
                    msg.role === 'user'
                      ? 'bg-indigo-600 text-white rounded-br-sm whitespace-pre-wrap'
                      : 'bg-gray-800 text-gray-200 rounded-bl-sm'
                  }`}
                >
                  <FormattedMessage content={msg.content} isUser={msg.role === 'user'} />
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-800 px-4 py-2 rounded-xl rounded-bl-sm">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <form id="chat-form" onSubmit={sendMessage} className="px-3 py-3 border-t border-gray-800">
            <div className="flex gap-2">
              <input
                ref={inputRef}
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about deadlines..."
                disabled={loading}
                className="flex-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-sm text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500 disabled:opacity-50"
              />
              <button
                type="submit"
                disabled={!input.trim() || loading}
                className="px-3 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg disabled:opacity-50 transition-colors"
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
          </form>
        </div>
      )}
    </>
  )
}
