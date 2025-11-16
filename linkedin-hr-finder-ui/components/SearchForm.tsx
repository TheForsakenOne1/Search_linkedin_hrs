'use client'

import { useState } from 'react'
import { Search, Plus, Trash2, Save, User, CheckCircle2, ChevronDown } from 'lucide-react'
import type { Project, SearchParams, UserProfile } from '@/lib/types'
import { storage } from '@/lib/utils'

interface SearchFormProps {
  onSearch: (params: SearchParams) => void
  isLoading: boolean
}

export default function SearchForm({ onSearch, isLoading }: SearchFormProps) {
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [companyName, setCompanyName] = useState('')
  const [maxResults, setMaxResults] = useState(20)
  const [showSaveSuccess, setShowSaveSuccess] = useState(false)

  // Load saved profile from localStorage
  const savedProfile = storage.get<UserProfile | null>('userProfile', null)

  const [yourName, setYourName] = useState(savedProfile?.your_name || '')
  const [yourRole, setYourRole] = useState(savedProfile?.your_role || '')
  const [yourExperience, setYourExperience] = useState(savedProfile?.your_experience || '')
  const [yourSkills, setYourSkills] = useState(savedProfile?.your_skills || '')
  const [projects, setProjects] = useState<Project[]>(savedProfile?.your_projects || [
    { name: '', description: '', tech: '' }
  ])

  const handleAddProject = () => {
    setProjects([...projects, { name: '', description: '', tech: '' }])
  }

  const handleRemoveProject = (index: number) => {
    setProjects(projects.filter((_, i) => i !== index))
  }

  const handleProjectChange = (index: number, field: keyof Project, value: string) => {
    const newProjects = [...projects]
    newProjects[index][field] = value
    setProjects(newProjects)
  }

  const handleSaveProfile = () => {
    const profile: UserProfile = {
      your_name: yourName,
      your_role: yourRole,
      your_experience: yourExperience,
      your_skills: yourSkills,
      your_projects: projects.filter(p => p.name || p.description || p.tech),
    }
    storage.set('userProfile', profile)
    setShowSaveSuccess(true)
    setTimeout(() => setShowSaveSuccess(false), 3000)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    const params: SearchParams = {
      company_name: companyName,
      max_results: maxResults,
    }

    if (showAdvanced && yourName) {
      params.your_name = yourName
      params.your_role = yourRole
      params.your_experience = yourExperience
      params.your_skills = yourSkills
      params.your_projects = projects.filter(p => p.name && p.description)
    }

    onSearch(params)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {/* Company Name Input - Stripe Style */}
      <div>
        <label htmlFor="company" className="block text-sm font-medium text-gray-900 mb-2">
          Company Name <span className="text-error-500">*</span>
        </label>
        <div className="relative group">
          <input
            id="company"
            type="text"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            placeholder="e.g., Google, Microsoft, Amazon..."
            required
            className="stripe-input pr-10"
          />
          <Search className="absolute right-3 top-3.5 h-5 w-5 text-gray-400 group-focus-within:text-stripe-500 transition-colors" />
        </div>
      </div>

      {/* Max Results - Enhanced Slider */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <label htmlFor="maxResults" className="text-sm font-medium text-gray-900">
            Maximum contacts
          </label>
          <span className="stripe-badge bg-stripe-50 text-stripe-700 border border-stripe-200">
            {maxResults}
          </span>
        </div>
        <input
          id="maxResults"
          type="range"
          min="5"
          max="50"
          value={maxResults}
          onChange={(e) => setMaxResults(Number(e.target.value))}
          className="w-full h-2 bg-gray-100 rounded-lg appearance-none cursor-pointer accent-stripe-500 hover:bg-gray-200 transition-colors"
        />
        <div className="flex justify-between text-xs text-gray-500 mt-2">
          <span>5</span>
          <span className="text-gray-400">contacts</span>
          <span>50</span>
        </div>
      </div>

      {/* Advanced Options Toggle - Stripe Style */}
      <div className="border-t border-gray-100 pt-4">
        <button
          type="button"
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="flex items-center justify-between w-full text-sm font-medium text-gray-700 hover:text-stripe-600 transition-colors group"
        >
          <div className="flex items-center">
            <User className="h-4 w-4 mr-2 text-stripe-500" />
            <span>Personalization options</span>
            {savedProfile && !showAdvanced && (
              <CheckCircle2 className="h-4 w-4 ml-2 text-success-500" />
            )}
          </div>
          <ChevronDown className={`h-4 w-4 text-gray-400 transition-transform duration-200 ${showAdvanced ? 'rotate-180' : ''}`} />
        </button>
      </div>

      {/* Advanced Options - Stripe Style */}
      {showAdvanced && (
        <div className="space-y-4 bg-stripe-50 border border-stripe-100 p-5 rounded-xl animate-slide-up">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-sm font-semibold text-gray-900">Your information</h3>
            <button
              type="button"
              onClick={handleSaveProfile}
              className={`stripe-button-secondary px-3 py-1.5 text-xs flex items-center transition-all ${showSaveSuccess ? 'bg-success-50 border-success-200 text-success-700' : ''}`}
            >
              {showSaveSuccess ? (
                <>
                  <CheckCircle2 className="h-3 w-3 mr-1.5" />
                  Saved!
                </>
              ) : (
                <>
                  <Save className="h-3 w-3 mr-1.5" />
                  Save
                </>
              )}
            </button>
          </div>

          <div className="grid grid-cols-1 gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1.5">Full name</label>
              <input
                type="text"
                value={yourName}
                onChange={(e) => setYourName(e.target.value)}
                placeholder="John Doe"
                className="stripe-input text-sm py-2"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1.5">Job title</label>
              <input
                type="text"
                value={yourRole}
                onChange={(e) => setYourRole(e.target.value)}
                placeholder="Software Engineer"
                className="stripe-input text-sm py-2"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1.5">Experience</label>
                <input
                  type="text"
                  value={yourExperience}
                  onChange={(e) => setYourExperience(e.target.value)}
                  placeholder="5 years"
                  className="stripe-input text-sm py-2"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1.5">Skills</label>
                <input
                  type="text"
                  value={yourSkills}
                  onChange={(e) => setYourSkills(e.target.value)}
                  placeholder="Python, React..."
                  className="stripe-input text-sm py-2"
                />
              </div>
            </div>
          </div>

          {/* Projects - Stripe Style */}
          <div className="mt-5 pt-4 border-t border-stripe-200">
            <div className="flex justify-between items-center mb-3">
              <label className="block text-sm font-semibold text-gray-900">Projects</label>
              <button
                type="button"
                onClick={handleAddProject}
                className="stripe-button-secondary px-3 py-1.5 text-xs flex items-center"
              >
                <Plus className="h-3 w-3 mr-1.5" />
                Add
              </button>
            </div>

            <div className="space-y-3">
              {projects.map((project, index) => (
                <div key={index} className="stripe-card p-3 animate-scale-in">
                  <div className="flex justify-between items-start mb-2.5">
                    <span className="stripe-badge bg-stripe-100 text-stripe-700 text-xs">
                      #{index + 1}
                    </span>
                    {projects.length > 1 && (
                      <button
                        type="button"
                        onClick={() => handleRemoveProject(index)}
                        className="text-gray-400 hover:text-error-500 transition-colors"
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                      </button>
                    )}
                  </div>

                  <div className="space-y-2.5">
                    <input
                      type="text"
                      value={project.name}
                      onChange={(e) => handleProjectChange(index, 'name', e.target.value)}
                      placeholder="Project name"
                      className="stripe-input text-sm py-2"
                    />
                    <textarea
                      value={project.description}
                      onChange={(e) => handleProjectChange(index, 'description', e.target.value)}
                      placeholder="Description with metrics (e.g., Increased sales by 40%)"
                      rows={2}
                      className="stripe-input text-sm py-2 resize-none"
                    />
                    <input
                      type="text"
                      value={project.tech}
                      onChange={(e) => handleProjectChange(index, 'tech', e.target.value)}
                      placeholder="Technologies (React, Node.js, AWS)"
                      className="stripe-input text-sm py-2"
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Submit Button - Stripe Style */}
      <button
        type="submit"
        disabled={isLoading || !companyName}
        className="stripe-button-primary w-full py-3 font-semibold flex items-center justify-center relative overflow-hidden group"
      >
        {isLoading ? (
          <>
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>Searching...</span>
          </>
        ) : (
          <>
            <Search className="h-5 w-5 mr-2 group-hover:scale-110 transition-transform" />
            <span>Find HR Contacts</span>
          </>
        )}
        {!isLoading && (
          <div className="absolute inset-0 bg-white/10 transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left"></div>
        )}
      </button>
    </form>
  )
}
