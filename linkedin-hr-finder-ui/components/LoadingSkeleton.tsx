'use client'

import { Sparkles } from 'lucide-react'

export default function LoadingSkeleton() {
  return (
    <div className="space-y-6 animate-fade-in">
      {/* Loading Header */}
      <div className="stripe-card overflow-hidden">
        <div className="bg-gradient-to-br from-stripe-500 via-stripe-600 to-stripe-700 p-6">
          <div className="flex items-center gap-4">
            <div className="bg-white/20 backdrop-blur-sm p-3 rounded-xl animate-pulse">
              <Sparkles className="h-7 w-7 text-white" />
            </div>
            <div className="flex-1">
              <div className="h-7 bg-white/20 rounded-lg w-48 mb-2 animate-pulse"></div>
              <div className="h-5 bg-white/10 rounded-lg w-32 animate-pulse"></div>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-r from-gray-50 to-white px-6 py-4 border-t border-gray-100">
          <div className="flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-stripe-500 animate-pulse"></div>
            <div className="h-4 bg-gray-200 rounded w-48 animate-pulse"></div>
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
      <div className="text-center py-8 animate-pulse">
        <div className="inline-flex items-center gap-3 text-stripe-600">
          <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span className="text-sm font-medium">Searching LinkedIn profiles and generating personalized messages...</span>
        </div>
      </div>
    </div>
  )
}
