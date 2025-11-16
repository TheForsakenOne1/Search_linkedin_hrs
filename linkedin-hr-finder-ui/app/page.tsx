'use client'

import { useState } from 'react'
import { Linkedin, Github, ExternalLink } from 'lucide-react'
import type { SearchParams, SearchResponse } from '@/lib/types'
import SearchForm from '@/components/SearchForm'
import ResultsDisplay from '@/components/ResultsDisplay'

export default function Home() {
  const [isLoading, setIsLoading] = useState(false)
  const [results, setResults] = useState<SearchResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSearch = async (params: SearchParams) => {
    setIsLoading(true)
    setError(null)
    setResults(null)

    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
      })

      const data: SearchResponse = await response.json()

      if (!response.ok) {
        throw new Error(data.error || `HTTP error! status: ${response.status}`)
      }

      setResults(data)
    } catch (err: any) {
      console.error('Search error:', err)
      setError(err.message || 'An error occurred while searching')
      setResults({
        success: false,
        company: params.company_name,
        total_profiles: 0,
        profiles: [],
        error: err.message,
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="bg-linkedin-500 p-2 rounded-lg mr-3">
                <Linkedin className="h-8 w-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">LinkedIn HR Finder</h1>
                <p className="text-sm text-gray-600">Find & message HR contacts with AI-powered personalization</p>
              </div>
            </div>
            <a
              href="https://github.com/TheForsakenOne1/Search_linkedin_hrs"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center text-gray-600 hover:text-gray-900 transition-colors"
            >
              <Github className="h-5 w-5 mr-2" />
              <span className="text-sm font-medium">View on GitHub</span>
              <ExternalLink className="h-3 w-3 ml-1" />
            </a>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Search Form */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-md p-6 sticky top-8">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Search Parameters</h2>
              <SearchForm onSearch={handleSearch} isLoading={isLoading} />
            </div>

            {/* Info Card */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-6">
              <h3 className="text-sm font-semibold text-blue-900 mb-2">💡 How it works</h3>
              <ol className="text-xs text-blue-800 space-y-1 list-decimal list-inside">
                <li>Enter company name</li>
                <li>Optionally add your profile & projects</li>
                <li>Click "Find HR Contacts"</li>
                <li>Review AI-generated messages</li>
                <li>Copy & send on LinkedIn</li>
              </ol>
            </div>

            {/* Stats Card */}
            <div className="bg-gradient-to-br from-linkedin-50 to-linkedin-100 border border-linkedin-200 rounded-lg p-4 mt-4">
              <h3 className="text-sm font-semibold text-linkedin-900 mb-2">✨ Features</h3>
              <ul className="text-xs text-linkedin-800 space-y-1">
                <li>✅ 100 free searches/day</li>
                <li>✅ AI-personalized messages</li>
                <li>✅ No database required</li>
                <li>✅ Export to JSON/CSV</li>
                <li>✅ One-click LinkedIn access</li>
              </ul>
            </div>
          </div>

          {/* Right Column - Results */}
          <div className="lg:col-span-2">
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                <h3 className="text-sm font-semibold text-red-900 mb-1">Error</h3>
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}

            <ResultsDisplay results={results} />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center text-sm text-gray-600">
            <p>© 2025 LinkedIn HR Finder. Built with Next.js & n8n.</p>
            <div className="flex items-center mt-4 md:mt-0">
              <span className="mr-4">Powered by:</span>
              <div className="flex gap-3">
                <span className="bg-gray-100 px-3 py-1 rounded-full text-xs font-medium">Google Search API</span>
                <span className="bg-gray-100 px-3 py-1 rounded-full text-xs font-medium">OpenAI GPT-4</span>
                <span className="bg-gray-100 px-3 py-1 rounded-full text-xs font-medium">n8n</span>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
