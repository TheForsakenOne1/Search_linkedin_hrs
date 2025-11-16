export interface Project {
  name: string
  description: string
  tech: string
}

export interface UserProfile {
  your_name: string
  your_role: string
  your_experience: string
  your_skills: string
  your_projects: Project[]
}

export interface SearchParams {
  company_name: string
  max_results?: number
  your_name?: string
  your_role?: string
  your_experience?: string
  your_skills?: string
  your_projects?: Project[]
}

export interface HRContact {
  name: string
  first_name: string
  title: string
  company: string
  location: string
  profile_url: string
  connection_request: string
  follow_up_message: string
  char_count_connection: number
  char_count_followup: number
  generated_at: string
  ai_provider: string
  your_name?: string
  your_role?: string
  your_skills?: string
  your_projects?: Project[]
}

export interface SearchResponse {
  success: boolean
  company: string
  total_profiles: number
  profiles: HRContact[]
  export_files?: {
    json: string
    csv: string
  }
  message?: string
  error?: string
}
