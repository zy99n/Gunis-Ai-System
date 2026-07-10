import request from '@/utils/request'

export interface Department {
  id: number
  name: string
  parent_id: number | null
  sort_order: number
  description: string | null
  children?: Department[]
  created_at: string
  updated_at: string
}

export interface DepartmentCreate {
  name: string
  parent_id?: number | null
  sort_order?: number
  description?: string | null
}

export interface UserDepartmentResponse {
  id: number
  user_id: number
  department_id: number
  is_primary: boolean
  department_name: string | null
}

export const getDepartmentTree = () => {
  return request.get<Department[]>('/organization/departments/tree')
}

export const getDepartments = (params?: { skip?: number; limit?: number }) => {
  return request.get<Department[]>('/organization/departments', { params })
}

export const getDepartment = (id: number) => {
  return request.get<Department>(`/organization/departments/${id}`)
}

export const createDepartment = (data: DepartmentCreate) => {
  return request.post<Department>('/organization/departments', data)
}

export const updateDepartment = (id: number, data: DepartmentCreate) => {
  return request.put<Department>(`/organization/departments/${id}`, data)
}

export const deleteDepartment = (id: number) => {
  return request.delete(`/organization/departments/${id}`)
}

export const moveDepartment = (id: number, parent_id: number | null) => {
  return request.put(`/organization/departments/${id}/move`, { params: { parent_id } })
}

export const getUserDepartments = (user_id: number) => {
  return request.get<UserDepartmentResponse[]>(`/organization/users/${user_id}/departments`)
}

export const addUserDepartment = (user_id: number, department_id: number, is_primary?: boolean) => {
  return request.post<UserDepartmentResponse>(`/organization/users/${user_id}/departments`, {
    params: { department_id, is_primary: is_primary ?? true }
  })
}

export const removeUserDepartment = (user_id: number, department_id: number) => {
  return request.delete(`/organization/users/${user_id}/departments/${department_id}`)
}