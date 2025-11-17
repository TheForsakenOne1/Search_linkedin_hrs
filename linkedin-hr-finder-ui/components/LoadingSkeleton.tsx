'use client'

import { Sparkles } from 'lucide-react'

export default function LoadingSkeleton() {
  return (
    <div className="space-y-6 animate-fade-in">
      {/* Loading Header */}
      <div className="stripe-card overflow-hidden shadow-brand-lg">
        <div className="relative bg-gradient-to-br from-brand-600 via-brand-500 to-accent-600 p-8 overflow-hidden">
          {/* Background pattern */}
          <div className="absolute inset-0 opacity-10">
            <div className="absolute inset-0" style={{
              backgroundImage: 'radial-gradient(circle at 2px 2px, white 1px, transparent 0)',
              backgroundSize: '24px 24px'
            }}></div>
          </div>

          <div className="relative flex items-center gap-5">
            <div className="bg-white/20 backdrop-blur-md p-4 rounded-2xl animate-pulse border border-white/20 shadow-2xl">
              <Sparkles className="h-8 w-8 text-white" />
            </div>
            <div className="flex-1">
              <div className="h-8 bg-white/25 rounded-xl w-56 mb-3 animate-pulse"></div>
              <div className="h-6 bg-white/15 rounded-lg w-40 animate-pulse"></div>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-r from-brand-50/50 via-white to-accent-50/50 px-8 py-5 border-t border-brand-100">
          <div className="flex items-center gap-2.5">
            <div className="h-2.5 w-2.5 rounded-full bg-success-500 animate-pulse shadow-lg shadow-success-500/50"></div>
            <div className="h-4 bg-neutral-200 rounded w-56 animate-pulse"></div>
          </div>
        </div>
      </div>

      {/* Loading Cards Grid */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-5">
        {[1, 2, 3, 4].map((index) => (
          <div
            key={index}
            className="stripe-card animate-scale-in"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            {/* Header Skeleton */}
            <div className="border-b border-gray-100 p-5">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <div className="h-5 bg-gray-200 rounded w-40 animate-pulse"></div>
                    <div className="h-5 bg-gray-100 rounded-full w-12 animate-pulse"></div>
                  </div>
                  <div className="h-4 bg-gray-100 rounded w-48 mb-2 animate-pulse"></div>
                  <div className="h-3 bg-gray-100 rounded w-32 animate-pulse"></div>
                </div>
                <div className="h-8 bg-gray-100 rounded-lg w-20 animate-pulse"></div>
              </div>
            </div>

            {/* Content Skeleton */}
            <div className="p-6 space-y-5">
              {/* Message 1 */}
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className="h-4 bg-gray-200 rounded w-36 animate-pulse"></div>
                  <div className="h-4 bg-gray-100 rounded w-16 animate-pulse"></div>
                </div>
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-3">
                  <div className="space-y-2">
                    <div className="h-3 bg-gray-200 rounded w-full animate-pulse"></div>
                    <div className="h-3 bg-gray-200 rounded w-5/6 animate-pulse"></div>
                    <div className="h-3 bg-gray-200 rounded w-4/6 animate-pulse"></div>
                  </div>
                </div>
                <div className="flex gap-2">
                  <div className="flex-1 h-10 bg-gray-100 rounded-lg animate-pulse"></div>
                  <div className="flex-1 h-10 bg-gray-100 rounded-lg animate-pulse"></div>
                </div>
              </div>

              {/* Divider */}
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-200"></div>
                </div>
                <div className="relative flex justify-center">
                  <div className="bg-white h-4 w-20 rounded animate-pulse"></div>
                </div>
              </div>

              {/* Message 2 */}
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className="h-4 bg-gray-200 rounded w-32 animate-pulse"></div>
                  <div className="h-4 bg-gray-100 rounded w-16 animate-pulse"></div>
                </div>
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-3">
                  <div className="space-y-2">
                    <div className="h-3 bg-gray-200 rounded w-full animate-pulse"></div>
                    <div className="h-3 bg-gray-200 rounded w-full animate-pulse"></div>
                    <div className="h-3 bg-gray-200 rounded w-3/4 animate-pulse"></div>
                  </div>
                </div>
                <div className="h-10 bg-gray-100 rounded-lg animate-pulse"></div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Searching Message */}
      <div className="text-center py-10 animate-pulse">
        <div className="inline-flex items-center gap-4 bg-gradient-to-r from-brand-50 to-accent-50 px-8 py-4 rounded-2xl border border-brand-200 shadow-brand">
          <svg className="animate-spin h-6 w-6 text-brand-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span className="text-sm font-bold text-brand-700">Searching LinkedIn profiles and generating personalized messages...</span>
        </div>
      </div>
    </div>
  )
}
