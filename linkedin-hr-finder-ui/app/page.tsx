'use client'

import { useState } from 'react'
import { Linkedin, Github, ExternalLink, Sparkles, Zap, Shield } from 'lucide-react'
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
    <div className="min-h-screen bg-stripe-50">
      {/* Header - Stripe Style */}
      <header className="bg-white border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="bg-gradient-to-br from-stripe-500 to-stripe-600 p-2.5 rounded-xl shadow-stripe">
                <Linkedin className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-semibold text-gray-900">LinkedIn HR Finder</h1>
                <p className="text-sm text-gray-500">AI-powered professional networking</p>
              </div>
            </div>
            <a
              href="https://github.com/TheForsakenOne1/Search_linkedin_hrs"
              target="_blank"
              rel="noopener noreferrer"
              className="hidden md:flex items-center space-x-2 text-sm text-gray-600 hover:text-stripe-600 transition-colors"
            >
              <Github className="h-4 w-4" />
              <span className="font-medium">View on GitHub</span>
              <ExternalLink className="h-3 w-3" />
            </a>
          </div>
        </div>
      </header>

      {/* Hero Section - Stripe Style */}
      <div className="bg-gradient-to-br from-stripe-500 via-stripe-600 to-stripe-700 text-white overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center max-w-3xl mx-auto">
            <div className="inline-flex items-center space-x-2 bg-white/10 backdrop-blur-sm rounded-full px-4 py-2 mb-6 animate-fade-in">
              <Sparkles className="h-4 w-4" />
              <span className="text-sm font-medium">Powered by GPT-4 & Google Search</span>
            </div>
            <h2 className="text-4xl md:text-5xl font-bold mb-4 animate-slide-up">
              Find HR contacts,<br />
              <span className="text-stripe-200">send personalized messages</span>
            </h2>
            <p className="text-lg text-stripe-100 mb-8 animate-slide-up" style={{ animationDelay: '0.1s' }}>
              Search any company and get AI-generated outreach messages in seconds.
              No database. No complexity. Just results.
            </p>
            <div className="flex flex-wrap justify-center gap-6 text-sm animate-slide-up" style={{ animationDelay: '0.2s' }}>
              <div className="flex items-center space-x-2">
                <Zap className="h-5 w-5 text-stripe-200" />
                <span>100 free searches/day</span>
              </div>
              <div className="flex items-center space-x-2">
                <Sparkles className="h-5 w-5 text-stripe-200" />
                <span>AI personalization</span>
              </div>
              <div className="flex items-center space-x-2">
                <Shield className="h-5 w-5 text-stripe-200" />
                <span>Privacy-first</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 -mt-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Search Form */}
          <div className="lg:col-span-1 space-y-6">
            <div className="stripe-card p-6 sticky top-6 animate-scale-in">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold text-gray-900">Search</h2>
                <span className="stripe-badge bg-stripe-50 text-stripe-700 border border-stripe-200">
                  Quick start
                </span>
              </div>
              <SearchForm onSearch={handleSearch} isLoading={isLoading} />
            </div>

            {/* Info Card - Stripe Style */}
            <div className="stripe-card p-5 border-l-4 border-stripe-500 animate-scale-in" style={{ animationDelay: '0.1s' }}>
              <div className="flex items-start space-x-3">
                <div className="bg-stripe-100 rounded-lg p-2">
                  <Sparkles className="h-5 w-5 text-stripe-600" />
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-gray-900 mb-2">How it works</h3>
                  <ol className="text-xs text-gray-600 space-y-1.5 list-decimal list-inside">
                    <li>Enter company name</li>
                    <li>Add your profile (optional)</li>
                    <li>Get AI-generated messages</li>
                    <li>Copy & send on LinkedIn</li>
                  </ol>
                </div>
              </div>
            </div>

            {/* Features Card */}
            <div className="stripe-card p-5 bg-gradient-to-br from-stripe-50 to-white animate-scale-in" style={{ animationDelay: '0.2s' }}>
              <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center">
                <Zap className="h-4 w-4 mr-2 text-stripe-600" />
                Platform features
              </h3>
              <div className="space-y-2">
                {[
                  'Google Search API integration',
                  'GPT-4 message generation',
                  'Export to JSON/CSV',
                  'No database required',
                  'Privacy-focused design'
                ].map((feature, index) => (
                  <div key={index} className="flex items-center text-xs text-gray-600">
                    <div className="h-1.5 w-1.5 rounded-full bg-stripe-500 mr-2"></div>
                    {feature}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column - Results */}
          <div className="lg:col-span-2 space-y-6">
            {error && (
              <div className="stripe-card p-5 border-l-4 border-error-500 bg-error-50 animate-slide-up">
                <div className="flex items-start space-x-3">
                  <div className="bg-error-100 rounded-lg p-2">
                    <ExternalLink className="h-5 w-5 text-error-600" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-error-900 mb-1">Error occurred</h3>
                    <p className="text-sm text-error-700">{error}</p>
                  </div>
                </div>
              </div>
            )}

            <div className="animate-fade-in">
              <ResultsDisplay results={results} />
            </div>
          </div>
        </div>
      </main>

      {/* Footer - Stripe Style */}
      <footer className="bg-white border-t border-gray-100 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-sm text-gray-500 mb-4 md:mb-0">
              © 2025 LinkedIn HR Finder. Built with Next.js, n8n & AI.
            </div>
            <div className="flex items-center space-x-3">
              <span className="text-xs text-gray-400">Powered by</span>
              {['Google', 'OpenAI', 'n8n'].map((tech) => (
                <span
                  key={tech}
                  className="stripe-badge bg-gray-50 text-gray-600 border border-gray-200 text-xs"
                >
                  {tech}
                </span>
              ))}
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
