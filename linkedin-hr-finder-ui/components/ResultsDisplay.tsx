'use client'

import { Download, Users, Building2 } from 'lucide-react'
import type { SearchResponse } from '@/lib/types'
import ProfileCard from './ProfileCard'

interface ResultsDisplayProps {
  results: SearchResponse | null
}

export default function ResultsDisplay({ results }: ResultsDisplayProps) {
  if (!results) {
    return (
      <div className="stripe-card text-center py-16 animate-fade-in">
        <div className="bg-gradient-to-br from-gray-100 to-gray-50 w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-5 shadow-inner">
          <Users className="h-10 w-10 text-gray-400" />
        </div>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Ready to search</h3>
        <p className="text-sm text-gray-500 max-w-sm mx-auto">
          Enter a company name in the search form to find HR contacts and generate personalized messages
        </p>
      </div>
    )
  }

  if (!results.success) {
    return (
      <div className="stripe-card border-l-4 border-error-500 bg-gradient-to-br from-error-50 to-white p-6 animate-slide-up">
        <div className="flex items-start gap-4">
          <div className="bg-error-100 p-3 rounded-xl">
            <svg className="h-6 w-6 text-error-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div className="flex-1">
            <h3 className="text-base font-semibold text-error-900 mb-1.5">Search failed</h3>
            <p className="text-sm text-error-700 leading-relaxed">{results.error || 'An error occurred while searching. Please try again.'}</p>
          </div>
        </div>
      </div>
    )
  }

  const handleDownloadJSON = () => {
    const dataStr = JSON.stringify(results.profiles, null, 2)
    const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr)
    const exportFileDefaultName = `linkedin_hr_${results.company}_${new Date().toISOString().split('T')[0]}.json`

    const linkElement = document.createElement('a')
    linkElement.setAttribute('href', dataUri)
    linkElement.setAttribute('download', exportFileDefaultName)
    linkElement.click()
  }

  const handleDownloadCSV = () => {
    if (!results.profiles.length) return

    const headers = ['Name', 'Title', 'Location', 'Profile URL', 'Connection Request', 'Follow-up Message']
    const rows = results.profiles.map(p => [
      p.name,
      p.title,
      p.location,
      p.profile_url,
      `"${p.connection_request.replace(/"/g, '""')}"`,
      `"${p.follow_up_message.replace(/"/g, '""')}"`,
    ])

    const csvContent = [headers, ...rows].map(row => row.join(',')).join('\n')
    const dataUri = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csvContent)
    const exportFileDefaultName = `linkedin_hr_${results.company}_${new Date().toISOString().split('T')[0]}.csv`

    const linkElement = document.createElement('a')
    linkElement.setAttribute('href', dataUri)
    linkElement.setAttribute('download', exportFileDefaultName)
    linkElement.click()
  }

  return (
    <div className="space-y-6">
      {/* Summary Header - Stripe Style */}
      <div className="stripe-card overflow-hidden animate-slide-up">
        <div className="bg-gradient-to-br from-stripe-500 via-stripe-600 to-stripe-700 p-6 text-white">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div className="flex items-start gap-4">
              <div className="bg-white/20 backdrop-blur-sm p-3 rounded-xl shadow-lg">
                <Building2 className="h-7 w-7" />
              </div>
              <div>
                <h2 className="text-2xl font-bold mb-1.5">{results.company}</h2>
                <div className="flex items-center gap-2">
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-white/20 backdrop-blur-sm border border-white/30">
                    {results.total_profiles} contact{results.total_profiles !== 1 ? 's' : ''}
                  </span>
                  {results.message && (
                    <span className="text-stripe-100 text-sm hidden sm:inline">• {results.message}</span>
                  )}
                </div>
              </div>
            </div>

            <div className="flex gap-2.5">
              <button
                onClick={handleDownloadJSON}
                className="group bg-white/10 hover:bg-white/20 backdrop-blur-sm border border-white/20 px-4 py-2.5 rounded-lg text-sm font-medium flex items-center transition-all duration-200 hover:shadow-lg shadow-stripe"
              >
                <Download className="h-4 w-4 mr-2 group-hover:scale-110 transition-transform" />
                <span>JSON</span>
              </button>
              <button
                onClick={handleDownloadCSV}
                className="group bg-white hover:bg-white/90 text-stripe-600 px-4 py-2.5 rounded-lg text-sm font-semibold flex items-center transition-all duration-200 shadow-stripe hover:shadow-stripe-lg"
              >
                <Download className="h-4 w-4 mr-2 group-hover:scale-110 transition-transform" />
                <span>CSV</span>
              </button>
            </div>
          </div>
        </div>

        {/* Quick Stats Bar */}
        <div className="bg-gradient-to-r from-gray-50 to-white px-6 py-4 border-t border-gray-100">
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-6">
              <div className="flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-success-500 animate-pulse"></div>
                <span className="text-gray-600">AI-generated messages ready</span>
              </div>
              <span className="text-gray-400 hidden md:inline">•</span>
              <span className="text-gray-500 hidden md:inline">Click cards to copy messages</span>
            </div>
          </div>
        </div>
      </div>

      {/* Profile Cards Grid */}
      {results.profiles.length > 0 && (
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-5">
          {results.profiles.map((contact, index) => (
            <div
              key={index}
              className="animate-scale-in"
              style={{ animationDelay: `${index * 0.05}s` }}
            >
              <ProfileCard contact={contact} />
            </div>
          ))}
        </div>
      )}

      {/* Empty State */}
      {results.profiles.length === 0 && (
        <div className="stripe-card text-center py-16 animate-fade-in">
          <div className="bg-gradient-to-br from-gray-100 to-gray-50 w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-5 shadow-inner">
            <Users className="h-10 w-10 text-gray-400" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No contacts found</h3>
          <p className="text-sm text-gray-500 max-w-md mx-auto mb-4">
            We couldn't find any HR contacts for <span className="font-semibold text-gray-700">{results.company}</span>
          </p>
          <p className="text-xs text-gray-400">
            Try searching for a different company or check the spelling
          </p>
        </div>
      )}
    </div>
  )
}
