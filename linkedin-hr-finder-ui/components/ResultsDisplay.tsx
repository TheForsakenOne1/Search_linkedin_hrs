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
      <div className="text-center py-12 bg-gray-50 rounded-lg">
        <Users className="h-16 w-16 text-gray-300 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-600 mb-2">No results yet</h3>
        <p className="text-gray-500">Enter a company name above to start searching</p>
      </div>
    )
  }

  if (!results.success) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-red-800 mb-2">Error</h3>
        <p className="text-red-600">{results.error || 'An error occurred'}</p>
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
      {/* Summary Header */}
      <div className="bg-gradient-to-r from-linkedin-500 to-linkedin-600 rounded-lg p-6 text-white">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center">
            <Building2 className="h-8 w-8 mr-3" />
            <div>
              <h2 className="text-2xl font-bold">{results.company}</h2>
              <p className="text-linkedin-100">
                Found {results.total_profiles} HR contact{results.total_profiles !== 1 ? 's' : ''}
              </p>
            </div>
          </div>

          <div className="flex gap-2">
            <button
              onClick={handleDownloadJSON}
              className="bg-white/20 hover:bg-white/30 backdrop-blur-sm px-4 py-2 rounded-lg text-sm font-medium flex items-center transition-colors"
            >
              <Download className="h-4 w-4 mr-2" />
              JSON
            </button>
            <button
              onClick={handleDownloadCSV}
              className="bg-white/20 hover:bg-white/30 backdrop-blur-sm px-4 py-2 rounded-lg text-sm font-medium flex items-center transition-colors"
            >
              <Download className="h-4 w-4 mr-2" />
              CSV
            </button>
          </div>
        </div>

        {results.message && (
          <p className="text-linkedin-50 text-sm">{results.message}</p>
        )}
      </div>

      {/* Profile Cards Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {results.profiles.map((contact, index) => (
          <ProfileCard key={index} contact={contact} />
        ))}
      </div>

      {/* Empty State */}
      {results.profiles.length === 0 && (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <Users className="h-16 w-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-600 mb-2">No contacts found</h3>
          <p className="text-gray-500">Try searching for a different company or adjust your parameters</p>
        </div>
      )}
    </div>
  )
}
