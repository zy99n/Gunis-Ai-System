import request from '@/utils/request'

export interface QueryRequest {
  natural_language: string
}

export interface QueryResponse {
  id: number
  natural_language: string
  generated_sql: string | null
  execution_result: Array<Record<string, any>> | null
  is_success: boolean
  error_message: string | null
  execution_time_ms: number | null
  created_at: string
}

export interface HistoryResponse {
  id: number
  natural_language: string
  generated_sql: string | null
  is_success: boolean | null
  is_favorite: boolean
  created_at: string
}

export const executeQuery = (data: QueryRequest) => {
  return request.post<QueryResponse>('/nl2sql/query', data)
}

export const getHistory = (params?: { skip?: number; limit?: number }) => {
  return request.get<HistoryResponse[]>('/nl2sql/history', { params })
}

export const toggleFavorite = (id: number) => {
  return request.post<HistoryResponse>(`/nl2sql/history/${id}/favorite`)
}

export const deleteHistory = (id: number) => {
  return request.delete(`/nl2sql/history/${id}`)
}