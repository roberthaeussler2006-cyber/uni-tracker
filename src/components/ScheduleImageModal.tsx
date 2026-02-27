'use client'

import Image from 'next/image'

interface Props {
  subjectColor: string
  images: string[]
  onClose: () => void
}

export default function ScheduleImageModal({ subjectColor, images, onClose }: Props) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80" onClick={onClose}>
      <div
        className="w-full max-w-3xl mx-4 max-h-[90vh] overflow-y-auto rounded-xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close button */}
        <button
          onClick={onClose}
          className="fixed top-4 right-4 z-60 bg-gray-900/80 rounded-full p-2 text-gray-400 hover:text-white transition-colors"
        >
          <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        {/* Images */}
        <div className="space-y-2">
          {images.map((src, i) => (
            <div key={i} className="relative w-full">
              <img
                src={src}
                alt={`Schedule page ${i + 1}`}
                className="w-full rounded-lg"
                style={{ borderTop: i === 0 ? `3px solid ${subjectColor}` : undefined }}
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
