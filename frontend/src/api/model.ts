import request from '@/utils/request'

export interface AiModel {
  id: number
  name: string
  model_type: string
  api_base: string | null
  api_key: string
  model_name: string
  temperature: number
  max_tokens: number
  timeout: number
  is_default: boolean
  is_active: boolean
  description: string | null
  created_at: string
  updated_at: string
}

export interface AiModelCreate {
  name: string
  model_type: string
  api_base?: string | null
  api_key: string
  model_name: string
  temperature?: number
  max_tokens?: number
  timeout?: number
  is_default?: boolean
  is_active?: boolean
  description?: string | null
}

export interface TestResult {
  success: boolean
  message: string
  response_time_ms?: number
}

export const getModels = (params?: { skip?: number; limit?: number }) => {
  return request.get<AiModel[]>('/model/models', { params })
}

export const getModel = (id: number) => {
  return request.get<AiModel>(`/model/models/${id}`)
}

export const createModel = (data: AiModelCreate) => {
  return request.post<AiModel>('/model/models', data)
}

export const updateModel = (id: number, data: Partial<AiModelCreate>) => {
  return request.put<AiModel>(`/model/models/${id}`, data)
}

export const deleteModel = (id: number) => {
  return request.delete(`/model/models/${id}`)
}

export const setDefaultModel = (id: number) => {
  return request.put<AiModel>(`/model/models/${id}/default`)
}

export const testModel = (id: number) => {
  return request.post<TestResult>(`/model/models/${id}/test`)
}