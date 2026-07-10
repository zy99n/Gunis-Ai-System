import request from '@/utils/request'

export interface AiSkill {
  id: number
  name: string
  code: string
  description: string | null
  prompt_template: string
  model_id: number | null
  parameters: Record<string, any> | null
  is_active: boolean
  category: string | null
  icon: string | null
  sort_order: number
  created_at: string
  updated_at: string
}

export interface SkillCreate {
  name: string
  code: string
  description?: string | null
  prompt_template: string
  model_id?: number | null
  parameters?: Record<string, any> | null
  is_active?: boolean
  category?: string | null
  icon?: string | null
  sort_order?: number
}

export interface SkillGenerateRequest {
  name: string
  description: string
}

export interface TestResult {
  success: boolean
  message: string
  output?: string
}

export const getSkills = (params?: { skip?: number; limit?: number; category?: string }) => {
  return request.get<AiSkill[]>('/skill/skills', { params })
}

export const getSkill = (id: number) => {
  return request.get<AiSkill>(`/skill/skills/${id}`)
}

export const createSkill = (data: SkillCreate) => {
  return request.post<AiSkill>('/skill/skills', data)
}

export const updateSkill = (id: number, data: Partial<SkillCreate>) => {
  return request.put<AiSkill>(`/skill/skills/${id}`, data)
}

export const deleteSkill = (id: number) => {
  return request.delete(`/skill/skills/${id}`)
}

export const aiGenerateSkill = (data: SkillGenerateRequest) => {
  return request.post<AiSkill>('/skill/skills/ai-generate', data)
}

export const testSkill = (id: number, test_input?: string) => {
  return request.post<TestResult>(`/skill/skills/${id}/test`, { params: { test_input } })
}

export const toggleSkill = (id: number) => {
  return request.put<AiSkill>(`/skill/skills/${id}/toggle`)
}