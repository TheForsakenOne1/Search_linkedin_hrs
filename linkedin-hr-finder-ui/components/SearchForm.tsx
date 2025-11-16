'use client'

import { useState } from 'react'
import { Search, Plus, Trash2, Save, User } from 'lucide-react'
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
    alert('Profile saved!')
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
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Company Name Input */}
      <div>
        <label htmlFor="company" className="block text-sm font-medium text-gray-700 mb-2">
          Company Name *
        </label>
        <div className="relative">
          <input
            id="company"
            type="text"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            placeholder="e.g., Google, Microsoft, Amazon..."
            required
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-linkedin-500 focus:border-transparent"
          />
          <Search className="absolute right-3 top-3.5 h-5 w-5 text-gray-400" />
        </div>
      </div>

      {/* Max Results */}
      <div>
        <label htmlFor="maxResults" className="block text-sm font-medium text-gray-700 mb-2">
          Max Results: {maxResults}
        </label>
        <input
          id="maxResults"
          type="range"
          min="5"
          max="50"
          value={maxResults}
          onChange={(e) => setMaxResults(Number(e.target.value))}
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-linkedin-500"
        />
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>5</span>
          <span>50</span>
        </div>
      </div>

      {/* Advanced Options Toggle */}
      <div className="border-t border-gray-200 pt-4">
        <button
          type="button"
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="flex items-center text-sm font-medium text-linkedin-600 hover:text-linkedin-700"
        >
          <User className="h-4 w-4 mr-2" />
          {showAdvanced ? 'Hide' : 'Show'} Advanced Options (Your Profile & Projects)
        </button>
      </div>

      {/* Advanced Options */}
      {showAdvanced && (
        <div className="space-y-4 bg-gray-50 p-4 rounded-lg">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-sm font-semibold text-gray-700">Your Profile</h3>
            <button
              type="button"
              onClick={handleSaveProfile}
              className="flex items-center text-xs text-linkedin-600 hover:text-linkedin-700"
            >
              <Save className="h-3 w-3 mr-1" />
              Save Profile
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Your Name</label>
              <input
                type="text"
                value={yourName}
                onChange={(e) => setYourName(e.target.value)}
                placeholder="John Doe"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-linkedin-500 focus:border-transparent text-sm"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Your Role</label>
              <input
                type="text"
                value={yourRole}
                onChange={(e) => setYourRole(e.target.value)}
                placeholder="Software Engineer"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-linkedin-500 focus:border-transparent text-sm"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Experience</label>
              <input
                type="text"
                value={yourExperience}
                onChange={(e) => setYourExperience(e.target.value)}
                placeholder="5 years"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-linkedin-500 focus:border-transparent text-sm"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Your Skills</label>
              <input
                type="text"
                value={yourSkills}
                onChange={(e) => setYourSkills(e.target.value)}
                placeholder="Python, React, AWS, Docker..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-linkedin-500 focus:border-transparent text-sm"
              />
            </div>
          </div>

          {/* Projects */}
          <div className="mt-6">
            <div className="flex justify-between items-center mb-3">
              <label className="block text-sm font-medium text-gray-700">Your Projects</label>
              <button
                type="button"
                onClick={handleAddProject}
                className="flex items-center text-xs text-linkedin-600 hover:text-linkedin-700"
              >
                <Plus className="h-3 w-3 mr-1" />
                Add Project
              </button>
            </div>

            <div className="space-y-3">
              {projects.map((project, index) => (
                <div key={index} className="bg-white p-3 rounded-md border border-gray-200">
                  <div className="flex justify-between items-start mb-2">
                    <span className="text-xs font-medium text-gray-500">Project {index + 1}</span>
                    {projects.length > 1 && (
                      <button
                        type="button"
                        onClick={() => handleRemoveProject(index)}
                        className="text-red-500 hover:text-red-700"
                      >
                        <Trash2 className="h-3 w-3" />
                      </button>
                    )}
                  </div>

                  <div className="space-y-2">
                    <input
                      type="text"
                      value={project.name}
                      onChange={(e) => handleProjectChange(index, 'name', e.target.value)}
                      placeholder="Project Name"
                      className="w-full px-2 py-1.5 border border-gray-300 rounded text-sm focus:ring-1 focus:ring-linkedin-500"
                    />
                    <textarea
                      value={project.description}
                      onChange={(e) => handleProjectChange(index, 'description', e.target.value)}
                      placeholder="Description (include metrics and impact)"
                      rows={2}
                      className="w-full px-2 py-1.5 border border-gray-300 rounded text-sm focus:ring-1 focus:ring-linkedin-500"
                    />
                    <input
                      type="text"
                      value={project.tech}
                      onChange={(e) => handleProjectChange(index, 'tech', e.target.value)}
                      placeholder="Technologies Used"
                      className="w-full px-2 py-1.5 border border-gray-300 rounded text-sm focus:ring-1 focus:ring-linkedin-500"
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isLoading || !companyName}
        className="w-full bg-linkedin-500 hover:bg-linkedin-600 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 flex items-center justify-center"
      >
        {isLoading ? (
          <>
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Searching...
          </>
        ) : (
          <>
            <Search className="h-5 w-5 mr-2" />
            Find HR Contacts
          </>
        )}
      </button>
    </form>
  )
}
