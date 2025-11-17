'use client'

import { useState } from 'react'
import { Linkedin, Github, ExternalLink, Sparkles, Zap, Shield } from 'lucide-react'
import type { SearchParams, SearchResponse } from '@/lib/types'
import SearchForm from '@/components/SearchForm'
import ResultsDisplay from '@/components/ResultsDisplay'
import LoadingSkeleton from '@/components/LoadingSkeleton'

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
    <div className="min-h-screen bg-gradient-to-br from-neutral-50 via-brand-50/30 to-neutral-50">
      {/* Header - Professional Style */}
      <header className="bg-white/80 backdrop-blur-md border-b border-neutral-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="relative bg-gradient-to-br from-brand-500 to-brand-600 p-2.5 rounded-xl shadow-brand">
                <Linkedin className="h-6 w-6 text-white" />
                <div className="absolute inset-0 bg-white/20 rounded-xl"></div>
              </div>
              <div>
                <h1 className="text-xl font-bold text-neutral-900 tracking-tight">LinkedIn HR Finder</h1>
                <p className="text-sm text-neutral-600">AI-powered professional networking</p>
              </div>
            </div>
            <a
              href="https://github.com/TheForsakenOne1/Search_linkedin_hrs"
              target="_blank"
              rel="noopener noreferrer"
              className="hidden md:flex items-center space-x-2 text-sm text-neutral-700 hover:text-brand-600 transition-colors group"
            >
              <Github className="h-4 w-4 group-hover:scale-110 transition-transform" />
              <span className="font-medium">View on GitHub</span>
              <ExternalLink className="h-3 w-3" />
            </a>
          </div>
        </div>
      </header>

      {/* Hero Section - Professional Green Theme */}
      <div className="relative bg-gradient-to-br from-brand-600 via-brand-500 to-accent-600 text-white overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute inset-0" style={{
            backgroundImage: 'radial-gradient(circle at 2px 2px, white 1px, transparent 0)',
            backgroundSize: '32px 32px'
          }}></div>
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center max-w-3xl mx-auto">
            <div className="inline-flex items-center space-x-2 bg-white/15 backdrop-blur-sm rounded-full px-5 py-2.5 mb-8 border border-white/20 animate-fade-in">
              <Sparkles className="h-4 w-4 text-brand-100" />
              <span className="text-sm font-semibold">Powered by GPT-4 & Google Search</span>
            </div>
            <h2 className="text-5xl md:text-6xl font-bold mb-6 animate-slide-up leading-tight">
              Find HR contacts,<br />
              <span className="text-brand-100 bg-gradient-to-r from-brand-100 to-accent-100 bg-clip-text text-transparent">
                send personalized messages
              </span>
            </h2>
            <p className="text-xl text-brand-50 mb-10 leading-relaxed animate-slide-up" style={{ animationDelay: '0.1s' }}>
              Search any company and get AI-generated outreach messages in seconds.
              <br className="hidden sm:block" />
              No database. No complexity. Just results.
            </p>
            <div className="flex flex-wrap justify-center gap-8 text-sm font-medium animate-slide-up" style={{ animationDelay: '0.2s' }}>
              <div className="flex items-center space-x-2 bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2 border border-white/20">
                <Zap className="h-5 w-5 text-brand-200" />
                <span>100 free searches/day</span>
              </div>
              <div className="flex items-center space-x-2 bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2 border border-white/20">
                <Sparkles className="h-5 w-5 text-brand-200" />
                <span>AI personalization</span>
              </div>
              <div className="flex items-center space-x-2 bg-white/10 backdrop-blur-sm rounded-lg px-4 py-2 border border-white/20">
                <Shield className="h-5 w-5 text-brand-200" />
                <span>Privacy-first</span>
              </div>
            </div>
          </div>
        </div>

        {/* Decorative bottom wave */}
        <div className="absolute bottom-0 left-0 right-0">
          <svg className="w-full h-12 text-neutral-50" preserveAspectRatio="none" viewBox="0 0 1200 120" fill="currentColor">
            <path d="M0,0 C300,80 600,80 900,40 C1050,20 1150,0 1200,0 L1200,120 L0,120 Z" />
          </svg>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 -mt-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Search Form */}
          <div className="lg:col-span-1 space-y-6">
            <div className="stripe-card p-6 sticky top-24 animate-scale-in shadow-lg">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-bold text-neutral-900">Search</h2>
                <span className="stripe-badge bg-gradient-to-br from-brand-50 to-accent-50 text-brand-700 border border-brand-200 font-semibold">
                  Quick start
                </span>
              </div>
              <SearchForm onSearch={handleSearch} isLoading={isLoading} />
            </div>

            {/* Info Card - Professional Style */}
            <div className="stripe-card p-6 border-l-4 border-brand-500 bg-gradient-to-br from-white to-brand-50/30 animate-scale-in shadow-lg" style={{ animationDelay: '0.1s' }}>
              <div className="flex items-start space-x-4">
                <div className="bg-gradient-to-br from-brand-100 to-brand-200 rounded-xl p-2.5 shadow-brand-sm">
                  <Sparkles className="h-5 w-5 text-brand-700" />
                </div>
                <div className="flex-1">
                  <h3 className="text-sm font-bold text-neutral-900 mb-3">How it works</h3>
                  <ol className="text-sm text-neutral-700 space-y-2.5 list-none">
                    <li className="flex items-start">
                      <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-brand-500 text-white text-xs font-bold mr-2.5 flex-shrink-0 mt-0.5">1</span>
                      <span>Enter company name</span>
                    </li>
                    <li className="flex items-start">
                      <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-brand-500 text-white text-xs font-bold mr-2.5 flex-shrink-0 mt-0.5">2</span>
                      <span>Add your profile (optional)</span>
                    </li>
                    <li className="flex items-start">
                      <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-brand-500 text-white text-xs font-bold mr-2.5 flex-shrink-0 mt-0.5">3</span>
                      <span>Get AI-generated messages</span>
                    </li>
                    <li className="flex items-start">
                      <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-brand-500 text-white text-xs font-bold mr-2.5 flex-shrink-0 mt-0.5">4</span>
                      <span>Copy & send on LinkedIn</span>
                    </li>
                  </ol>
                </div>
              </div>
            </div>

            {/* Features Card */}
            <div className="stripe-card p-6 bg-gradient-to-br from-neutral-50 to-white animate-scale-in shadow-lg" style={{ animationDelay: '0.2s' }}>
              <h3 className="text-sm font-bold text-neutral-900 mb-4 flex items-center">
                <div className="bg-gradient-to-br from-accent-100 to-accent-200 rounded-lg p-1.5 mr-2.5">
                  <Zap className="h-4 w-4 text-accent-700" />
                </div>
                Platform features
              </h3>
              <div className="space-y-3">
                {[
                  'Google Search API integration',
                  'GPT-4 message generation',
                  'Export to JSON/CSV',
                  'No database required',
                  'Privacy-focused design'
                ].map((feature, index) => (
                  <div key={index} className="flex items-center text-sm text-neutral-700 group">
                    <div className="h-2 w-2 rounded-full bg-gradient-to-r from-brand-500 to-accent-500 mr-3 group-hover:scale-125 transition-transform"></div>
                    <span className="group-hover:text-brand-700 transition-colors">{feature}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column - Results */}
          <div className="lg:col-span-2 space-y-6">
            {error && !isLoading && (
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

            {isLoading ? (
              <LoadingSkeleton />
            ) : (
              <div className="animate-fade-in">
                <ResultsDisplay results={results} />
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer - Professional Style */}
      <footer className="bg-white/80 backdrop-blur-md border-t border-neutral-200 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-sm text-neutral-600 mb-4 md:mb-0 font-medium">
              © 2025 LinkedIn HR Finder. Built with Next.js, n8n & AI.
            </div>
            <div className="flex items-center space-x-3">
              <span className="text-xs text-neutral-500 font-medium">Powered by</span>
              {['Google', 'OpenAI', 'n8n'].map((tech, index) => (
                <span
                  key={tech}
                  className="stripe-badge bg-gradient-to-br from-neutral-100 to-neutral-50 text-neutral-700 border border-neutral-200 text-xs font-semibold hover:border-brand-300 hover:text-brand-700 transition-all cursor-default"
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
